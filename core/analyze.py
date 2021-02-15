from json import loads
from subprocess import STDOUT, check_output


class Analysis():
    def run_file(self, file):
        # Run 'file <file>' command
        return check_output(["file", f"files/{file}"]).decode("utf-8")

    def checksec(self, file):
        # Run 'checksec -j <file>' command
        # stderr=STDOUT is required in order to turn the output into a dictionary, then a list
        output = check_output(["checksec", "-j", f"files/{file}"],
                              stderr=STDOUT,
                              encoding="utf-8"
                              )

        # Load the `json` output as a dictionary
        dict = loads(output)

        # Take out the irrelevant lines from the dictionary
        dict = dict[list(dict.keys())[0]].values()

        # Turn the dictionary into a list
        listified = list(dict)

        return listified
