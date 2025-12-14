from db.db_mongo import connect_mongo, get_patients_collection

def main():
    connect_mongo()                     # ✅ CONNECT FIRST
    collection = get_patients_collection()
    print("Collection ready:", collection.name)

if __name__ == "__main__":
    main()
