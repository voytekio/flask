from flaskvc import flaskproject

def test_tst():
    assert flaskproject.tst(4) == 5

def test_get_minions():
    assert flaskproject.get_minions() == 'MANUAL_FOR_NOW, minion1, minion2, minion3'
