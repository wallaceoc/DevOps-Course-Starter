import os
import pytest
import requests
from todo_app import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

# Stub replacement for requests.get(url)
def stub(url, params={}):
    test_board_id = os.environ.get('CORNDEL_BOARD_ID')
    test_card_id = "123abc"    
    trello_key = os.environ.get('TRELLO_API_KEY')
    trello_token = os.environ.get('TRELLO_TOKEN')

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card'}]
        }]
        return StubResponse(fake_response_data)
    
    elif url == f'https://api.trello.com/1/board/{test_board_id}/cards?key={trello_key}&token={trello_token}':
        fake_response_data = [{
            'id': '123abc',
            'name': 'TestCard1',
            'idList': '64faketodo1234e86c4c2ff3',
            'desc': "Test desc",
            'due': None},
            {'id': '456def',
            'name': 'TestCard2',
            'idList': '64fakedone999985b9aac33',
            'desc': "Test desc 2",
            'due': '2023-09-05T09:59:00.000Z'
        }]
        return StubResponse(fake_response_data)
    
    elif url == f'https://api.trello.com/1/card/{test_card_id}?key={trello_key}&token={trello_token}':
        fake_response_data = [{
            'id': '123abc',
            'name': 'TestCard1',
            'idList': '64faketodo1234e86c4c2ff3',
            'desc': "Test desc",
            'due': None},
            {'id': '456def',
            'name': 'TestCard2',
            'idList': '64fakedone999985b9aac33',
            'desc': "Test desc 2",
            'due': '2023-09-05T09:59:00.000Z'
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')

def test_index_page(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')

    assert response.status_code == 200
    assert 'TestCard1' in response.data.decode()
    assert 'Test desc 2' in response.data.decode()
    assert False == response.is_json

def test_update_item(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'put', stub)

    #trello_response = requests.put(request_url, data={'idList': list_id})
    test_done_list_id = os.environ.get('CORNDEL_DONE_LIST_ID')
    #'64f666e31523671500de9f0f': 'Update Status'
    response = client.post('/todo/update_item', data={'123abc', 'Update Status'})

    assert response.status_code == 200
    assert 'TestCard1' in response.data.decode()
    assert 'Test desc 2' in response.data.decode()
    assert False == response.is_json
