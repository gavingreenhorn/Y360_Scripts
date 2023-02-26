import csv
from enum import Enum, IntEnum
from typing import Iterable, Sequence, TYPE_CHECKING

from prettytable import PrettyTable

from constants import USERS_OUTPUT_FIELDS

if TYPE_CHECKING:
    from users import User


def user_to_row(user: 'User') -> Iterable[Sequence]:
    yield [getattr(user, field) for field in USERS_OUTPUT_FIELDS]


def get_user_rows(users: Iterable['User']) -> Iterable[Sequence]:
    for user in users:
        yield from user_to_row(user)


def get_users_table(rows: Iterable[Sequence]) -> None:
    users_table = PrettyTable()
    users_table.field_names = USERS_OUTPUT_FIELDS
    users_table.add_rows(rows)
    return users_table


def write_to_csv(rows, filename) -> None:
    with open(filename, 'wt', encoding='utf8') as file:
        writer = csv.writer(
            file,
            dialect=csv.unix_dialect,
            quoting=csv.QUOTE_MINIMAL)
        writer.writerows(
            [USERS_OUTPUT_FIELDS, *rows])


class GroupPrompts(Enum):
    NAME = 'Name for the team:\n'
    LABEL = 'Mailing list name (the part preceding @nmrauto.ru):\n'
    DESCRIPTION = 'Description for the team:\n'
    ADMINS = 'Admin(s) ID(s):\n'
    MEMBERS = 'Member(s) ID(s):\n'

    def __str__(self):
        return self.value


class GroupActions(IntEnum):
    SHOW_ALL_GROUPS = 1
    GROUP_DETAILS = 2
    MODIFY_GROUP = 3
    CREATE_GROUP = 4

    def __str__(self):
        return f'{self.value}: {self.name.title().replace("_", " ")}'

    @classmethod
    def to_str(cls):
        return '\n'.join(str(action) for action in cls)
