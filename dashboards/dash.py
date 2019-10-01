import yaml

class Dash:
    def __init__(self, dash_param):
        with open(dash_param) as param_file:
            self.dash_obj = yaml.load(param_file, Loader=yaml.FullLoader)

    def getpath(self, service):
        return self.dash_obj[service]['path']

    def setid(self, id, service):
        self.dash_obj[service]['id'] = id
    
    def getid(self, service):
        return self.dash_obj[service]['id']
    
    def setmark(self, new_mark, service):
        self.dash_obj[service]['mark'] = new_mark
    
    def getmark(self, service):
        return self.dash_obj[service]['mark']
    
    def getdashobj(self):
        return self.dash_obj
    
    def printdashobj(self):
        print(self.dash_obj)