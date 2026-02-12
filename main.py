'''
This is the main entry point of the application. It sets up the database connection, creates necessary tables, imports data from JSON files, executes queries, and exports results in the specified format (JSON or XML).
'''

import argparse
from database import Database
from importer import Importer
from exporter import Exporter, XMLFormat, JSONFormat
from tables import Rooms, Students
from queries import Queries


def main():

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Students and rooms management system')
    parser.add_argument('--students', required=True, help='Path to JSON file with students data')
    parser.add_argument('--rooms', required=True, help='Path to JSON file with rooms data')
    parser.add_argument('--format', choices=['json', 'xml'], required=True, help='Output format (JSON or XML)')
    args = parser.parse_args()

    format_strategies = {
        'json': JSONFormat(),
        'xml': XMLFormat()
    }
    selected_strategy = format_strategies[args.format]

    # Initialize database connection
    db = Database(
        host='localhost',
        user='root',
        password='1212',
        database='mydatabase1'
    )

    # Create tables and import data
    try:
        Rooms(db).create_table()
        Students(db).create_table()

        importer = Importer(db)
        importer.import_rooms(args.rooms)
        importer.import_students(args.students)

        queries = Queries(db)

        description, rows = queries.student_count_per_room()
        exporter = Exporter(description, rows, selected_strategy)
        exporter.export(f'student_count.{args.format}')
        print(f"Exported to file student_count.{args.format} successfully.")

        description, rows = queries.smallest_avg_age()
        exporter = Exporter(description, rows, selected_strategy)
        exporter.export(f'smallest_avg_age.{args.format}')
        print(f"Exported to file smallest_avg_age.{args.format} successfully.")

        description, rows = queries.largest_age_diff()
        exporter = Exporter(description, rows, selected_strategy)
        exporter.export(f'largest_age_diff.{args.format}')
        print(f"Exported to file largest_age_diff.{args.format} successfully.")

        description, rows = queries.mixed_sex_rooms()  
        exporter = Exporter(description, rows, selected_strategy)
        exporter.export(f'mixed_sex_rooms.{args.format}')
        print(f"Exported to file mixed_sex_rooms.{args.format} successfully.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    