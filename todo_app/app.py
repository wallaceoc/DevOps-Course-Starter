from flask import Flask, redirect, url_for, render_template, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_item, get_items, add_item, save_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    todo = get_items()
    print(todo)
    todo = sorted(todo, key=lambda x: x['status'], reverse=True)
    print(todo)
    return render_template('index.html', todo=todo)

@app.route('/todo/submit', methods=['POST'])
def add_todo():
    add_item(request.form.get('todo-title'))

    return redirect(url_for('index'))

@app.route('/todo/update', methods=['POST'])
def update_todo():
    todo = get_items()

    for item in todo:
        form_item = dict(request.form)
        id = str(item['id'])
        if id in form_item:            
            item['status'] = 'Completed'
        else:            
            item['status'] = 'Not Started'

        save_item(item)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
