import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import timedelta

app = Flask(__name__)

# Caminho para o arquivo JSON
TASKS_FILE = 'tasks.json'

# Função para carregar tarefas do arquivo JSON
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Função para salvar tarefas no arquivo JSON
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Carregar as tarefas no início
tasks = load_tasks()

@app.route('/')
def index():
    total_time = sum([timedelta(hours=task['hours'], minutes=task['minutes']) for task in tasks], timedelta())
    return render_template('index.html', tasks=tasks, total_time=total_time)

@app.route('/add_task', methods=['POST'])
def add_task():
    project_name = request.form['project_name']
    task_name = request.form['task_name']
    hours = int(request.form['hours'])
    minutes = int(request.form['minutes'])
    description = request.form['description']
    
    # Adicionar o Project Name ao dicionário de tarefa
    task = {
        'project_name': project_name,
        'name': task_name,
        'hours': hours,
        'minutes': minutes,
        'description': description
    }
    
    tasks.append(task)
    save_tasks(tasks)  # Salvar as tarefas no arquivo JSON após adicionar uma nova
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
