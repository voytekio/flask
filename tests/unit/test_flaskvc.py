import sys, os
myp = sys.path[0] + '/../../'
sys.path.insert(0, myp)
from flaskvc import flaskproject
from flaskvc import vc_libs
import mock
from mock import patch
#from flaskvc.flaskproject import app


def test_tst():
    assert flaskproject.tst(4) == 5

def test_get_minions():
    assert flaskproject.get_minions() == 'MANUAL_FOR_NOW, minion1, minion2, minion3'

class fakes_weather:
    def __init__(self, status_code=400, text='error'):
        self.status_code = status_code
        self.text = text

    def json(self):
        return {'main':{'temp':51,'humidity':'60'},'weather':[{'main':'drizzle'},{'main':'rain'}],'wind':{'speed':'8'}} 

def test_get_weather_bad():
    test_result_dict = fakes_weather(300)
    res = flaskproject.weather(test_result_dict)
    assert res['Error'] == 'error: error'

def t_get_weather_good():
    test_result_dict = fakes_weather(200)
    res = flaskproject.weather(test_result_dict, 'New York')
    assert res['Temperature'] == 51
    assert res['City'] == 'New York'
    assert res['Weather'] == 'drizzle/rain'

def test_mock_number_of_times_called():
    m = mock.Mock()
    m.status_code = 200
    m.json.return_value = {'main':{'temp':51,'humidity':'60'},'weather':[{'main':'drizzle'},{'main':'rain'}],'wind':{'speed':'8'}}
    res = flaskproject.weather(m)

    assert m.json.call_count == 5
    assert str(m.method_calls[0]) == 'call.json()'
    m.json.assert_called_with() # somewhat redundant to the one above

@patch('flaskvc.flaskproject.render_template')
@patch('flaskvc.vc_libs.get_all_vms')
@patch('flaskvc.vc_libs.connect')
def test_vcenter_with_patch_good(vc_connection_mock, vc_return_mock, render_template_mock):
    flaskproject.args = {'last':'kru2','first':'voy'}
    flaskproject.config_dict = {'last':'kru2','first':'voy'}
    flaskproject.sec_dict  = {'last':'kru2','first':'voy'}

    vc_connection_mock.return_value = None
    vc_return_mock.return_value = {'vms_as_string':'vm1,vm4','vms_as_list':['vm1','vm4']}
    render_template_mock.return_value = 'vm1,vm3'

    res = flaskproject.vcenter()
    assert vc_return_mock.call_count == 0

    vc_connection_mock.return_value = 'successful connection'
    res = flaskproject.vcenter()
    assert vc_return_mock.call_count == 1

