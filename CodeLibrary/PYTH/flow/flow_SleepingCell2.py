# coding=utf-8
import os

import obj_data
import obj_file
import obj_log_split
from func_log_process import LogProcess
from obj_mobatch import OsMobatch
from obj_read_config import Config


def grep_log_files_put_to_log_output(path):
    """
    grep the log files, put the result to new file
    :return: grep_file_list as type list
    """
    log_process = LogProcess()
    log_process.log_path = path
    log_process.output_path = os.path.join(path, "temp")
    obj_file.cleanup_dir(log_process.output_path)

    csv_mdt_debug = log_process.mtd_debug()
    return csv_mdt_debug


def judging_and_output_sleeping_file(csv_file="", number=0):
    data = obj_data.read_csv_to_data(csv_file)
    data_head = [["SiteName", "numPktsDropBbmCmFull"]]
    new_data = []
    for row in data:
        if row[1] == "numPktsDropBbmCmFull" and eval(row[2]) > number:
            new_data.append([row[0], row[2]])
    if new_data:
        data_head.extend(new_data)
        csv_sleeping_file = obj_data.write_data_to_csv(data_head,
                                                       os.path.join(os.path.dirname(csv_file),
                                                                    "mdt_sleeping_cell_" + str(number) + ".csv"))
    else:
        csv_sleeping_file = obj_data.write_data_to_csv(new_data,
                                                       os.path.join(os.path.dirname(csv_file),
                                                                    "mdt_sleeping_cell_" + str(number) + ".csv"))
    return csv_sleeping_file


def manual_crash_for_sleeping_cell(sleeping_file="", csv_file=""):
    data = [x[0] for x in obj_data.read_csv_to_data(sleeping_file)]
    site_list = []
    i = 0
    for row in data:
        if i > 0:
            if row not in site_list:
                site_list.append(row)
        i = i + 1

    if site_list:
        output_path = os.path.join(config.output_path, "manual_crash_" + config.date_time)
        obj_file.copy_file(sleeping_file, output_path)
        obj_file.copy_file(csv_file, output_path)

        report_path = os.path.join(config.report_path, "manual_crash_" + config.date_time)
        obj_file.copy_file(sleeping_file, report_path)
        obj_file.copy_file(csv_file, report_path)

        mobatch.site_info = "'%s'" % (",".join(site_list))
        mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "manual_crash_for_sleeping_cell.mos")
        mobatch.log_path = output_path
        mobatch.execute_mobatch()


if __name__ == '__main__':
    config = Config()
    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "SleepingCellMonitor2.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "sitelist_sleeping_cell.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_SleepingCell2")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return mdt debug file
    mdt_debug_file = grep_log_files_put_to_log_output(log_path)

    # output the file sleeping cell
    file_sleeping_cell_0 = judging_and_output_sleeping_file(mdt_debug_file, 0)
    obj_file.copy_file(file_sleeping_cell_0, config.report_path)

    file_sleeping_cell_20 = judging_and_output_sleeping_file(mdt_debug_file, 200000)
    obj_file.copy_file(file_sleeping_cell_20, config.report_path)

    # perform the manual crash for sleeping cell
    manual_crash_for_sleeping_cell(file_sleeping_cell_20, mdt_debug_file)
