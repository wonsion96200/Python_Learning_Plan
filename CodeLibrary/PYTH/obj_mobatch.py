# coding=utf-8
import os
from obj_read_config import Config

"""
mobatch sitelist mos_script log_path
"""


class OsMobatch(object):
    def __init__(self):
        config = Config()
        self.site_info = ""
        self.commands = ""
        self.log_path = config.log_path
        self.moshell_path = config.moshell_path

    def execute_mobatch(self):
        """
        run mobatch
        :return: log_path
        """
        os.makedirs(self.log_path, exist_ok=True)
        mobatch_command = "%s/mobatch -p 50 %s %s %s" % (
            self.moshell_path, self.site_info, self.commands, self.log_path)
        print(mobatch_command)
        os.system(mobatch_command)
        return self.log_path


if __name__ == '__main__':
    mobatch = OsMobatch()

    mobatch.execute_mobatch()
