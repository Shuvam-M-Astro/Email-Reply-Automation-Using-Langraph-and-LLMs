import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
import torch

# Step 1: Load and Preprocess Data

# Load the email dataset (ensure it's in the same directory or provide the path)
data = pd.read_csv('Training_Data/data.csv')  # Adjust the path if needed

# Extract 'body' and 'category' columns
emails = data['body'].tolist()  # Updated to 'body' column
labels = data['subject'].tolist()  # Assuming you're classifying by subject or another label

# Convert to Hugging Face dataset format
dataset = Dataset.from_dict({
    'email_body': emails,
    'category': labels
})

# Split the dataset into training and validation sets (80% train, 20% validation)
train_dataset, test_dataset = dataset.train_test_split(test_size=0.2).values()

# Step 2: Tokenize the Dataset using RoBERTa tokenizer

# Load the RoBERTa tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Function to tokenize the text
def tokenize_function(examples):
    return tokenizer(examples['email_body'], padding="max_length", truncation=True)

# Apply the tokenization function
train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Step 3: Load Pre-trained RoBERTa Model for Sequence Classification

# Load the RoBERTa model for classification (adjust num_labels based on your dataset's classes)
model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=len(set(labels)))

# Step 4: Define Training Arguments

training_args = TrainingArguments(
    output_dir='./results',          # Output directory
    num_train_epochs=3,              # Number of training epochs
    per_device_train_batch_size=8,   # Batch size for training
    per_device_eval_batch_size=16,   # Batch size for evaluation
    warmup_steps=500,                # Number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # Strength of weight decay
    logging_dir='./logs',            # Directory for storing logs
    logging_steps=10,
    # Remove or comment out this line if using an older transformers version
    # evaluation_strategy="epoch",     # Evaluation during training after every epoch
)


# Step 5: Define the Trainer

trainer = Trainer(
    model=model,                         # The model to train
    args=training_args,                  # Training arguments
    train_dataset=train_dataset,         # Training dataset
    eval_dataset=test_dataset,           # Evaluation dataset
)

# Step 6: Train the Model

trainer.train()

# Step 7: Save the Model and Tokenizer

# Save the fine-tuned model and tokenizer
model.save_pretrained('./fine_tuned_roberta')
tokenizer.save_pretrained('./fine_tuned_roberta')

# Step 8: Evaluate the Model

# Evaluate the model on the test dataset
results = trainer.evaluate()
print(results)

# Step 9: Classify New Emails

# Function to classify a new email
def classify_email(email_body):
    # Tokenize the email body
    inputs = tokenizer(email_body, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Get model prediction
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted class (highest probability)
    predicted_class = torch.argmax(outputs.logits, dim=-1).item()

    # Map the predicted class to category (adjust the categories according to your dataset)
    categories = ['support', 'schedule', 'billing', 'other']  # Modify if necessary
    return categories[predicted_class]

# Example: Classify a new email
email_body = "Can you help me with my account?"
category = classify_email(email_body)
print(f"Predicted category: {category}")
