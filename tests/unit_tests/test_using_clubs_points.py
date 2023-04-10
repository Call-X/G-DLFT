from conftest import client


def test_should_get_points_display_board_page(client):
    response = client.get('/points_display_board')
    assert response.status_code == 200