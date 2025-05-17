"""
Alternative MongoDB Connection Setup

If you encounter issues with the Djongo adapter, you can use this alternative approach
that uses PyMongo directly through a MongoDB router.

Steps to implement:
1. Install PyMongo: pip install pymongo[srv]
2. Add this file to your project
3. Update settings.py to use the MongoDBRouter
4. Use the direct_mongodb_connection function to access MongoDB directly if needed

Example settings.py configuration:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongodb': {
        'ENGINE': 'django.db.backends.dummy',
        'NAME': 'chitfunds_db',
    }
}

DATABASE_ROUTERS = ['path.to.alternative_mongodb_connection.MongoDBRouter']

"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from django.conf import settings

# Load environment variables
load_dotenv()

# MongoDB Connection URI
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'chitfunds_db')
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', '')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')
MONGODB_AUTH_SOURCE = os.environ.get('MONGODB_AUTH_SOURCE', 'admin')

# MongoDB Client instance
_mongo_client = None


def get_mongo_client():
    """Returns a MongoDB client instance."""
    global _mongo_client
    if _mongo_client is None:
        if MONGODB_USERNAME and MONGODB_PASSWORD:
            _mongo_client = MongoClient(
                MONGODB_URI,
                username=MONGODB_USERNAME,
                password=MONGODB_PASSWORD,
                authSource=MONGODB_AUTH_SOURCE
            )
        else:
            _mongo_client = MongoClient(MONGODB_URI)
    return _mongo_client


def get_db():
    """Returns the MongoDB database instance."""
    client = get_mongo_client()
    return client[MONGODB_NAME]


def direct_mongodb_connection(collection_name):
    """
    Get a direct connection to a MongoDB collection.
    
    Usage:
        collection = direct_mongodb_connection('my_collection')
        results = collection.find({'field': 'value'})
    """
    db = get_db()
    return db[collection_name]


class MongoDBRouter:
    """
    A database router that directs MongoDB-related models to MongoDB and all others to default.
    
    To use, add model Meta property:
    
    class Meta:
        mongodb_collection = 'collection_name'
    """
    
    def db_for_read(self, model, **hints):
        if hasattr(model._meta, 'mongodb_collection'):
            return 'mongodb'
        return 'default'
    
    def db_for_write(self, model, **hints):
        if hasattr(model._meta, 'mongodb_collection'):
            return 'mongodb'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if neither object uses MongoDB
        if (not hasattr(obj1._meta, 'mongodb_collection') and 
            not hasattr(obj2._meta, 'mongodb_collection')):
            return True
        # Allow relations if both objects use MongoDB
        if (hasattr(obj1._meta, 'mongodb_collection') and 
            hasattr(obj2._meta, 'mongodb_collection')):
            return True
        return False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only allow migrations for the default database
        if db == 'default':
            # Don't migrate MongoDB models
            if model_name:
                model = hints.get('model')
                if model and hasattr(model._meta, 'mongodb_collection'):
                    return False
            return True
        return False


class MongoDBModel:
    """
    A mixin for models that use MongoDB.
    
    Example usage:
    
    class MyModel(models.Model, MongoDBModel):
        # Define fields as usual
        name = models.CharField(max_length=100)
        
        class Meta:
            mongodb_collection = 'my_collection'
    
    # Using the model
    # Create:
    instance = MyModel(name='Test')
    instance.mongo_save()
    
    # Read:
    results = MyModel.mongo_find({'name': 'Test'})
    
    # Update:
    instance.name = 'Updated'
    instance.mongo_save()
    
    # Delete:
    instance.mongo_delete()
    """
    
    @classmethod
    def get_collection(cls):
        """Get the MongoDB collection for this model."""
        collection_name = getattr(cls._meta, 'mongodb_collection', cls.__name__.lower())
        return direct_mongodb_connection(collection_name)
    
    @classmethod
    def mongo_find(cls, query=None, **kwargs):
        """Find documents in MongoDB."""
        collection = cls.get_collection()
        if query is None:
            query = {}
        return collection.find(query, **kwargs)
    
    @classmethod
    def mongo_find_one(cls, query=None, **kwargs):
        """Find one document in MongoDB."""
        collection = cls.get_collection()
        if query is None:
            query = {}
        return collection.find_one(query, **kwargs)
    
    def to_mongo_dict(self):
        """Convert model instance to a dictionary for MongoDB."""
        return {
            field.name: getattr(self, field.name)
            for field in self._meta.fields
            if hasattr(self, field.name)
        }
    
    def mongo_save(self):
        """Save model to MongoDB."""
        collection = self.__class__.get_collection()
        data = self.to_mongo_dict()
        if hasattr(self, '_id') and self._id:
            collection.update_one({'_id': self._id}, {'$set': data})
        else:
            result = collection.insert_one(data)
            self._id = result.inserted_id
        return self
    
    def mongo_delete(self):
        """Delete model from MongoDB."""
        if hasattr(self, '_id') and self._id:
            collection = self.__class__.get_collection()
            collection.delete_one({'_id': self._id})