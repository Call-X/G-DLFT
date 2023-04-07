import json
from flask import Flask,render_template,request,redirect,flash,url_for
import os
import datetime

base_dir = f"{os.path.dirname(os.path.abspath(__file__))}/"

def loadClubs(file_path=f"{base_dir}clubs.json"):
    with open(file_path) as c:
        listOfClubs = json.load(c)['clubs']
        for club in listOfClubs:
            club['points'] = int(club['points'])
        return listOfClubs

def loadCompetitions(file_path=f"{base_dir}competitions.json"):
    with open(file_path) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        for competition in listOfCompetitions:
            if not "Reservation" in competition:
                competition["Reservation"] = {}
        return listOfCompetitions
    
def serializeClub(club_to_save, filename="clubs.json"):
    with open(filename, 'r+') as f:
        data = json.load(f)
        clubs = data['clubs']
        for club in clubs:
            if club['email'] == club_to_save['email']:
                club['points'] = str(club_to_save['points'])
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
        
def serializeCompetition(comp_to_save, filename="competitions.json"):
    with open(filename, 'r+') as f:
        data = json.load(f)
        competitions = data['competitions']
        for competition in competitions:
            if competition['name'] == comp_to_save['name']:
                competition['numberOfPlaces'] = str(comp_to_save['numberOfPlaces'])
                competition['Reservation'] = str(comp_to_save['Reservation'])
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    
all_competitions = loadCompetitions()
clubs = loadClubs()
app = Flask(__name__)
app.secret_key = '192b9bdd12ab9ad4d12e236c78afcc9a343ec15f71bbf5dc987d54727823xcbf'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/showSummary",methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=all_competitions)
    
@app.route("/book/<competition>/<club>")
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in all_competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=all_competitions, club_list=clubs)
                                      
@app.route("/purchasePlaces",methods=['POST'])
def purchasePlaces():
    competition = [c for c in all_competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=all_competitions)

    # check if club as enough points
    
    # check if there is enough place available  

@app.route("/points_display_board", methods=['GET'])
def points_display_board():
    headings = ("Club Name - ", "Points")
    data = []
    for club in loadClubs():
        club_data = (club['name'], club['points'])
        data.append(club_data)

    return render_template('points_display_board.html', headings=headings, data=data)
    
@app.route("/logout")
def logout():
    return redirect(url_for('index'))



@app.route('/logout')
def logout():
    return redirect(url_for('index'))