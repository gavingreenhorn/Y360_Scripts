from argparse import ArgumentParser
from pathlib import Path

from constants import OUTPUT_FOLDER_NAME
from groups import main as run_groups
from rules import main as run_rules
from users import main as run_users


def main(args):
    preferred_location = args.output
    if preferred_location and Path(preferred_location).parent.exists():
        save_dir = Path(preferred_location)
    else:
        save_dir = Path(Path.cwd() / OUTPUT_FOLDER_NAME)
    actions = {
        'users': run_users,
        'groups': run_groups,
        'rules': run_rules
    }
    actions[args.script](save_dir, verbose=args.verbose)


if __name__ == '__main__':
    parser = ArgumentParser(description='Menu to launch scripts')
    parser.add_argument(
        'script',
        choices=('users', 'groups', 'rules'),
        help='Select a script to run')
    parser.add_argument('-o', '--output', help='Save directory path')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output to console')
    main(parser.parse_args())
