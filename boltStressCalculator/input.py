import yaml

def loadYML(path):

    try:
        with open(path) as f:
            data = yaml.load(f, Loader = yaml.FullLoader)
            return data
    except:
        print('YML does not work')

def parseYML(path):

    data = loadYML(path)
    
    if 'files' in data:
        queue = True
        if validateYML(data,queue):
            jobs = []
            for case in data['files']:
                data = loadYML(case)
                if validateYML(data):
                    jobs.append(data)
                else:
                    raise Exception(f'check YML file {case}')
            return jobs
        else:
            raise Exception('the queue file is broken')
    else:
        if validateYML(data):
            return [data]
        else:
            raise Exception('the yml file is wrong')

def validateYML(data,queue = False):

    return True