import csv
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