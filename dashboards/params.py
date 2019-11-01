import yaml, sys

class Params:
    def __init__(self):
        with open('etc/auth_param.yaml') as param_file:
            self.param_obj = yaml.load(param_file, Loader=yaml.FullLoader)
    
    def geturl(self):
        if(self.param_obj['auth'][0]['url'].endswith("/")):
            print('Incorrect Inputs: The tenant URL in the auth_params.yaml file. Remove this and try again')
            sys.exit()
        else:
            return self.param_obj['auth'][0]['url']

    def getapi(self):
        self.param = {'Api-Token': self.param_obj['auth'][0]['api']}
        return self.param

    def setparams(self, dashobj):
        dashobj['dashboardMetadata']['owner'] = self.param_obj['dashboard_config']['owner']
        dashobj['dashboardMetadata']['shared'] = self.param_obj['dashboard_config']['shared']['val']
        dashobj['dashboardMetadata']['sharingDetails']['linkShared'] = self.param_obj['dashboard_config']['shared']['linkShared']
        dashobj['dashboardMetadata']['sharingDetails']['published'] = self.param_obj['dashboard_config']['shared']['published']
        return dashobj
    
