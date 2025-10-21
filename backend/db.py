import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()

print("URL:", os.getenv("SUPABASE_URL"))
print("KEY:", os.getenv("SUPABASE_KEY")[:10], "...")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def add_transaction(data):
    response = supabase.table("transactions").insert(data).execute()
    return response

def get_transactions():
    response = supabase.table("transactions").select("*").execute()
    return response

if __name__ == "__main__":
    print("Database module loaded successfully.")
    test_data = {
        "id": 1,
        "date": "2025-10-21",
        "amount": 1200,
        "category": "Food",
        "note": "Dinner with friends",
        "payment_method": "UPI"
    }

    response = add_transaction(test_data)
    print("Insert response:", response)

