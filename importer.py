import json

class Importer:
    """
    This class is responsible for importing data from JSON files into the database.
    It has two main methods: import_rooms and import_students, which read data from the specified JSON files and insert it into the corresponding tables in the database. 
    The methods use prepared statements to ensure efficient and secure data insertion, and they handle exceptions by rolling back transactions in case of errors.

    """
    def __init__(self, db):
        self.db = db

    def import_rooms(self, path):
        with self.db.get_cursor() as cursor:
            with open(path, 'r') as f:
                rooms = json.load(f)
                values = [(room['id'], room['name']) for room in rooms]
                try:
                    cursor.executemany("""
                        INSERT IGNORE INTO rooms (id, name) VALUES (%s, %s)
                    """, values
                    )
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
                    print(f"Error importing rooms: {e}")

    def import_students(self, path):
        with self.db.get_cursor() as cursor:
            with open(path, 'r') as f :
                students = json.load(f)
                values = [(student['birthday'], student['id'], student['name'], student['room'], student['sex']) for student in students]
                try:
                    cursor.executemany("""
                        INSERT IGNORE INTO students (birthday, id, name, room, sex) VALUES (%s, %s, %s, %s, %s)
                    """, values
                    )
                    self.db.commit() 
                # Handle exceptions and rollback in case of errors
                except Exception as e:
                    self.db.rollback()
                    print(f"Error importing students: {e}")