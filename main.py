import yaml
from os import path, environ
from pathlib import Path
import logging
from argparse import ArgumentParser
from termcolor import colored


logger = logging.getLogger(__name__)


class Todo:
    def __init__(self, file="todo.yaml"):
        self.file_name = file
        if not path.isfile(file):
            logger.info("Todo file does not exist, creating one instead")
            try:
                Path(file).touch()
            except Exception as e:
                logger.critical(f"Failed to create Todo file ({file}): {e}")
                return

        with open(file, "r", encoding="utf-8") as file:
            self._raw = yaml.safe_load(file)

    def write(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.write(yaml.safe_dump(self._raw, sort_keys=False))

    def print(self, item):
        heading = self.headings[item]

        print(colored(f"{item} - {heading}", "red"))
        counter = 0
        for item in self._raw[heading]:
            counter += 1
            print(f" {counter:>2} {item}")

    def add_item(self, item, heading):
        self._raw[self.headings[heading]].append(item)

    def remove_item(self, item, heading):
        try:
            print(self.headings[heading], int(item) - 1)
            self._raw[self.headings[heading]].pop(int(item) - 1)
            self.write()
            return True
        except Exception as e:
            logger.error(e)
            return False

    @property
    def headings(self):
        counter = ord("A")
        tmp = {}
        for key in self._raw.keys():
            tmp[chr(counter)] = key
            counter += 1

        return tmp


def arguments():
    parser = ArgumentParser(prog="todo")
    subparsers = parser.add_subparsers(help="help for subcommand", dest="subcommand")

    # create the parser for the "remove" command
    parser_a = subparsers.add_parser("remove")
    parser_a.add_argument("item", type=str)

    # create the parser for the "add" command
    parser_b = subparsers.add_parser("add")
    parser_b.add_argument("item", type=str)

    parser_b.add_argument("--heading", type=str, help="Specify heading")

    return parser.parse_args()


def add():
    if not args.heading:
        heading = "A"
    else:
        heading = args.heading
    todo.add_item(args.item, heading)

    print_list()
    todo.write()


def remove():
    if not len(args.item) > 1:
        print("Invalid item provided, too short")
        return

    heading = args.item[0]
    item = args.item[1:]

    if not heading.isalpha() or not item.isnumeric():
        print("Invalid item provided")
        return

    if not heading in todo.headings.keys():
        print(f"Heading {heading} does not exist")
        return

    if not todo.remove_item(item, heading):
        print("Item does not exist")

    print_list()


def print_list():
    print()
    for heading in todo.headings.keys():
        todo.print(heading)
        print()


def main():
    if args.subcommand == "add":
        add()
    if args.subcommand == "remove":
        remove()
    if args.subcommand is None:
        print_list()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = arguments()
    todo = Todo(file=environ.get("TODO_FILE", "todo.yaml"))
    main()
