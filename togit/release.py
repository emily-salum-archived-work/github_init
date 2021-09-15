from togit import github_behaviour

if __name__ == '__main__':

    github_behaviour.github_init('github_init',
                                 ['C:\\Users\\user\\PycharmProjects\\github_init\\togit',
                                  'C:\\Users\\user\\PycharmProjects\\github_init\\empty_file'],
                                 {'commit_message': "committed by-self"},
                                 ['C:\\Users\\user\\PycharmProjects\\github_init\\info.json'])