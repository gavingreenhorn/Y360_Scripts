# Y360 API scripts
## Requirements
 - Python 3.9+ (`python3 --version`)
## Deployment
 - `git clone git@github.com:gavingreenhorn/Y360_Scripts.git`
 - `cd Y360_Scripts`
 - *optionally & preferrably deploy to isolated environment:*  
 `python3 -m venv venv`  
 `. venv/bin/activate`
 - `python3 -m pip install -r requirements.txt`
 - `echo TOKEN=... > .env`
 - `echo ORG_ID=... >> .env`
 - `echo MAIL_DOMAIN=... >> .env`

## Usage
### Users
- get all users: `python3 scripts users.py`

| user data is controled by `USERS_INPUT_FIELDS` (see scripts/constants.py)

| csv columns are controlled by `USERS_OUTPUT_FIELDS`

| csv file is saved to `OUTPUT_FOLDER_NAME` under `USERS_OUTPUT_FILE_NAME` inside the current working directory

| if `-o --output` argument is given, file is saved to the given directory under `USERS_OUTPUT_FILE_NAME`

| calling with the option `-v --verbose` outputs user data to console 
### Groups
Calling with the option `-v --verbose` will output all group members to console.

Default number of users to output is controlled by the `MEMBERS_OUTPUT_LIMIT` constant.

- get all groups: `python3 scripts groups`

| select 1 in the menu
- get group details: `python3 scripts groups`

| select 2 in the menu and provide group ID

| if `[-o --output]` option is specified, saves file to the specified location, otherwise saves to the location defined by the `OUTPUT_FOLDER_NAME` constant
- patch existing group: `python3 scripts groups`

| select 3 in the menu, provide group ID and required details
- create a new group: `python3 scripts groups`

| select 4 in the menu and provide required details
### Rules
- get current mail routing configuration: `python3 scripts rules`

| 'pretty prints' raw JSON response containing current rules