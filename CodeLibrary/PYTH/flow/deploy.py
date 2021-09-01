#!python3
import json
import os
import subprocess

if __name__ == '__main__':
    tool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(tool_path, "config")
    config_file = os.path.join(config_path, "config.json")
    v = str(os.path.dirname(subprocess.check_output('which mobatch', shell=True).strip()), encoding='utf-8')
    d = {'moshell_path': v}
    js = json.dumps(d, indent=4)
    print(js)
    with open(config_file, "w") as f:
        f.write(js)
