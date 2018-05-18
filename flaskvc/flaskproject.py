from __future__ import print_function
from flask import Flask, render_template, url_for
import pdb
import argparse
import json
import requests

app = Flask(__name__)

def setup_args():
    """
    Get standard connection arguments
    """
    #parser = cli.build_arg_parser()
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--user", help="username", action = 'store')
    parser.add_argument("-s", "--host", help="VC or ESX name", action = 'store')
    parser.add_argument("-p", "--password", help="password, leave blank for prompt", action = 'store')
    parser.add_argument("-o", "--port", help="port, defaults to 443", action = 'store', default="443")

    args = parser.parse_args()
    return args

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/salt')
def salt():
    return render_template('salt.html', vms_as_string=get_minions())

@app.route('/chef')
def chef():
    return render_template('chef.html')

@app.route('/weather')
def weather(force_result = None, force_city_name = None):
    #print('force_res: {0}, f_city: {1}'.format(force_result.status_code, force_city_name))
    if force_result:
        #config_dict = {}
        cityname = force_city_name
    else:
        # lots of repetition here, need to refactor
        api_header = config_dict.get('weather',{}).get('api_header','missing_api_header')
        cityname = config_dict.get('weather',{}).get('cityname','missing_city_name')
        unit = config_dict.get('weather',{}).get('unit','missing_unit')
        weather_api_key = config_dict.get('secs',{}).get('openweather_api_key','missing_api_key')
        full_api_url = api_header + cityname + '&mode=json&units=' + unit + '&APPID=' + weather_api_key 
        print('URL: {0}'.format(full_api_url))
    if force_result:
        req_result = force_result
    else:
        req_result = requests.get(full_api_url)
    if req_result.status_code == 200:
        weather_result = req_result.json().get('main',{}).get('temp','temperature-error')
        weather_result = cityname + ': ' + str(weather_result)
    else:
        #error_text = req_result.json().get('message','unable to get error details')
        error_text = req_result.text
        weather_result = 'error: ' + error_text
    #print('weather: {0}'.format(weather_result))
    if force_result:
        return weather_result
    else:
        return render_template('weather.html', weather_result = weather_result)

@app.route('/vcenter')
def vcenter():
    import vc_libs
    vc_connect_object = vc_libs.connect(args, config_dict)
    if vc_connect_object:
        vmlist = vc_libs.get_all_vms(vc_connect_object)
        #may need to string this into one string
        vms_as_string = vmlist
    else:
        vms_as_string = "error accessing VC info"
    print('VMs: {0}'.format(vms_as_string))
    return render_template('vcenter.html', vms_as_string=vms_as_string)

def tst(some_number):
    print('inside tst func')
    return some_number + 1

def get_minions():
    #pdb.set_trace()
    vm_names = ['MANUAL_FOR_NOW', 'minion1','minion2','minion3']
    vmdetails = [{'name':'minion1','power':'on'},{'name':'minion2','power':'on'}]
    vms_as_string = ''
    for one_vm in vm_names:
        print(one_vm)
        if vms_as_string:
            vms_as_string = vms_as_string + ", " + one_vm
        else:
            vms_as_string = one_vm
    
    return vms_as_string

if __name__ == '__main__':
    args = setup_args()
    with open('flaskproject.cfg') as f:
        config_dict = json.load(f)

    app.run(host = '0.0.0.0')
