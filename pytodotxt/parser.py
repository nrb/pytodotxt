import re
import collections

def parse(line):
    artifacts = {}
    artifacts['projects'] = match_projects(line)
    artifacts['contexts'] = match_contexts(line)
    artifacts['priority'] = None
    artifacts['completed'] = None

    priority = match_priority(line)

    if priority:
        artifacts['priority'] = (priority)

    completed = match_completed(line)
    if completed:
        artifacts['completed'] = (completed)

    return artifacts

def _generic_matcher(symbol, line):
    results = []

    if not symbol in line:
        return results

    words = line.split()
    for word in words:
        if word.startswith(symbol):
            results.append(word)

    return results


def match_projects(line):
    return _generic_matcher('+', line)

def match_contexts(line):
    return _generic_matcher('@', line)

def match_priority(line):
    match = re.match("^\(\w\) ", line)
    if match:
        priority = match.group()[:-1]
        return priority
    return ""

def match_completed(line):
    if re.match("^x \d{4}-\d{2}-\d{2}", line):
        return True
    return False

