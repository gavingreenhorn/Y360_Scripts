from itertools import islice
from requests_cache import CachedSession
from urllib.parse import urljoin

from users import get_users
from utils import get_users_table, get_user_rows
from constants import (
    CACHE_EXPIRATION, GROUPS_URL, MAIL_DOMAIN,
    MEMBER_FORMAT_INVALID, GROUPS_MENU, ACCEPT_HEADER,
    CONTENT_TYPE_HEADER, GROUP_INFO, GROUP_FIELDS,
    MEMBERS_OUTPUT_LIMIT, TRUNCATED_NOTIFICATION,
    JSON_CONTENT_MISSING)


def validate_user_id(input_string, users):
    if input_string.isdigit():
        return {'type': 'user', 'id': input_string}
    if input_string.endswith(MAIL_DOMAIN):
        attribute = 'email'
    elif (input_string.isalnum() or
          ''.join(input_string.split('.')).isalnum()):
        attribute = 'nickname'
    else:
        raise ValueError(
            MEMBER_FORMAT_INVALID.format(identifier=input_string))
    if user_id := next((user.id for user in users
                        if getattr(user, attribute) == input_string), None):
        return {'type': 'user', 'id': user_id}
    return None


def validate_user_ids(input_list, users):
    for input_string in input_list:
        yield validate_user_id(input_string, users)
        

def get_payload(session, existing_users, for_method='post'):
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


def get_request_parameters(action, session):
    parameters = {
        '1': {'verb': 'get', 'headers': ACCEPT_HEADER},
        '2': {'verb': 'get', 'headers': ACCEPT_HEADER},
        '3': {'verb': 'patch', 'headers': CONTENT_TYPE_HEADER},
        '4': {'verb': 'post', 'headers': CONTENT_TYPE_HEADER}
    }
    params = parameters[action]
    method = getattr(session, params['verb'])
    headers = params['headers']
    url = GROUPS_URL
    if action in '23':
        if not (group_id := input('Enter group ID: ')):
            raise ValueError('ID cannot be empty')
        url = urljoin(GROUPS_URL, group_id)
    return method, url, headers


def get_request_payload(action, session, users):
    json = None
    if action == '3':
        json=get_payload(session, users, for_method='patch')
    elif action == '4':
        json=get_payload(session, users)
    return json


def get_group_data(json_object, users):
    group_data = {}
    for key in GROUP_FIELDS:
        group_data[key] = json_object.get(key)
    if members := group_data.get('members'):
        group_data['members'] = get_user_rows(
            (user for user in users if user.id in
            (member['id'] for member in members)))
    group_data['members_count'] = len(members) if members else 0
    yield group_data


def get_group_users_table(data, limit=None):
    if members := data.get('members'):
        data['members'] = (
            get_users_table(islice(members or (), limit)) if limit
            else get_users_table(members))
    return (GROUP_INFO.format(**data) + (
            TRUNCATED_NOTIFICATION.format(limit=limit) if limit else ''))


def process_json_data(json_data, users):
    if 'groups' in json_data:
        for group in json_data['groups']:
            yield from get_group_data(group, users)
    else:
        yield from get_group_data(json_data, users)


def main(path, verbose=False, *args, **kwargs):
    with CachedSession(expire_after=CACHE_EXPIRATION) as session:
        if (action := input(GROUPS_MENU)) in '1234':
            existing_users = list(get_users(session))
            method, url, headers = get_request_parameters(action, session)
            payload = get_request_payload(action, session, existing_users)
            response = method(
                url=url,
                headers=headers,
                json=payload)
            if not (json_data := response.json()):
                raise ValueError(JSON_CONTENT_MISSING)
            for group_data in process_json_data(json_data, existing_users):
                print(get_group_users_table(
                    group_data, None if verbose else MEMBERS_OUTPUT_LIMIT))
        else:
            print('Unsupported action')

if __name__ == '__main__':
    main()
