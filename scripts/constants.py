import os
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

TOKEN = os.environ['TOKEN']  # your token
ORG_ID = os.environ['ORG_ID']  # organisation ID
MAIL_DOMAIN = os.environ['MAIL_DOMAIN']

BASE_URL = 'https://api360.yandex.net/directory/v1/org/{org_id}/'.format(org_id=ORG_ID) # base API endpoint
USERS_URL = urljoin(BASE_URL, 'users/')  # users endpoint
GROUPS_URL = urljoin(BASE_URL, 'groups/')  # users endpoint
RULES_URL = urljoin(BASE_URL, 'rules/')  # rules endpoint

OUTPUT_FOLDER_NAME = 'results'  # name of the folder that is created to store saved files
OUTPUT_FILE_NAME = 'users.csv'  # name under which a csv is saved

USERS_PER_PAGE = 800  # how many users are loaded
CACHE_EXPIRATION = 600  # milliseconds
MEMBERS_OUTPUT_LIMIT = 5 # milliseconds

USERS_INPUT_FIELDS = ['id', 'name', 'nickname', 'email']  # fields to read from JSON response - see available fields @ YAPI docs
USERS_OUTPUT_FIELDS = ['id', 'first_name', 'last_name', 'nickname', 'email']  # fields to output to CSV / console
GROUP_FIELDS = ('id', 'name', 'email', 'members')

BASE_HEADERS = {'Authorization': f'OAuth {TOKEN}'}
ACCEPT_HEADER = BASE_HEADERS | {'Accept': 'application/json'}
CONTENT_TYPE_HEADER = BASE_HEADERS | {'Content-Type': 'text/plain; charset=utf-8'}

USER_STR_TEMPLATE = '{class_name}{fields}'

# MESSAGES

GROUP_INFO = ('ID: [{id}]  Name: [{name}]  Email: [{email}]'
              '\nMembers: [{members_count}]\n{members}')
GROUPS_MENU = """
Select an action:
1. Show all groups
2. Group details
3. Change a group
4. Create a new group
"""
JSON_CONTENT_MISSING = 'No json data was returned in response'
MEMBER_FORMAT_INVALID = (
    'Invalid user identifier provided: {identifier} '
    'Only:\n'
    '- IDs: [numeric strings]\n'
    f'- emails: [alphanumeric strings ending with {MAIL_DOMAIN}]\n'
    '- nicknames [alphanumeric strings]\n'
    'are accepted!')
TRUNCATED_NOTIFICATION = '\n[Members output truncated to {limit}]'

# RULES TEMPLATES

RECIEVER_EMAIL = f'someone{MAIL_DOMAIN}'
FORWARDED_TO = f'someone-else{MAIL_DOMAIN}'
DEFAULT_RULES = {
    'rules': [
        {
            'actions': [
                {
                    'action': 'forward',
                    'data': {
                        'email': RECIEVER_EMAIL
                    }
                }
            ],
            'condition': {
                'to': FORWARDED_TO,
                'from': {'$ne': RECIEVER_EMAIL},
            },
            'scope': {
                'direction': 'inbound'
            },
            'terminal': False
        }
    ]
}
