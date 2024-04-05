import sqlite3
import os


def create_project_database(database_name='projects.db'):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create projects table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ProjectName TEXT NOT NULL,
        IsActive Text Not NULL,
        CreateDatetime datetime DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


def create_pipeline_table(database_name='projects.db'):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create projects table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pipelines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        input_source TEXT NOT NULL,
        output_table TEXT NOT NULL,
        file_location TEXT,
        database_name TEXT,
        project_id INTEGER NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')

    conn.commit()
    conn.close()


def delete_database_file(database_name='projects.db'):
    if os.path.exists(database_name):
        os.remove(database_name)
        print(f"Database file '{database_name}' deleted successfully.")
    else:
        print(f"Database file '{database_name}' not found.")


delete_database_file()
create_project_database()
create_pipeline_table()