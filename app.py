from flask import Flask, render_template, request, url_for
from h2h import load_data, get_team_names, get_teams_for_h2h, get_h2h_details, calculate_overview_stats

from jinja2 import Environment, FileSystemLoader
import os

app = Flask(__name__)

# Configure the template loader
template_dir = os.path.join(app.root_path, 'templates')
env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
env.globals.update(zip=zip, url_for=url_for)  # Add the zip function to the global namespace
app.jinja_env = env

@app.route('/', methods=['GET', 'POST'])
def index():
    data = []
    if request.method == 'POST':
        comp = request.form['competition']
        data = load_data(comp)

        team1_index = int(request.form['team1']) - 1
        team2_index = int(request.form['team2']) - 1
        team1, team2 = get_teams_for_h2h(team1_index, team2_index, data)

        team1_wins, team2_wins, draws, matches = get_h2h_details(team1, team2)
        team1_stats, team2_stats = calculate_overview_stats(team1, team2, team1_wins, team2_wins, draws, matches)

        return render_template('results.html', team1=team1, team2=team2,
                                team1_wins=team1_wins, team2_wins=team2_wins, draws=draws,
                                team1_stats=team1_stats, team2_stats=team2_stats, matches=matches)

    team_names = get_team_names(data)

    return render_template('index.html', team_names=team_names, enumerate=enumerate)

@app.route('/get_teams', methods=['GET'])
def get_teams():
    comp = request.args.get('competition')
    data = load_data(comp)
    team_names = get_team_names(data)
    return '\n'.join(team_names)

if __name__ == '__main__':
    app.run(debug=True)