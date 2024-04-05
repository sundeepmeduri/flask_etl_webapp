from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

DATABASE = 'projects.db'


def create_connection():
    return sqlite3.connect(DATABASE)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST' and request.form['project_name'] != '':
        project_name = request.form['project_name']
        conn = create_connection()
        cursor = conn.cursor()
        IsActive = 'Yes'
        cursor.execute('INSERT INTO projects (ProjectName,IsActive) VALUES (?,?)'
                       , (project_name,IsActive))
        conn.commit()
        conn.close()
        success_message = f"Project '{project_name}' created successfully."
    else:
        success_message = None

    if request.method == 'POST' and request.form['project_name'] == '':
        success_message = 'Enter Project Name'

    return render_template('create_project.html', success_message=success_message)


def read_projects(database_name='projects.db'):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    conn.close()
    return projects


@app.route('/list_projects')
def list_projects():
    projects = read_projects()
    return render_template('projects.html', projects=projects)


@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):

    success_message = ''
    if request.method == 'POST':
        new_name = request.form['project_name']
        is_active = request.form['is_active']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE projects SET ProjectName = ?,IsActive = ? WHERE id = ?', (new_name, is_active, project_id))
        conn.commit()
        conn.close()
        success_message = f"Project '{new_name}' saved successfully."

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    conn.close()

    return render_template('edit_project.html', project=project, success_message=success_message)


@app.route('/view_project/<int:project_id>')
def view_project(project_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    conn.close()

    return render_template('view_project.html', project=project)


@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('list_projects'))


@app.route('/create_pipeline/<int:project_id>', methods=['GET', 'POST'])
def create_pipeline(project_id):
    if request.method == 'POST':
        pipeline_name = request.form['pipeline_name']
        input_source = request.form['input_source']
        output_table = request.form['output_table']
        file_location = request.form['file_location']
        database_name = request.form['database_name']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pipelines (name, input_source, output_table, file_location, database_name, project_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pipeline_name, input_source, output_table, file_location, database_name, project_id))
        conn.commit()
        conn.close()

        return redirect(url_for('view_project', project_id=project_id))

    return render_template('create_pipeline.html', project_id=project_id)


@app.route('/show_pipelines/<int:project_id>')
def show_pipelines(project_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pipelines WHERE project_id = ?', (project_id,))
    pipelines = cursor.fetchall()
    conn.close()

    return render_template('show_pipelines.html', pipelines=pipelines)


@app.route('/get_file', methods=['GET', 'POST'])
def get_file():
    if request.method == 'POST':
        file = request.files['fileInput']
        if file:
            metadata = {
                'Name': file.filename,
                'Size': file.seek(0, 2),  # Get file size in bytes
                'Type': file.content_type,
                'Last Modified': file.modified
            }
        else:
            metadata = {'Error': 'No file selected'}
        print(metadata)
        return render_template('file_metadata.html', metadata=metadata)
    return render_template('file_upload.html')


@app.route('/edit_pipeline/<int:pipeline_id>', methods=['GET', 'POST'])
def edit_pipeline(pipeline_id):
    pipeline = get_pipeline_by_id(pipeline_id)  # Retrieve pipeline data from the database
    msg = ''
    if request.method == 'POST':
        pipeline_name = request.form['pipeline_name']
        input_source = request.form['input_source']
        output_table = request.form['output_table']
        file_location = request.form['file_location']
        database_name = request.form['database_name']

        data = (pipeline_name, input_source, output_table, file_location, database_name, pipeline_id)
        update_pipeline(data)
        pipeline = get_pipeline_by_id(pipeline_id)
        msg = pipeline_name + ' Pipeline is updated successfully.'

    return render_template('edit_pipeline.html', pipeline=pipeline, msg=msg)


def get_pipeline_by_id(pipeline_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pipelines WHERE id = ?', (pipeline_id,))
    pipelines = cursor.fetchone()
    conn.close()
    return pipelines


def update_pipeline(data):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('update pipelines set name = ?, input_source = ?, output_table = ?, file_location = ?, database_name = ? where id = ?'
                   , (data[0],data[1],data[2],data[3],data[4],data[5]))
    conn.commit()
    conn.close()

    print('updates complete')


if __name__ == '__main__':
    app.run(debug=True)
