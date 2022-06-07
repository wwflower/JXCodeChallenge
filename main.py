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
    def sort_on_columns(self, sort_order, has_heading):
        # Since the first column number should be the primary sort order
        # it should be handled last. Reverse the list of column numbers
        sort_order.reverse()
        for sort_index in sort_order:
            # Check if input text file has heading row and exclude it from sort if True
            if has_heading:
                self.list_of_rows[1:] = sorted(self.list_of_rows[1:], key=lambda row: row[sort_index - 1])
            else:           
                # sort_index - 1 because an input of 1 needs to indicate the first row which is index 0
                self.list_of_rows.sort(key=lambda row: row[sort_index - 1])
                


def get_runtime_options():
    from argparse import ArgumentParser
    cmd_parser = ArgumentParser(description="""Read and process a file""")
    _opt = cmd_parser.add_argument

    _opt("-f", "--file_name",
         help="Enter the name of a file in the current directory.")

    _opt(
        "-c", "--columns",
        # Changed default from int to string because that's how it would be if the user entered it
        default="1",
        help="Enter the indexes of the columns to sort by. The first column is 1 and is the default. "
             "To enter more than one column, separate the numbers by commas with NO SPACES")

    # Added -hh arg to indicate if the input text file has a heading row
    _opt("-hh", "--has_heading", 
        action="store_true",
        help="Use if the input test file should treat the first row as a heading row.")

    if len(sys.argv) > 1:
        # Remove parentheses from sys.argv because it's a list and not callable
        cmd_options = cmd_parser.parse_args(args=sys.argv[1:]) 
    else:
        cmd_parser.print_help()
        sys.exit(1)

    print(f"Running with the following options {cmd_options}")

    sort_order_options = [int(col) for col in cmd_options.columns.split(",")]

    return cmd_options.file_name, sort_order_options, cmd_options.has_heading


if __name__ == '__main__':
    file_name, sort_order_list, has_heading = get_runtime_options()
    file_handler = FileSorter()
    file_handler.validate_file(file_name)
    file_handler.read_the_file(file_name)
    file_handler.sort_on_columns(sort_order_list, has_heading)
    file_handler.print_result()
