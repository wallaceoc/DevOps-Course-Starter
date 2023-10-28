from todo_app.view_model import ViewModel
from todo_app.data.Item import Item

import pytest

@pytest.fixture
def view_model() -> ViewModel:
    todo_items = []
    item1 = Item("id1", "ToDo1", "Test Todo 1", "testListid", "", "To Do")
    item2 = Item("id2", "ToDo2", "Test Todo 2", "testListid", "", "Done")
    todo_items.append(item1)
    todo_items.append(item2)
    view_model = ViewModel(todo_items)
    return view_model

def test_view_model_done_property(view_model: ViewModel):
    done_items = view_model.done_items

    assert len(done_items) == 1

def test_view_model_todo_property(view_model: ViewModel):
    todo_items = view_model.todo_items

    assert len(todo_items) == 1
    assert todo_items[0].status == "To Do"

def test_view_model_doing_property(view_model: ViewModel):
    doing_items = view_model.doing_items

    assert len(doing_items) == 0