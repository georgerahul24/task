import pickle
import time
import win10toast

file = "todo.data"
import datetime


def addTodos(name, date, priority="Low"):
    try:
        with open(file, 'rb') as f:
            todos = pickle.load(f)
    except FileNotFoundError:
        todos = {}

    finally:
        todos[name] = [date, priority]
        with open(file, 'wb') as f:
            pickle.dump(todos, f)


def getAllTodos():
    with open('todo.data', 'rb') as f:
        todos = pickle.load(f)
    alltodosdata = []
    for key, value in todos.items():
        alltodosdata.append([key, value[0], value[1]])
    return alltodosdata


def deleteTODO(name):
    with open('todo.data', 'rb+') as f:
        todos = pickle.load(f)
        del todos[name]
        f.seek(0)
        f.truncate(0)
        pickle.dump(todos, f)


class TODOHandler:
    def __init__(self):
        pass

    def start(self):
        def _start():
            todos = getAllTodos()
            latestdate = min(i[1] for i in todos)
            name = ''
            for todo in todos:
                if todo[1] == latestdate:
                    name = todo[0]

            deleteTODO(name)
            return name, latestdate

        while True:
            try:
                name, latestdate = _start()
                time.sleep(latestdate)  # assume tht it is in seconds
                win10toast.ToastNotifier().show_toast("Elsa", name)
            except:  # Give time to update the todos as this exception usually comes when no todos are present
                time.sleep(60)


TODOHandler().start()
