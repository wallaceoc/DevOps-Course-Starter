import os

class Item:
    def __init__(self, id, name, desc, idList, due_date, status = 'To Do'):
        self.id = id
        self.name = name
        self.description = desc
        self.idList = idList
        self.dueDate = due_date
        self.status = status        

    @classmethod
    def from_trello_card(cls, card):
        todo_list_id = os.getenv('CORNDEL_TODO_LIST_ID')
        trello_idList = card['idList']
        status = "To Do" if trello_idList == todo_list_id else "Done"
        return cls(card['id'], card['name'], card['desc'], trello_idList, card['due'], status)
        
    def datePickerDueDate(self):
        if(self.dueDate is None):
            return ""
        return self.dueDate[0:10]