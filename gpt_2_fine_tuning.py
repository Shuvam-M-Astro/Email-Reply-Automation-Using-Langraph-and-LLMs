from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Set pad token to eos_token (if necessary)
tokenizer.pad_token = tokenizer.eos_token

# Fine-tuning step (assuming you already have fine-tuned the model)

# Save the fine-tuned model and tokenizer
model.save_pretrained('./fine_tuned_model')
tokenizer.save_pretrained('./fine_tuned_model')

# Function to generate a reply
def generate_reply(input_text):
    prompt = f"Customer: {input_text}\n\nYour response:"

    # Tokenize the input and generate the response
    inputs = tokenizer.encode(prompt, return_tensors="pt", padding=True, truncation=True)

    # Generate a response from the fine-tuned model
    reply = model.generate(
        inputs,
        max_length=150,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode and return the generated text
    reply_text = tokenizer.decode(reply[0], skip_special_tokens=True)
    
    return reply_text

# Example usage
input_email = "Can you help me with my account?"
generated_reply = generate_reply(input_email)
print(f"Generated Reply: {generated_reply}")
