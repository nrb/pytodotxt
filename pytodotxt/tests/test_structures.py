from pytodotxt.structures import List, Task

from mock import patch
import pytest

def test_init_task():
    t = Task('(A) +project @context')
    assert t.priority == '(A)'
    assert t.contexts == ['@context']
    assert t.projects == ['+project']
    assert t.completed == False

def test_complete_task():
    line = "This task will be done!"
    t = Task(line)

    @staticmethod
    def fake_done_date():
        return '1910-10-10'
    with patch.object(Task,'done_date',fake_done_date):
        t.done()

    assert t.completed == True
    assert t.line == 'x 1910-10-10 ' + line

def test_init_list():
    lines = ['A line with @context and a +project',
             'A line without context but a +project']
    l = List(lines)
    assert len(l.lines) == 2

def test_init_list():
    lines = ['A line with @context and a +project',
             'A line without context but a +project']
    l = List(lines)
    assert len(l.tasks) == 2

def test_list_filter_keyword():
    target = 'Another line with @context and @thing.'
    lines = ['A line with @context.',
             target]
    l = List(lines)
    assert l.filter('thing') == [target]

def test_list_filter_context():
    targets = ['This line will match with @context',
               'So will this @context line.']
    lines = []
    for line in targets:
        lines.append(line)
    lines.append("Won't match.")
    l = List(lines)
    results = l.filter(context='@context')
    assert len(results) == 2
    for t in targets:
        assert t in results

def test_list_filter_projects():
    targets = ['This line has a +project',
               'So do this +project']
    lines = []
    for line in targets:
        lines.append(line)
    lines.append("Won't match")
    l = List(lines)

    results = l.filter(project='+project')
    assert len(results) == 2
    for t in targets:
        assert t in results

def test_list_filter_projects_context():
    targets = ['This line has a +project and a @context',
               'This line also has a +project and a @context']
    lines = []
    for line in targets:
        lines.append(line)
    lines.append("Won't match +butproject")
    l = List(lines)
    results = l.filter(project="+project", context="@context")
    assert len(results) == 2
    for t in targets:
        assert t in results

def test_list_filter_completed():
    targets = ['x 1910-10-11 Done.',
               'x 1910-10-12 Also done.']
    lines = []
    for line in targets:
        lines.append(line)
    lines.append('Not done')
    l = List(lines)
    results = l.filter(completed=True)
    assert len(results) == 2
    for t in targets:
        assert t in results

def test_list_filtering_maintains_order():
    pytest.skip("Not yet implemented")

def test_list_filter_without_project():
    pytest.skip("Not yet implemented")

def test_list_filter_without_context():
    pytest.skip("Not yet implemented")

def test_list_filter_not_project():
    """Make sure we can match everything that DOESN'T match specified project."""
    targets = ["No project here", "Nor here."]
    lines = []
    for line in targets:
        lines.append(line)
    lines.append("This has a +project")
    l = List(lines)
    results = l.filter(not_project="+project")
    assert len(results) == 2
    for t in targets:
        assert t in results

def test_list_filter_not_context():
    pytest.skip("Not yet implemented")

def test_list_not_keyword():
    pytest.skip("Not yet implemented")
