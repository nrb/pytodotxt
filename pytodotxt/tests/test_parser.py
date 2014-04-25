from pytodotxt.parser import match_contexts, match_projects, match_priority
from pytodotxt.parser import match_completed, parse


def test_match_one_context():
    line = "This has one @context"
    contexts = match_contexts(line)
    assert contexts == ['@context']

def test_match_no_context():
    line = "No contexts"
    contexts = match_contexts(line)
    assert contexts == []

def test_match_multiple_contexts():
    line = "Has @many @contexts"
    contexts = match_contexts(line)
    assert contexts == ['@many', '@contexts']

def test_match_context_not_project():
    line = "Has a @context and a +project"
    contexts = match_contexts(line)
    assert contexts == ['@context']

def test_match_one_project():
    line = "Has one +project"
    projects = match_projects(line)
    assert projects == ['+project']

def test_match_no_project():
    line = "No project"
    projects = match_projects(line)
    assert projects == []

def test_match_multiple_projects():
    line = "More +than on +project"
    projects = match_projects(line)
    assert projects == ['+than', '+project']

def test_match_completed_line():
    line = 'x 2014-01-01 Do thing.'
    completed = match_completed(line)
    assert completed == True

def test_fail_to_match_no_x_line():
    line = '10-10-2010'
    completed = match_completed(line)
    assert completed == False

def test_fail_to_match_no_date_line():
    line = 'x This task is not properly completed.'
    completed = match_completed(line)
    assert completed == False

def test_match_priority():
    line = "(A) High priority"
    priority = match_priority(line)
    assert priority == "(A)"

def test_match_no_priority():
    line = "No priorities"
    priority = match_priority(line)
    assert priority == ''

def test_parse_for_project_context_and_completed():
    line = "Has a +project and a @context"
    values = parse(line)

    assert 'projects' in values.keys()
    assert 'contexts' in values.keys()
    assert 'completed' in values.keys()
    assert 'priority' in values.keys()

def test_parse_populates_artifacts():
    line = "Has a +project and a @context"
    artifacts = parse(line)
    assert artifacts['projects'] == (['+project'])
    assert artifacts['contexts'] == (['@context'])

def test_parse_populates_multiple_projects():
    line = "Has +multiple +projects"
    artifacts = parse(line)
    assert artifacts['projects'] == (['+multiple', '+projects'])

def test_parse_populates_multiple_contexts():
    line = "Has @multiple @contexts"
    artifacts = parse(line)
    assert artifacts['contexts'] == (['@multiple', '@contexts'])

def test_parse_populates_completed():
    line = "x 1910-10-10 is done."
    artifacts = parse(line)
    assert artifacts['completed'] == True

def test_parse_doesnt_add_incomplete():
    line = "(A) Do this first!"
    artifacts = parse(line)
    assert artifacts['completed'] == False

def test_parse_adds_priorities():
    line = "(A) Do this first!"
    artifacts = parse(line)
    assert artifacts['priority'] == '(A)'

def test_parse_no_priority():
    line = "Do this first!"
    artifacts = parse(line)
    assert artifacts['priority'] == ''
