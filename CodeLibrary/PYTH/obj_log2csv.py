#!python2
# coding:utf8

import os
import re

import obj_data
import obj_file
from obj_read_config import Config

config = Config()


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


def nr_cell_relation2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;NRCellCU;nRCellRef;nRFreqRelationRef"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetcnrcellrelation(.*?).log", "|:NRCellCU=|,NRCellRelation=|;")
                data.append([words[0], words[2], words[-2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def external_nr_cell_cu2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;ExternalGNBCUCPFunction;ExternalNRCellCU;nRCellRef;cellLocalId;plmnIdList;nRFrequencyRef" \
                ";nRPCI;nRTAC "
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            temp_nr_cell_ref = ""
            for line in f:
                if line:
                    words = get_words_from_line(line, "_hgetcexternalnrcell(.*?).log:", "|;")
                    site_name = words[0]
                    nr_cell_ref = words[1]
                    temp_words = get_words_from_line(nr_cell_ref, "=", "|,")
                    external_gnb_cucp_function = temp_words[-3]
                    external_nr_cell_cu = temp_words[-1]

                    # nr_cell_ref
                    if temp_nr_cell_ref == nr_cell_ref:
                        is_last_row = True
                    else:
                        is_last_row = False
                        temp_nr_cell_ref = nr_cell_ref

                    if not is_last_row:
                        cell_local_id = words[-6]
                        nr_frequency_ref = words[-3]
                        nr_pci = words[-2]
                        nr_tac = words[-1]
                    else:
                        plmn_id_list = words[-5] + words[-4]
                        data.append(
                            [site_name, external_gnb_cucp_function, external_nr_cell_cu, nr_cell_ref, cell_local_id,
                             plmn_id_list, nr_frequency_ref, nr_pci, nr_tac])
            output_file = output_data(text_head, data, input_file)
            return output_file


def external_gnb_cucp_function2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;ExternalGNBCUCPFunction;gNBId;gNBIdLength;pLMNId"
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetcexternalgnbcucpfunction(.*?).log:",
                                            "|ExternalGNBCUCPFunction=|;")
                data.append([words[0], words[-5], words[-4], words[-3], words[-2] + words[-1]])

            output_file = output_data(text_head, data, input_file)
            return output_file


def nr_freq_relation2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;NRFreqRelation;NRFrequencyRef"
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetcnrfreqrelation(.*?).log:", "|;")
                data.append([words[0], words[-2], words[-1]])

            output_file = output_data(text_head, data, input_file)
            return output_file


def nr_frequency2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;NRFrequency;arfcnValueNRDl;smtcDuration;smtcOffset;smtcPeriodicity;smtcScs"
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetcnrfrequency(.*?).log:", "|;")
                data.append([words[0], words[1], words[2], words[3], words[4], words[5], words[6]])

            output_file = output_data(text_head, data, input_file)
            return output_file


def gnb_cucp_function(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;GNBCUCPFunction;gNBId;gNBIdLength"
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetcgnbcucpfunction(.*?).log", "|:GNBCUCPFunction=|;")
                if len(words) > 3:
                    data.append([words[0], words[-3], words[-2], words[-1]])

            output_file = output_data(text_head, data, input_file)
            return output_file


def pmxocsv2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;CellName;CounterName;CounterValue"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_pmxocsv(.*?).log:", "|=|;")
                total = 0
                if len(words) > 4:
                    for j in range(4, len(words) - 1):
                        total = total + eval(words[j])
                data.append([words[0], words[2], words[3], total])
        output_file = output_data(text_head, data, input_file)
    return output_file


def mtd_debug2csv(input_file=""):
    """
    extract mtd_debug.txt to mtd_debug.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;dbgCounters;Value"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "", "_mtddebug|::|=")
                data.append([words[0], words[-2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def sleeping_cell2csv(input_file=""):
    """
    extract txt to csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Counter;PreviousRop;LastRop;Ratio"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "=", "|;")
                if eval(words[-3]) == 0:
                    data.append([words[-5], words[-4], words[-3], words[-2], words[-2]])
                else:
                    data.append(
                        [words[-5], words[-4], words[-3], words[-2], round(float(words[-2]) / float(words[-3]), 2)])
        output_file = output_data(text_head, data, input_file)
    return output_file


def altc2csv(input_file=""):
    """
    extract grep_altc.txt to grep_altc.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Date;Time;Severity;Object;Problem;Cause;AdditionalText;AckState;AlarmId;NotificationId"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_altc(.*?).log:", "|;")
                data.append(words)
        output_file = output_data(text_head, data, input_file)
    return output_file


def nocontact2csvaltc(src_file=os.path.join(config.output_path, "grep_no_contact.txt"),
                      dst_file=os.path.join(config.output_path, "grep_altc.csv")):
    """
    extract report_no_contact.txt to dst_file
    :return: dst_file
    """
    data = []
    input_file = src_file
    output_file = dst_file
    if os.path.exists(output_file) and os.path.exists(input_file):
        if os.path.getsize(input_file):
            with open(input_file, 'r') as f:
                for line in f:
                    words = get_words_from_line(line, "", r"\s\s+")
                    data.append([words[-1], "-", "-", "-", "-", "Heartbeat Failure", "-", "-", "-", "-", "-"])
                if data:
                    obj_data.append_data_to_csv(data, output_file)
                    print("extract %s to csv %s" % (input_file, output_file))
    return output_file


def lggc2csv(input_file=""):
    """
    extract grep_lggc.txt to grep_lggc.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Date;Time;Board;No;Reason;Program;Rank;Signal;PMD;Extra"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_lggc(.*?).log:", "|;")
                node = words[0]
                date = words[1]
                time = words[2]
                if (";DU" in line) or ";BB" in line:
                    board = words[5].strip()
                else:
                    board = words[4].strip()
                t_words = re.split(r"\.", words[-1])
                no = reason = program = rank = signal = pmd = extra = "-"
                for word in t_words:
                    if " No:" in word:
                        no = word.replace(" No:", "").strip()
                    elif " Reason:" in word:
                        reason = word.replace(" Reason:", "").strip()
                    elif " Program:" in word:
                        program = word.replace(" Program:", "").strip()
                    elif " Rank:" in word:
                        rank = word.replace(" Rank:", "").strip()
                    elif " Signal:" in word:
                        signal = word.replace(" Signal:", "").strip()
                    elif " PMD:" in word:
                        pmd = word.replace(" PMD:", "").strip()
                    elif " Extra:" in word:
                        extra = word.replace(" Extra:", "").strip()
                    if word == t_words[-1]:
                        data.append([node, date, time, board, no, reason, program, rank, signal, pmd, extra])
        output_file = output_data(text_head, data, input_file)
    return output_file


def lgjc2csv(input_file=""):
    """
    extract grep_lgjc.txt to grep_lgjc.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Date;Time;Severity;Status;Duration;Object;Problem;Cause;AdditionalText;AckState;AlarmId"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_lgjc(.*?).log:", "|;")
                data.append(words)
        output_file = output_data(text_head, data, input_file)
    return output_file


def lgoc2csv(input_file=""):
    """
    extract grep_lgoc.txt to grep_lgoc.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Date;Time;User;Action;MO;Attributes;Value"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_lgoc(.*?).log:", "|;")
                x = re.split(r" ", words[-1])
                list1 = [words[0], words[1], words[2]]
                for i in x:
                    list1.append(i)
                data.append(list1)
        output_file = output_data(text_head, data, input_file)
    return output_file


def lguc2csv(input_file=""):
    """
    extract grep_lguc.txt to grep_lguc.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Date;Time;UP"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_lguc(.*?).log:", r"|;|\s+|=")
                data.append([words[0], words[1], words[2], words[8]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def interference_pwr2csv(input_file=""):
    """
    extract grep_pmxet_RadioRecInterferencePwr.txt to grep_pmxet_RadioRecInterferencePwr.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Cell;RadioRecInterferencePwr"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_pmx(.*?).log:", r"|=|\s+")
                data.append([words[0], words[2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def invlrc2csv(input_file=""):
    """
    extract grep_invlrc.txt to grep_invlrc.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;LicenseType;LicenseName;SiteNameLicenseKey;FAJ;LicenseState;FeatureState;ServiceState" \
                ";ValidFrom;ValidUntil;currLimit;grantedLevel;limitReached;Description "
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_invlrc(.*?).log:", "|;")
                node_name = words[0]
                license_name = words[1]
                license_key = node_name + words[2]
                faj = words[3]
                license_state = words[4]
                if len(words) == 10:
                    license_type = "Feature"
                    feature_state = words[5]
                    service_state = words[6]
                    valid_from = words[7]
                    valid_until = words[8]
                    description = words[9]
                    curr_limit = "-"
                    granted_level = "-"
                    limit_reached = "-"
                elif len(words) == 11:
                    license_type = "Capacity"
                    valid_from = words[5]
                    valid_until = words[6]
                    curr_limit = words[7]
                    granted_level = words[8]
                    limit_reached = words[9]
                    description = words[10]
                    feature_state = "-"
                    service_state = "-"
                data.append(
                    [node_name, license_type, license_name, license_key, faj, license_state, feature_state,
                     service_state, valid_from, valid_until, curr_limit, granted_level, limit_reached,
                     description])
        output_file = output_data(text_head, data, input_file)
    return output_file


def st2csv(input_file=""):
    """
    extract grep_st.txt to grep_st.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Adm_State;Op_State;MO"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_st(.*?).log:", r"|\s+")
                if len(words) == 8:
                    data.append([words[0], words[4], words[-2], words[-1]])
                else:
                    data.append([words[0], "-", words[-2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def cvsw2csv(input_file=""):
    """
    extract grep_sw_version.txt to grep_sw_version.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;SW"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_cv(.*?).log:", r"|:\s")
                data.append([words[0], words[2]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def up2csv(input_file=""):
    """
    extract grep_UpgradePackage.txt to grep_UpgradePackage.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;UpgradePackage"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_lpr(.*?).log:", "|=")
                data.append([words[0], words[4]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def pci2csv(input_file=""):
    """
    extract grep_UpgradePackage.txt to grep_UpgradePackage.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Cell;pci;"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetc(.*?).log:", "|=|;")
                if words[-1] and (len(words) > 3):
                    data.append([words[0], words[2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def plmnidlist2csv(input_file=""):
    """
    extract grep_UpgradePackage.txt to grep_UpgradePackage.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Cell;mcc;mnc;"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetc(.*?).log:", "|=|;")
                if words[-1] and (len(words) > 4):
                    data.append([words[0], words[-3], words[-2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def plmnlist2csv(input_file=""):
    """
    extract grep_UpgradePackage.txt to grep_UpgradePackage.csv
    :param input_file: str
    :return: output_file:str
    """
    data = []
    text_head = "SiteName;Cell;mcc;mnc;mncLength"
    output_file = None
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            for line in f:
                words = get_words_from_line(line, "_hgetc(.*?).log:", "|=|;")
                if words[-1] and (len(words) > 5):
                    data.append([words[0], words[-4], words[-3], words[-2], words[-1]])
        output_file = output_data(text_head, data, input_file)
    return output_file


def get_data_invxc(node="Node", line=""):
    text_data = node + ";" + line.strip()
    words = [[x.strip() for x in re.split(";", text_data)]]
    return words


class Log2Csv(object):
    def __init__(self):
        self.log_prefix = ""
        self.input_path = config.log_path
        self.output_path = config.output_path

    def invxc2csv(self, tail_of_file="_invxc.log"):
        invxc_sw = invxc_board = invxc_xpboard = invxc_ret = ""
        invxc_rilink1 = invxc_rilink2 = invxc_rilink3 = invxc_sfp = ""
        invxc_tn = invxc_rf = ""
        head_sw = data_sw = []
        head_board = data_board = []
        head_ret = data_ret = []
        head_xpboard = data_xpboard = []
        head_rilink1 = data_rilink1 = []
        head_rilink2 = data_rilink2 = []
        head_rilink3 = data_rilink3 = []
        head_sfp = data_sfp = []
        head_tn = data_tn = []
        head_rf = data_rf = []
        input_files = obj_file.file_number(os.path.join(self.input_path, "*" + tail_of_file))
        if not input_files:
            pass
        else:
            for file_name in input_files:
                head_line = ""
                node_name = os.path.basename(file_name)[:-len(tail_of_file)]
                # read log file
                lines = open(file_name, "r").readlines()
                for line in lines:
                    # data_sw
                    if "Node: RadioNode " in line:
                        # get head for SW
                        head_sw = get_data_invxc("Node", "SW")
                        # get data for SW
                        sw_name = line.replace(line[:+len("Node: RadioNode N")], "").strip()
                        data_sw.append([node_name, sw_name])
                    # get head for others
                    elif line.startswith("FRU") & (";ST" in line):
                        head_line = line
                        head_board = get_data_invxc("Node", line)
                        if not ("PMTEMP" in head_line):
                            head_board[0].insert(-3, "PMTEMP")
                    elif line.startswith("XPBOARD"):
                        head_line = line
                        head_xpboard = get_data_invxc("Node", line)
                    elif line.startswith("AntennaNearUnit"):
                        head_line = line
                        head_ret = get_data_invxc("Node", line)
                    elif line.startswith("ID") & (";BOARD1" in line):
                        head_line = line
                        head_rilink1 = get_data_invxc("Node", line)
                    elif line.startswith("ID") & (";VENDOR1" in line):
                        head_line = line
                        head_rilink2 = get_data_invxc("Node", line)
                    elif line.startswith("ID") & (";WL1" in line):
                        head_line = line
                        head_rilink3 = get_data_invxc("Node", line)
                    elif line.startswith("ID") & (";SFPLNH" in line):
                        head_line = line
                        head_sfp = get_data_invxc("Node", line)
                    elif line.startswith("BOARD") & (";MacAddress" in line):
                        head_line = line
                        head_tn = get_data_invxc("Node", line)
                    elif line.startswith("FRU") & (";RF" in line):
                        head_line = line
                        head_rf = get_data_invxc("Node", line)
                    # get data for others
                    elif ";" in line:
                        if head_line.startswith("FRU") & (";ST" in head_line):
                            data = get_data_invxc(node_name, line)
                            if "PMTEMP" not in head_line:
                                data[0].insert(-3, "")
                            if "SUP " not in line:
                                data_board.extend(data)
                        elif head_line.startswith("XPBOARD"):
                            data_xpboard.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("AntennaNearUnit"):
                            data_ret.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("ID") & (";BOARD1" in head_line):
                            data_rilink1.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("ID") & (";VENDOR1" in head_line):
                            data_rilink2.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("ID") & (";WL1" in head_line):
                            data_rilink3.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("ID") & (";SFPLNH" in head_line):
                            data_sfp.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("BOARD") & (";MacAddress" in head_line):
                            data_tn.extend(get_data_invxc(node_name, line))
                        elif head_line.startswith("FRU") & (";RF" in head_line):
                            data_rf.extend(get_data_invxc(node_name, line))
                    # end of data
                    elif (not line.strip()) | (line.startswith("Tip:")):
                        head_line = ""
                    else:
                        pass
            # write data to CSV
            if data_sw:
                head_sw.extend(data_sw)
                invxc_sw = obj_data.write_data_to_csv(head_sw, os.path.join(self.output_path,
                                                                            config.log_prefix + "invxc_SW.csv"))
            if data_board:
                head_board.extend(data_board)
                invxc_board = obj_data.write_data_to_csv(head_board, os.path.join(self.output_path,
                                                                                  config.log_prefix + "invxc_Board.csv")
                                                         )
            if data_xpboard:
                head_xpboard.extend(data_xpboard)
                invxc_xpboard = obj_data.write_data_to_csv(head_xpboard,
                                                           os.path.join(self.output_path,
                                                                        config.log_prefix + "invxc_xpBoard.csv"))
            if data_ret:
                head_ret.extend(data_ret)
                invxc_ret = obj_data.write_data_to_csv(head_ret, os.path.join(self.output_path,
                                                                              config.log_prefix + "invxc_ret.csv"))
            if data_rilink1:
                head_rilink1.extend(data_rilink1)
                invxc_rilink1 = obj_data.write_data_to_csv(head_rilink1,
                                                           os.path.join(self.output_path,
                                                                        config.log_prefix + "invxc_RiLink1.csv"))
            if data_rilink2:
                head_rilink2.extend(data_rilink2)
                invxc_rilink2 = obj_data.write_data_to_csv(head_rilink2,
                                                           os.path.join(self.output_path,
                                                                        config.log_prefix + "invxc_RiLink2.csv"))
            if data_rilink3:
                head_rilink3.extend(data_rilink3)
                invxc_rilink3 = obj_data.write_data_to_csv(head_rilink3,
                                                           os.path.join(self.output_path,
                                                                        config.log_prefix + "invxc_RiLink3.csv"))
            if data_sfp:
                head_sfp.extend(data_sfp)
                invxc_sfp = obj_data.write_data_to_csv(head_sfp, os.path.join(self.output_path,
                                                                              config.log_prefix + "invxc_sfp.csv"))
            if data_tn:
                head_tn.extend(data_tn)
                invxc_tn = obj_data.write_data_to_csv(head_tn, os.path.join(self.output_path,
                                                                            config.log_prefix + "invxc_tn.csv"))
            if data_rf:
                head_rf.extend(data_rf)
                invxc_rf = obj_data.write_data_to_csv(head_rf, os.path.join(self.output_path,
                                                                            config.log_prefix + "invxc_rf.csv"))
        file_list = [invxc_sw, invxc_board, invxc_xpboard, invxc_ret,
                     invxc_rilink1, invxc_rilink2, invxc_rilink3,
                     invxc_sfp, invxc_tn, invxc_rf]
        print("extract %s to csv %s" % ("*_invxc.log", file_list))
        return file_list

    def dullogl2csv(self, tail_of_file="_llogl.log"):
        data = []
        text_head = "SiteName;Type;No;Reason;Time;Program;Rank;Signal;PMD;Extra"
        input_files = obj_file.file_number(os.path.join(self.input_path, "*" + tail_of_file))
        if not input_files:
            output_file = None
        else:
            # define the file names
            output_file = os.path.join(self.output_path,
                                       config.log_prefix + tail_of_file.replace("_", "")[:-4] + ".csv")
            data_head = [re.split(";", text_head)]
            # get the log file name
            for file_name in input_files:
                node_name = os.path.basename(file_name).replace(tail_of_file, "")
                # read log file
                lines = open(file_name, "r").readlines()
                for line in lines:
                    words = re.split(r";", line.replace(r":  ", ";", 1))
                    board = no = reason = time = program = pid = rank = signal = pmd = extra = "-"
                    if "No:  " in line:
                        board = "DU"
                        no = words[-1].strip()
                    elif "Reason:  " in line:
                        reason = words[-1].strip()
                    elif "Time:  " in line:
                        time = words[-1].strip()
                    elif "Program:  " in line:
                        program = words[-1].strip()
                    elif "Pid:  " in line:
                        pid = words[-1].strip()
                    elif "Rank:  " in line:
                        rank = words[-1].strip()
                    elif "Signal:  " in line:
                        signal = words[-1].strip()
                    elif "PMD:  " in line:
                        pmd = words[-1].strip()
                    elif "Extra:  " in line:
                        extra = words[-1].strip()
                    if "Extra:  " in line:
                        data.append([node_name, board, no, reason, time, program, pid, rank,
                                     signal, pmd, extra])
            if data:
                data_head.extend(data)
                obj_data.write_data_to_csv(data_head, output_file)
            else:
                obj_data.write_data_to_csv(data, output_file)
            print("extract %s to csv %s" % ("*" + tail_of_file, output_file))
        return output_file

    def scg2csv(self, tail_of_file="_scg.log"):
        data = []
        text_head = "SiteName;Type;SystemConstants"
        input_files = obj_file.file_number(os.path.join(self.input_path, "*" + tail_of_file))
        if not input_files:
            output_file = None
        else:
            # define the file names
            output_file = os.path.join(self.output_path,
                                       config.log_prefix + tail_of_file.replace("_", "")[:-4] + ".csv")
            data_head = [re.split(";", text_head)]
            # get the log file name
            for file_name in input_files:
                node_name = os.path.basename(file_name).replace(tail_of_file, "")
                # read log file
                lines = open(file_name, "r").readlines()
                sc_type = None
                for line in lines:
                    if "All: " in line:
                        sc_type = "All"
                        data.append([node_name, sc_type, line.replace("All: ", "").strip()])
                        break
                    elif "Namespace  SystemConstants" in line:
                        sc_type = "Namespace"
                    elif sc_type == "Namespace":
                        if "================" in line:
                            pass
                        elif not line.strip():
                            break
                        else:
                            words = re.split(r"\s+", line.strip())
                            if len(words) >= 2:
                                data.append([node_name, words[0], words[1]])
            if data:
                data_head.extend(data)
                obj_data.write_data_to_csv(data_head, output_file)
            else:
                obj_data.write_data_to_csv(data, output_file)
            print("extract %s to csv %s" % ("*" + tail_of_file, output_file))
        return output_file

    def rullogl2csv(self, tail_of_file="_lhrullogl.log"):
        # define the file names
        data = []
        text_head = "SiteName;Type;No;Reason;Time;Program;Pid;Rank;Signal;PMD;Extra"
        input_files = obj_file.file_number(os.path.join(self.input_path, "*" + tail_of_file))
        if not input_files:
            output_file = None
        else:
            # define the file names
            output_file = os.path.join(self.output_path,
                                       config.log_prefix + tail_of_file.replace("_", "")[:-4] + ".csv")
            data_head = [re.split(";", text_head)]
            # get the log file name
            for file_name in input_files:
                node_name = os.path.basename(file_name).replace(tail_of_file, "")
                # read log file
                lines = open(file_name, "r").readlines()
                for line in lines:
                    words = re.split(r";", line.replace(":", ";", 2))
                    board = no = reason = time = program = pid = rank = signal = pmd = extra = "-"
                    if "No:  " in line:
                        board = words[0].strip()
                        no = words[-1].strip()
                    elif "Reason:  " in line:
                        reason = words[-1].strip()
                    elif "Time:  " in line:
                        time = words[-1].strip()
                    elif "Program:  " in line:
                        program = words[-1].strip()
                    elif "Pid:  " in line:
                        pid = words[-1].strip()
                    elif "Rank:  " in line:
                        rank = words[-1].strip()
                    elif "Signal:  " in line:
                        signal = words[-1].strip()
                    elif "PMD:  " in line:
                        pmd = words[-1].strip()
                    elif "Extra:  " in line:
                        extra = words[-1].strip()
                    if "Extra:  " in line:
                        data.append(
                            [node_name, board, no, reason,
                             time, program, pid, rank,
                             signal, pmd, extra])
            # write data to CSV
            if data:
                data_head.extend(data)
                obj_data.write_data_to_csv(data_head, output_file)
            else:
                obj_data.write_data_to_csv(data, output_file)
            print("extract %s to csv %s" % ("*" + tail_of_file, output_file))
        return output_file

    def invlr2csv(self, tail_of_file="_invlrc.log"):
        # define the file names
        license_state = finger_print = installation_time = sequence_number = autonomous_mode = emergency_unlock = ""
        integration_unlock = feature_expire = capacity_expire = graceperiod_state = graceperiod_expire = ""
        data = []
        text_head = "SiteName;LicenseState;FingerPrint;InstallationTime;SequenceNumber;AutonomousMode;EmergencyUnlock" \
                    ";IntegrationUnlock;FeatureExpire;CapacityExpire;GracePeriodState;GracePeriodExpire "
        input_files = obj_file.file_number(os.path.join(self.input_path, "*" + tail_of_file))
        if not input_files:
            output_file = None
        else:
            # define the file names
            output_file = os.path.join(self.output_path,
                                       config.log_prefix + tail_of_file.replace("_", "")[:-4] + ".csv")
            data_head = [re.split(";", text_head)]
            # get the log file name
            for file_name in input_files:
                node_name = os.path.basename(file_name).replace(tail_of_file, "")
                # read log file
                lines = open(file_name, "r").readlines()
                for line in lines:
                    words = re.split(r":\s+\s+", line.strip())
                    if "LicenseState:  " in line:
                        license_state = words[-1].strip()
                    elif "FingerPrint:  " in line:
                        finger_print = words[-1].strip()
                    elif "InstallationTime:  " in line:
                        installation_time = words[-1].strip()
                    elif "SequenceNumber:  " in line:
                        sequence_number = words[-1].strip()
                    elif "AutonomousMode:  " in line:
                        autonomous_mode = words[-1].strip()
                    elif "EmergencyUnlock:  " in line:
                        emergency_unlock = words[-1].strip()
                    elif "IntegrationUnlock:  " in line:
                        integration_unlock = words[-1].strip()
                    elif "FeatureExpire:  " in line:
                        feature_expire = words[-1].strip()
                    elif "CapacityExpire:  " in line:
                        capacity_expire = words[-1].strip()
                    elif "GracePeriodState:  " in line:
                        graceperiod_state = words[-1].strip()
                    elif "GracePeriodExpire:  " in line:
                        graceperiod_expire = words[-1].strip()

                    if "GracePeriodExpire:  " in line:
                        data.append(
                            [node_name, license_state, finger_print, installation_time,
                             sequence_number, autonomous_mode, emergency_unlock, integration_unlock,
                             feature_expire, capacity_expire, graceperiod_state, graceperiod_expire])
            # write data to CSV
            if data:
                data_head.extend(data)
                obj_data.write_data_to_csv(data_head, output_file)
            else:
                obj_data.write_data_to_csv(data, output_file)
            print("extract %s to csv %s" % ("*" + tail_of_file, output_file))
        return output_file


if __name__ == '__main__':
    # pass
    log = "/home/ejungwa/hcTool/log/14-07/temp1"
    # altc2csv(os.path.join(log, "grep_altc.txt"))
    # nocontact2csvaltc(os.path.join(log, "grep_no_contact.txt"),
    #                   os.path.join(log, "grep_altc.csv"))
    # st2csv(os.path.join(log, "grep_st_cell.txt"))
    # st2csv(os.path.join(log, "grep_st_TermPointToENB.txt"))
    # st2csv(os.path.join(log, "grep_st_TermPointToGNB.txt"))
    # st2csv(os.path.join(log, "grep_st_TermPointToAmf.txt"))
    # st2csv(os.path.join(log, "grep_st_FieldReplaceableUnit.txt"))
    # st2csv(os.path.join(log, "grep_st_disable.txt"))
    # invlrc2csv(os.path.join(log, "grep_invlrc.txt"))
    # interferencePwr2csv(os.path.join(log, "grep_pmxet_RadioRecInterferencePwr.txt"))
    # lguc2csv(os.path.join(log, "grep_lguc.txt"))
    # scg2csv(os.path.join(log, "grep_scg.txt"))
    # cv_sw2csv(os.path.join(log, "grep_sw_version.txt"))
    # lgoc2csv(os.path.join(log, "grep_lgoc.txt"))
    # lgjc2csv(os.path.join(log, "grep_lgjc.txt"))
    # lggc2csv(os.path.join(log, "grep_lggc.txt"))

    log1 = "/home/ejungwa/hcTool/log/20201122010228"
    log2csv = Log2Csv()
    log2csv.input_path = log1
    log2csv.output_path = config.output_path
    # log2csv.invxc2csv("_invxc.log")
    # log2csv.dullogl2csv("_llogl.log")
    # log2csv.rullogl2csv("_lhrullogl.log")
    # log2csv.invlr2csv("_invlrc.log")
    log2csv.scg2csv("_scg.log")
