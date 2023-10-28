import os
import pytest
from time import sleep
from threading import Thread
from todo_app import app
import requests
from flask import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv, find_dotenv
import time

def create_trello_board():
    url = "https://api.trello.com/1/boards"

    query = setup_query()  
    query['name'] = "SeleniumBoard"

    response = requests.request("POST", url, params=query)
    return json.loads(response.text)['id']

def delete_trello_board(board_id):
    url = f"https://api.trello.com/1/boards/{id}"

    query = setup_query()
    query['id'] = board_id

    response = requests.request( "DELETE",  url, params=query ) 

def setup_query():
    trello_key = os.environ.get('TRELLO_API_KEY')
    trello_token = os.environ.get('TRELLO_TOKEN')
    query = {'key': trello_key, 'token': trello_token}
    return query

def add_list_to_trello_board(name, board_id):
    url = "https://api.trello.com/1/lists"

    query = setup_query()
    query['name'] = name
    query['idBoard'] = board_id

    response = requests.request( "POST", url, params=query )
    return json.loads(response.text)['id']

def add_card_to_trello_list(name, list_id):
    url = "https://api.trello.com/1/cards"

    query = setup_query()
    query['name'] = name
    query['idList'] = list_id

    response = requests.request("POST", url, params=query)
    return json.loads(response.text)['id']

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Use our test integration config instead of the 'real' version
    load_dotenv(override=True)

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    todo_list_id = add_list_to_trello_board("TEST_TO_DO", board_id)
    done_list_id = add_list_to_trello_board("TEST_DONE", board_id)

    os.environ['CORNDEL_BOARD_ID'] = board_id
    os.environ['CORNDEL_TODO_LIST_ID'] = todo_list_id
    os.environ['CORNDEL_DONE_LIST_ID'] = done_list_id

    card_id = add_card_to_trello_list('TestCard', todo_list_id)

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    # Give the app a moment to start
    sleep(1)

    yield application

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
 
    text_box = driver.find_element(By.ID, "todo-title")
    text_box.send_keys("NEW_TEST_CARD_Selenium3")
    driver.find_element(By.ID, "todo-submit").click()
    time.sleep(2)
    content = driver.page_source

    assert driver.title == 'To-Do App' 
    assert 'NEW_TEST_CARD_Selenium3' in content
