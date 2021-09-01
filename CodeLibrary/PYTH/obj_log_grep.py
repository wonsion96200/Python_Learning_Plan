import os

import obj_file


class Grep(object):

    def __init__(self):
        self.log_prefix = ""
        self.log_path = ""
        self.output_path = ""
        self.grep_i = ""
        self.grep_i2 = ""
        self.grep_i3 = ""
        self.grep_files = ""
        self.grep_v = ""
        self.output_file = ""

    def execute_grep(self, over_write=True):
        """
        execute the linux command grep
        output self.grep_output_file
        :return:
        """
        if self.log_prefix:
            if not self.log_prefix.endswith("_"):
                self.log_prefix = self.log_prefix + "_"

        if self.grep_i:
            if self.grep_i.startswith(r"E "):
                grep_include = " -ai" + self.grep_i
            else:
                grep_include = " -ai " + self.grep_i
        else:
            grep_include = ""

        if self.grep_i2:
            if self.grep_i.startswith(r"E "):
                grep_include2 = "|grep -ai" + self.grep_i2
            else:
                grep_include2 = "|grep -ai " + self.grep_i2
        else:
            grep_include2 = ""

        if self.grep_i3:
            if self.grep_i.startswith(r"E "):
                grep_include3 = "|grep -ai" + self.grep_i3
            else:
                grep_include3 = "|grep -ai " + self.grep_i3
        else:
            grep_include3 = ""

        if self.grep_v:
            if self.grep_v.startswith(r"E "):
                grep_exclude = "|grep -av" + self.grep_v
            else:
                grep_exclude = "|grep -av " + self.grep_v
        else:
            grep_exclude = ""

        if over_write:
            put = ">"
        else:
            put = ">>"

        path_output_file = os.path.join(self.output_path, self.log_prefix + self.output_file)
        system_command = """cd %s; grep %s %s %s %s %s %s %s;""" % (
            self.log_path, grep_include, self.grep_files, grep_include2, grep_include3,
            grep_exclude, put, path_output_file)

        if obj_file.file_number(os.path.join(self.log_path, self.grep_files)):
            print(system_command)
            os.system(system_command)
        return path_output_file


if __name__ == '__main__':
    pass
    grep = Grep()
    grep.log_path = "/home/ejungwa/hcTool/log/15-45"
    grep.output_path = "/home/ejungwa/hcTool/log/output"
    grep.grep_i = "'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9];[0-9][0-9]:[0-9][0-9]:[0-9][0-9];'"
    grep.output_file = "grep_altc.txt"
    grep.grep_files = "*_altc.log"
    grep.grep_v = "'External Link Failure'"
    grep.execute_grep()
