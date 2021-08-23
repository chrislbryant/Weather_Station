import psycopg2

HOST=*****
DB=*****
USER=*****
PSWD=*****

class DatabaseInterface():

    def __init__(self,):
        self.connection = psycopg2.connect(host=HOST,database=DB,user=USER,password=PSWD)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def fetch_all(self, query):
        DatabaseInterface.execute(self, query)
        all_rows = self.cursor.fetchall()
        return all_rows

    def fetch_one(self, query):
        DatabaseInterface.execute(self, query)
        result = self.cursor.fetchone()
        return result