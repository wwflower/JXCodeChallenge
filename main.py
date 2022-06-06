"""
Core requirements:
-	The program must read a text file and sort the results.
-	The user must be able to provide the name of the file to read in the current directory
-	The user must be able to specify which columns to sort on using 1 to indicate the first, 2 to indicate the second and so on.
-	The order of the sorting is determined by the order in which the columns are listed.
-	The program should print the sorted results
Assumptions:
-	The input file is expected to have comma delimited values which may all be treated as string.
-	Every row should have the same number of entries.

"""
import sys
from code_test_pack.file_handler import FileHandler


class FileSorter(FileHandler):
    def sort_on_columns(self, sort_order):
        # Since the first column number should be the primary sort order
        # it should be handled last. Reverse the list of column numbers
        sort_order.reverse()
        for sort_index in sort_order:
            self.list_of_rows.sort(key=lambda row: row[sort_index])


def get_runtime_options():
    from argparse import ArgumentParser
    cmd_parser = ArgumentParser(description="""Read and process a file""")
    _opt = cmd_parser.add_argument

    _opt("-f", "--file_name",
         help="Enter the name of a file in the current directory.")

    _opt(
        "-c", "--columns",
        default=1,
        help="Enter the indexes of the columns to sort by. The first column is 1 and is the default. "
             "To enter more than one column, separate the numbers by commas with NO SPACES")

    if len(sys.argv) > 1:
        cmd_options = cmd_parser.parse_args(args=sys.argv()[1:])
    else:
        cmd_parser.print_help()
        sys.exit(1)

    print(f"Running with the following options {cmd_options}")

    sort_order_options = [int(col) for col in cmd_options.columns.split(",")]

    return cmd_options.file_name, sort_order_options


if __name__ == '__main__':
    file_name, sort_order_list = get_runtime_options()
    file_handler = FileSorter()
    file_handler.validate_file(file_name)
    file_handler.read_the_file(file_name)
    file_handler.sort_on_columns(sort_order_list)
    file_handler.print_result()
