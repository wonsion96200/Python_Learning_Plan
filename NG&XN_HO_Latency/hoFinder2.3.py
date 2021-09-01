# Python3
# 1.0  2021-7-29 First Release
# 1.1  2021-8-3  Improved the calculation of Xn handover
# 1.2  2021-8-3  Optimized the Xn handover head
# 2.0  2021-8-6  rewrite the code, optimized the data structure for easy to read
# 2.1  2021-8-12 Adding the E2E CP latency
# 2.2  2021-8-12 Adding a detail switch, run tool with parameter detail will get more intermediate data
# 2.3  2021-8-13 new function cp latency regarding calculate, output file xn(or ng)_cp_latency_xxx.csv


import csv
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

OFF_SET_OF_NG_SOURCE = 4
OFF_SET_OF_NG_TARGET = 3
OFF_SET_OF_XN_SOURCE = 3
OFF_SET_OF_XN_TARGET = 3
COUNT_NG_SOURCE = 6
COUNT_NG_TARGET = 4
COUNT_XN_SOURCE = 5
COUNT_XN_TARGET = 6


def read_csv_to_data(csv_file=""):
    """
    read the csv_file to the data table(csv_file shall be exist)
    :param csv_file:str
    :return:data
    """
    data = []
    if csv_file:
        if os.path.exists(csv_file):
            with open(os.path.join(csv_file), "r", encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
    return data


def write_data_to_csv(data, csv_file=""):
    """
    write the data list to a new csv file(overwrite if csv_file exist)
    :param data:list
    :param csv_file: str
    :return:csv_file
    """
    with open(csv_file, "w", encoding='utf-8-sig', newline='') as csvfile:
        if data:
            writer = csv.writer(csvfile, dialect="excel")
            writer.writerows(data)
    return csv_file


def get_ue_trace_id_and_time_stamp(line):
    ue_trace_id = time_stamp = ""
    if line.strip():
        words = line.strip().split()
        if words[0].startswith("2"):
            time_stamp = words[0] + " " + words[1][0:15]
            for word in words:
                if '0x' in word:
                    ue_trace_id = word
    return ue_trace_id, time_stamp


def ng_source_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    with open(file_path) as fs:
        lines = fs.readlines()

    data = []
    for num, line in enumerate(lines):
        # S1 (NGAP)  HandoverRequired
        if "(NGAP)  HandoverRequired" in line:
            # get ue_trace_id and time_stamp
            ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(line)
            bin_gnbid = "0b" + re.search(r'gNBId:(.*)\'B', line).group(1)
            str_gnbid = str((int(bin_gnbid, 2)))
            # Structure the data row
            row = [file_name, ue_trace_id, str(num + 1), str_gnbid, None, time_stamp, None, None, None, None]
            states = [False, True, False, False, False, False, False]
            # S0 (RRC5G) MeasurementReport
            i = num - 1
            while i >= 0:
                next_ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if "(RRC5G) MeasurementReport:" in lines[i] and next_ue_trace_id == ue_trace_id:
                    row[0 + OFF_SET_OF_NG_SOURCE] = time_stamp
                    states[0] = True
                    break
                i -= 1

            # S2 - S5
            i = num + 1
            while i < len(lines):
                next_ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if next_ue_trace_id == ue_trace_id:
                    # S2 (NGAP)  HandoverCommand
                    if "(NGAP)  HandoverCommand:" in lines[i]:
                        row[2 + OFF_SET_OF_NG_SOURCE] = time_stamp
                        states[2] = True
                    # S3 (RRC5G) RRCReconfiguration
                    elif "(RRC5G) RRCReconfiguration:" in lines[i] and states[2]:
                        row[3 + OFF_SET_OF_NG_SOURCE] = time_stamp
                        states[3] = True
                    # S4 (NGAP)  UEContextReleaseCommand
                    elif "(NGAP)  UEContextReleaseCommand:" in lines[i] and states[2]:
                        row[4 + OFF_SET_OF_NG_SOURCE] = time_stamp
                        states[4] = True
                    # S5 (NGAP)  UEContextReleaseComplete
                    elif "(NGAP)  UEContextReleaseComplete:" in lines[i] and states[4]:
                        row[5 + OFF_SET_OF_NG_SOURCE] = time_stamp
                        states[5] = True
                        # put data row into data
                        data.append(row)
                        break
                i += 1
    return data


def ng_target_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    with open(file_path) as fs:
        lines = fs.readlines()

    is_repeat_handover_request = False
    next_ue_trace_id = ""
    dada = []
    for num, line in enumerate(lines):
        # T0 (NGAP)  HandoverRequest
        if "(NGAP)  HandoverRequest:" in line:
            # get ue_trace_id and time_stamp
            ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(line)
            if ue_trace_id != next_ue_trace_id:
                is_repeat_handover_request = False
            if is_repeat_handover_request:
                is_repeat_handover_request = False
            else:
                # Structure the data row
                row = [file_name, ue_trace_id, str(num + 1), time_stamp, None, None, None]
                states = [True, False, False, False, False]
                is_repeat_handover_request = True

                # T1 - T4
                i = num + 1
                while i < len(lines):
                    next_ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                    if next_ue_trace_id == ue_trace_id:
                        # T1 (NGAP)  HandoverRequestAcknowledge
                        if "(NGAP)  HandoverRequestAcknowledge:" in lines[i]:
                            row[1 + OFF_SET_OF_NG_TARGET] = time_stamp
                            states[1] = True
                        # T2 (RRC5G) RRCReconfigurationComplete
                        elif "(RRC5G) RRCReconfigurationComplete:" in lines[i] and states[1]:
                            row[2 + OFF_SET_OF_NG_TARGET] = time_stamp
                            states[2] = True
                        # T3 (NGAP)  HandoverNotify
                        elif "(NGAP)  HandoverNotify:" in lines[i] and states[2]:
                            row[3 + OFF_SET_OF_NG_TARGET] = time_stamp
                            states[3] = True
                            dada.append(row)
                            break
                    i += 1
    return dada


def ng_source_matching_target(data_source, data_target):
    data = []
    for row_source in data_source:
        if not (None in row_source):
            # filter out the columns for filename, ue_trace_id, row
            s = row_source[OFF_SET_OF_NG_SOURCE:]
            s1 = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S.%f')
            s2 = datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
            s3 = datetime.strptime(s[3], '%Y-%m-%d %H:%M:%S.%f')
            s4 = datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S.%f')
            for row_target in data_target:
                if not (None in row_target) and (row_source[0] != row_target[0]):
                    # filter out the columns for filename, ue_trace_id, row
                    t = row_target[OFF_SET_OF_NG_TARGET:]
                    t0 = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S.%f')
                    t1 = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f')
                    t2 = datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S.%f')
                    t3 = datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S.%f')
                    time_diff1 = (t0 - s1).total_seconds()
                    time_diff2 = (s2 - t1).total_seconds()
                    time_diff3 = (t2 - s3).total_seconds()
                    time_diff4 = (s4 - t3).total_seconds()
                    if time_diff1 > 0 and time_diff2 > 0 and time_diff3 > 0 and time_diff4 > 0:
                        row_source.extend(row_target)
                        data.append(row_source)
    return data


def ng_valid_matching_filter(data_in):
    col_source_file = 0
    col_target_file = OFF_SET_OF_NG_SOURCE + COUNT_NG_SOURCE
    col_gnbid = OFF_SET_OF_NG_SOURCE - 1
    # dict_gnbid is a Nested dictionaries
    dict_gnbid = defaultdict(dict)
    for row in data_in:
        key1 = row[col_source_file] + ";" + row[col_target_file]
        key2 = row[col_gnbid]
        dict_gnbid.setdefault(key1, {key2: 0})
        temp_dict = dict_gnbid[key1]
        if not (key2 in temp_dict):
            temp_dict.setdefault(key2, 0)
        dict_gnbid[key1][key2] += 1
    data_valid = []
    data_fake = []
    for key1 in dict_gnbid:
        tmp = dict_gnbid[key1]
        value = 0
        gnb_id = ""
        for key2 in tmp:
            if value < dict_gnbid[key1][key2]:
                value = dict_gnbid[key1][key2]
                gnb_id = key2
        for row in data_in:
            if row[col_source_file] + ";" + row[col_target_file] == key1:
                if row[col_gnbid] == gnb_id:
                    data_valid.append(row)
                else:
                    data_fake.append(row)
    return data_valid, data_fake


def ng_delta_time_summary(data_in):
    head = [["ue_source", "PhaseA", "PhaseB", "PhaseC", "PhaseD", "PhaseE",
             "TotalSrc(A+B+C)", "TotalTar(D+E)", "E2E", "ue_target"]]
    data = []
    for row in data_in:
        s = row[OFF_SET_OF_NG_SOURCE:]  # get the datetime of s0 - s5
        t = row[-COUNT_NG_TARGET:]  # get the datetime of t0 - t3
        s0 = datetime.strptime(s[0], '%Y-%m-%d %H:%M:%S.%f')
        s1 = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S.%f')
        s2 = datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
        s3 = datetime.strptime(s[3], '%Y-%m-%d %H:%M:%S.%f')
        s4 = datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S.%f')
        s5 = datetime.strptime(s[5], '%Y-%m-%d %H:%M:%S.%f')
        t0 = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S.%f')
        t1 = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S.%f')
        t3 = datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S.%f')
        phase_a = (s1 - s0).total_seconds() * 1000
        phase_b = (s3 - s2).total_seconds() * 1000
        phase_c = (s5 - s4).total_seconds() * 1000
        phase_d = (t1 - t0).total_seconds() * 1000
        phase_e = (t3 - t2).total_seconds() * 1000
        e2e = (s4 - s0).total_seconds() * 1000
        phase_a_b_c = phase_a + phase_b + phase_c
        phase_d_e = phase_d + phase_e
        source = ".".join(row[0:3])
        target = ".".join(row[9:12])
        data_row = [source, round(phase_a, 3), round(phase_b, 3), round(phase_c, 3), round(phase_d, 3),
                    round(phase_e, 3), round(phase_a_b_c, 3), round(phase_d_e, 3), round(e2e, 3), target]
        data.append(data_row)
    if data:
        head.extend(data)
    else:
        head = []
    return head


def ng_delta_time_cp_latency(head, data_in):
    data = []
    for row in data_in:
        s = row[OFF_SET_OF_NG_SOURCE:]  # get the datetime of s0 - s3
        t = row[-COUNT_NG_TARGET:]  # get the datetime of t0 - t5
        new_row = row.copy()
        s0 = datetime.strptime(s[0], '%Y-%m-%d %H:%M:%S.%f')
        s1 = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S.%f')
        s2 = datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
        s3 = datetime.strptime(s[3], '%Y-%m-%d %H:%M:%S.%f')
        s4 = datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S.%f')
        s5 = datetime.strptime(s[5], '%Y-%m-%d %H:%M:%S.%f')
        t0 = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S.%f')
        t1 = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S.%f')
        t3 = datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S.%f')

        new_row[0 + OFF_SET_OF_NG_SOURCE] = (s0 - s0).total_seconds() * 1000
        new_row[1 + OFF_SET_OF_NG_SOURCE] = (s1 - s0).total_seconds() * 1000
        new_row[2 + OFF_SET_OF_NG_SOURCE] = (s2 - s0).total_seconds() * 1000
        new_row[3 + OFF_SET_OF_NG_SOURCE] = (s3 - s0).total_seconds() * 1000
        new_row[4 + OFF_SET_OF_NG_SOURCE] = (s4 - s0).total_seconds() * 1000
        new_row[5 + OFF_SET_OF_NG_SOURCE] = (s5 - s0).total_seconds() * 1000
        new_row[0 - COUNT_NG_TARGET] = (t0 - s0).total_seconds() * 1000
        new_row[1 - COUNT_NG_TARGET] = (t1 - s0).total_seconds() * 1000
        new_row[2 - COUNT_NG_TARGET] = (t2 - s0).total_seconds() * 1000
        new_row[3 - COUNT_NG_TARGET] = (t3 - s0).total_seconds() * 1000
        data.append(new_row)
    if data:
        head.extend(data)
    else:
        head = []
    return head


def ng_handover_parsing(file_path, debug=False):
    ho_source = []
    ho_target = []
    for root_dir, dirs, files in os.walk(file_path):
        for file_name in files:
            extension = os.path.splitext(file_name)[-1]
            if extension in ".flow" or extension in ".flw":
                fileurl = os.path.join(root_dir, file_name)
                temp_data = ng_source_gnb(fileurl)
                if temp_data:
                    ho_source.extend(temp_data)
                temp_data = ng_target_gnb(fileurl)
                if temp_data:
                    ho_target.extend(temp_data)
    if debug:
        source_head = [
            ["SourceFile", "SourceTraceId", "RowNo", "TargetGNB", "S1(RRC5G) MeasurementReport",
             "S2(NGAP)  HandoverRequired",
             "S3(NGAP)  HandoverCommand", "S4(RRC5G) RRCReconfiguration", "S5(NGAP)  UEContextReleaseCommand",
             "S6(NGAP)  UEContextReleaseComplete"]]
        if ho_source:
            source_head.extend(ho_source)
            write_data_to_csv(source_head, os.path.join(file_path, "ng_ho_source.csv"))
        target_head = [["TargetFile", "TargetTraceId", "RowNo", "T1(NGAP)  HandoverRequest",
                        "T2NGAP)  HandoverRequestAcknowledge", "T3(RRC5G) RRCReconfigurationComplete",
                        "T4(NGAP)  HandoverNotify"]]
        if ho_target:
            target_head.extend(ho_target)
            write_data_to_csv(ho_target, os.path.join(file_path, "ng_ho_target.csv"))

    # ho matching between source and target
    ho_matching = ng_source_matching_target(ho_source, ho_target)
    ho_valid, ho_fake = ng_valid_matching_filter(ho_matching)
    head = [["SourceFile", "SourceTraceId", "RowNo", "TargetGNB", "S1(RRC5G) MeasurementReport",
             "S2(NGAP)  HandoverRequired", "S3(NGAP)  HandoverCommand", "S4(RRC5G) RRCReconfiguration",
             "S5(NGAP)  UEContextReleaseCommand", "S6(NGAP)  UEContextReleaseComplete", "TargetFile",
             "TargetTraceId", "RowNo", "T1(NGAP)  HandoverRequest", "T2NGAP)  HandoverRequestAcknowledge",
             "T3(RRC5G) RRCReconfigurationComplete", "T4(NGAP)  HandoverNotify"]]
    if debug:
        if ho_matching:
            matching_head = head.copy()
            matching_head.extend(ho_matching)
            write_data_to_csv(matching_head, os.path.join(file_path, "ng_ho_matching_all.csv"))
        if ho_valid:
            valid_head = head.copy()
            valid_head.extend(ho_valid)
            write_data_to_csv(valid_head, os.path.join(file_path, "ng_ho_matching_valid.csv"))
        if ho_fake:
            fake_head = head.copy()
            fake_head.extend(ho_fake)
            write_data_to_csv(fake_head, os.path.join(file_path, "ng_ho_matching_fake.csv"))

    data_list = ng_delta_time_summary(ho_valid)
    output_url = os.path.join(file_path, "ng_ho_summary" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv")
    if data_list:
        write_data_to_csv(data_list, output_url)
        print(output_url)
    cp_latency = ng_delta_time_cp_latency(head, ho_valid)
    output_url = os.path.join(file_path, "ng_ho_cp_latency" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv")
    if cp_latency:
        write_data_to_csv(cp_latency, output_url)
        print(output_url)


def xn_source_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    with open(file_path) as fs:
        lines = fs.readlines()

    data = []
    for num, line in enumerate(lines):
        # S1 (XNAP)  HandoverRequest:
        if "(XNAP)  HandoverRequest:" in line and "==>" in line:
            # get ue_trace_id and time_stamp
            ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(line)
            # Structure the data row
            row = [file_name, ue_trace_id, str(num + 1), None, time_stamp, None, None, None]
            states = [False, True, False, False, False]

            # S0 (RRC5G) MeasurementReport
            i = num - 1
            while i >= 0:
                new_ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if "(RRC5G) MeasurementReport:" in lines[i] and new_ue_trace_id == ue_trace_id:
                    row[0 + OFF_SET_OF_XN_SOURCE] = time_stamp
                    states[0] = True
                    break
                i -= 1

            # S2 - S4
            i = num + 1
            while i < len(lines):
                new_ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if new_ue_trace_id == ue_trace_id:
                    # S2 (XNAP)  HandoverRequestAcknowledge
                    if "(XNAP)  HandoverRequestAcknowledge:" in lines[i]:
                        row[2 + OFF_SET_OF_XN_SOURCE] = time_stamp
                        states[2] = True
                    # S3 (RRC5G) RRCReconfiguration
                    elif "(RRC5G) RRCReconfiguration:" in lines[i] and states[2]:
                        row[3 + OFF_SET_OF_XN_SOURCE] = time_stamp
                        states[3] = True
                    # S4 (NGAP)  UEContextReleaseCommand
                    elif "(XNAP)  UEContextRelease:" in lines[i] and states[2]:
                        row[4 + OFF_SET_OF_XN_SOURCE] = time_stamp
                        states[4] = True
                        # put data row into data
                        data.append(row)
                        break
                i += 1
    return data


def xn_target_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    with open(file_path) as fs:
        lines = fs.readlines()

    is_repeat_handover_request = False
    next_ue_trace_id = ""
    dada = []
    for num, line in enumerate(lines):
        # T0 (XNAP)  HandoverRequest
        if "(XNAP)  HandoverRequest:" in line and "<==" in line:
            # get ue_trace_id and time_stamp
            ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(line)
            if ue_trace_id != next_ue_trace_id:
                is_repeat_handover_request = False
            if is_repeat_handover_request:
                is_repeat_handover_request = False
            else:
                # Structure the data row
                row = [file_name, ue_trace_id, str(num + 1), time_stamp, None, None, None, None, None]
                states = [True, False, False, False, False, False]
                is_repeat_handover_request = True

                # T1 - T5
                i = num + 1
                while i < len(lines):
                    next_ue_trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                    if next_ue_trace_id == ue_trace_id:
                        # T1 (NGAP)  HandoverRequestAcknowledge
                        if "(XNAP)  HandoverRequestAcknowledge:" in lines[i]:
                            row[1 + OFF_SET_OF_XN_TARGET] = time_stamp
                            states[1] = True
                        # T2 (RRC5G) RRCReconfigurationComplete
                        elif "(RRC5G) RRCReconfigurationComplete:" in lines[i] and states[1]:
                            row[2 + OFF_SET_OF_XN_TARGET] = time_stamp
                            states[2] = True
                        # T3 (NGAP)  PathSwitchRequest:
                        elif "(NGAP)  PathSwitchRequest:" in lines[i] and states[2]:
                            row[3 + OFF_SET_OF_XN_TARGET] = time_stamp
                            states[3] = True
                        # T4 (NGAP)  PathSwitchRequestAcknowledge
                        elif "(NGAP)  PathSwitchRequestAcknowledge:" in lines[i] and states[3]:
                            row[4 + OFF_SET_OF_XN_TARGET] = time_stamp
                            states[4] = True
                        # T5 (XNAP)  UEContextRelease
                        elif "(XNAP)  UEContextRelease:" in lines[i] and states[4]:
                            row[5 + OFF_SET_OF_XN_TARGET] = time_stamp
                            states[2] = True
                            dada.append(row)
                            break
                    i += 1
    return dada


def xn_source_matching_target(data_source, data_target):
    data = []
    for row_source in data_source:
        if not (None in row_source):
            # filter out the columns for filename, ue_trace_id, row
            s = row_source[OFF_SET_OF_XN_SOURCE:]
            s0 = datetime.strptime(s[0], '%Y-%m-%d %H:%M:%S.%f')
            s2 = datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
            s3 = datetime.strptime(s[3], '%Y-%m-%d %H:%M:%S.%f')
            s4 = datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S.%f')
            for row_target in data_target:
                if not (None in row_target) and (row_source[0] != row_target[0]):
                    # filter out the columns for filename, ue_trace_id, row
                    t = row_target[OFF_SET_OF_XN_TARGET:]
                    t0 = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S.%f')
                    t1 = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f')
                    t3 = datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S.%f')
                    time_diff1 = (t1 - s0).total_seconds()
                    time_diff2 = (s2 - t0).total_seconds()
                    time_diff3 = (t3 - s3).total_seconds()
                    time_diff4 = (s4 - t3).total_seconds()
                    if time_diff1 > 0 and time_diff2 > 0 and time_diff3 > 0 and time_diff4 > 0:
                        row_source.extend(row_target)
                        data.append(row_source)
    return data


def xn_valid_matching_filter(data_in):
    col_source_trace_id = 1
    col_target_trace_id = OFF_SET_OF_XN_SOURCE + COUNT_XN_SOURCE + 1
    data_valid = []
    data_fake = []
    for row in data_in:
        if row[col_source_trace_id] == row[col_target_trace_id]:
            data_valid.append(row)
        else:
            data_fake.append(row)
    return data_valid, data_fake


def xn_delta_time_summary(data_in):
    head = [["ue_source", "PhaseA", "PhaseB", "PhaseC", "PhaseD", "PhaseE",
             "TotalSrc(A+C)", "TotalTar(B+D+E)", "E2E", "ue_target"]]
    data = []
    for row in data_in:
        s = row[OFF_SET_OF_XN_SOURCE:]  # get the datetime of s0 - s3
        t = row[-COUNT_XN_TARGET:]  # get the datetime of t0 - t5
        s0 = datetime.strptime(s[0], '%Y-%m-%d %H:%M:%S.%f')
        s1 = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S.%f')
        s2 = datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
        s3 = datetime.strptime(s[3], '%Y-%m-%d %H:%M:%S.%f')
        s4 = datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S.%f')
        t0 = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S.%f')
        t1 = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S.%f')
        t3 = datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S.%f')
        t4 = datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S.%f')
        t5 = datetime.strptime(t[5], '%Y-%m-%d %H:%M:%S.%f')

        phase_a = (s1 - s0).total_seconds() * 1000
        phase_c = (s3 - s2).total_seconds() * 1000
        phase_b = (t1 - t0).total_seconds() * 1000
        phase_d = (t3 - t2).total_seconds() * 1000
        phase_e = (t5 - t4).total_seconds() * 1000
        e2e = (s4 - s0).total_seconds() * 1000

        phase_a_c = phase_a + phase_c
        phase_b_d_e = phase_b + phase_d + phase_e
        source = ".".join(row[0:3])
        target = ".".join(row[8:11])
        data_row = [source, round(phase_a, 3), round(phase_b, 3), round(phase_c, 3), round(phase_d, 3),
                    round(phase_e, 3), round(phase_a_c, 3), round(phase_b_d_e, 3), round(e2e, 3), target]
        data.append(data_row)
    if data:
        head.extend(data)
    else:
        head = []
    return head


def xn_delta_time_cp_latency(head, data_in):
    data = []
    for row in data_in:
        s = row[OFF_SET_OF_XN_SOURCE:]  # get the datetime of s0 - s3
        t = row[-COUNT_XN_TARGET:]  # get the datetime of t0 - t5
        new_row = row.copy()
        s0 = datetime.strptime(s[0], '%Y-%m-%d %H:%M:%S.%f')
        s1 = datetime.strptime(s[1], '%Y-%m-%d %H:%M:%S.%f')
        s2 = datetime.strptime(s[2], '%Y-%m-%d %H:%M:%S.%f')
        s3 = datetime.strptime(s[3], '%Y-%m-%d %H:%M:%S.%f')
        s4 = datetime.strptime(s[4], '%Y-%m-%d %H:%M:%S.%f')
        t0 = datetime.strptime(t[0], '%Y-%m-%d %H:%M:%S.%f')
        t1 = datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S.%f')
        t3 = datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S.%f')
        t4 = datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S.%f')
        t5 = datetime.strptime(t[5], '%Y-%m-%d %H:%M:%S.%f')

        new_row[0 + OFF_SET_OF_XN_SOURCE] = (s0 - s0).total_seconds() * 1000
        new_row[1 + OFF_SET_OF_XN_SOURCE] = (s1 - s0).total_seconds() * 1000
        new_row[2 + OFF_SET_OF_XN_SOURCE] = (s2 - s0).total_seconds() * 1000
        new_row[3 + OFF_SET_OF_XN_SOURCE] = (s3 - s0).total_seconds() * 1000
        new_row[4 + OFF_SET_OF_XN_SOURCE] = (s4 - s0).total_seconds() * 1000
        new_row[0 - COUNT_XN_TARGET] = (t0 - s0).total_seconds() * 1000
        new_row[1 - COUNT_XN_TARGET] = (t1 - s0).total_seconds() * 1000
        new_row[2 - COUNT_XN_TARGET] = (t2 - s0).total_seconds() * 1000
        new_row[3 - COUNT_XN_TARGET] = (t3 - s0).total_seconds() * 1000
        new_row[4 - COUNT_XN_TARGET] = (t4 - s0).total_seconds() * 1000
        new_row[5 - COUNT_XN_TARGET] = (t5 - s0).total_seconds() * 1000
        data.append(new_row)
    if data:
        head.extend(data)
    else:
        head = []
    return head


def xn_handover_parsing(file_path, debug=False):
    ho_source = []
    ho_target = []
    for root_dir, dirs, files in os.walk(file_path):
        for file_name in files:
            extension = os.path.splitext(file_name)[-1]
            if extension in ".flow" or extension in ".flw":
                fileurl = os.path.join(root_dir, file_name)
                temp_data = xn_source_gnb(fileurl)
                if temp_data:
                    ho_source.extend(temp_data)
                temp_data = xn_target_gnb(fileurl)
                if temp_data:
                    ho_target.extend(temp_data)
    if debug:
        source_head = [
            ["SourceFile", "SourceTraceId", "RowNo", "S1(RRC5G) MeasurementReport", "S2(XNAP)  HandoverRequest",
             "S3(XNAP)  HandoverRequestAcknowledge", "S4(RRC5G) RRCReconfiguration", "S5(XNAP)  UEContextRelease"]]
        if ho_source:
            source_head.extend(ho_source)
            write_data_to_csv(source_head, os.path.join(file_path, "xn_ho_source.csv"))
        target_head = [["TargetFile", "TargetTraceId", "RowNo", "T1(XNAP)  HandoverRequest",
                        "T2(XNAP)  HandoverRequestAcknowledge", "T3(RRC5G) RRCReconfigurationComplete",
                        "T4(NGAP)  PathSwitchRequest", "T5(NGAP)  PathSwitchRequestAcknowledge",
                        "T6(XNAP)  UEContextRelease"]]
        if ho_target:
            target_head.extend(ho_target)
            write_data_to_csv(target_head, os.path.join(file_path, "xn_ho_target.csv"))

    # ho matching between source and target
    head = [["SourceFile", "SourceTraceId", "RowNo", "S1(RRC5G) MeasurementReport", "S2(XNAP)  HandoverRequest",
             "S3(XNAP)  HandoverRequestAcknowledge", "S4(RRC5G) RRCReconfiguration", "S5(XNAP)  UEContextRelease",
             "TargetFile", "TargetTraceId", "RowNo", "T1(XNAP)  HandoverRequest",
             "T2(XNAP)  HandoverRequestAcknowledge", "T3(RRC5G) RRCReconfigurationComplete",
             "T4(NGAP)  PathSwitchRequest", "T5(NGAP)  PathSwitchRequestAcknowledge",
             "T6(XNAP)  UEContextRelease"]]
    ho_matching = xn_source_matching_target(ho_source, ho_target)
    ho_valid, ho_fake = xn_valid_matching_filter(ho_matching)
    if debug:
        if ho_matching:
            matching_head = head.copy()
            matching_head.extend(ho_matching)
            write_data_to_csv(matching_head, os.path.join(file_path, "xn_ho_matching_all.csv"))
        if ho_valid:
            valid_head = head.copy()
            valid_head.extend(ho_valid)
            write_data_to_csv(valid_head, os.path.join(file_path, "xn_ho_matching_valid.csv"))
        if ho_fake:
            fake_head = head.copy()
            fake_head.extend(ho_fake)
            write_data_to_csv(fake_head, os.path.join(file_path, "xn_ho_matching_fake.csv"))

    data_list = xn_delta_time_summary(ho_valid)
    output_url = os.path.join(file_path, "xn_ho_summary" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv")
    if data_list:
        write_data_to_csv(data_list, output_url)
        print(output_url)
    cp_latency = xn_delta_time_cp_latency(head, ho_valid)
    output_url = os.path.join(file_path, "xn_ho_cp_latency" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv")
    if cp_latency:
        write_data_to_csv(cp_latency, output_url)
        print(output_url)


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) == 1:
        flag = False
    else:
        flag = True
    ng_handover_parsing(base_path, flag)
    xn_handover_parsing(base_path, flag)
