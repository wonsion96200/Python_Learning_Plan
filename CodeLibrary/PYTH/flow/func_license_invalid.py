#!python2
# coding=utf-8
import datetime
import os
import re

import obj_file
from obj_read_config import Config

config = Config()


def valid_days(str_time):
    if not str_time:
        days = 365
    else:
        now = datetime.datetime.now()
        valid_time = datetime.datetime.strptime(str_time, '%Y-%m-%d')
        days = (valid_time - now).days + 1
    return days


def license_valid_to_csv(src_file=config.report_path + "/record_license.csv"):
    """
    invalid license
    "DISABLED" in license_state
    "TRUE" in limit_reached
    valid_until less than 30days
    output to file report_license_invalid
    :return: dst_file
    """
    head = ""
    filepath, shot_name, extension = obj_file.get_filepath_filename_fileext(src_file)
    dst_file = os.path.join(filepath, config.log_prefix + "report_license_invalid.csv")
    lines = []
    list_src = open(src_file).readlines()
    i = 0
    for line in list_src:
        if i == 0:
            head = "ValidType," + line
            i = i + 1
        else:
            words = re.split(r",", line)
            license_state = words[5]
            valid_from = words[8]
            valid_until = words[9]
            limit_reached = words[12]
            if valid_from:
                if "disable" in license_state.lower():  # invalid LicenseState
                    lines.append("LicenseState is disable," + line)
                elif "true" in limit_reached.lower():  # invalid limitReached
                    lines.append("limitReached is true," + line)
                elif valid_days(valid_until) < 30:  # invalid ValidUntil
                    lines.append("license less than 30days," + line)
    with open(dst_file, 'w') as dst_csv_file:
        if lines:
            dst_csv_file.write(head)
            # for line in lines:
            dst_csv_file.writelines(lines)
    return dst_file


if __name__ == '__main__':
    # pass
    src = "/home/ejungwa/hcTool3/report.sample/SiteInfo/record_license.csv"
    license_valid_to_csv(src)
