from collections import namedtuple
from pathlib import Path
from typing import Iterable, Optional

from requests_cache import CachedSession

from constants import (
    CACHE_EXPIRATION, OUTPUT_FILE_NAME, USERS_INPUT_FIELDS, USER_STR_TEMPLATE,
    USERS_PER_PAGE, USERS_URL, ACCEPT_HEADER)
from utils import get_user_rows, write_to_csv, get_users_table


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
    params = {
        'perPage': USERS_PER_PAGE
    }
    response = session.get(
            url=USERS_URL,
            headers=ACCEPT_HEADER,
            params=params)
    response.raise_for_status()
    if 'users' not in (json_data := response.json()):
        raise KeyError('Couldn\'t extract users from server response')
    for json_object in json_data['users']:
        yield User(**json_object)


def main(path, verbose=False, *args, **kwargs):
    path.mkdir(exist_ok=True)
    output_file = Path(path) / OUTPUT_FILE_NAME
    with CachedSession(expire_after=CACHE_EXPIRATION) as session:
        rows = list(get_user_rows(get_users(session)))
        write_to_csv(rows, output_file)
        if verbose:
            print(get_users_table(rows))
    print(f'Saved results to {output_file}')


if __name__ == '__main__':
    main(Path(input('Enter a path to save directory:\n')))
