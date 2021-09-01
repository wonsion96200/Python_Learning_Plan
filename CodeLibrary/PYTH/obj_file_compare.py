#!python2
# coding=utf-8
import re

import obj_data


def ignores(line="", separator=None, skip=None):
    line = line.strip()
    if separator:
        words = re.split(separator, line)
        if skip:
            skips = [eval(x) for x in re.split(",", skip)]
            for i in skips:
                if len(words) > i + 1:
                    del words[i]
        line = separator.join(words)
    return line


class FileCompare(object):
    def __init__(self):

        self.diff_report_path = ""
        self.src_file = ""
        self.dst_file = ""
        self.diff_report_file = ""

    def common_diff(self, separator="", skips=""):
        """
        compare two logfile with the original content
        :return: output_file
        """
        list_dst = open(self.dst_file).readlines()
        list_src = [ignores(x, separator, skips) for x in open(self.src_file).readlines()]
        with open(self.diff_report_file, 'w') as f:
            for line in list_dst:
                if ignores(line, separator, skips) not in list_src:
                    f.write(line)
        print("compare %s and %s, output to %s" % (self.src_file, self.dst_file, self.diff_report_file))
        return self.diff_report_file

    def csv_diff_from_to(self, col_key, col_value):
        list_src = obj_data.read_csv_to_data(self.src_file)
        list_dst = obj_data.read_csv_to_data(self.dst_file)
        data = []
        dict_src = obj_data.make_data_to_dict(list_src, [col_key], [col_value])
        for words in list_dst:
            if words[col_key] in dict_src:
                value_src = dict_src[words[col_key]][0]
            else:
                value_src = ""
            if value_src != words[col_value]:
                data.append([words[col_key], value_src, words[col_value]])
        if data:
            data_head = [[list_src[0][col_key], "from_" + list_src[0][col_value], "to_" + list_dst[0][col_value]]]
            data_head.extend(data)

        else:
            data_head = []
        obj_data.write_data_to_csv(data_head, self.diff_report_file)
        print("compare %s and %s, output to %s" % (self.src_file, self.dst_file, self.diff_report_file))
        return self.diff_report_file


if __name__ == '__main__':
    # pass
    compare = FileCompare()
    # compare.src_file = "/home/ejungwa/hcTool/log/11-13/temp/grep_altc.csv"
    # compare.dst_file = "/home/ejungwa/hcTool/log/13-01/temp/grep_altc.csv"
    # # compare active alarm, ignore date,time,AlarmId,NotificationId
    # compare.common_diff(separator=",", skips="2,1,-2,-1")
    # # compare history alarm, ignore Status,Duration
    # compare.src_file = "/home/ejungwa/hcTool/log/11-13/temp/grep_lgjc.csv"
    # compare.dst_file = "/home/ejungwa/hcTool/log/13-01/temp/grep_lgjc.csv"
    # compare.common_diff(separator=",", skips="5,4")
    # compare sw_version, output to csv format
    compare.src_file = "/home/ejungwa/hcTool/log/20201118232341/temp/pre_invxc_SW.csv"
    compare.dst_file = "/home/ejungwa/hcTool/log/20201122010228/temp/invxc_SW.csv"
    compare.diff_report_file = "/home/ejungwa/hcTool/report/diff_invxc_SW.csv"
    compare.csv_diff_from_to(0, 1)
    # # compare common log file
    # compare.src_file = "/home/ejungwa/hcTool/log/11-13/temp/grep_lggc.csv"
    # compare.dst_file = "/home/ejungwa/hcTool/log/13-01/temp/grep_lggc.csv"
    # compare.common_diff()
