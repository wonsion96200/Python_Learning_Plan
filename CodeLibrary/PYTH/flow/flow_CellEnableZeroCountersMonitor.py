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

    csv_st_file = log_process.st_cell()
    csv_counters_file = log_process.counters_cell()

    data_st = obj_data.read_csv_to_data(csv_st_file)
    data_volume = obj_data.read_csv_to_data(csv_counters_file)

    csv_counters_cell_state = os.path.join(os.path.dirname(csv_counters_file), "csv_counters_cell_state.csv")
    data = obj_data.vlookup(data_volume, data_st, [0, 1], [0, -1], [-2])
    obj_data.write_data_to_csv(data, csv_counters_cell_state)
    return csv_counters_cell_state


def get_zero_counter_and_cell_enable(csv_file="", csv_output="report_cell_enable_zero_counter.csv"):
    head = [["SiteName", "CellName", "CounterName", "CounterValue", "CellState"]]
    counters = obj_data.read_csv_to_data(csv_file)
    data = []
    i = 0
    for line in counters:
        if i > 0:
            # when pmCellDowntimeAuto is not zero
            if eval(line[-2]) > 0 and line[-3] == "pmCellDowntimeAuto":
                data.append(line)

            # when CounterValue is zero and CellState is ENABLED not is pmCellDowntimeAuto
            if eval(line[-2]) == 0 and line[-1] == "(ENABLED)" and (not line[-3] == "pmCellDowntimeAuto"):
                data.append(line)
        i = i + 1
    csv_output_file = os.path.join(os.path.dirname(csv_file), csv_output)
    if data:
        head.extend(data)
        obj_data.write_data_to_csv(head, csv_output_file)
    else:
        obj_data.write_data_to_csv(data, csv_output_file)
    return csv_output_file


if __name__ == '__main__':
    config = Config()
    config.report_path = os.path.join(config.report_path, "HealthCheck")
    os.makedirs(config.report_path, exist_ok=True)
    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "CellEnableZeroCountersMonitor.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "all_sitelist.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_CellEnableZeroCountersMonitor")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return csvfile
    counter_state_file = grep_log_files_put_to_log_output(log_path)

    cell_enable_zero_counter_file = get_zero_counter_and_cell_enable(counter_state_file)

    obj_file.copy_file(cell_enable_zero_counter_file, config.report_path)
