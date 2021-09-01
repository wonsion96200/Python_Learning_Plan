# coding=utf-8
import os

import obj_data
import obj_file
import obj_log_split
from func_log_process import LogProcess
from obj_mobatch import OsMobatch
from obj_read_config import Config


def extract_log_files_put_to_csv_files(in_path):
    """
    extract the log files, put the result to csv files
    :return: grep_file_list as type list
    """
    out_path = os.path.join(in_path, "temp")
    os.makedirs(out_path, exist_ok=True)
    log_process = LogProcess()
    log_process.log_path = in_path
    log_process.output_path = out_path
    csv_sw = log_process.cvsw()
    csv_crash = log_process.lggc()

    # copy the csv files to output and report
    obj_file.copy_file(csv_crash, config.report_path)
    if os.path.getsize(csv_crash):
        output_path = os.path.join(config.output_path, "dcgm_crash_" + config.date_time)
        report_path = os.path.join(config.report_path, "crash_" + config.date_time)
        obj_file.copy_file(csv_crash, output_path)
        obj_file.copy_file(csv_crash, report_path)
        if csv_sw:
            obj_file.copy_file(csv_sw, output_path)
            obj_file.copy_file(csv_sw, report_path)
    return csv_crash


def get_dcgm_when_crash_is_observed(csv_crash=""):
    output_path = os.path.join(config.output_path, "dcgm_crash_" + config.date_time)
    if os.path.getsize(csv_crash):
        data = obj_data.read_csv_to_data(csv_crash)
        crash_list = []
        i = 0
        for row in data:
            if i > 0:
                if row[0] not in crash_list:
                    crash_list.append(row[0])
            i = i + 1
        mobatch.site_info = "'%s'" % (",".join(crash_list))
        mobatch.commands = os.path.join("'dcgm -k 1 %s'" % output_path)
        mobatch.log_path = output_path
        mobatch.execute_mobatch()


if __name__ == '__main__':
    config = Config()
    config.output_path = os.path.join(config.output_path, "Crash")
    config.report_path = os.path.join(config.report_path, "Crash")
    os.makedirs(config.output_path, exist_ok=True)
    os.makedirs(config.report_path, exist_ok=True)

    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "crash_check.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "all_sitelist.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_crash_check")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # extract the log files, put the result to csv files
    csv_file = extract_log_files_put_to_csv_files(log_path)

    if csv_file:
        get_dcgm_when_crash_is_observed(csv_file)
