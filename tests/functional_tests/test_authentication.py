from conftest import client


def test_should_logout(client):
    email = 'kate@shelifts.co.uk'
    client.post('/showSummary', data={'email': email})
    response = client.get('/logout')
    assert response.status_code == 302
    
def test_should_fail_with_unknow_email(client):
    email = ''
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200

def test_should_pass_with_register_email(client):
    email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200