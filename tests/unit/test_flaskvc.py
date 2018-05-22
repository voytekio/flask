from flaskvc import flaskproject
import mock

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
