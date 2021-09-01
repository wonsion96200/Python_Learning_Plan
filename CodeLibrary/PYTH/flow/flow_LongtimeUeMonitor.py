# coding=utf-8
import os
import re

import obj_data
import obj_file
import obj_log_split
from obj_log_grep import Grep
from obj_mobatch import OsMobatch
from obj_read_config import Config


def get_words_from_line(line, s_char1="_(.*?).log:", s_char2="|;"):
    words = []
    if s_char1:
        s = re.search(s_char1, line.strip())
        if s:
            words = [x.strip() for x in re.split(s.group(0) + s_char2, line.strip())]
    else:
        words = [x.strip() for x in re.split(s_char2, line.strip())]
    return words


def output_data(text_head, data, input_file):
    data_head = [re.split(";", text_head)]
    filepath, shot_name, extension = obj_file.get_filepath_filename_fileext(input_file)
    output_file = os.path.join(filepath, shot_name + ".csv")
    if data:
        data_head.extend(data)
        obj_data.write_data_to_csv(data_head, output_file)
    else:
        obj_data.write_data_to_csv(data, output_file)
    print("extract %s to csv %s" % (input_file, output_file))
    return output_file


def grep_log_files_put_to_csv_output(path):
    """
    grep the log files, put the result to new file
    :return: grep_file_list as type list
    """
    grep = Grep()
    grep.output_path = os.path.join(path, "temp")
    obj_file.cleanup_dir(grep.output_path)
    grep.log_path = path
    grep.grep_files = "*_lhsh000100*.log"
    grep.grep_v = ""
    grep.output_file = "record_ue_list.txt"
    grep.grep_i = "'time:'"
    grep_file = grep.execute_grep()

    data = []
    text_head = "SiteName;Type;ueId;ueTraceId;time"
    csv_file = None
    if os.path.exists(grep_file):
        with open(grep_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "", "_lhsh000100|rcUeId:|rpcUeId:|ueTraceId:|traceFlag:|time:")
                if "rpcUeId:" in line:
                    data.append([words[0], "rpc", words[2], words[3], words[-1]])
                elif "rcUeId:" in line:
                    data.append([words[0], "rc", words[2], words[3], words[-1]])

        csv_file = output_data(text_head, data, grep_file)
    return csv_file, grep_file


def judging_and_output(csv_file="", number=0):
    # get ueTraceId for already take action
    file_path_ue_trace_id = os.path.join(config.output_path, "ueTraceId" + str(number) + ".log")
    if not os.path.exists(file_path_ue_trace_id):
        ue_trace = [["ueTraceId", "datetime"]]
    else:
        ue_trace = obj_data.read_csv_to_data(file_path_ue_trace_id)

    ue_trace_ids = [x[0] for x in ue_trace]

    data = obj_data.read_csv_to_data(csv_file)
    data_rpc = []
    data_rc = []
    for row in data:
        if "rpc" in row[1]:
            data_rpc.append(row)
        elif "rc" in row[1]:
            data_rc.append(row[3])
    new_data = []
    for row in data_rpc:
        if row[3] not in data_rc and (eval(row[-1]) > number) and (not row[3] in ue_trace_ids):
            ue_trace_ids.append(row[3])
            ue_trace.append([row[3], config.date_time])
            new_data.append(row)

    data_head = [["SiteName", "Type", "ueId", "ueTraceId", "time"]]
    file_path = os.path.join(os.path.dirname(csv_file), "ue_list_" + str(number) + ".csv")
    if new_data:
        # write ueTraceId to file
        obj_data.write_data_to_csv(ue_trace, file_path_ue_trace_id)
        # put data to file
        data_head.extend(new_data)
        obj_data.write_data_to_csv(data_head, file_path)
    else:
        # put none to file
        obj_data.write_data_to_csv([], file_path)
    return file_path


def log_collection(file_ue_list="", csv_file="", log_file="", number=0):
    # get the site list for the action
    site_list = []
    ue_show = ""
    if os.path.exists(file_ue_list):
        data = obj_data.read_csv_to_data(file_ue_list)
        count = 0
        for row in data:
            if count > 0:
                ue_show = "%srpc/nrat/ue show %s --history --procedure;" % (ue_show, row[2])
                if row[0] not in site_list:
                    site_list.append(row[0])

            count = count + 1

    if site_list:
        # put files to output path
        file_name = "ue_l   ist_" + str(number) + "_" + config.date_time
        output_path = os.path.join(config.output_path, file_name)
        obj_file.copy_file(file_ue_list, output_path)
        obj_file.copy_file(csv_file, output_path)
        obj_file.copy_file(log_file, output_path)

        # put files to report path
        report_path = os.path.join(config.report_path, file_name)
        obj_file.copy_file(file_ue_list, report_path)

        # take action
        mobatch.site_info = "'%s'" % (",".join(site_list))
        mobatch.commands = "'lt all;%s;ter;dcgm -k 1 %s'" % (ue_show, output_path)
        mobatch.log_path = output_path
        mobatch.execute_mobatch()


if __name__ == '__main__':
    config = Config()
    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "rpcHangingUEMonitor.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "sitelist_c1cd.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_LongtimeUeMonitor")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return output file
    csv_output_file, log_output_file = grep_log_files_put_to_csv_output(log_path)

    # output the file
    file_ue_list_900 = judging_and_output(csv_output_file, 900)
    obj_file.copy_file(file_ue_list_900, config.report_path)

    # perform the 2nd mobatch to collect log
    log_collection(file_ue_list_900, csv_output_file, log_output_file, 900)

    # output the file
    file_ue_list_3600 = judging_and_output(csv_output_file, 3600)
    obj_file.copy_file(file_ue_list_3600, config.report_path)

    # perform the 2nd mobatch to collect log
    log_collection(file_ue_list_3600, csv_output_file, log_output_file, 3600)
