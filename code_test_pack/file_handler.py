import os
import sys


class FileHandler(object):
    """
    The FileHandler provides a base class for the FileSorter and
    may also be used by other programs. Anything you do here might impact
    other subclasses. Tread carefully.
    """
    def __init__(self):
        super(FileHandler, self).__init__()
        self.file_path = None
        self.validated_file_name = None
        self.list_of_rows = []

    def validate_file(self, file_name):
        # Use the specified .conf if any, otherwise use mkpy.conf
        if self.validated_file_name == file_name and self.file_path is not None:
            return self.file_path

        file_path = None
        currentDir = os.getcwd()
        full_file_path = os.path.join(currentDir, file_name)
        if os.path.isfile(full_file_path):
            file_path = full_file_path
        if file_path:
            print(f"Using input file: {full_file_path}")
        else:
            print(f"No such file in current directory: {full_file_path}")
            sys.exit(2)
        self.file_path = full_file_path
        self.validated_file_name = file_name
        return full_file_path

    def read_the_file(self, file_name):
        file_path = self.validate_file(file_name)

        # Check the length of all rows and select the max as the "correct" length
        # You could also take first line as the "correct" length but there is a risk of it being the wrong length
        with open(file_path) as file: 
            max_length = len(file.readline().split(","))        
            for line in file:
                row_entries = line.strip().split(',')
                if len(row_entries) > max_length:
                    max_length = len(row_entries)

        with open(file_path) as file:
            for line in file:
                row = line.strip()
                new_row = []
                # self.list_of_rows.append(row.split(","))
                # ERROR introduce None into sort order
                for item in row.split(","):
                    if item:
                        new_row.append(item)
                    else:
                        # Instead of appending None we append whitespace so it can be sorted as a string and will sort to the top if that column is sorted
                        new_row.append(" ")

                # If there are less entries in a row than the max_length add a whitespace entry for each missing entry
                if len(row.split(",")) < max_length: 
                    for i in range(max_length - len(row.split(","))):
                        new_row.append(" ")

                self.list_of_rows.append(new_row)

    def print_result(self):
        message = f"Results from {self.file_path}"
        print(message)
        print("_" * len(message))
        row_number = 1
        for row in self.list_of_rows:
            print(f"{row_number}:  {', '.join(row)}")
            row_number += 1

        print("_" * len(message))
        print("COMPLETE")


