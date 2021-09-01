# coding=utf-8
import os

import obj_file
from obj_read_config import Config


def get_dirlist(root):
    dirlist = []
    for s in os.listdir(root):
        if os.path.isdir(os.path.join(root, s)):
            dirlist.append(s)
    return dirlist


if __name__ == '__main__':
    config = Config()
    log_path = os.path.join(config.tool_path, "log")
    if not os.path.exists(log_path):
        pass
    else:
        dirs = get_dirlist(log_path)
        for d in dirs:
            if obj_file.file_created_days(os.path.join(log_path, d)) > 0:
                os.system("cd %s;zip -rm %s.zip %s" % (log_path, d, d))
