import os


import base64
from github import Github, InputGitAuthor

from github import InputGitTreeElement

default_configs = {'is_public': True , 'branch': "main",
                   'commit_message': "--sent by github_init--"}

def github_init(name, files, configs = default_configs, ignore_files = []):

    for key in default_configs.keys():
        if key in configs.keys():
            continue
        configs[key] = default_configs[key]

    if isinstance(files[0],str):
        files = get_all_files_from(files)

    import json

    with open("C:\\Users\\user\\PycharmProjects\\github_init\\info.json", 'r') as f:
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
        if file.file_path in ignore_files:
            continue
        element = update_file(branch_to_put, file, repo)
        if element:
            element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)

    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(configs["commit_message"], tree, [parent])
    master_ref.edit(commit.sha)


def update_file(branch_to_put, file, repo):
    if(file.folder_name):
        file.name = file.folder_name +"/"+ file.name

    if file.file_path.endswith('.png'):
        with open(file.file_path, 'rb') as f:
            data = f.read()
            data = base64.b64encode(data).decode()
            sh = repo.create_git_blob(data, "base64").sha
            return InputGitTreeElement(file.name, '100644', 'blob', sha=sh)
    print("creating file : " + file.file_path)
    with open(file.file_path) as f:
        data = f.read()


    return InputGitTreeElement(file.name, '100644', 'blob', data)



def have_branch(name, repo):
    branches = repo.get_branches()
    if branches.totalCount == 0:
        file = File("C:\\Users\\user\\PycharmProjects\\github_init\\empty_file")
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


def inicialize_behaviour(file_paths):
    import json
    for file in file_paths:
        file_name = os.path.basename(file)
        print(file_name)
        if not file_name == 'build_configurations.json':
            continue
        with open(file) as f:
            data = json.loads(f.read())
        build_configurations(file.replace(file_name,''), data)
        return

def build_configurations(dir, data):
    if 'create' in data:
        for file_to_make in data['create']:
            with open(dir + file_to_make['name'], 'w') as f:
                f.write(file_to_make['content'])

def get_all_files_from(file_paths, dir = None):




    all_files = []

    for path in file_paths:
        if os.path.isdir(path):
            nlist = [path + "/" + x for x in os.listdir(path)]

            inicialize_behaviour(nlist)
            path = os.path.basename(path)

            if path == "__pycache__":
                continue
            if dir:
                path = dir + '/' + path
            all_files += get_all_files_from(nlist, path)
            continue

        all_files.append(File(path, dir))

    return all_files


class File:
    file_path: str
    name: str
    folder_name: str


    def __init__(self, file_path, folder_name=None):
        self.file_path = file_path


        name = os.path.basename(file_path)
        self.name = name
        self.folder_name = folder_name