from togit.github_behaviour import github_init, get_all_files_from
import sys
sys.path.append("..")
from builder_helper import builder_help

project = builder_help.get_latest_project()

name = project['name']
project_path = project['Project Path']

github_init(name, get_all_files_from([project_path]
                                   ), False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
