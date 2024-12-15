from dotenv import load_dotenv
import os

'''
if this code raises a ValueError you either haven't created a .env file with a following structure:
OPENAI_API_KEY=YOUR_API_KEY
or your API key is not valid
'''

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if API_KEY is None:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")