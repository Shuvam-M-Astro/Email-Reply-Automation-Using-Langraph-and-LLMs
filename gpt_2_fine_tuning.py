import os
import pandas as pd
import torch
from torch.utils.data import random_split
from transformers import (
    GPT2Tokenizer, 
    GPT2LMHeadModel, 
    Trainer, 
    TrainingArguments,
    EvalPrediction
)
from datasets import Dataset
import numpy as np
from sklearn.model_selection import train_test_split
import logging
from typing import Dict, List, Union
import wandb  # for experiment tracking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)

class EmailDatasetPreprocessor:
    def __init__(self, file_path: str, tokenizer: GPT2Tokenizer, max_length: int = 512):
        self.file_path = file_path
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def load_and_preprocess(self) -> Dataset:
        try:
            df = pd.read_csv(self.file_path)
            logging.info(f"Loaded dataset with {len(df)} samples")
            
            # Data validation
            if not all(col in df.columns for col in ['subject', 'body']):
                raise ValueError("Dataset must contain 'subject' and 'body' columns")
            
            # Remove empty rows and duplicates
            df = df.dropna(subset=['subject', 'body'])
            df = df.drop_duplicates()
            
            # Preprocess text
            df['input_text'] = df.apply(
                lambda x: f"Subject: {x['subject'].strip()} Email: {x['body'].strip()}", 
                axis=1
            )
            df['target_text'] = df['body'].str.strip()
            
            # Tokenization with proper padding and truncation
            encoded_data = self.tokenize_data(df)
            
            # Create dataset
            dataset = Dataset.from_dict(encoded_data)
            return dataset
            
        except Exception as e:
            logging.error(f"Error in data preprocessing: {str(e)}")
            raise
    
    def tokenize_data(self, df: pd.DataFrame) -> Dict[str, List]:
        encoded_data = {
            'input_ids': [],
            'attention_mask': [],
            'labels': []
        }
        
        for _, row in df.iterrows():
            input_encoding = self.tokenizer(
                row['input_text'],
                padding='max_length',
                truncation=True,
                max_length=self.max_length,
                return_tensors='pt'
            )
            
            label_encoding = self.tokenizer(
                row['target_text'],
                padding='max_length',
                truncation=True,
                max_length=self.max_length,
                return_tensors='pt'
            )
            
            encoded_data['input_ids'].append(input_encoding['input_ids'][0])
            encoded_data['attention_mask'].append(input_encoding['attention_mask'][0])
            encoded_data['labels'].append(label_encoding['input_ids'][0])
            
        return encoded_data

class EmailResponseTrainer:
    def __init__(
        self,
        model_name: str = 'gpt2',
        output_dir: str = './fine_tuned_model',
        num_train_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 5e-5,
        warmup_steps: int = 500,
        weight_decay: float = 0.01,
        logging_steps: int = 10,
        eval_steps: int = 100,
        save_steps: int = 500,
    ):
        self.model_name = model_name
        self.output_dir = output_dir
        self.training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            warmup_steps=warmup_steps,
            weight_decay=weight_decay,
            logging_steps=logging_steps,
            logging_dir='./logs',
            evaluation_strategy="steps",
            eval_steps=eval_steps,
            save_steps=save_steps,
            save_total_limit=2,
            learning_rate=learning_rate,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            report_to="wandb"  # Enable wandb logging
        )
        
        # Initialize tokenizer and model
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        
        # Set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
    
    def compute_metrics(self, eval_pred: EvalPrediction) -> Dict[str, float]:
        predictions, labels = eval_pred
        # Compute perplexity
        loss = torch.nn.CrossEntropyLoss()(
            torch.tensor(predictions).view(-1, self.model.config.vocab_size),
            torch.tensor(labels).view(-1)
        )
        perplexity = torch.exp(loss)
        return {
            "perplexity": perplexity.item()
        }
    
    def train(self, dataset: Dataset):
        # Split dataset into train and validation
        train_size = int(0.9 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
        
        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics,
            tokenizer=self.tokenizer
        )
        
        try:
            # Initialize wandb
            wandb.init(project="email-response-generator", name="gpt2-fine-tuning")
            
            # Train the model
            trainer.train()
            
            # Save the model and tokenizer
            self.model.save_pretrained(self.output_dir)
            self.tokenizer.save_pretrained(self.output_dir)
            
            # Close wandb
            wandb.finish()
            
        except Exception as e:
            logging.error(f"Error during training: {str(e)}")
            raise

class EmailResponseGenerator:
    def __init__(self, model_path: str):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.model.eval()
        
    @torch.no_grad()
    def generate_reply(
        self,
        input_text: str,
        max_length: int = 150,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        num_return_sequences: int = 1
    ) -> Union[str, List[str]]:
        try:
            prompt = f"Subject: {input_text}\nResponse:"
            inputs = self.tokenizer.encode(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=1024
            )
            
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                no_repeat_ngram_size=2,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True
            )
            
            responses = [
                self.tokenizer.decode(output, skip_special_tokens=True).split("Response:")[1].strip()
                for output in outputs
            ]
            
            return responses[0] if num_return_sequences == 1 else responses
            
        except Exception as e:
            logging.error(f"Error in response generation: {str(e)}")
            return "Error generating response. Please try again."

def main():
    # Initialize wandb
    wandb.login()
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")
    
    try:
        # Initialize trainer
        trainer = EmailResponseTrainer(
            model_name='gpt2',
            num_train_epochs=3,
            batch_size=4,
            learning_rate=5e-5
        )
        
        # Prepare data
        preprocessor = EmailDatasetPreprocessor(
            file_path='./Training_data/data.csv',
            tokenizer=trainer.tokenizer
        )
        dataset = preprocessor.load_and_preprocess()
        
        # Train model
        trainer.train(dataset)
        
        # Test generation
        generator = EmailResponseGenerator(model_path='./fine_tuned_model')
        test_input = "Can you help me with my account?"
        response = generator.generate_reply(test_input)
        logging.info(f"Test generation:\nInput: {test_input}\nResponse: {response}")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
