import os
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']  # your token
ORG_ID = os.environ['ORG_ID']  # organisation ID

BASE_URL = 'https://api360.yandex.net/directory/v1/org/{org_id}/'.format(org_id=ORG_ID) # base API endpoint
USERS_URL = urljoin(BASE_URL, 'users/')  # users endpoint
GROUPS_URL = urljoin(BASE_URL, 'groups/')  # users endpoint
RULES_URL = urljoin(BASE_URL, 'rules/')  # rules endpoint
MAIL_DOMAIN = os.environ['MAIL_DOMAIN']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # current directory location
SAVE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'results')  # save directory location
OUTPUT_FILE_NAME = 'users.csv'  # name under which a csv is saved
OUTPUT_FILE_PATH = os.path.join(SAVE_DIR, OUTPUT_FILE_NAME)  # full path to a a file being saved

USERS_PER_PAGE = 800  # how many users are loaded
CACHE_EXPIRATION = 600  # milliseconds

USERS_INPUT_FIELDS = ['id', 'name', 'nickname', 'email']  # fields to read from JSON response - see available fields @ YAPI docs
USERS_OUTPUT_FIELDS = ['id', 'first_name', 'last_name', 'nickname', 'email']  # fields to output to CSV / console

BASE_HEADERS = {'Authorization': f'OAuth {TOKEN}'}
ACCEPT_HEADER = BASE_HEADERS | {'Accept': 'application/json'}
CONTENT_TYPE_HEADER = BASE_HEADERS | {'Content-Type': 'text/plain; charset=utf-8'}

USER_STR_TEMPLATE = '{class_name}{fields}'

# MESSAGES

MEMBER_FORMAT_INVALID = (
    'Invalid user identifier provided: {identifier} '
    'Only:\n'
    '- IDs: [numeric strings]\n'
    f'- emails: [alphanumeric strings ending with {MAIL_DOMAIN}]\n'
    '- nicknames [alphanumeric strings]\n'
    'are accepted!')
GROUPS_MENU = """
Select an action:
1. Show all groups
2. Group details
3. Change a group
4. Create a new group
"""

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
