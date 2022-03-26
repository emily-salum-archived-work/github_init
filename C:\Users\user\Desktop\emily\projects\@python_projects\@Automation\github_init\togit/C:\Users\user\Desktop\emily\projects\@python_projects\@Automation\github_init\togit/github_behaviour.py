import os


import base64
from github import Github, InputGitAuthor

from github import InputGitTreeElement

default_configs = {'is_public': True , 'branch': "main",
                   'commit_message': "--sent by github_init--"}

replacements = []

def github_init(name, files, configs = default_configs, ignore_files = []):

    for key in default_configs.keys():
        if key in configs.keys():
            continue
        configs[key] = default_configs[key]

    if isinstance(files[0], str):
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

    file_name = file.get_file_name()

    for r in replacements:
        if r['name'] == file.name:
            return InputGitTreeElement(file_name, '100644', 'blob', r["content"])


    if file.file_path.endswith('.png') or file.file_path.endswith('.jpg'):
        with open(file.file_path, 'rb') as f:
            data = f.read()
            data = base64.b64encode(data).decode()
            sh = repo.create_git_blob(data, "base64").sha
            return InputGitTreeElement(file_name, '100644', 'blob', sha=sh)
    print("creating file : " + file.file_path)

    with open(file.file_path, encoding="utf-8") as f:
        data = f.read()


    return InputGitTreeElement(file_name, '100644', 'blob', data)



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
    if 'replace' in data:
        for replacer in data['replace']:
            replacements.append({'name':replacer['name']
                                 , 'content': replacer['content'].replace("'", '"')})


def get_all_files_from(file_paths, dir = None):




    all_files = []

    for path in file_paths:

        path_str = path
        if isinstance(path, dict):
            path_str = path['str']


        if os.path.isdir(path_str):
            nlist = [path_str + "/" + x for x in os.listdir(path_str)]
            inicialize_behaviour(nlist)
            nlist = [path_str + "/" + x for x in os.listdir(path_str)]
            path_str = os.path.basename(path_str)

            if path_str == "__pycache__":
                continue

            if dir:
                if isinstance(dir, str):
                    path_str = dir + '/' + path_str
                else:
                    path_str = dir['str'] + '/' + path_str

            if isinstance(path, dict):
                path['str'] = path_str
            all_files += get_all_files_from(nlist, path)
            continue

        all_files.append(File(path, dir))

    return all_files


class File:
    file_info: dict
    folder_info: dict
    file_path: str
    name: str
    folder_name: str


    def get_file_name(self):

        file_path = self.file_path

        folder_name = None
        if (self.folder_name):
            folder_name = self.folder_name

        if self.file_info:
            if 'replace' in self.file_info:
                file_path = self.file_info['replace']

        if self.folder_info:
            if 'replace' in self.folder_info:
                folder_name = self.folder_info['replace']

        if folder_name:
            file_path = folder_name + "/" + file_path

        print(f"Returning file path {file_path}")
        return file_path


    def __init__(self, path, folder=None):

        self.file_info = None
        self.folder_info = None
        file_path = path

        if isinstance(path, dict):
            self.file_info = path

            file_path = path['str']

        self.file_path = file_path
        name = os.path.basename(file_path)

        self.name = name

        folder_name = folder

        if isinstance(folder, dict):
            self.folder_info = folder
            folder_name = folder['str']

        self.folder_name = folder_name
