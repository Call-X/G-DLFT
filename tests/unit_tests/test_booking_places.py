from http import HTTPStatus
from pathlib import Path
import server
from conftest import client, clubs_data, competitions_data
from server import loadClubs, loadCompetitions

tests_unit_dir = Path(__file__).parent

def test_load_clubs_file_not_empty():
    """ Test that clubs database is not empty """
    data_clubs = loadClubs()
    assert data_clubs != ""


def test_load_competitions_file_not_empty():
    """ Test that competitions database is not empty """
    data_competitions = loadCompetitions()
    assert data_competitions != ""

def setUp(self):
        with open(tests_unit_dir / 'clubs.json') as database:
            clubs = []
        with open(tests_unit_dir / 'competitions.json') as database:
            competitions = []
        return clubs, competitions


class TestClass:
    def test_allow_to_book_places(self,client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "all_competitions", competitions_data)
        
        club = "Test Club"
        competition = "Competition Test"
        email = 'test@example.com'
        places = 1
        
        response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'email': email,  'places': places})
        html_response = response.data.decode()

        assert response.status_code == 200 
        assert "<li>Great Booking complete! You purchased 1 for the Competition Test!</li>" in html_response
    
    def test_club_has_not_enough_points(self,client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "all_competitions", competitions_data)
        
        club = "Test Club"
        competition = "Competition Test"
        email = 'test@example.com'
        places = 10
        
        response = client.post('/purchasePlaces', data={'email': email, "club": club, "competition": competition, "places": places })
        html_response = response.data.decode()
        
        assert response.status_code == 200
        assert "<li>Your club doesn&#39;t have enough point !</li>" in html_response
        

    def test_purchase_places_12_place_limitation(self,client, mocker): 
        mocker.patch.object(server, "project_dir", tests_unit_dir)  
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "all_competitions", competitions_data)
        
        club = "Test Club overbook"
        competition = "Competition Test"
        email = 'test3@example.com'
        places = 13
        
        response = client.post('/purchasePlaces', data={'email': email, "club": club, "competition": competition, "places": places })
        html_response = response.data.decode()
        print(html_response)
        assert response.status_code == 200
        assert "You can&#39;t book more than 12 places per competition" in html_response
    
    def test_purchase_places_already_booked_12_places(self,client, mocker):   
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "all_competitions", competitions_data)
        
        club = "Test Club 2"
        competition = "Competition Test"
        email = 'test@example.com'
        places = 1
        
        response = client.post('/purchasePlaces', data={'email': email, "club": club, "competition": competition, "places": places })
        html_response = response.data.decode()
        assert response.status_code == 200
        assert "<li>You can&#39;t book more than 12 places per competition</li>" in html_response
    
    def test_check_booking_places_in_past_competition(self,client, mocker):
        mocker.patch.object(server, "project_dir", tests_unit_dir)
        mocker.patch.object(server, "clubs", clubs_data)
        mocker.patch.object(server, "all_competitions", competitions_data)
        
        club = "Test Club 2"
        competition = "Past Competition Test"
        date = "2020-03-27 10:00:00"
        places = 1
        
        response = client.post('/purchasePlaces', data={"club": club, "competition": competition, "date": date, "places": places})
        html_reponse = response.data.decode()
        assert response.status_code == 200
        assert "This competition already happened !" in html_reponse