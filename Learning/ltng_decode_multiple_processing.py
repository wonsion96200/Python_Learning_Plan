# auto decode raw files to .dec & .flow files #

import os
from multiprocessing import Process
import subprocess


def ltng_decode(raw_file):
    decoder_cmd = "%s/bin/ltng-decoder -f %s > %s.dec" % (ltng_path, raw_file, os.path.splitext(raw_file)[0])
    flow_cmd = "%s/bin/ltng-flow -f %s > %s.flow" % (ltng_path, raw_file, os.path.splitext(raw_file)[0])
    zip_raw_cmd = "zip %s.zip %s" % (raw_file, raw_file)
    zip_dec_cmd = "zip %s.dec.zip %s.dec" % (os.path.splitext(raw_file)[0], os.path.splitext(raw_file)[0])
    zip_flow_cmd = "zip %s.flow.zip %s.flow" % (os.path.splitext(raw_file)[0], os.path.splitext(raw_file)[0])
    print(decoder_cmd)
    # subprocess.run(decoder_cmd, shell=True)
    os.system(decoder_cmd)
    print(flow_cmd)
    # subprocess.run(flow_cmd, shell=True)
    os.system(flow_cmd)
    print(zip_raw_cmd)
    # subprocess.run(zip_raw_cmd, shell=True)
    os.system(zip_raw_cmd)
    print(zip_dec_cmd)
    # subprocess.run(zip_dec_cmd, shell=True)
    os.system(zip_dec_cmd)
    print(zip_flow_cmd)
    # subprocess.run(zip_flow_cmd, shell=True)
    os.system(zip_flow_cmd)


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    # ltng_path = input("Please input the path of ltng (e.g. '/home/shared/Szeric/5GSA/ltng'): ")
    ltng_path = "/home/shared/Szeric/5GSA/ltng"
    # print(os.walk(current_path))
    loop = 1
    # total = subprocess.getoutput("ls *.raw | wc -l")
    total = os.popen("ls *.raw | wc -l").read()
    # print(total)
    for root_dir, dirs, files in os.walk(current_path):
        # print(files)
        for file in files:
            # print(file)
            # print(os.path.splitext(file)[1])
            if "raw" in os.path.splitext(file)[1]:
                # ltng_decode(file)
                p = Process(target=ltng_decode, args=(file,))
                p.start()
