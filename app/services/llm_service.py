from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
# CPU Enabled uncomment below 👇🏽
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it")
# GPU Enabled use below 👇🏽
# model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it", device_map="auto")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_response_from_documents(combined_information: str) -> str:
    # Moving tensors to GPU
    input_ids = tokenizer(combined_information, return_tensors="pt").to(device)
    response = model.generate(**input_ids, max_new_tokens=700)

    return tokenizer.decode(response[0], skip_special_tokens=True)