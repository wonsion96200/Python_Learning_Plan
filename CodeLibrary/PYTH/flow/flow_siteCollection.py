#!python2
# coding=utf-8
import os
import sys

import func_license_invalid
import func_log_compare
import obj_file
import obj_log_split
from func_log_process import LogProcess
from obj_mobatch import OsMobatch
from obj_read_config import Config


def grep_log_files_put_to_csv_output(path):
    """
    grep the log files, put the result to new file
    :return: grep_file_list as type list
    """
    log_process = LogProcess()
    log_process.log_path = path
    log_process.output_path = os.path.join(path, "temp")
    obj_file.cleanup_dir(log_process.output_path)
    csv_alarm, no_contact = log_process.altc()
    csv_alarm_history = log_process.lgjc()
    csv_audit = log_process.lgoc()
    csv_crash = log_process.lggc()
    csv_scg = log_process.scg()
    csv_st_disable = log_process.st_disable()
    csv_st_cell = log_process.st_cell()
    csv_st_cn = log_process.st_term_point_to_cn()
    csv_st_x2 = log_process.st_term_point_to_x2()
    csv_up_record = log_process.lguc()
    csv_license = log_process.invlrc()
    license_invalid = func_license_invalid.license_valid_to_csv(csv_license)
    csv_pci = log_process.hgetc_pci()
    csv_active_plmn = log_process.hgetc_active_plmn_list()
    csv_endc_plmn = log_process.hgetc_endc_allowed_plmn_list()
    csv_plmn_list = log_process.hgetc_plmn_id_list()
    csv_invxc_files = log_process.invxc()
    csv_sw = csv_invxc_files[0]
    csv_board = csv_invxc_files[1]
    # create a list to save log_grep_file
    grep_file_list = [csv_alarm, csv_alarm_history, csv_audit,
                      csv_crash, csv_scg, csv_sw, csv_board,
                      csv_st_cell, csv_st_cn, csv_st_x2, csv_st_disable,
                      csv_license, license_invalid, csv_up_record, csv_pci,
                      csv_active_plmn, csv_endc_plmn, csv_plmn_list]

    output_path = os.path.join(config.output_path, config.date_time)
    obj_file.mkdir(output_path)
    out_file_list = []
    for each_file in grep_file_list:
        obj_file.copy_file(each_file, output_path)
        out_file_list.append(os.path.join(output_path, os.path.split(each_file)[1]))
    return out_file_list


def put_output_file_list_as_new_file_to_log_output(lines, file_name):
    with open(file_name, "w") as new_file:
        for line in lines:
            new_file.write(line + "\n")
    return new_file


if __name__ == '__main__':
    config = Config()
    config.report_path = os.path.join(config.report_path, "SiteInfo")
    config.output_path = os.path.join(config.output_path, "SiteInfo")
    config.src_file_list = os.path.join(config.output_path, "file_list_src.txt")
    config.dst_file_list = os.path.join(config.output_path, "file_list_dst.txt")

    os.makedirs(config.output_path, exist_ok=True)
    obj_file.cleanup_dir(config.report_path)

    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "siteinfo.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "all_sitelist.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_siteCollection")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return output_file_list
    output_file_list = grep_log_files_put_to_csv_output(log_path)

    if len(sys.argv) == 1:
        file_name_of_list = config.dst_file_list
    else:
        file_name_of_list = config.src_file_list

    put_output_file_list_as_new_file_to_log_output(output_file_list, file_name_of_list)

    # compare difference
    if file_name_of_list.endswith(config.src_file_list):
        diff_flag = False
    else:
        if not os.path.isfile(config.src_file_list):
            diff_flag = False
        elif obj_file.file_created_days(config.src_file_list) > 0:
            diff_flag = False
        else:
            diff_flag = True

    if not diff_flag:
        obj_file.copy_file_list(file_name_of_list, config.report_path)
    else:
        func_log_compare.file_list_diff(config.src_file_list, config.dst_file_list, config.report_path)
        obj_file.copy_file_list(config.dst_file_list, config.report_path + "/dst")
        obj_file.copy_file_list(config.src_file_list, config.report_path + "/src")
