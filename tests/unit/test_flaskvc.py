from flaskvc import flaskproject

def test_tst():
    assert flaskproject.tst(4) == 5

def test_get_minions():
    assert flaskproject.get_minions() == 'MANUAL_FOR_NOW, minion1, minion2, minion3'

class fakes_weather:
    def __init__(self, status_code=400, text='error'):
        self.status_code = status_code
        self.text = text

    def json(self):
        return {'main':{'temp':51}} 

def test_get_weather_bad():
    test_result_dict = fakes_weather(300)
    res = flaskproject.weather(test_result_dict)
    assert res == 'error: error'

def test_get_weather_good():
    test_result_dict = fakes_weather(200)
    res = flaskproject.weather(test_result_dict, 'New York')
    assert res == 'New York: 51'
