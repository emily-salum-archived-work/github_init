import os

import base64

# Proposal > An object that receives configuration options can inherit
# OptionControlled.
class OptionControlled:
    def __init__(self, options):

        self.options = options

    def get_option(self, str):
        if not self.options:
            return

        if str in self.options:
            return self.options[str]

    def add_to_options(self, additional_options):

        if not self.options:
            self.options = additional_options
            return

        for k, v in additional_options:
            self.options[k] = v


class Folder(OptionControlled):

    def __init__(self, path, dir=None):
        options = None
        if isinstance(path, dict) and 'options' in path:
            options = path['options']

        super().__init__(options)
        self.path = path

        self.parent:Folder = dir

    def get_file_options(self, file_name):

        file_options = self.get_option("fileOptions")

        if not file_options:
            if self.parent:
                return self.parent.get_file_options(file_name)
            return None

        if file_name not in file_options:
            return None

        return file_options[file_name]

    def get_parent_str(self):

        path_str = self.path

        if isinstance(path_str, dict):
            path_str = self.path['str']

        return os.path.dirname(path_str)


    def get_dir_path(self):

        dir_str = self.path

        if self.get_option("extract"):
            dir_str = ""

        if isinstance(dir_str, dict):
            dir_str = os.path.basename(self.path['str'])
            if 'replace' in self.path:
                dir_str = self.path['replace']
        elif dir_str:
            dir_str = os.path.basename(dir_str)

        if self.parent:

            parent_dir_path = self.parent.get_dir_path()
            if parent_dir_path:
                dir_str = parent_dir_path + "/" + dir_str

        return dir_str


def read_as_binary(path) -> bool:

    types_to_open_rb = ["png", "jpg", "pdf"]

    for type in types_to_open_rb:
        if path.endswith(f".{type}"):
            return True

    return False

class File(OptionControlled):
    file_info: dict
    folder: Folder
    file_path: str
    name: str
    folder_name: str


    # Gets file data
    def get_data(self):

        open_rb = read_as_binary(self.file_path)

        if open_rb:
            with open(self.file_path, 'rb') as f:
                data = f.read()
                return "rb", base64.b64encode(data).decode()

        with open(self.file_path, encoding="utf-8") as f:
            data = f.read()

        data = self.transform_data(data)

        return "r", data

    # Uses option configurations to modify the file information
    def transform_data(self, data):
        replace_options = self.get_option('replace')
        print(f"replace options : {replace_options}")
        if replace_options:
            for to_find, to_replace in replace_options.items():
                data = data.replace(to_find, to_replace)

        return data

    # Gets full file name, based on all parents
    def get_file_name(self):

        file_path = self.name

        if self.file_info:
            if 'rename' in self.file_info:
                file_path = self.file_info['rename']

        if self.folder:
            dir_path = self.folder.get_dir_path()

            if dir_path:
                file_path = dir_path + "/" + file_path

        print(f"Returning file path {file_path}")
        return file_path


    def __init__(self, path, folder=None):

        self.file_info = None
        self.folder_info = None

        self.folder = None
        file_path = path
        options = None

        if isinstance(path, dict):
            self.file_info = path

            if 'options' in path:
                options = path['options']

            file_path = path['str']

        super().__init__(options)
        self.file_path = file_path
        name = os.path.basename(file_path)

        self.name = name

        folder_name = folder

        if folder and not isinstance(folder, str):
            self.folder = folder

            folder_file_options = self.folder.get_file_options(self.name)
            self.add_to_options(folder_file_options)

        self.folder_name = folder_name