from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['assignment_db']  # Change to your database name
collection = db['dataset']  # Change to your collection name

def create_document(data):
    """Create a new document in the collection."""
    try:
        result = collection.insert_one(data)
        print(f"Document inserted with ID: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        print(f"Error creating document: {e}")
        return None

def read_documents(query=None, limit=10):
    """Read documents from the collection."""
    if query is None:
        query = {}
    try:
        documents = list(collection.find(query).limit(limit))
        return documents
    except Exception as e:
        print(f"Error reading documents: {e}")
        return []

def update_document(query, update_data):
    """Update a document in the collection."""
    try:
        result = collection.update_one(query, {'$set': update_data})
        print(f"Documents matched: {result.matched_count}, modified: {result.modified_count}")
        return result.modified_count
    except Exception as e:
        print(f"Error updating document: {e}")
        return 0

def delete_document(query):
    """Delete a document from the collection."""
    try:
        result = collection.delete_one(query)
        print(f"Documents deleted: {result.deleted_count}")
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting document: {e}")
        return 0

def import_csv_to_mongo(csv_file_path, collection_name=None):
    """Import CSV file to MongoDB collection."""
    global collection
    if collection_name:
        collection = db[collection_name]

    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)

        # Convert DataFrame to list of dictionaries
        data = df.to_dict('records')

        # Insert data into MongoDB
        if data:
            result = collection.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} documents from CSV")
            return len(result.inserted_ids)
        else:
            print("No data to insert")
            return 0
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
        return 0
    except Exception as e:
        print(f"Error importing CSV: {e}")
        return 0

# Example usage
if __name__ == "__main__":
    # Example CRUD operations
    # Create
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "created_at": datetime.now()
    }
    create_document(sample_data)

    # Read
    docs = read_documents()
    print("Documents:", docs)

    # Update
    update_document({"name": "John Doe"}, {"age": 31})

    # Delete
    delete_document({"name": "John Doe"})

    # Import CSV (replace 'healthcare.csv' with your actual CSV file path)
    import_csv_to_mongo('healthcare.csv')
