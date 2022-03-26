from togit import github_behaviour


init_path = "C:\\Users\\user\\Desktop\\emily\projects\\@python_projects\\@Automation\\github_init\\"
if __name__ == '__main__':

        github_behaviour.github_init('github_init',
            [init_path + 'togit',
            init_path + 'empty_file'],
            {'commit_message': "config_test"},
            [init_path + 'info.json'])