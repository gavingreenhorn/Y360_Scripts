from typing import NamedTuple

from pprint import pprint
from requests_cache import CachedSession
from urllib.parse import urljoin

from Y360_allusers import get_users

from constants import (
    CACHE_EXPIRATION, GROUPS_URL, MAIL_DOMAIN,
    MEMBER_FORMAT_INVALID, GROUPS_MENU, ACCEPT_HEADER,
    CONTENT_TYPE_HEADER)


def validate_user_id(input_string, users):
    if input_string.isdigit():
        return {'type': 'user', 'id': input_string}
    elif input_string.endswith(MAIL_DOMAIN):
        if user := next((user for user in users if user.email == input_string), None):
            return {'type': 'user', 'id': user.id}
        return None
    elif (input_string.isalnum() or
          ''.join(input_string.split('.')).isalnum()):
        if user := next((user for user in users if user.nickname == input_string), None):
            return {'type': 'user', 'id': user.id}
        return None
    raise ValueError(
        MEMBER_FORMAT_INVALID.format(identifier=input_string))


def validate_user_ids(input_list, users):
    for input_string in input_list:
        yield validate_user_id(input_string, users)
        

def get_payload(session, for_method='post'):
    existing_users = get_users(session)
    payload = {}
    if for_method == 'post':
        if group_name := input('Name for the team:\n'):
            payload['name'] = group_name
        else:
            raise ValueError('Group name cannot be empty')
        payload['type'] = 'generic'
    label = input('Mailing list name (the part preceding @nmrauto.ru):\n')
    if label:
        payload['label'] = label
    elif not label and for_method == 'post':
        raise ValueError('Group label cannot be empty')
    if description := input('Description for the team:\n'):
        payload['description'] = description
    if admins := [
        user_id for user_id in
        validate_user_ids(
            input('Admin(s) ID(s):\n').split(), existing_users) if user_id]:
        payload['admins'] = admins
    if members := [
        user_id for user_id
        in validate_user_ids(
            input('Member(s) ID(s):\n').split(), existing_users) if user_id]:
        payload['members'] = members
    return payload


def send_request(action, session):
    parameters = {
        '1': {'verb': 'get', 'headers': ACCEPT_HEADER},
        '2': {'verb': 'get', 'headers': ACCEPT_HEADER},
        '3': {'verb': 'patch', 'headers': CONTENT_TYPE_HEADER},
        '4': {'verb': 'post', 'headers': CONTENT_TYPE_HEADER}
    }
    params = parameters[action]
    method = getattr(session, params['verb'])
    headers = params['headers']
    json = None
    url = GROUPS_URL
    if action in '23':
        if not (group_id := input('Enter group ID: ')):
            raise ValueError('ID cannot be empty')
        url = urljoin(GROUPS_URL, group_id)
    if action == '3':
        json=get_payload(session, for_method='patch')
    elif action == '4':
        json=get_payload(session)
    return method(
        url=url,
        headers=headers,
        json=json)


def main():
    with CachedSession(expire_after=CACHE_EXPIRATION) as session:
        if (action := input(GROUPS_MENU)) in '1234':
            response = send_request(action, session)
            print(response.status_code)
            pprint(response.json())
        else:
            print('Unsupported action')

if __name__ == '__main__':
    main()
