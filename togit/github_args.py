import sys
import json

from togit import github_behaviour

if __name__ == '__main__':
    name = sys.argv[1]
    update_paths = json.loads(sys.argv[2])["paths"]
    is_public = sys.argv[3] == "true"

    file_paths = github_behaviour.get_all_files_from(update_paths)

    github_behaviour.github_init(name, file_paths, is_public)