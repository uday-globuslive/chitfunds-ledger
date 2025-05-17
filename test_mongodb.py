#!/usr/bin/env python
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# MongoDB Connection details
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'chitfunds_db')
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', '')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')
MONGODB_AUTH_SOURCE = os.environ.get('MONGODB_AUTH_SOURCE', 'admin')

print(f"Testing connection to MongoDB...")
print(f"URI: {MONGODB_URI}")
print(f"Database: {MONGODB_NAME}")

try:
    # Establish connection
    if MONGODB_USERNAME and MONGODB_PASSWORD:
        client = MongoClient(
            MONGODB_URI,
            username=MONGODB_USERNAME,
            password=MONGODB_PASSWORD,
            authSource=MONGODB_AUTH_SOURCE
        )
    else:
        client = MongoClient(MONGODB_URI)
    
    # Test connection
    db = client.admin
    server_info = db.command('ping')
    print(f"Connection successful: {server_info}")
    
    # Test database access
    db = client[MONGODB_NAME]
    collections = db.list_collection_names()
    print(f"Available collections: {collections}")
    
    # Test creating a test document
    test_collection = db['test_connection']
    test_doc = {
        'test': 'document', 
        'timestamp': datetime.datetime.now(),
        'source': 'test_mongodb.py script'
    }
    result = test_collection.insert_one(test_doc)
    print(f"Created test document with ID: {result.inserted_id}")
    
    # Clean up
    test_collection.delete_one({'_id': result.inserted_id})
    print("Test document deleted")
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Connection failed: {str(e)}")