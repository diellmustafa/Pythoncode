from uuid import uuid4
from dotenv import load_dotenv, set_key
import os

def generate_and_save_api_key():
    load_dotenv()
    api_key = str(uuid4)
    print(f"Generated API key: {api_key}")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(root_dir, '.env')

    if not os.path.isfile(env_file):
        open(env_file, 'w').close()

    existing_key = os.getenv('API_KEY', "")

    if existing_key:
        existing_key = existing_key.strip(',')
        new_key = f"{existing_key},{api_key}" if existing_key else api_key
    else:
        new_key = api_key

    set_key(env_file, 'API_KEY', new_key)
    print(f"API Key saved to {new_key}")

    if __name__ == "__main__":
        generate_and_save_api_key()