#!python2
# coding=utf-8
import os
import re
import shutil


def log_split(log_path=None):
    # get all log files
    # split path
    split_path = os.path.join(log_path, "split")
    os.makedirs(split_path, exist_ok=True)
    # cp mobatch_result.txt to split path
    file_mobatch_result = os.path.join(log_path, "mobatch_result.txt")
    if os.path.exists(file_mobatch_result):
        shutil.copy(file_mobatch_result, split_path)
    # split_path = log_path
    for root_dir, dirs, files in os.walk(log_path):
        for file_name in files:
            # get the log file name
            # site_name = file.split(".")[0]
            site_name = file_name[:-4]
            with open("%s/%s" % (root_dir, file_name), "r") as f:
                # read log file
                log_file = f.read()
                # split the log file as per "\w+> |\d+.\d+.\d+.\d+> "
                log_lists = re.split(r"\w+> |\d+.\d+.\d+.\d+> ", log_file)
                i = 0
                for command_info in log_lists:
                    # skip the 0
                    if i == 0:
                        pass
                    else:
                        # get the command
                        command = re.sub(r"[^a-zA-Z0-9]", "", command_info.splitlines()[0]).lower()
                        # write to new log file
                        fileurl = os.path.join(split_path, "%s_%s.log" % (site_name, command))
                        with open(fileurl, "w") as new_log_file:
                            new_log_file.write(command_info)
                    i = i + 1
    # return the log file split path
    return split_path


if __name__ == '__main__':
    log_split("/home/ejungwa/hcTool3/log.sample/flow_CellEnableZeroCountersMonitor")
