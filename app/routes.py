from app import app
from flask import render_template, abort
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "videogame.db")
db.init_app(app)
import app.models as models


@app.route("/")
def home():
    all_genres = models.Genre.query.all()
    all_companies = models.Company.query.all()
    all_series = models.Series.query.all()
    all_directors = models.Director.query.all()
    return render_template('home.html', all_genres=all_genres, all_companies=all_companies, all_series=all_series, all_directors=all_directors)


@app.route("/series_list")
def series_list():
    series_list = models.Series.query.all()
    return render_template('all_series.html', series_list=series_list)


@app.route("/game_series/<int:id>")
def game_series(id):
    game_series = models.Videogame.query.filter_by(series_id=id).all()
    return render_template("game_series.html", game_series=game_series)


# @app.route("/game_genres/<int:id>")
# def game_list(id):
#     genre = models.Genre.query.get_or_404(id)
#     game_genres = genre.videogame.all()
#     return render_template("game_genres.html", game_genres=game_genres, genre=genre)


@app.route("/game/<int:id>")
def game(id):
    game = models.Videogame.query.filter_by(id=id).first()
    return render_template("game.html", game=game)


@app.route("/company_list")
def company_list():
    company_list = models.Company.query.all()
    return render_template("company_list.html", company_list=company_list)


@app.route("/company/<int:id>")
def company(id):
    company = models.Company.query.filter_by(id=id).first()
    return render_template("company.html", company=company)


@app.route("/founder_list")
def founder_list():
    founder_list = models.Founder.query.all()
    return render_template("founder_list.html", founder_list=founder_list)


@app.route("/founder/<int:id>")
def founder(id):
    founder = models.Founder.query.filter_by(id=id).first()
    return render_template("founder.html", founder=founder)


@app.route("/director_list")
def director_list():
    director_list = models.Director.query.all()
    return render_template("director_list.html", director_list=director_list)


@app.route("/director/<int:id>")
def director(id):
    director = models.Director.query.filter_by(id=id).first()
    return render_template("director.html", director=director)
