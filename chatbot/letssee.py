from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

def chat_with_bot(user_input):  # Simplified: No history for now
    inputs = tokenizer.encode_plus(user_input + tokenizer.eos_token, return_tensors='pt')
    chat_ids = model.generate(inputs['input_ids']) # Basic generate
    response = tokenizer.decode(chat_ids[0], skip_special_tokens=True)
    return response

print("Test Bot")
while True:
    user_input = input("You: ").strip()
    if user_input.lower() == 'exit':
        break
    response = chat_with_bot(user_input)
    print("Bot:", response)