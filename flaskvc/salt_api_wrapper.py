'''
Salt api module that allows to query Salt API via requests library. 
usage: n/a
'''
from __future__ import print_function
import os
import sys
import requests
import time
import pdb

class salt_api():
    '''
    salt_api objects
    should contain attribs: token, minion_status_dict
    should contain methods: get_token, get_minion_status
    '''
    def __init__(self, full_server_url, salt_api_service_username, salt_api_pass):
        self.full_server_url = full_server_url
        self.salt_api_service_username = salt_api_service_username
        self.salt_api_pass = salt_api_pass
        self.token = ''
        self.minion_status_dict = {}

    def get_token(self):
        if self.token:
            print('Token already present; reusing')
        else:
            print('Obtaining token from api')
            self.token = get_rest_request(self.full_server_url, request_type='login', header={'Accept':'application/json'}, header_data_dict={'username':self.salt_api_service_username,'password':self.salt_api_pass,'eauth':'pam'}, verify_ssl=False)
        return

    def get_minion_status(self):
        self.get_token()
        if self.minion_status_dict:
            print('minion status list already present')
            return
        else:
            print('need to obtain minion status list')

            if self.token:
                jid_structure = get_rest_request(self.full_server_url, request_type=None, header={'Accept':'application/json','X-Auth-Token':self.token}, header_data_dict={'client':'runner_async', 'fun':'manage.status'}, verify_ssl=False)

            if jid_structure:
                job_url = str(jid_structure.get('return')[0].get('jid'))
                #job_url = str(jid_structure.get('_links').get('jobs')[0].get('href'))
                job_url = 'jobs/' + job_url

                while True:
                    print('Sleeping')
                    time.sleep(3)
                    jobs_data = get_rest_request(self.full_server_url, request_type=job_url, header={'Accept':'application/json','X-Auth-Token':self.token}, header_data_dict={}, verify_ssl=False)
                    return_list = jobs_data.get('return')[0]
                    if len(return_list) > 0:
                        break
                
                print('Return_list: {0}'.format(return_list))
                self.minion_status_dict = return_list
                return 
            return 'token missing or jid get error.'

    def get_minions(self, up_or_down = 'up'):
        self.get_minion_status()
        for onek,onev in self.minion_status_dict.iteritems():
            print('one dict iteration')
            print('{0}: {1}'.format(onek,onev))
            for one in onev.get('return').get(up_or_down):
                print(one)
            return onev.get('return').get(up_or_down)

    def __str__(self):
        return 'salt_api object. Minions considered up: {0}'.format(self.get_minions())


def get_rest_request(server, request_type, header, header_data_dict, verify_ssl):
    print('ENTERING GET REQUEST FUNC')
    #pdb.set_trace()
    server_url = (server + '/' + request_type) if request_type else server
    print('server_url: {0}'.format(server_url))
    request_type = request_type if request_type else 'foo'
    print('headers: {0}'.format(header))
    #print('header_data: {0}'.format(header_data_dict))
    if 'job' in request_type:
        rr = requests.get(server_url, headers=header, data=header_data_dict, verify=verify_ssl)
    else:
        rr = requests.post(server_url, headers=header, data=header_data_dict, verify=verify_ssl)
    if rr.status_code >= 400:
        print('non ok status returned from http query')
        print('details: {0}:{1}'.format(rr.status_code, rr.text))
        return 1
    print('{0}: Success http return'.format(rr.status_code)) 
    print('URL is: {0}'.format(rr.url))
    if 'login' in request_type:
        res_header = rr.headers.get('Set-Cookie')
        try:
            auth_token = res_header.split(';')[0].split('=')[1]
        except IndexError:
            print('index error while extracting token.')
            return False
        print('auth token: {0}'.format(auth_token))
        return auth_token
    print(rr.json())
    return rr.json()

def main():
    print('hello world from salt main')

if __name__ == '__main__':
    main()
