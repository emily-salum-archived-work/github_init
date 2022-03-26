import sys
import json


import os

dir_path = os.path.dirname(__file__)
os.chdir(dir_path)

sys.path.append("..")
sys.path.append(".")
import github_behaviour

if __name__ == '__main__':
    name = sys.argv[1]

    update_paths = json.loads(sys.argv[2])["paths"]


    is_public = sys.argv[3] == "true"

    file_paths = github_behaviour.get_all_files_from(update_paths)

    configs = {'is_public': is_public}
    github_behaviour.github_init(name, file_paths, configs)