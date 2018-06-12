'''
Main flask project module.
Currently all in one - accepts arguments, routes urls, runs the flask app and renders templates.
usage: python flaskproject.py --help
'''
from __future__ import print_function
import os
import sys
import pdb
import argparse
import json
import requests
import time

from flask import Flask, render_template, url_for
from salt_api_wrapper import get_rest_request, salt_api

app = Flask(__name__)

def setup_args():
    """
    Get standard connection arguments
    """
    #parser = cli.build_arg_parser()
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--user", help="username", action='store')
    parser.add_argument("-s", "--host", help="VC or ESX name", action='store')
    parser.add_argument("-p", "--password", help="password, leave blank for prompt", action='store')
    parser.add_argument("-o", "--port", help="port, defaults to 443", action='store', default="443")

    args = parser.parse_args()
    return args

@app.route('/')
@app.route('/index')
def index():
    'default web page route'
    return render_template('index.html')

@app.route('/salt')
def salt():
    'route func for /salt endpoint. Prints Salt stuff'
    salt_hostname = str(sec_dict.get('salt_config', {}).get('salt_hostname', 'missing_salt_hostname'))
    salt_api_port = str(sec_dict.get('salt_config', {}).get('salt_api_port', 'missing_salt_port'))
    salt_api_service_username  = str(sec_dict.get('salt_config', {}).get('salt_api_service_username', 'missing_salt_api_service_username'))
    salt_api_pass = str(sec_dict.get('secs', {}).get('salt_api_service_pass', 'missing_salt_pass'))

    full_server_url = 'https://'+salt_hostname+':'+salt_api_port
    salt_object = salt_api(full_server_url, salt_api_service_username, salt_api_pass)
    salt_minions_up = sorted(salt_object.get_minions('up'))
    salt_minions_down = sorted(salt_object.get_minions('down'))

    return render_template('salt.html', salt_minions_up=salt_minions_up, salt_minions_down=salt_minions_down)

@app.route('/chef')
def chef():
    'route func for /chef endpoint. Prints Chef stuff'
    return render_template('chef.html')

@app.route('/weather')
def weather(force_result=None, force_city_name=None):
    'route func for /weather endpoint. Prints weather information.'
    #print('force_res: {0}, f_city: {1}'.format(force_result.status_code, force_city_name))
    weather_result = {}
    if force_result:
        #config_dict = {}
        weather_result['City'] = force_city_name
    else:
        # lots of repetition here, need to refactor
        api_header = config_dict.get('weather', {}).get('api_header', 'missing_api_header')
        cityname = config_dict.get('weather', {}).get('cityname', 'missing_city_name')
        unit = config_dict.get('weather', {}).get('unit', 'missing_unit')
        weather_api_key = sec_dict.get('secs', {}).get('openweather_api_key', 'missing_api_key')
        full_api_url = api_header + cityname + '&mode=json&units=' + unit + '&APPID=' + weather_api_key
        print('URL: {0}'.format(full_api_url))

        weather_result['City'] = cityname
    if force_result:
        req_result = force_result
    else:
        req_result = requests.get(full_api_url)
    if req_result.status_code == 200:
        weather_result['Temperature'] = req_result.json().get('main', {}).get('temp', 'temperature-error')
        weather_result['Clouds'] = req_result.json().get('clouds', 'clouds-error')
        weather_result['Wind'] = req_result.json().get('wind', {}).get('speed', 'wind-error')
        weather_tags = ''
        for one_full_tag in req_result.json().get('weather', 'weather-error'):
            if weather_tags:
                weather_tags += '/'
            weather_tags += one_full_tag.get('main')
        weather_result['Weather'] = weather_tags
        weather_result['Humidity'] = req_result.json().get('main', {}).get('humidity', 'humidity-error')
    else:
        error_text = req_result.text
        weather_result['Error'] = 'error: ' + str(error_text)
    print('weather: {0}'.format(weather_result))
    if force_result:
        return weather_result
    else:
        return render_template('weather.html', weather_result=weather_result)

@app.route('/vcenter')
def vcenter():
    'route func for /vcenter endpoint. Shows vCenter related information.'
    import vc_libs
    vm_return = {}
    vc_connect_object = vc_libs.connect(args, config_dict, sec_dict)
    if vc_connect_object:
        vm_return = vc_libs.get_all_vms(vc_connect_object)
    else:
        vm_return['vms_as_string'] = 'ERROR: exception while accessing VC info.'
    print('VMs: {0}'.format(vm_return['vms_as_string']))
    return render_template('vcenter.html', vms_as_string=vm_return.get('vms_as_string', 'no_vms'), vms_as_list=sorted(vm_return.get('vms_as_list', 'no_vms')))

def tst(some_number):
    'test func, not used'
    print('inside tst func')
    return some_number + 1


if __name__ == '__main__':
    args = setup_args()
    with open('flaskproject.cfg') as f:
        config_dict = json.load(f)
    with open('flaskproject.sec') as sec:
        sec_dict = json.load(sec)

    app.run(host='0.0.0.0')
