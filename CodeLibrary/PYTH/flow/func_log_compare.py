#!python2
# coding=utf-8
import os

from obj_file_compare import FileCompare


# import re


def file_list_diff(src_file_list="", dst_file_list="", report_path=""):
    compare = FileCompare()
    compare.diff_report_path = report_path
    list_dst = [x.strip() for x in open(dst_file_list).readlines()]
    list_src = [x.strip() for x in open(src_file_list).readlines()]
    for dst_file in list_dst:
        for src_file in list_src:
            if src_file.endswith(os.path.basename(dst_file)):
                compare.src_file = src_file
                compare.dst_file = dst_file
                compare.diff_report_file = os.path.join(compare.diff_report_path, "diff_" + os.path.basename(dst_file))
                # compare active alarm, ignore date,time,AlarmId,NotificationId
                if dst_file.endswith("_alarm.csv"):
                    compare.common_diff(separator=",", skips="2,1,-2,-1")
                # compare history alarm, ignore Status,Duration
                elif dst_file.endswith("_alarm_history.csv"):
                    compare.common_diff(separator=",", skips="5,4")
                # compare invxc_Board, output to csv format
                elif dst_file.endswith("invxc_Board.csv"):
                    compare.common_diff(separator=",", skips="-3,-2")
                # compare sw_version, output to csv format
                elif dst_file.endswith("_sw_version.csv") or dst_file.endswith("invxc_SW.csv"):
                    compare.csv_diff_from_to(0, 1)

                # compare common log file
                else:
                    compare.common_diff()


if __name__ == '__main__':
    # pass
    src = "/home/ejungwa/hcTool/log/output/file_list_src.txt"
    dst = "/home/ejungwa/hcTool/log/output/file_list_dst.txt"
    file_list_diff(src, dst)
