import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables
load_dotenv()

MODEL_NAME = "meta-llama/Llama-3.1-8B"
MAX_TOKENS = 200
HF_TOKEN = os.getenv("HF_TOKEN")

print("Loading LLaMA 3.1 8B model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16,
    token=HF_TOKEN
)
print("Model loaded successfully!")

def generate_advice(transaction: dict, max_length=MAX_TOKENS) -> str:
    """
    Generate parent-like advice for a single transaction.
    """
    prompt = f"""
You are a friendly finance buddy. Analyze the following transaction and give advice in a casual, helpful tone:
Transaction: {transaction}
Advice:
"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_length)
    advice = tokenizer.decode(outputs[0], skip_special_tokens=True)
    advice = advice.replace(prompt, "").strip()
    return advice

if __name__ == "__main__":
    test_transaction = {
        "date": "2025-10-21",
        "amount": 1200,
        "category": "Food",
        "note": "Dinner with friends",
        "payment_method": "UPI"
    }
    advice = generate_advice(test_transaction)
    print("\n💬 Generated advice:")
    print(advice)
