'''
This is the main entry point of the application. It sets up the database connection, creates necessary tables, imports data from JSON files, executes queries, and exports results in the specified format (JSON or XML).
'''

import argparse
from database import Database
from importer import Importer
from exporter import Exporter, XMLFormat, JSONFormat
from tables import Rooms, Students
from queries import Queries
import os
from dotenv import load_dotenv

load_dotenv()

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
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        database=os.getenv('database')
    )

    # Create tables and import data
    try:
        Rooms(db).create_table()
        Students(db).create_table()

        importer = Importer(db)
        importer.import_rooms(args.rooms)
        importer.import_students(args.students)

        queries = Queries(db)

        # Helper function to avoid repeating the export code 4 times
        def run_and_export(query_method, filename_base):
            description, rows = query_method()
            exporter = Exporter(description, rows, selected_strategy)
            exporter.export(f'{filename_base}.{args.format}')
            print(f"Exported to {filename_base}.{args.format} successfully.")

        run_and_export(queries.student_count_per_room, 'student_count')
        run_and_export(queries.smallest_avg_age, 'smallest_avg_age')
        run_and_export(queries.largest_age_diff, 'largest_age_diff')
        run_and_export(queries.mixed_sex_rooms, 'mixed_sex_rooms')

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
    