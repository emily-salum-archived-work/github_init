


path = "C:/Users/user/Desktop/emily/projects/@site_projects/portfolio-builder/"

from togit import github_behaviour


init_path = "C:/Users/user/Desktop/emily/projects/@site_projects/portfolio-builder/"
if __name__ == '__main__':

        github_behaviour.github_init('p-teste',
            [init_path + "portfolio_need"],

            {'commit_message': "config_test"})