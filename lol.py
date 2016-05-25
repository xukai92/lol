from flask import Flask, request, redirect, url_for, render_template
import api
from check_online import CheckOnline

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search_mastery', methods=['GET', 'POST'])
def search_mastery():
    error = None
    if request.method == 'POST':
        # get query from form
        summonerName = request.form['summonerName']
        championName = request.form['championName']
        region = request.form['region']

        # get master info
        masteries = api.getMasteriesBySummonerAndChampion(summonerName, championName, region)
        if masteries:
            masterySet = api.formatMasteries(masteries)

            # format parameters
            param = dict()
            param["summonerName"] = summonerName
            param["championName"] = championName
            param["region"] = region
            param["masterySet"] = masterySet
            return render_template('show_mastery.html', error=error, param=param)
        else:
            error = "summoner name not found."
    return render_template('search_mastery.html', error=error)


@app.route('/check_online', methods=['GET', 'POST'])
def check_online():
    error = None
    if request.method == 'POST':
        co = CheckOnline()
        region = request.form['region']
        name = request.form['name']
        data = co.check(["", region, name])
        if data["type"] == "message":
            flash(data["message"])
            return redirect(url_for('check_online'))
        else:
            error = data["message"]
    return render_template('check_online.html', error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
