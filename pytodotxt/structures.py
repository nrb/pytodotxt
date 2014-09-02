from pytodotxt.parser import parse

from datetime import datetime


class Task(object):
    def __init__(self, line):
        self.line = line
        attributes = parse(line)
        self.priority = attributes['priority']
        self.projects = attributes['projects']
        self.contexts = attributes['contexts']
        self.completed = attributes['completed']

    @staticmethod
    def done_string():
        return 'x ' + Task.done_date() + ' '

    @staticmethod
    def done_date():
        return datetime.now().strftime('%Y-%d-%m')

    def done(self):
        new_line = Task.done_string() + self.line
        self.line = new_line
        self.completed = True

class List(object):
    def __init__(self, lines):
        self.lines = lines
        self.tasks = [Task(line) for line in lines]

    def filter(self, keyword=None, context=None, project=None, completed=None):
        # Add a kwargs parsing method in here that takes the keys
        # and does the search base on the attribute name

        # Add our own hashing method or list insertion function to
        # maintain our order, since sets lose it.

        # Hashing can be cheated by maintaining a parallel,
        # empty dictionary that just has the key.
        # That dict could be useful for tracking changes during runtime, too.
        results = set()
        if keyword:
            results.update([t.line for t in self.tasks if keyword in t.line])
        if context:
            results.update([t.line for t in self.tasks if context in t.contexts])
        if project:
            results.update([t.line for t in self.tasks if project in t.projects])
        if completed is not None:
            results.update([t.line for t in self.tasks if t.completed == completed])
        return list(results)
