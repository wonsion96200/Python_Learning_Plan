#!python3
# coding=utf-8
import os

import obj_file
import obj_log_split
from func_log_process import LogProcess
from obj_file_compare import FileCompare
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
    csv_invxc_files = log_process.invxc()
    csv_board = csv_invxc_files[1]
    return csv_board


def board_where_are_you_going(csv_board):
    compare = FileCompare()
    compare.diff_report_path = config.report_path
    compare.src_file = os.path.join(config.config_path, os.path.split(csv_board)[1])
    compare.dst_file = csv_board
    compare.diff_report_file = os.path.join(compare.diff_report_path, "where_" + os.path.basename(csv_board))
    if os.path.exists(compare.src_file):
        compare.csv_diff_from_to(11, 0)
        obj_file.copy_file(csv_board, config.report_path)
    else:
        obj_file.copy_file(csv_board, config.config_path)


if __name__ == '__main__':
    config = Config()
    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "invxc.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "all_sitelist.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_Board_Wherereyougoing")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return output_file_list
    file_board = grep_log_files_put_to_csv_output(log_path)

    board_where_are_you_going(file_board)
