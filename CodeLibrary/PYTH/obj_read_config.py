#!python2
# coding=utf-8
import datetime
import os
import sys


class Config(object):
    def __init__(self):
        self.tool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(r"%s/config/config.json" % self.tool_path, "r") as f:
            self.config = eval(f.read())
            self.moshell_path = self.config.get("moshell_path")

        self.config_path = os.path.join(self.tool_path, "config")

        self.output_path = os.path.join(self.tool_path, "output")
        self.report_path = os.path.join(self.tool_path, "report")

        self.date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.log_path = os.path.join(self.tool_path, "log/" + self.date_time)

        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.report_path, exist_ok=True)

        if len(sys.argv) == 1:
            self.log_prefix = ""
        else:
            self.log_prefix = sys.argv[1]
            if self.log_prefix.endswith("_"):
                pass
            else:
                self.log_prefix = self.log_prefix + "_"


if __name__ == '__main__':
    pass
