import requests
from pprint import pprint

from constants import RULES_URL, DEFAULT_RULES, TOKEN


ERROR_TEMPLATE = '{code}: {reason}'


def get_rules(session):
    return session.get(RULES_URL)


def put_rules(session, json=DEFAULT_RULES):
    response = session.put(
        RULES_URL,
        json=json
    )
    response.raise_for_status()
    return get_rules(session)


def print_rules(rules):
    print('Current rules configuration:\n')
    for rule in rules:
        pprint(rule)


def modify(json):
    return json


def main(*args, **kwargs):
    with requests.Session() as session:
        session.headers.update({
            'Authorization': f'OAuth {TOKEN}',
            'Content-Type': 'text/plain; charset=utf-8'
        })
        response = get_rules(session)
        try:
            response.raise_for_status()
        except Exception:
            print(ERROR_TEMPLATE.format(
                    code=response.status_code,
                    reason=response.reason
                ))
        else:
            json = response.json()
            if json and ('rules' in json):
                print_rules(json['rules'])
            if input('Write a new rule? [Y|N]: ') in ('Y', 'y', 'yes'):
                json = modify(json)
                put_rules(session, json)


if __name__ == '__main__':
    main()
