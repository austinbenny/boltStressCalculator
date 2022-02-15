import yaml

def parseYML(path):

    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    
    if validateYML(data):
        return data
    else:
        raise Exception('check YML file')

def validateYML(data):

    return True