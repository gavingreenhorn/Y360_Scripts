import requests
from pprint import pprint

from constants import (
    RULES_URL, ACCEPT_HEADER,
    JSON_CONTENT_MISSING, JSON_KEY_MISSING)


def print_rules(rules):
    print('Current rules configuration:\n')
    for rule in rules:
        pprint(rule)


def main(*args, **kwargs):
    with requests.Session() as session:
        response = session.get(RULES_URL, headers=ACCEPT_HEADER)
        response.raise_for_status()
        if not (json := response.json()):
            raise ValueError(JSON_CONTENT_MISSING)
        if not (rules := json.get('rules')):
            raise KeyError(JSON_KEY_MISSING.format(key='rules'))
        print_rules(rules)            
