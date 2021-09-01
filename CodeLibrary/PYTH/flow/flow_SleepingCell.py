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

    csv_sleeping_cell = log_process.sleeping_cell()
    return csv_sleeping_cell


def get_suspect_and_ensure(site, suspect, ensure, sleeping_file=""):
    if suspect:
        suspect = 1
    else:
        suspect = 0
    if ensure:
        ensure = 1
    else:
        ensure = 0

    if os.path.exists(sleeping_file):
        d_suspect = obj_data.make_data_to_dict(obj_data.read_csv_to_data(sleeping_file), [0], [3])
        d_ensure = obj_data.make_data_to_dict(obj_data.read_csv_to_data(sleeping_file), [0], [4])
        if suspect:
            if site in d_suspect:
                suspect = eval(d_suspect[site][0]) + suspect
        if ensure:
            if site in d_ensure:
                ensure = eval(d_ensure[site][0]) + ensure

        if suspect > 2:
            if site in d_ensure:
                ensure = eval(d_ensure[site][0]) + 1
            else:
                ensure = 1
        if ensure and (not suspect):
            suspect = 1

    return suspect, ensure


def judging_and_output_sleeping_file(csv_file=""):
    sleeping_file = os.path.join(config.output_path, "quick_view.csv")
    ratio_pdcp = ratio_rrc = ratio_ucast = value_pdcp = None
    data = obj_data.read_csv_to_data(csv_file)
    quick_list = []
    for row in data:
        if row[1] == "ifHCInUcastPkts":
            ratio_ucast = float(row[-1])
        elif row[1] == "pmPdcpPktReceivedDl":
            ratio_pdcp = float(row[-1])
            value_pdcp = eval(row[-2])
        elif row[1] == "pmRrcConnLevSum":
            ratio_rrc = float(row[-1])

        if ratio_pdcp is not None and ratio_rrc is not None and ratio_ucast is not None:
            quick_row = [row[0], ratio_pdcp, ratio_rrc, ratio_pdcp < 0.6 and ratio_rrc > 1, value_pdcp < 1]
            quick_list.append(quick_row)
            ratio_pdcp = ratio_rrc = ratio_ucast = value_pdcp = None
    if quick_list:
        this_list = [["Site Name", "ratio_pdcp", "ratio_rrc", "Suspect", "Ensure"]]
        this_list.extend([[x[0], x[1], x[2], get_suspect_and_ensure(x[0], x[3], x[4], sleeping_file)[0],
                           get_suspect_and_ensure(x[0], x[3], x[4], sleeping_file)[1]] for x in quick_list])
        obj_data.write_data_to_csv(this_list, sleeping_file)

    return sleeping_file


def get_log_for_sleeping_cell(sleeping_file="", csv_file=""):
    site_list = []
    suspect_list = []
    ensure_list = []
    if os.path.exists(sleeping_file):
        site_list = obj_data.read_csv_to_data(sleeping_file)
    i = 0
    for row in site_list:
        if i:
            # suspect
            if eval(row[-2]) > 0:
                suspect_list.append(row[0])
            # ensure
            if eval(row[-1]) == 1:
                ensure_list.append(row[0])
        i = i + 1
    if suspect_list:
        output_path = os.path.join(config.output_path, "log_" + config.date_time)
        obj_file.copy_file(sleeping_file, output_path)
        obj_file.copy_file(csv_file, output_path)

        report_path = os.path.join(config.report_path, config.date_time)
        obj_file.copy_file(sleeping_file, report_path)
        obj_file.copy_file(csv_file, report_path)

        mobatch.site_info = "'%s'" % (",".join(suspect_list))
        mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "get_log_for_sleeping_cell.mos")
        mobatch.log_path = output_path
        mobatch.execute_mobatch()

    if ensure_list:
        report_path = os.path.join(config.report_path, "manual_crash_" + config.date_time)
        if os.path.exists(sleeping_file):
            obj_file.copy_file(sleeping_file, report_path)
        if os.path.exists(csv_file):
            obj_file.copy_file(csv_file, report_path)

        mobatch.site_info = "'%s'" % (",".join(ensure_list))
        # mobatch.commands = os.path.join("'dcgm -k 1 %s'" % report_path)
        mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "manual_crash_for_sleeping_cell.mos")
        mobatch.log_path = report_path
        # mobatch.execute_mobatch()


if __name__ == '__main__':
    config = Config()

    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "SleepingCellMonitor.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "sitelist_sleeping_cell.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_SleepingCell")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return csvfile
    kpi_file = grep_log_files_put_to_log_output(log_path)
    obj_file.copy_file(kpi_file, config.report_path)

    # output the kpi file
    file_sleeping_cell = judging_and_output_sleeping_file(kpi_file)
    obj_file.copy_file(file_sleeping_cell, config.report_path)

    # get the log for sleeping cell
    get_log_for_sleeping_cell(file_sleeping_cell, kpi_file)
