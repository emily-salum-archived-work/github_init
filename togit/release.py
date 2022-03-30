from togit import github_behaviour


init_path = "C:\\Users\\user\\Desktop\\emily\projects\\@python_projects\\@Automation\\github_init\\"
if __name__ == '__main__':

        github_behaviour.github_init('github_init',
            ["../welcome.txt",
            { "str": init_path + 'togit' },

             {  "str": init_path + "test-folder" }],

            {'commit_message': "config_test", "ignore_files": [
              init_path + "togit/info.json"
            ]})