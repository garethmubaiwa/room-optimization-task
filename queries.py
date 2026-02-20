
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
        """
        Task: Return the number of students in each room, including rooms with zero students.
        Logic: The query uses a LEFT JOIN to include all rooms, even those without students, and counts the number of students in each room.
        """
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name, COUNT(s.id) AS student_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
        """)
        return cursor.description, cursor.fetchall()
    
    def smallest_avg_age(self):
        """
        Task: Return the 5 rooms with the smallest average age of students.
        Logic: The query calculates the average age of students in each room using the TIMESTAMPDIFF function to find the difference in years between the current date and the students' birthdays.
                It then orders the results by average age in ascending order and limits the output to the top 5 rooms.
        """
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name, TIMESTAMPDIFF(YEAR, unix_timestamp(AVG(UNIX_TIMESTAMP(s.birthday))), CURDATE()) AS avg_age
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY avg_age ASC
            LIMIT 5
        """)
        return cursor.description, cursor.fetchall()
    
    def largest_age_diff(self):
        """
        Task: Return the 5 rooms with the largest age difference between students.
        Logic: The query calculates the age difference in each room by finding the minimum and maximum birthdays of students in that room and using the TIMESTAMPDIFF function to calculate the difference in years.
                It then orders the results by age difference in descending order and limits the output to the top 5 rooms.
        """
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name, TIMESTAMPDIFF(YEAR, MIN(s.birthday), MAX(s.birthday)) AS age_diff
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            ORDER BY age_diff DESC
            LIMIT 5
        """)
        return cursor.description, cursor.fetchall()
    
    def mixed_sex_rooms(self):
        """
        Task: Return the list of rooms that have students of both sexes.
        Logic: The query uses a JOIN to combine the rooms and students tables, groups the results by room, and uses the HAVING clause to filter for rooms that have more than one distinct sex among the students assigned to that room.
        """
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT r.id, r.name
            FROM rooms r
            JOIN students s ON r.id = s.room
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
        """)
        return cursor.description, cursor.fetchall()
    
