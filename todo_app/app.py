from flask import Flask, redirect, url_for, render_template, request

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items, save_item, add_item, get_item
from todo_app.view_model import ViewModel

import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        todo_cards = get_items()
        sorted_todo = sorted(todo_cards, key=lambda x: x.idList, reverse=True)
        item_view_model = ViewModel(sorted_todo)
        return render_template('index.html', todo_view_model=item_view_model)

    @app.route('/todo/submit', methods=['POST'])
    def add_todo():
        add_item(request.form.get('todo-title'), os.getenv('CORNDEL_TODO_LIST_ID'))

        return redirect(url_for('index'))

    @app.route('/todo/update', methods=['POST'])
    def update_todo():
        todo_cards = get_items()

        for todo_card in todo_cards:
            form_item = dict(request.form)
            todo_card_id = str(todo_card.id)
            if todo_card_id in form_item:
                if len(form_item[todo_card_id]) != 0:
                    # this todo item has been udpated so persist to trello
                    # only get form data for check boxes that are checked
                    save_item(todo_card_id, os.getenv('CORNDEL_DONE_LIST_ID'))            
            else:
                save_item(todo_card_id, os.getenv('CORNDEL_TODO_LIST_ID'))

        return redirect(url_for('index'))

    @app.route('/todo/update_item', methods=['POST'])
    def update_single_item():
        form_item = dict(request.form)
        form_item_id = list(form_item.keys())[0]

        todo_card = get_item(form_item_id)
        done_list_id = os.getenv('CORNDEL_DONE_LIST_ID')
        if(todo_card.idList == done_list_id):
            save_item(form_item_id, os.getenv('CORNDEL_TODO_LIST_ID'))
        else:
            save_item(form_item_id, done_list_id)

        return redirect(url_for('index'))
    
    return app