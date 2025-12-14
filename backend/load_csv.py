"""CSV Data Loader for MongoDB

Loads patient data from healthcare.csv into MongoDB Atlas.
Converts CSV data to MongoDB documents and performs bulk insert.
"""

import csv
import os
from db.db_mongo import (
    connect_mongo,
    bulk_insert_patients_mongo,
    count_patients_mongo,
    clear_all_patients_mongo
)

def load_csv_to_mongo(csv_file='healthcare.csv', clear_existing=False):
    """Load patient data from CSV file to MongoDB
    
    Args:
        csv_file (str): Path to CSV file (default: healthcare.csv)
        clear_existing (bool): Whether to clear existing data first
    
    Returns:
        int: Number of records inserted
    """
    # Get absolute path to CSV file
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)
    
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        return 0
    
    print(f"📂 Loading data from: {csv_path}")
    
    # Connect to MongoDB
    connect_mongo()
    
    # Clear existing data if requested
    if clear_existing:
        deleted = clear_all_patients_mongo()
        print(f"🗑️  Cleared {deleted} existing records")
    
    # Read CSV and prepare documents
    patients_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Helper function to safely convert to float
            def safe_float(value, default=0.0):
                try:
                    return float(value) if value and value != 'N/A' else default
                except (ValueError, TypeError):
                    return default
            
            def safe_int(value, default=0):
                try:
                    return int(value) if value and value != 'N/A' else default
                except (ValueError, TypeError):
                    return default
            
            # Convert string values to appropriate types
            patient = {
                'name': row.get('name', 'Unknown'),
                'age': safe_int(row.get('age'), 0),
                'gender': row.get('gender', 'Unknown'),
                'hypertension': safe_int(row.get('hypertension'), 0) == 1,
                'heart_disease': safe_int(row.get('heart_disease'), 0) == 1,
                'ever_married': row.get('ever_married', 'Unknown'),
                'work_type': row.get('work_type', 'Unknown'),
                'residence_type': row.get('Residence_type', row.get('residence_type', 'Unknown')),
                'avg_glucose_level': safe_float(row.get('avg_glucose_level'), 0.0),
                'bmi': safe_float(row.get('bmi'), 0.0),
                'smoking_status': row.get('smoking_status', 'Unknown'),
                'stroke': safe_int(row.get('stroke'), 0)
            }
            patients_data.append(patient)
    
    # Bulk insert to MongoDB
    if patients_data:
        inserted_count = bulk_insert_patients_mongo(patients_data)
        total_count = count_patients_mongo()
        print(f"✅ Inserted {inserted_count} patients to MongoDB")
        print(f"📊 Total patients in database: {total_count}")
        return inserted_count
    else:
        print("⚠️  No data to insert")
        return 0

def main():
    """Main function to run CSV import"""
    print("=" * 50)
    print("📦 MongoDB Data Loader")
    print("=" * 50)
    
    # Load CSV data (set clear_existing=True to replace all data)
    load_csv_to_mongo(clear_existing=True)
    
    print("=" * 50)
    print("✅ Data loading complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
