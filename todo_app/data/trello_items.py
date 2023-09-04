from flask import session

import os, requests

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """

    BOARD_ID = os.getenv('CORNDEL_BOARD_ID')
    API = os.getenv('TRELLO_API')
    BOARD = os.getenv('TRELLO_BOARD').replace('{id}', BOARD_ID)
    request_url = API+BOARD+'?key='+os.getenv('TRELLO_API_KEY')+'&token='+os.getenv('TRELLO_TOKEN')
    trello_response = requests.get(request_url)

    return build_items_dict(trello_response.json())

def build_items_dict(trello_response):
    cards = []
    
    for trello_list in trello_response:
        cards.append(trello_list)

    return cards

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


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