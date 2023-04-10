from conftest import client


def allow_to_book_places(client):
    club = "Simply lifts"
    competition = "Spring Festival"
    email = 'john@simplylift.co'
    client.post('/showSummary', data={'email': email})
    response = client.post('/purchasePlaces', data={'competition': competition, 'club': club, 'places': 1})
    assert response.status_code == 200

def not_allowed_to_book_places(client):
    club = "Simply Lift"
    competition = "Fall Classic"
    email = 'john@simplylift.co'
    client.post('/showSummary', data={'email': email})
    response = client.post('/purchasePlaces', data={'competition': competition, 'club': club, 'places': 5})
    assert response.status_code == 500
    
    
def test_check_booking_places_in_past_competition(client):
    email = 'john@simplylift.co'
    response = client.post('/showSummary',data={'email': email})
    assert response.status_code == 200
    