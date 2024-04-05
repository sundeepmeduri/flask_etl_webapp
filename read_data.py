import sqlite3

def read_projects(database_name='projects.db'):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Execute a query to select all projects
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()

    conn.close()
    return projects

def read_pipeline(database_name='projects.db'):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Execute a query to select all projects
    cursor.execute('SELECT * FROM pipelines')
    pipeline = cursor.fetchall()

    conn.close()
    return pipeline

# Example usage
projects = read_projects()
for project in projects:
    print(project)

# Example usage
pipeline = read_pipeline()
for project in pipeline:
    print(project)
