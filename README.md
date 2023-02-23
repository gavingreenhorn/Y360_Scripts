# Y360 API scripts
## Requirements
 - Python 3.9+ (`python3 --version`)
## Deployment
 - `git clone git@github.com:gavingreenhorn/Y360_Scripts.git`
 - `cd .YandexScripts`
 - `python3 -m venv venv`
 - `. venv/bin/activate`
 - `python3 -m pip install -r requirements.txt`
 - `echo TOKEN=... > .env`
 - `echo ORG_ID=... >> .env`
 - `echo MAIL_DOMAIN=... >> .env`

## Usage

- get all users: `python3 scripts users.py`

| user data is controled by `USERS_INPUT_FIELDS` (see scripts/constants.py)

| csv columns are controlled by `USERS_OUTPUT_FIELDS`

| csv file is saved to OUTPUT_FOLDER_NAME under OUTPUT_FILE_NAME inside the current working directory (unless -o --output is specified)

| calling with the argument `-v --verbose` outputs user data to console 
- get all groups: `python3 scripts groups`

| select 1 in the menu
- get group details: `python3 scripts groups`

| select 2 in the menu and provide group ID
- patch existing group: `python3 scripts groups`

| select 3 in the menu, provide group ID and required details
- create a new group: `python3 scripts groups`

| select 4 in the menu and provide required details