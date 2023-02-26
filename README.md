# Y360 API scripts
## Requirements
 - Python 3.9+ (`python3 --version`)
## Deployment
 `git clone git@github.com:gavingreenhorn/Y360_Scripts.git`  
 `cd Y360_Scripts`  
 > optionally & preferrably deploy to isolated environment:
 ```
 python3 -m venv venv 
 . venv/bin/activate
 ```
 `python3 -m pip install -r requirements.txt`  
 `echo TOKEN=... > .env`  
 `echo ORG_ID=... >> .env`  
 `echo MAIL_DOMAIN=... >> .env`

## Usage
### __Users__
**Get all users:**
```
python3 scripts users
```

> User data is controled by the `USERS_INPUT_FIELDS` constant    
Columns in the console output and csv file are controlled by `USERS_OUTPUT_FIELDS`

> Csv file is saved to `OUTPUT_FOLDER_NAME` under `USERS_OUTPUT_FILE_NAME` inside the current working directory  
If `[-o --output]` argument is given, file is saved to the given directory under `USERS_OUTPUT_FILE_NAME`

> Calling with the option `[-v --verbose]` outputs user data to console 
<hr>

### __Groups__

```
python3 scripts group
```

>Default number of group members to print to console is controlled by the `MEMBERS_OUTPUT_LIMIT` constant.  
Calling with the option `[-v --verbose]` will output all members.

> User fields and output columns for group members are defined by the same constants as for `users` request



**Get all groups:** select option 1  
**Get group details:** select option 2  
> If `[-o --output]` option is specified, saves a csv file with group members to the specified location, otherwise saves it to the location defined by the `OUTPUT_FOLDER_NAME` constant; group name is used as a file name

**Patch existing group:**: select option 3  
**Create a new group:** select option 4
<hr>

### __Rules__
**Get current mail routing configuration:**
```
python3 scripts rules
```
>"pretty prints" raw JSON response to console