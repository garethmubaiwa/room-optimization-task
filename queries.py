
'''
SQL queries for the student-room database. Each method returns a tuple of (description, results) where description is the cursor description and results is the fetched data.
S - Sngle responsibility: Each method corresponds to a specific query, making it easy to maintain and extend.
O - Open/Closed Principle: The class is open for extension (new queries can be added) but closed for modification (existing methods don't need to be changed).
'''



from decimal import Decimal


class Queries:
    def __init__(self, db):
        self.db = db

    def student_count_per_room(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name, COUNT(s.id) AS student_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
        """)
        return cursor.description, cursor.fetchall()
    
    def smallest_avg_age(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name, AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY avg_age ASC
            LIMIT 5
        """)
        return cursor.description, cursor.fetchall()
    
    def largest_age_diff(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name, MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS age_diff
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY age_diff DESC
            LIMIT 5
        """)
        return cursor.description, cursor.fetchall()
    
    def mixed_sex_rooms(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
        """)
        return cursor.description, cursor.fetchall()
    
