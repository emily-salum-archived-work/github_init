from togit import github_behaviour


init_path = "C:\\Users\\user\\Desktop\\emily\projects\\@python_projects\\@Automation\\github_init\\"
if __name__ == '__main__':

        github_behaviour.github_init('github_init',
            [init_path + 'togit',
             {"str": init_path + 'empty_file', "replace":  "empty_test"},
             {"str": init_path + "test-folder", "replace": "folder-test"}],

            {'commit_message': "config_test"},
            [init_path + 'info.json'])