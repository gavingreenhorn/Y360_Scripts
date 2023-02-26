from itertools import islice
from requests_cache import CachedSession
from urllib.parse import urljoin

from users import get_users
from utils import (
    GroupActions, GroupPrompts, get_users_table,
    get_user_rows, write_to_csv)
from constants import (
    CACHE_EXPIRATION, GROUPS_URL, MAIL_DOMAIN, GROUP_ID_PROMPT,
    MEMBER_FORMAT_INVALID, GROUPS_MENU, GROUP_INFO,
    GROUP_FIELDS, MEMBERS_OUTPUT_LIMIT, NO_GROUP_ID_ENTERED,
    TRUNCATED_NOTIFICATION, JSON_CONTENT_MISSING, REQUEST_PARAMETERS,
    NOT_A_NUMBER, GROUP_FIELD_MANDATORY, SAVED_TO_FILE, UNKNOWN_GROUP_ID)


def validate_group_id(input_string, groups):
    if input_string.isdigit():
        return input_string
    print(groups)
    if group_id := next(
        (group['id'] for group in groups
         if input_string in
         (group.get('name'), group.get('label'))), None
    ):
        return group_id
    else:
        raise ValueError(UNKNOWN_GROUP_ID.format(id=input_string))


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


def get_users_ids(input_list, users):
    return [
        user_id for user_id in
        validate_user_ids(input_list, users) if user_id]


def get_post_payload(users, create=True):
    payload = {}
    payload['type'] = 'generic'
    if group_name := input(GroupPrompts.NAME):
        payload['name'] = group_name
    elif create:
        raise ValueError(GROUP_FIELD_MANDATORY.format(field='name'))
    if label := input(GroupPrompts.LABEL):
        payload['label'] = label
    elif create:
        raise ValueError(GROUP_FIELD_MANDATORY.format(field='label'))
    if description := input(GroupPrompts.DESCRIPTION):
        payload['description'] = description
    if admins := get_users_ids(input(GroupPrompts.ADMINS).split(), users):
        payload['admins'] = admins
    if members := get_users_ids(input(GroupPrompts.MEMBERS).split(), users):
        payload['members'] = members
    return payload


def get_patch_payload(users):
    return get_post_payload(users, create=False)


def get_request_payload(action, users):
    if action == GroupActions.MODIFY_GROUP:
        return get_patch_payload(users)
    if action == GroupActions.CREATE_GROUP:
        return get_post_payload(users)
    return None


def make_request(action, session, users):
    verb, headers = REQUEST_PARAMETERS[action].values()
    method = getattr(session, verb)
    url = GROUPS_URL
    if action in (GroupActions.GROUP_DETAILS, GroupActions.MODIFY_GROUP):
        if not (group_id_input := input(GROUP_ID_PROMPT)):
            raise ValueError(NO_GROUP_ID_ENTERED)
        group_id = validate_group_id(
            group_id_input, get_json_data(
                GroupActions.SHOW_ALL_GROUPS, session, users).get('groups'))
        url = urljoin(GROUPS_URL, str(group_id))
    return method(
        url=url,
        headers=headers,
        json=get_request_payload(action, users))


def get_json_data(action, session, users):
    response = make_request(
        action, session, users)
    if not (json_data := response.json()):
        raise ValueError(JSON_CONTENT_MISSING)
    return json_data


def get_members_data(members, users):
    yield from get_user_rows(
        (user for user in users if user.id in
            (member['id'] for member in members)))


def get_group_data(json_object, users):
    group_data = {}
    for key in GROUP_FIELDS:
        group_data[key] = json_object.get(key)
    if members := group_data.get('members'):
        group_data['members'] = list(get_members_data(members, users))
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
        try:
            action = int(input(
                GROUPS_MENU.format(actions=GroupActions.to_str())))
        except ValueError:
            raise ValueError(NOT_A_NUMBER)
        if action in iter(GroupActions):
            existing_users = list(get_users(session))
            json_data = get_json_data(action, session, existing_users)
            for group_data in process_json_data(json_data, existing_users):
                if action == GroupActions.GROUP_DETAILS:
                    path.mkdir(exist_ok=True)
                    name, members = group_data['name'], group_data['members']
                    output_file = path / (name + '.csv')
                    write_to_csv(members, output_file)
                    print(SAVED_TO_FILE.format(file=output_file))
                print(get_group_users_table(
                    group_data, None if verbose else MEMBERS_OUTPUT_LIMIT))
        else:
            print('Unsupported action')
