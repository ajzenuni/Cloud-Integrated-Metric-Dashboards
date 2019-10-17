import requests, json, io, click, yaml

from dash import Dash
from params import Params

def createdashboard():
    global dash, config
    for service, sdict in dash.getdashobj().items():
        dashobj = getFileJSON('template/template.json')
        dashobj['dashboardMetadata']['name'] = sdict['name']
        post = requests.post(config.geturl() + '/api/config/v1/dashboards',headers={'Content-Type': 'application/json'},data=json.dumps(dashobj), params=config.getapi())
        id_content = post.json()
        dash.setid(id_content['id'], service)

def putdashboard():
    global dash, config
    final_menu = []
    for service in dash.getdashobj():
        final_menu.append(dash.getmark(service))

    for service in dash.getdashobj():
        dashobj = getFileJSON(dash.getpath(service))
        dashobj['id'] = dash.getid(service)
        dashobj['tiles'].extend(final_menu)
        dashobj = config.setparams(dashobj)
        
        requests.put(config.geturl() + '/api/config/v1/dashboards/'+dash.getid(service),headers={'Content-Type': 'application/json'},data=json.dumps(dashobj), params=config.getapi())

def editmenu(menu):
    global dash, config
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
help='''-----------Available Scripts-----------\n
    -n awS : aws Dashboards\n
    -n k8s : k8s Dashboards\n
    -n vmware : vmware Dashboards\n
    -n azure : azure Dashboards\n 
    --------------------------------------\n''')

def main(idash):
    global dash, config
    with open('etc/dash_param.yaml') as param_file:
            params = yaml.load(param_file, Loader=yaml.FullLoader)
    if idash in params:
        config = Params()
        dash = Dash(params[idash]['param'])
        createdashboard()
        editmenu(getFileJSON(params[idash]['menu']))
        putdashboard()
    else:
        print('Please provide the correct arguments, for help re-run with --help')

if __name__ == "__main__":
    main()