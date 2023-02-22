import csv
import sys
from collections import namedtuple
from typing import Iterable, Sequence, Optional

from requests_cache import CachedSession
from prettytable import PrettyTable

from constants import (
    USERS_INPUT_FIELDS, USERS_OUTPUT_FIELDS,
    CACHE_EXPIRATION, USERS_URL, USER_STR_TEMPLATE,
    USERS_PER_PAGE, TOKEN, OUTPUT_FILE_PATH)


class User(namedtuple('User', USERS_INPUT_FIELDS)):

    def __new__(cls, *args, **kwargs) -> 'User':
        kwargs = { k: v for k, v in kwargs.items() if k in cls._fields }
        return super().__new__(cls, *args, **kwargs)

    @property
    def first_name(self) -> Optional[str]:
        if self.name:
            return self.name.get('first')
        return None

    @property
    def last_name(self) -> Optional[str]:
        if self.name:
            return self.name.get('last')
        return None

    def __repr__(self) -> str:
        return str(self._asdict())

    def __str__(self) -> str:
        return USER_STR_TEMPLATE.format(
            class_name=self.__class__.__name__,
            fields=(self.id, self.nickname))


def get_users(session: CachedSession) -> Iterable[User]:
    headers = {
        'Authorization': f'OAuth {TOKEN}',
        'Accept': 'application/json'
    }
    params = {
        'perPage': USERS_PER_PAGE
    }
    response = session.get(
            url=USERS_URL,
            headers=headers,
            params=params)
    response.raise_for_status()
    if 'users' not in (json_data := response.json()):
        raise KeyError('Couldn\'t extract users from server response')
    for json_object in json_data['users']:
        yield User(**json_object)


def user_to_row(user: User) -> Iterable[Sequence]:
    yield [getattr(user, field) for field in USERS_OUTPUT_FIELDS]


def get_user_rows(session: CachedSession) -> Iterable[Sequence]:
    for user in get_users(session):
        yield from user_to_row(user)


def write_to_csv(rows) -> None:
    with open(OUTPUT_FILE_PATH, 'wt', encoding='utf8') as file:
            writer = csv.writer(
                file,
                dialect=csv.unix_dialect,
                quoting=csv.QUOTE_MINIMAL)
            writer.writerows(
                [USERS_OUTPUT_FIELDS, *rows])


def print_users_table(rows) -> None:
    users_table = PrettyTable()
    users_table.field_names = USERS_OUTPUT_FIELDS
    users_table.add_rows(rows)
    print(users_table)


def main():
    with CachedSession(expire_after=CACHE_EXPIRATION) as session:
        rows = list(get_user_rows(session))
        write_to_csv(rows)
        if '-v' in sys.argv:
            print_users_table(rows)


if __name__ == '__main__':
    main()
