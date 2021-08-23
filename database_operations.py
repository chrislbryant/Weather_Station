from postgres_interface import DatabaseInterface

db = DatabaseInterface()

def main():
    db.delete_foreign_duplicates()
    
if __name__ == "__main__":
    main()