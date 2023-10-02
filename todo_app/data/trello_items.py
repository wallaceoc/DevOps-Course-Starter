from flask import session

from todo_app.data.Item import Item

import os, requests

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """

    BOARD_ID = os.getenv('CORNDEL_BOARD_ID')
    API = os.getenv('TRELLO_API')
    BOARD = os.getenv('TRELLO_BOARD').replace('{id}', BOARD_ID)
    
    # https://api.trello.com/1/board/{board_id}/cards
    request_url = API+BOARD+'?key='+os.getenv('TRELLO_API_KEY')+'&token='+os.getenv('TRELLO_TOKEN')
    trello_response = requests.get(request_url)

    return build_card_items(trello_response.json())

def build_card_items(trello_response):
    card_items = []
    
    for trello_list in trello_response:
        card_items.append(Item.from_trello_card(trello_list))

    return card_items

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == id), None)


def add_item(title, list_id):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the card.
        list_id: The list to add the card to

    Returns:
        item: The saved item.
    """
    # Add the item to the list
    API = os.getenv('TRELLO_API')
    CARD = os.getenv('TRELLO_CARDs')
    request_url = API+CARD+'?key='+os.getenv('TRELLO_API_KEY')+'&token='+os.getenv('TRELLO_TOKEN')

    trello_response = requests.post(request_url, data={'name': title, 'idList': list_id})

    return trello_response

def save_item(card_id, list_id):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        card_id: The card_id to move to the new list.
        list_id: The list id to move the card to
    """

    API = os.getenv('TRELLO_API')
    CARD = os.getenv('TRELLO_CARD').replace('{id}', card_id)
    request_url = API+CARD+'?key='+os.getenv('TRELLO_API_KEY')+'&token='+os.getenv('TRELLO_TOKEN')

    trello_response = requests.put(request_url, data={'idList': list_id})

    return trello_response