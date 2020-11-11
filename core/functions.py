from os import makedirs
from os.path import isdir, isfile


class Functions():
    def check_directory(self):
        """
        This function allows the creation of the `files` folder in the 
        main folder of the bot. It allows the bot to check if the 
        folder exists, if not create it.
        """

        directory = "files"
        check_directory = isdir(directory)

        # First check if the directory exists. If it doesn't, create it
        if not check_directory:
            makedirs(directory)

        # If `files` exists, continue
        else:
            pass

    def check_file(self, filename):
        """
        This function allows the bot to check if any other files exist 
        with the same name. If there is a file with the same name, 
        rename the new file with a number at the end. i.e If `example` 
        exists in `/files`, rename it to `example-1`. If `example-1` 
        also exists, rename it to `example-2` etc...
        """

        directory = "files"

        # Check if the file exists in `/files`
        if isfile(f"files/{filename}") is True:
            i = 1

            # Check if `file-i` (where `i` is the current value of
            # `i`) exists in `/files`.
            while isfile(f"files/{filename}-{i}"):
                i += 1

            # Based on the previous loops, rename the old file
            filename = f"{filename}-{i}"

            return filename

        else:
            # If there are no duplicates of the file, continue
            return filename
