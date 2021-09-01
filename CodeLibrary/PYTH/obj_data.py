#!python3
# -*- coding: utf-8 -*-
import csv
import os


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


def append_data_to_csv(data, csv_file=""):
    """
    append the data list to the csv file(csv_file shall be exist)
    :param data:list
    :param csv_file:str
    :return:
    """
    if data:
        with open(os.path.join(csv_file), "a+", encoding='utf-8-sig', newline='') as csvfile:  #
            writer = csv.writer(csvfile, dialect="excel")
            writer.writerows(data)
    return csv_file


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


def get_dict_key(data_row, key_cols=None):
    """
    get the dictionary key, if key_cols is None return data[0]
    :param data_row: list
    :param key_cols: list
    :return: key
    """
    key = ""
    if not key_cols:
        key = data_row[0]  # default key_cols is 0
    else:
        for j in key_cols:
            key = key + data_row[j]
    return key


def get_dict_values(data_row, value_cols=None):
    """
    get the dictionary value, if value_cols is None return data_row
    :param data_row: list
    :param value_cols: list
    :return: values
    """
    values = []
    if not value_cols:
        values = data_row
    else:
        for j in value_cols:
            values.append(data_row[j])
    return values


def make_data_to_dict(data, key_cols=None, value_cols=None):
    """
    make a dictionary value with the data
    key_cols(the columns of data) as the keys, value_cols as the data values
    if key_cols is none, the 0 column will be used as the key
    if value_cols is none, all data will be the data values
    :param data: list
    :param key_cols: list
    :param value_cols: list
    :return:the_dict
    """
    the_dict = {}  # make a empty dictionary
    for row in data:
        # get the key
        key = get_dict_key(row, key_cols)
        # get the values
        values = get_dict_values(row, value_cols)
        # append to dict
        the_dict.setdefault(key, []).extend(values)  # update the dictionary
    return the_dict


def vlookup(src_data, look_data, indexs_look_src=None, indexs_look_in=None, indexs_look_out=None):
    """
    similar vlookup in Excel
    :param src_data:list
    :param look_data:list
    :param indexs_look_src:list
    :param indexs_look_in:list
    :param indexs_look_out:list
    :return: merge_data
    """
    # get the number of column in indexs_look_out
    # if indexs_look_out is none, get number of column in look_data
    if indexs_look_out:
        len_indexs_look_out = len(indexs_look_out)
    else:
        len_indexs_look_out = len(look_data[0])

    look_dict = make_data_to_dict(look_data, indexs_look_in, indexs_look_out)
    data = []
    for row_src in src_data:
        # get the key
        key = get_dict_key(row_src, indexs_look_src)
        look_values = []
        # get look_values
        if key in look_dict:
            look_values = look_dict[key]
        else:
            # append "" if the key not in dict
            j = 0
            while j < len_indexs_look_out:
                look_values.append("")
                j += 1
        # look_values extend to row
        row_src.extend(look_values)
        # row_src extend to data
        data.append(row_src)
    return data


if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # file_name = os.path.join(base_path, "test.csv")
    #
    # csv_data = [["a", "b", "c"], [1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # write_data_to_csv(csv_data, file_name)
    # csv_data = read_csv_to_data(file_name)
    # print(csv_data)
    data_nrfrequency = read_csv_to_data(os.path.join(base_path, "record_NRFrequency.csv"))
    data_nrfreqrelation = read_csv_to_data(os.path.join(base_path, "record_NRFreqRelation.csv"))
    data_nrfreqrelation = vlookup(data_nrfreqrelation, data_nrfrequency, [0, 2], [0, 1])
    write_data_to_csv(data_nrfreqrelation, os.path.join(base_path, "new_record_NRFreqRelation.csv"))
