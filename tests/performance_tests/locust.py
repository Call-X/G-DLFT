from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    
    @task(6)
    def index(self):
        self.client.get("/")
    
    @task(6)
    def show_summary(self):
        email = "kate@shelifts.co.uk"
        self.client.post("/showSummary", {"email": email})
    
    @task(6)
    def points_display_board(self):
        email = "kate@shelifts.co.uk"
        self.client.get("/points_display_board")
        
    @task(6)
    def book(self):
        club = "She Lifts"
        competition = "Fall Classic"
        email = "kate@shelifts.co.uk"
        self.client.post('/showSummary', {'email': email})
        self.client.get('/book/{}/{}'.format(competition, club))

    @task(6)
    def logout(self):
        email = "admin@irontemple.com"
        self.client.post('/showSummary', {'email': email})
        self.client.get('/logout')
    
