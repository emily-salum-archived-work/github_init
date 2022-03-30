import os




def build_configurations(dir, data):
    from togit.github_behaviour import replacements
    if 'create' in data:
        for file_to_make in data['create']:
            with open(dir + file_to_make['name'], 'w') as f:
                f.write(file_to_make['content'])
    if 'replace' in data:
        for replacer in data['replace']:
            replacements.append({'name':replacer['name']
                                 , 'content': replacer['content'].replace("'", '"')})


def inicialize_behaviour(file_paths):
    import json
    for file in file_paths:
        file_name = os.path.basename(file)
        print(file_name)
        if not file_name == 'build_configurations.json':
            continue
        with open(file) as f:
            data = json.loads(f.read())
        build_configurations(file.replace(file_name, ''), data)
        return