import requests, json, io, click, yaml, sys

from dash import Dash
from params import Params

def createdashboard(dash, config):
    for service, sdict in dash.getdashobj().items():
        dashobj = getFileJSON('template/template.json')
        dashobj['dashboardMetadata']['name'] = sdict['name']
        post = requests.post('{url}/api/config/v1/dashboards'.format(url = config.geturl()),headers={'Content-Type': 'application/json'},data=json.dumps(dashobj), params=config.getapi())
        id_content = post.json()
        if(post.status_code >= 400):
            print("The API Token in the auth_params.yaml file is incorrect or has improper permissions. Please ensure the correct token is supplied or it has the 'Read configuration' and 'Write configuration' permissions.")
            sys.exit()
        else:
            id_content = post.json()
            dash.setid(id_content['id'], service)

def putdashboard(dash, config):
    final_menu = []
    for service in dash.getdashobj():
        final_menu.append(dash.getmark(service))

    for service in dash.getdashobj():
        dashobj = getFileJSON(dash.getpath(service))
        dashobj['id'] = dash.getid(service)
        dashobj['tiles'].extend(final_menu)
        dashobj = config.setparams(dashobj)
        
        requests.put('{url}/api/config/v1/dashboards/{service}'.format(url = config.geturl(),service = dash.getid(service)),headers={'Content-Type': 'application/json'},data=json.dumps(dashobj), params=config.getapi())

def editmenu(menu, dash, config):
    new_menu = []
    for mark_val in menu:
        mark_val['markdown'] = mark_val['markdown'].replace('{'+'url'+'}',config.geturl())
        new_menu.append(mark_val)

    for service, sdict in dash.getdashobj().items():
        for new_mark in new_menu:
            if '{'+service+'}' in new_mark['markdown']:
                new_mark['markdown'] = new_mark['markdown'].replace('{'+service+'}', sdict['id'])
                dash.setmark(new_mark, service)

def getFileJSON(fileName):
    fileObj = io.open(fileName, mode="r", encoding="utf-8")
    fileJSON = json.loads(fileObj.read())
    fileObj.close()
    return fileJSON

@click.command()
@click.option('--idash', '-d', 
help='''-----------Available Dashbaords-----------\n
    aws : aws Dashboards\n
    k8s : k8s Dashboards\n
    vmware : vmware Dashboards\n
    azure : azure Dashboards\n 
    --------------------------------------\n''')

def main(idash):
    with open('etc/dash_param.yaml') as param_file:
            params = yaml.load(param_file, Loader=yaml.FullLoader)
    if idash in params:
        config = Params()
        dash = Dash(params[idash]['param'])
        createdashboard(dash, config)
        editmenu(getFileJSON(params[idash]['menu']), dash, config)
        putdashboard(dash, config)
    else:
        print('Please provide the correct arguments, for help re-run with --help')

if __name__ == "__main__":
    main()