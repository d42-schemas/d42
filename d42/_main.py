import argparse
import os

from d42.migration.migrate_v1_to_v2 import migrate_v1_to_v2


def run() -> None:
    parser = argparse.ArgumentParser("d42")

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    v1_to_v2_parser = subparsers.add_parser("v1-to-v2", help="Migrate schemas from v1 to v2")
    v1_to_v2_parser.add_argument("schema_directory", type=str,
                                 help="Path to the directory containing schema files")

    args = parser.parse_args()
    if args.command == "v1-to-v2":
        if not os.path.isdir(args.schema_directory):
            print(f"Error: The path '{args.schema_directory}' is not a valid directory")
            return

        migrate_v1_to_v2(args.schema_directory)
        print(f"Migration completed for schemas in '{args.schema_directory}'")
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
