# Python3
# 1.0  2021-7-29
import csv
import os
from copy import deepcopy
from datetime import datetime


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
    time_dict = {}
    state_dict = {}
    with open(file_path) as fs:
        lines = fs.readlines()
    for num, line in enumerate(lines):
        # S1 (NGAP)  HandoverRequired
        if "(NGAP)  HandoverRequired" in line:
            # get ue_trace_id and time_stamp
            trace_id_1, time_stamp = get_ue_trace_id_and_time_stamp(line)
            ue_trace_id = file_name + "." + trace_id_1 + "." + str(num + 1)
            state_dict.setdefault(ue_trace_id, [False, True, False, False, False, False, False])
            time_dict.setdefault(ue_trace_id, [None, time_stamp, None, None, None, None, None])

            # S0 (RRC5G) MeasurementReport
            i = num - 1
            while i >= 0:
                trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if "(RRC5G) MeasurementReport:" in lines[i] and trace_id == trace_id_1:
                    time_dict[ue_trace_id][0] = time_stamp
                    state_dict[ue_trace_id][0] = True
                    break
                i -= 1

            i = num + 1
            while i < len(lines):
                trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if trace_id == trace_id_1:
                    # S2 (NGAP)  HandoverCommand
                    if "(NGAP)  HandoverCommand:" in lines[i]:
                        time_dict[ue_trace_id][2] = time_stamp
                        state_dict[ue_trace_id][2] = True
                    # S3 (RRC5G) RRCReconfiguration
                    elif "(RRC5G) RRCReconfiguration:" in lines[i] and state_dict[ue_trace_id][2]:
                        time_dict[ue_trace_id][-1] = "ng_ou"
                        time_dict[ue_trace_id][3] = time_stamp
                        state_dict[ue_trace_id][3] = True
                    # S4 (NGAP)  UEContextReleaseCommand
                    elif "(NGAP)  UEContextReleaseCommand:" in lines[i] and state_dict[ue_trace_id][2]:
                        time_dict[ue_trace_id][4] = time_stamp
                        state_dict[ue_trace_id][4] = True
                    # S5 (NGAP)  UEContextReleaseComplete
                    elif "(NGAP)  UEContextReleaseComplete:" in lines[i] and state_dict[ue_trace_id][4]:
                        time_dict[ue_trace_id][5] = time_stamp
                        state_dict[ue_trace_id][5] = True
                        break
                i += 1
    return time_dict


def ng_target_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    time_dict = {}
    state_dict = {}
    trace_id = ""
    is_repeat_handover_request = False
    with open(file_path) as fs:
        lines = fs.readlines()
    for num, line in enumerate(lines):
        # T0 (NGAP)  HandoverRequest
        if "(NGAP)  HandoverRequest:" in line:
            # get ue_trace_id and time_stamp
            trace_id_1, time_stamp = get_ue_trace_id_and_time_stamp(line)
            ue_trace_id = file_name + "." + trace_id_1 + "." + str(num + 1)
            if not trace_id == trace_id_1:
                is_repeat_handover_request = False
            if is_repeat_handover_request:
                is_repeat_handover_request = False
            else:
                is_repeat_handover_request = True
                state_dict.setdefault(ue_trace_id, [True, False, False, False, False])
                time_dict.setdefault(ue_trace_id, [time_stamp, None, None, None, None])

                i = num + 1
                while i < len(lines):
                    trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                    if trace_id == trace_id_1:
                        # T1 (NGAP)  HandoverRequestAcknowledge
                        if "(NGAP)  HandoverRequestAcknowledge:" in lines[i]:
                            time_dict[ue_trace_id][1] = time_stamp
                            state_dict[ue_trace_id][1] = True
                        # T2 (RRC5G) RRCReconfigurationComplete
                        elif "(RRC5G) RRCReconfigurationComplete:" in lines[i] and state_dict[ue_trace_id][1]:
                            time_dict[ue_trace_id][-1] = "ng_in"
                            time_dict[ue_trace_id][2] = time_stamp
                            state_dict[ue_trace_id][2] = True
                        # T3 (NGAP)  HandoverNotify
                        elif "(NGAP)  HandoverNotify:" in lines[i] and state_dict[ue_trace_id][2]:
                            time_dict[ue_trace_id][3] = time_stamp
                            state_dict[ue_trace_id][3] = True
                            break
                    i += 1
    return time_dict


def ng_min_gap(dict_source, dict_target):
    data = []
    for temp_key1 in dict_source:
        value1 = dict_source[temp_key1]
        if not (None in value1) and value1[-1] in "ng_ou":
            s1_time = datetime.strptime(value1[1], '%Y-%m-%d %H:%M:%S.%f')
            s2_time = datetime.strptime(value1[2], '%Y-%m-%d %H:%M:%S.%f')
            s3_time = datetime.strptime(value1[3], '%Y-%m-%d %H:%M:%S.%f')
            s4_time = datetime.strptime(value1[4], '%Y-%m-%d %H:%M:%S.%f')
            gap = k = v = None
            for temp_key2 in dict_target:
                value2 = dict_target[temp_key2]
                if not (None in value2):
                    t0_time = datetime.strptime(value2[0], '%Y-%m-%d %H:%M:%S.%f')
                    t1_time = datetime.strptime(value2[1], '%Y-%m-%d %H:%M:%S.%f')
                    t2_time = datetime.strptime(value2[2], '%Y-%m-%d %H:%M:%S.%f')
                    t3_time = datetime.strptime(value2[3], '%Y-%m-%d %H:%M:%S.%f')
                    time_diff1 = (t0_time - s1_time).total_seconds()
                    time_diff2 = (s2_time - t1_time).total_seconds()
                    time_diff3 = (t2_time - s3_time).total_seconds()
                    time_diff4 = (s4_time - t3_time).total_seconds()
                    if time_diff1 > 0 and time_diff2 > 0 and time_diff3 > 0 and time_diff4 > 0:
                        if gap:
                            if gap - time_diff1 > 0:
                                gap = time_diff1
                                k = temp_key2
                                v = value2
                        else:
                            gap = time_diff1
                            k = temp_key2
                            v = value2
            if k:
                data.append([temp_key1, value1, k, v])
    return data


def ng_delta_time_summary_e2e(data_in):
    head = [["ue_source", "PhaseA", "PhaseB", "PhaseC", "PhaseD", "PhaseE", "TotalSrc(A+B+C)", "TotalTar(D+E)",
             "ue_target"]]
    data = []
    for row in data_in:
        if "ng" in row[-1][-1]:
            value1 = row[1]
            value2 = row[3]
            s0_time = datetime.strptime(value1[0], '%Y-%m-%d %H:%M:%S.%f')
            s1_time = datetime.strptime(value1[1], '%Y-%m-%d %H:%M:%S.%f')
            s2_time = datetime.strptime(value1[2], '%Y-%m-%d %H:%M:%S.%f')
            s3_time = datetime.strptime(value1[3], '%Y-%m-%d %H:%M:%S.%f')
            s4_time = datetime.strptime(value1[4], '%Y-%m-%d %H:%M:%S.%f')
            s5_time = datetime.strptime(value1[5], '%Y-%m-%d %H:%M:%S.%f')
            t0_time = datetime.strptime(value2[0], '%Y-%m-%d %H:%M:%S.%f')
            t1_time = datetime.strptime(value2[1], '%Y-%m-%d %H:%M:%S.%f')
            t2_time = datetime.strptime(value2[2], '%Y-%m-%d %H:%M:%S.%f')
            t3_time = datetime.strptime(value2[3], '%Y-%m-%d %H:%M:%S.%f')
            a = (s1_time - s0_time).total_seconds() * 1000
            b = (s3_time - s2_time).total_seconds() * 1000
            c = (s5_time - s4_time).total_seconds() * 1000
            d = (t1_time - t0_time).total_seconds() * 1000
            e = (t3_time - t2_time).total_seconds() * 1000
            data_row = [row[0], round(a, 3), round(b, 3), round(c, 3), round(d, 3), round(e, 3), round(a + b + c, 3),
                        round(d + e, 3), row[2]]
            data.append(data_row)
    if data:
        head.extend(data)
    else:
        head = []
    return head


def xn_source_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    time_dict = {}
    state_dict = {}
    with open(file_path) as fs:
        lines = fs.readlines()
    for num, line in enumerate(lines):
        # S1 (XNAP)  HandoverRequest:
        if "(XNAP)  HandoverRequest:" in line and "==>" in line:
            # get ue_trace_id and time_stamp
            trace_id_1, time_stamp = get_ue_trace_id_and_time_stamp(line)
            ue_trace_id = file_name + "." + trace_id_1 + "." + str(num + 1)
            state_dict.setdefault(ue_trace_id, [False, True, False, False, False, False])
            time_dict.setdefault(ue_trace_id, [None, time_stamp, None, None, None, None])

            # S0 (RRC5G) MeasurementReport
            i = num - 1
            while i >= 0:
                trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if "(RRC5G) MeasurementReport:" in lines[i] and trace_id == trace_id_1:
                    time_dict[ue_trace_id][0] = time_stamp
                    state_dict[ue_trace_id][0] = True
                    break
                i -= 1

            i = num + 1
            while i < len(lines):
                trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                if trace_id == trace_id_1:
                    # S2 (XNAP)  HandoverRequestAcknowledge
                    if "(XNAP)  HandoverRequestAcknowledge:" in lines[i]:
                        time_dict[ue_trace_id][2] = time_stamp
                        state_dict[ue_trace_id][2] = True
                    # S3 (RRC5G) RRCReconfiguration
                    elif "(RRC5G) RRCReconfiguration:" in lines[i] and state_dict[ue_trace_id][2]:
                        time_dict[ue_trace_id][-1] = "xn_ou"
                        time_dict[ue_trace_id][3] = time_stamp
                        state_dict[ue_trace_id][3] = True
                    # S4 (NGAP)  UEContextReleaseCommand
                    elif "(XNAP)  UEContextRelease:" in lines[i] and state_dict[ue_trace_id][2]:
                        time_dict[ue_trace_id][4] = time_stamp
                        state_dict[ue_trace_id][4] = True
                        break
                i += 1
    return time_dict


def xn_target_gnb(file_path):
    file_name = os.path.split(file_path)[-1]
    time_dict = {}
    state_dict = {}
    trace_id = ""
    is_repeat_handover_request = False
    with open(file_path) as fs:
        lines = fs.readlines()
    for num, line in enumerate(lines):
        # T0 (XNAP)  HandoverRequest
        if "(XNAP)  HandoverRequest:" in line and "<==" in line:
            # get ue_trace_id and time_stamp
            trace_id_1, time_stamp = get_ue_trace_id_and_time_stamp(line)
            ue_trace_id = file_name + "." + trace_id_1 + "." + str(num + 1)
            if not trace_id == trace_id_1:
                is_repeat_handover_request = False

            if is_repeat_handover_request:
                is_repeat_handover_request = False
            else:
                is_repeat_handover_request = True
                state_dict.setdefault(ue_trace_id, [True, False, False, False, False, False, False])
                time_dict.setdefault(ue_trace_id, [time_stamp, None, None, None, None, None, None])

                i = num + 1
                while i < len(lines):
                    trace_id, time_stamp = get_ue_trace_id_and_time_stamp(lines[i])
                    if trace_id == trace_id_1:
                        # T1 (NGAP)  HandoverRequestAcknowledge
                        if "(XNAP)  HandoverRequestAcknowledge:" in lines[i]:
                            time_dict[ue_trace_id][1] = time_stamp
                            state_dict[ue_trace_id][1] = True
                        # T2 (RRC5G) RRCReconfigurationComplete
                        elif "(RRC5G) RRCReconfigurationComplete:" in lines[i] and state_dict[ue_trace_id][1]:
                            time_dict[ue_trace_id][-1] = "xn_in"
                            time_dict[ue_trace_id][2] = time_stamp
                            state_dict[ue_trace_id][2] = True
                        # T3 (NGAP)  PathSwitchRequest:
                        elif "(NGAP)  PathSwitchRequest:" in lines[i] and state_dict[ue_trace_id][2]:
                            time_dict[ue_trace_id][3] = time_stamp
                            state_dict[ue_trace_id][3] = True
                        # T4 (NGAP)  PathSwitchRequestAcknowledge
                        elif "(NGAP)  PathSwitchRequestAcknowledge:" in lines[i] and state_dict[ue_trace_id][3]:
                            time_dict[ue_trace_id][4] = time_stamp
                            state_dict[ue_trace_id][4] = True
                        # T5 (XNAP)  UEContextRelease
                        elif "(XNAP)  UEContextRelease:" in lines[i] and state_dict[ue_trace_id][4]:
                            time_dict[ue_trace_id][5] = time_stamp
                            state_dict[ue_trace_id][5] = True
                            break
                    i += 1
    return time_dict


def xn_min_gap(dict_source, dict_target):
    data = []
    for temp_key1 in dict_source:
        value1 = dict_source[temp_key1]
        if not (None in value1) and value1[-1] in "xn_ou":
            s1_time = datetime.strptime(value1[1], '%Y-%m-%d %H:%M:%S.%f')
            s2_time = datetime.strptime(value1[2], '%Y-%m-%d %H:%M:%S.%f')
            s3_time = datetime.strptime(value1[3], '%Y-%m-%d %H:%M:%S.%f')
            s4_time = datetime.strptime(value1[4], '%Y-%m-%d %H:%M:%S.%f')
            gap = k = v = None
            for temp_key2 in dict_target:
                value2 = dict_target[temp_key2]
                if not (None in value2):
                    t0_time = datetime.strptime(value2[0], '%Y-%m-%d %H:%M:%S.%f')
                    t1_time = datetime.strptime(value2[1], '%Y-%m-%d %H:%M:%S.%f')
                    t2_time = datetime.strptime(value2[2], '%Y-%m-%d %H:%M:%S.%f')
                    t5_time = datetime.strptime(value2[5], '%Y-%m-%d %H:%M:%S.%f')
                    time_diff1 = (t0_time - s1_time).total_seconds()
                    time_diff2 = (s2_time - t1_time).total_seconds()
                    time_diff3 = (t2_time - s3_time).total_seconds()
                    time_diff4 = (s4_time - t5_time).total_seconds()
                    if time_diff1 > 0 and time_diff2 > 0 and time_diff3 > 0 and time_diff4 > 0:
                        if gap:
                            if gap - time_diff1 > 0:
                                gap = time_diff1
                                k = temp_key2
                                v = value2
                        else:
                            gap = time_diff1
                            k = temp_key2
                            v = value2
            if k:
                data.append([temp_key1, value1, k, v])
    return data


def xn_delta_time_summary_e2e(data_in):
    head = [["ue_source", "PhaseA", "PhaseB", "PhaseC", "PhaseD", "PhaseE", "TotalSrc(A+B+C)", "TotalTar(D+E)",
             "ue_target"]]
    data = []
    for row in data_in:
        if "xn" in row[-1][-1]:
            value1 = row[1]
            value2 = row[3]
            s0_time = datetime.strptime(value1[0], '%Y-%m-%d %H:%M:%S.%f')
            s1_time = datetime.strptime(value1[1], '%Y-%m-%d %H:%M:%S.%f')
            s2_time = datetime.strptime(value1[2], '%Y-%m-%d %H:%M:%S.%f')
            s3_time = datetime.strptime(value1[3], '%Y-%m-%d %H:%M:%S.%f')
            t0_time = datetime.strptime(value2[0], '%Y-%m-%d %H:%M:%S.%f')
            t1_time = datetime.strptime(value2[1], '%Y-%m-%d %H:%M:%S.%f')
            t2_time = datetime.strptime(value2[2], '%Y-%m-%d %H:%M:%S.%f')
            t3_time = datetime.strptime(value2[3], '%Y-%m-%d %H:%M:%S.%f')
            t4_time = datetime.strptime(value2[4], '%Y-%m-%d %H:%M:%S.%f')
            t5_time = datetime.strptime(value2[5], '%Y-%m-%d %H:%M:%S.%f')
            a = (s1_time - s0_time).total_seconds() * 1000
            b = (t1_time - t0_time).total_seconds() * 1000
            c = (s3_time - s2_time).total_seconds() * 1000
            d = (t3_time - t2_time).total_seconds() * 1000
            e = (t5_time - t4_time).total_seconds() * 1000
            data_row = [row[0], round(a, 3), round(b, 3), round(c, 3), round(d, 3), round(e, 3), round(a + c, 3),
                        round(b + d + e, 3), row[2]]
            data.append(data_row)
        if data:
            head.extend(data)
        else:
            head = []
        return head


def ng_handover_parsing(file_path):
    dict_ho_source = {}
    dict_ho_target = {}
    for root_dir, dirs, files in os.walk(file_path):
        for file_name in files:
            extension = os.path.splitext(file_name)[-1]
            if extension in ".flow" or extension in ".flw":
                fileurl = os.path.join(root_dir, file_name)
                ho_source = ng_source_gnb(fileurl)
                ho_target = ng_target_gnb(fileurl)
                dict_ho_source.setdefault(file_name, ho_source)
                dict_ho_target.setdefault(file_name, ho_target)
    data = []
    for key1 in dict_ho_source:
        temp_dict = deepcopy(dict_ho_target)
        del temp_dict[key1]
        for key2 in temp_dict:
            row = ng_min_gap(dict_ho_source[key1], temp_dict[key2])
            data.extend(row)
    data_list = ng_delta_time_summary_e2e(data)

    output_url = os.path.join(file_path, "ng_ho_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv")
    write_data_to_csv(data_list, output_url)
    print(output_url)


def xn_handover_parsing(file_path):
    dict_ho_source = {}
    dict_ho_target = {}
    for root_dir, dirs, files in os.walk(file_path):
        for file_name in files:
            extension = os.path.splitext(file_name)[-1]
            if extension in ".flow" or extension in ".flw":
                fileurl = os.path.join(root_dir, file_name)
                ho_source = xn_source_gnb(fileurl)
                ho_target = xn_target_gnb(fileurl)
                dict_ho_source.setdefault(file_name, ho_source)
                dict_ho_target.setdefault(file_name, ho_target)
    data = []

    for key1 in dict_ho_source:
        temp_dict = deepcopy(dict_ho_target)
        del temp_dict[key1]
        for key2 in temp_dict:
            row = xn_min_gap(dict_ho_source[key1], temp_dict[key2])
            data.extend(row)
    data_list = xn_delta_time_summary_e2e(data)

    output_url = os.path.join(file_path, "xn_ho_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv")
    write_data_to_csv(data_list, output_url)
    print(output_url)


if __name__ == '__main__':
    tool_path = os.path.dirname(os.path.abspath(__file__))
    ng_handover_parsing(tool_path)
    xn_handover_parsing(tool_path)
