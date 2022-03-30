import os


import base64
from github import Github, InputGitAuthor

from github import InputGitTreeElement

from togit.build_configurations import inicialize_behaviour
from togit.structure_classes import Folder, File

default_configs = {'is_public': True, 'branch': "main",
                   'commit_message': "--sent by github_init--",
                   "ignore_files": []}

replacements = []

def github_init(name, files, configs = default_configs):

    for key in default_configs.keys():
        if key in configs.keys():
            continue
        configs[key] = default_configs[key]

    if not isinstance(files[0], File):
        files = get_all_files_from(files)

    import json

    with open("C:\\Users\\user\\Desktop\\emily\\projects\\@python_projects\\@Automation\\github_init\\togit\\info.json", 'r') as f:
        data = json.loads(f.read())

    g = Github(data["github_key"])
    author = InputGitAuthor(
        data["name"],
        data["email"]
    )

    user = g.get_user()

    repo = have_repository(name, user, configs['is_public'])

    branch_to_put = configs['branch']
    branch = have_branch(branch_to_put, repo)
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = list()

    for file in files:
        if file.file_path in default_configs["ignore_files"]:
            continue
        element = update_file(branch_to_put, file, repo)
        if element:
            element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)

    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(configs["commit_message"], tree, [parent])
    master_ref.edit(commit.sha)


def update_file(branch_to_put, file, repo):

    file_name = file.get_file_name()

    for r in replacements:
        if r['name'] == file.name:
            return InputGitTreeElement(file_name, '100644', 'blob', r["content"])




    type, data = file.get_data()

    if type == "rb":

        sh = repo.create_git_blob(data, "base64").sha
        return InputGitTreeElement(file_name, '100644', 'blob', sha=sh)

  
    return InputGitTreeElement(file_name, '100644', 'blob', data)



def have_branch(name, repo):
    branches = repo.get_branches()
    if branches.totalCount == 0:
        file = File("C:\\Users\\user\\Desktop\\emily\projects\\@python_projects\\@Automation\\github_init\\empty_file")
        with open(file.file_path) as f:
            data = f.read()
        repo.create_file(file.name, "test", data, branch="main")


    try:
        branch = repo.get_branch(name)
    except:
        branch = repo.create_git_ref(ref='refs/heads/'+name,sha=branches[0].commit.sha)
    return branch


def have_repository(name, user, is_public = True):
    try:
        repo = user.get_repo(name)
    except:
        repo = user.create_repo(name, private=not is_public)

    return repo


# Receives:
    # file_paths -> a list of paths (str or dict)
    # files_dir -> a Folder object, parent of the paths passed
# Based on a path, will walk through it and
# check if its a file. If it is, creates a file object for it.
# If its a folder...
    # 1- Creates File objects for every child file of the folder
    # 2- Looks for a "build_configurations.json" file in the folder
    # 3- Create Folder objects for every child folder
    # 4- For every Folder, calls this function again. Go back to step 1!
def get_all_files_from(file_paths, files_dir:Folder=None):

    all_files = []

    for path in file_paths:

        path_str = path
        if isinstance(path, dict):
            path_str = path['str']


        if os.path.isdir(path_str):

            new_folder = Folder(path, files_dir)

            nlist = [path_str + "/" + x for x in os.listdir(path_str)]
            inicialize_behaviour(nlist)
            # nlist = [path_str + "/" + x for x in os.listdir(path_str)]

            base_path_str = os.path.basename(path_str)

            # Default folders that the system doesnt commit
            if base_path_str in ["__pycache__", 'node_modules']:
                continue

            all_files += get_all_files_from(nlist, new_folder)
            continue

        all_files.append(File(path, files_dir))

    return all_files


