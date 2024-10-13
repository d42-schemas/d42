import argparse
import os

from d42.migration.migrate_v1_to_v2 import migrate_v1_to_v2


def run() -> None:
    parser = argparse.ArgumentParser("d42", description="Migrate schemas from v1 to v2")
    parser.add_argument("schema_directory", type=str,
                        help="Path to the directory containing schema files")

    args = parser.parse_args()
    if not os.path.isdir(args.schema_directory):
        print(f"Error: The path '{args.schema_directory}' is not a valid directory")
        return

    migrate_v1_to_v2(args.schema_directory)
    print(f"Migration completed for schemas in '{args.schema_directory}'")


if __name__ == "__main__":
    run()
