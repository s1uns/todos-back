from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


load_dotenv()
password = os.getenv("PASSWORD")
client = MongoClient(f"mongodb+srv://admin:{password}@todolistdatabase.ca6loya.mongodb.net/?retryWrites=true&w=majority&appName=ToDoListDatabase", server_api=ServerApi('1'))

db = client.todo_db

todo_collection = db["todo_collection"]
