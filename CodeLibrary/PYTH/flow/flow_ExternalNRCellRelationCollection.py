# coding=utf-8
import os

import obj_data
import obj_file
import obj_log_split
from func_log_process import LogProcess
from obj_mobatch import OsMobatch
from obj_read_config import Config


def grep_log_files_put_to_csv(path):
    """
    grep the log files, put the result to new file
    :return: grep_file_list as type list
    """
    log_process = LogProcess()
    log_process.log_path = path
    log_process.output_path = os.path.join(path, "temp")
    obj_file.cleanup_dir(log_process.output_path)

    csv_nrcellrelation = log_process.nr_cell_relation()
    csv_externalnrcellcu = log_process.external_nr_cell_cu()
    csv_externalgnbcucpfunction = log_process.external_gnb_cucp_function()
    csv_nrfreqrelation = log_process.nr_freq_relation()
    csv_nrfrequency = log_process.nr_frequency()
    csv_gnbcucpfunction = log_process.gnb_cucp_function()

    data_nrcellrelation = obj_data.read_csv_to_data(csv_nrcellrelation)
    data_externalnrcellcu = obj_data.read_csv_to_data(csv_externalnrcellcu)
    data_externalgnbcucpfunction = obj_data.read_csv_to_data(csv_externalgnbcucpfunction)
    data_nrfreqrelation = obj_data.read_csv_to_data(csv_nrfreqrelation)
    data_nrfrequency = obj_data.read_csv_to_data(csv_nrfrequency)
    data_gnbcucpfunction = obj_data.read_csv_to_data(csv_gnbcucpfunction)

    data_nrfreqrelation = obj_data.vlookup(data_nrfreqrelation, data_nrfrequency, [0, 2], [0, 1],
                                           [-5, -4, -3, -2, -1])
    data_externalnrcellcu = obj_data.vlookup(data_externalnrcellcu, data_nrfrequency, [0, 6], [0, 1],
                                             [-5, -4, -3, -2, -1])
    data_externalnrcellcu = obj_data.vlookup(data_externalnrcellcu, data_externalgnbcucpfunction, [0, 1], [0, 1],
                                             [-3, -2, -1])
    data_nrcellrelation = obj_data.vlookup(data_nrcellrelation, data_gnbcucpfunction, [0], [0],
                                           [-3, -2, -1])
    data_nrcellrelation = obj_data.vlookup(data_nrcellrelation, data_nrfreqrelation, [0, 3], [0, 1],
                                           [-6, -5, -4, -3, -2, -1])
    data_nrcellrelation = obj_data.vlookup(data_nrcellrelation, data_externalnrcellcu, [0, 2], [0, 3],
                                           [1, 2, 4, 5, 6, 7, 8, -8, -7, -6, -5, -4, -3, -2, -1])

    obj_data.write_data_to_csv(data_nrcellrelation, csv_nrcellrelation + ".csv")

    data = data_nrcellrelation

    head = [["Serving_SiteId", "Serving_gNodeBID", "Serving_CellName", "Serving_Cell_Mode", "Neighbor_SiteId",
             "Neighbor_gNodeBID", "Neighbor_CellName", "Neighbor_Cell_Mode", "Neighbor_arfcn",
             "Neighbor_gNodeBIdLength", "Neighbor_Cellid", "Neighbor_PCI", "Neighbor_TAC", "Neighbor_PLMN",
             "smtcDuration", "smtcOffset", "smtcPeriodicity", "smtcScs", "Neighbor_gNodeB_IP"]]
    new_data = []
    i = 0
    for words in data:
        serving_siteid = words[0]
        serving_gnodebid = words[-23]
        serving_cellname = words[1]
        serving_cell_mode = ""
        neighbor_siteid = words[-15]
        neighbor_gnodebid = words[-3]
        neighbor_cellname = words[-14]
        neighbor_cell_mode = ""
        neighbor_arfcn = words[-8]
        neighbor_gnodebidlength = words[-2]
        neighbor_cellid = words[-13]
        neighbor_pci = words[-10]
        neighbor_tac = words[-9]
        neighbor_plmn = words[-1]
        smtcduration = words[-7]
        smtcoffset = words[-6]
        smtcperiodicity = words[-5]
        smtcscs = words[-4]
        neighbor_gnodeb_ip = ""
        row = [serving_siteid, serving_gnodebid, serving_cellname, serving_cell_mode, neighbor_siteid,
               neighbor_gnodebid,
               neighbor_cellname, neighbor_cell_mode, neighbor_arfcn, neighbor_gnodebidlength, neighbor_cellid,
               neighbor_pci, neighbor_tac, neighbor_plmn, smtcduration, smtcoffset, smtcperiodicity, smtcscs,
               neighbor_gnodeb_ip]
        if i > 0:
            new_data.append(row)
        i = i + 1
    if new_data:
        head.extend(new_data)
    csv_file = os.path.join(config.report_path, "Inter_5G_Neighbor.csv")
    obj_data.write_data_to_csv(head, csv_file)


if __name__ == '__main__':
    config = Config()
    # run mobatch
    mobatch = OsMobatch()
    mobatch.commands = os.path.join(os.path.join(config.tool_path, "MOS"), "ExternalNRCellRelationCollection.mos")
    mobatch.site_info = os.path.join(os.path.join(config.tool_path, "config"), "all_sitelist.txt")
    log_path = mobatch.execute_mobatch()
    # log_path = os.path.join(os.path.join(config.tool_path, "log.sample"), "flow_ExternalNRCellRelationCollection")

    # split the logs
    log_path = obj_log_split.log_split(log_path)

    # grep the log, return csvfile
    grep_log_files_put_to_csv(log_path)
