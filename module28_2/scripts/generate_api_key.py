from uuid import uuid4
from dotenv import load_dotenv, set_key
import os

def generate_and_save_api_key():
    load_dotenv()

    api_key = str(uuid4())
    print(f"Generated API Key: {api_key}")

    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(root_directory, ".env")

    if not os.path.isfile(env_file):
        open(env_file, 'w').close()

    existing_keys = os.getenv("API_KEYS", "")

    if existing_keys:
        existing_keys = existing_keys.strip(',')

    else:
        new_keys = api_key

    set_key(env_file, "API_KEY", new_keys)
    print(f"API Keys updated: {new_keys}")

if __name__ == "__main__":
    generate_and_save_api_key()