'''
This module defines the database tables for the application. It includes the Rooms and Students tables, along with their respective methods for creating the tables in the database.
The Rooms table stores information about the rooms, while the Students table stores information about the students, including their birthday, name, room assignment, and sex.
The Students table also includes foreign key constraints to ensure data integrity, and indexes to optimize query performance.

relationship: - The Rooms table has a one-to-many relationship with the Students table, as each room can have multiple students assigned to it, but each student can only be assigned to one room.
'''
class Rooms:
    def __init__(self, db) -> None:
        self.db = db

    def create_table(self):
        cursor = self.db.get_cursor()
        try:
            # Drop child tables first to avoid Foreign Key constraint errors, then the parent.
            cursor.execute("DROP TABLE IF EXISTS students")
            cursor.execute("DROP TABLE IF EXISTS rooms")
            
            cursor.execute("""
                CREATE TABLE rooms (
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)
            self.db.commit()
        finally:
            cursor.close()

class Students:
    def __init__(self, db) -> None:
        self.db = db

    def create_table(self):
        cursor = self.db.get_cursor()
        try:
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    birthday DATE NOT NULL,
                    id INT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    room INTEGER,
                    sex char(1) NOT NULL,
                    FOREIGN KEY (room) REFERENCES rooms(id)
                )
            """)
            
            cursor.execute("CREATE INDEX idx_students_room_sex ON students(room, sex)")
            cursor.execute("CREATE INDEX idx_students_birthday ON students(birthday)") 
            
            self.db.commit()
        finally:
            cursor.close()