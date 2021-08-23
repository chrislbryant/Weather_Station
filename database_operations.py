from postgres_interface import DatabaseInterface

db = DatabaseInterface()

def delete_foreign_duplicates():
    query = """
            DELETE FROM foreign_weather_station a
            USING foreign_weather_station b
            WHERE a.ctid < b.ctid
            AND a.timestamp = b.timestamp
        ; """
    db.execute(query)
    db.commit()
    db.close()
    
def main():
    delete_foreign_duplicates()
    
if __name__ == "__main__":
    main()