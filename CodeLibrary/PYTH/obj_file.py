#!python2
# coding=utf-8
import datetime
import glob
import os
import shutil

"""
common function for file and dirs 
"""


def copy_file_list(list_path="", dir_dst=""):
    """
    copy the file list to report_path
    :param dir_dst:
    :param list_path:
    :return:
    """
    if os.path.isfile(list_path):
        file_lists = [x.strip() for x in open(list_path, 'r').readlines()]
        for file_src in file_lists:
            copy_file(file_src, dir_dst)


def cleanup_dir(dir_name):
    rm_dirs(dir_name)
    mkdir(dir_name)


def rm_dirs(dir_name=None):
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)
        print("rm -r %s" % dir_name)


def mkdir(dir_name=""):
    os.makedirs(dir_name, exist_ok=True)
    print("mkdir %s" % dir_name)


def copy_file(file_src="", dir_dst=""):
    os.makedirs(dir_dst, exist_ok=True)
    if os.path.exists(file_src):
        shutil.copy(file_src, dir_dst)
        print("cp -f %s %s" % (file_src, dir_dst))


def file_created_days(file_name=None):
    """
    check the file create days
    :param file_name:
    :return days(file create days)
    """
    if not os.path.exists(file_name):
        days = 0
    else:
        now = datetime.datetime.now()
        file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_name))
        days = (now - file_time).days
    return days


def get_filepath_filename_fileext(fileurl):
    """
    get file path, file name and file extension
    :param fileurl:
     :return:filepath, shot_name, extension
     """
    filepath, tmp_filename = os.path.split(fileurl)
    shot_name, extension = os.path.splitext(tmp_filename)
    return filepath, shot_name, extension


def file_number(fileurl):
    """
    get file number
    :param fileurl:
     :return: number of exist files
     """
    path_file_number = glob.glob(fileurl)
    return path_file_number


if __name__ == '__main__':
    mkdir("/home/ejungwa/hcTool3/report")
