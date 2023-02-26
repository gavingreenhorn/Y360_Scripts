import os
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

TOKEN = os.environ['TOKEN']  # your token
ORG_ID = os.environ['ORG_ID']  # organisation ID
MAIL_DOMAIN = os.environ['MAIL_DOMAIN']

BASE_URL = f'https://api360.yandex.net/directory/v1/org/{ORG_ID}/'  # base API endpoint
USERS_URL = urljoin(BASE_URL, 'users/')  # users endpoint
GROUPS_URL = urljoin(BASE_URL, 'groups/')  # users endpoint
RULES_URL = f'https://api360.yandex.net/admin/v1/mail/routing/org/{ORG_ID}/rules'  # rules endpoint

OUTPUT_FOLDER_NAME = 'results'  # name of the folder that is created to store saved files
USERS_OUTPUT_FILE_NAME = 'users.csv'  # name under which a csv is saved

USERS_PER_PAGE = 800  # how many users are loaded
CACHE_EXPIRATION = 600  # milliseconds
MEMBERS_OUTPUT_LIMIT = 5  # milliseconds

USERS_INPUT_FIELDS = ['id', 'name', 'nickname', 'email']  # fields to read from JSON response - see available fields @ YAPI docs
USERS_OUTPUT_FIELDS = ['id', 'first_name', 'last_name', 'nickname', 'email']  # fields to output to CSV / console
GROUP_FIELDS = ('id', 'name', 'email', 'members')

BASE_HEADERS = {'Authorization': f'OAuth {TOKEN}'}
ACCEPT_HEADER = BASE_HEADERS | {'Accept': 'application/json'}
CONTENT_TYPE_HEADER = BASE_HEADERS | {'Content-Type': 'text/plain; charset=utf-8'}
REQUEST_PARAMETERS = {
    1: {'verb': 'get', 'headers': ACCEPT_HEADER},
    2: {'verb': 'get', 'headers': ACCEPT_HEADER},
    3: {'verb': 'patch', 'headers': CONTENT_TYPE_HEADER},
    4: {'verb': 'post', 'headers': CONTENT_TYPE_HEADER}
}

USER_STR_TEMPLATE = '{class_name}{fields}'
SAVED_TO_FILE = 'Saved results to {file}'

GROUP_INFO = ('ID: [{id}]  Name: [{name}]  Email: [{email}]'
              '\nMembers: [{members_count}]\n{members}')
GROUPS_MENU = 'Select an action:\n{actions}\n'

GROUP_FIELD_MANDATORY = 'Group {field} cannot be empty'
GROUP_ID_PROMPT = 'Enter group ID: '
NO_GROUP_ID_ENTERED = 'ID cannot be empty'
UNKNOWN_GROUP_ID = 'Could not find a group by the given identifier "{id}"'
JSON_CONTENT_MISSING = 'No json data was returned in response'
JSON_KEY_MISSING = 'JSON contains no {key}'
MEMBER_FORMAT_INVALID = (
    'Invalid user identifier provided: {identifier} '
    'Only:\n'
    '- IDs: [numeric strings]\n'
    f'- emails: [alphanumeric strings ending with {MAIL_DOMAIN}]\n'
    '- nicknames [alphanumeric strings]\n'
    'are accepted!')
NOT_A_NUMBER = 'Only numeric values are accepted'
TRUNCATED_NOTIFICATION = '\n[Members output truncated to {limit}]'
