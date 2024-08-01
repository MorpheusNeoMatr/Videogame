from app import app
from flask import render_template, abort, redirect, url_for, flash
import os
from flask import request
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "videogame.db")
app.config['GAME_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'games_images')
app.config['DIRECTOR_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'directors_images')
app.config['COMPANY_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'companies_images')
app.config['FOUNDER_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'founders_images')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_EXPIRE'] = False  # Cookie will expire when the browser is closed
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


import app.models as models
from app.forms import Add_Game, Add_Series, Add_Genre, Add_Directors, Add_Company, Add_Founders, Register, Login
from app.models import Genre, Company, Director, Series, Videogame, Founder, Username_Pending, Username


@app.route("/")
def home():
    genres = Genre.query.order_by(Genre.name).all()
    companies = Company.query.order_by(Company.name).all()
    directors = Director.query.order_by(Director.name).all()
    series = Series.query.order_by(Series.name).all()
    games = models.Videogame.query.all()  # Fetch all games initially
    return render_template('home.html', genres=genres, companies=companies, directors=directors, series=series, games=games)


@app.route("/api/games", methods=["GET"])
def filter_games():
    genre_id = request.args.get('Genre')
    company_id = request.args.get('Company')
    director_id = request.args.get('Director')
    series_id = request.args.get('Series')
    query = models.Videogame.query
    if genre_id and genre_id != 'all':
        query = query.filter(models.Videogame.game_genres.any(id=genre_id))  
    if company_id and company_id != 'all':
        query = query.filter(models.Videogame.game_companies.any(id=company_id)) 
    if director_id and director_id != 'all':
        query = query.filter(models.Videogame.game_directors.any(id=director_id))
    if series_id and series_id != 'all':
        query = query.filter(models.Videogame.series_id == series_id)
    games = query.all()
    games_list = [{"id": game.id, "name": game.name} for game in games]   # Return only names
    return jsonify({"games": games_list})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged in. Cannot access register page while logged in')
        return redirect(url_for('home'))
    else:
        username_form = Register()
        if request.method == 'GET':
            return render_template('register.html', username_form=username_form)
        else:
            if username_form.validate_on_submit():
                new_username = models.Username_Pending()
                new_username.email = username_form.user_email.data
                new_username.name = username_form.user_name.data
                new_username.password_hash = generate_password_hash(username_form.user_password.data)
                db.session.add(new_username)
                db.session.commit()
                flash('Username pending, wait for approval')
                return redirect(url_for('register'))
            else:
                return render_template('register.html', username_form=username_form)
        

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Username.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are logged in. Cannot access the login page while logged in')
        return redirect(url_for('home'))
    else:
        login_form = Login()
        if request.method == 'GET':
                return render_template('login.html', login_form=login_form)
        else:
            if login_form.validate_on_submit():
                email = login_form.login_user_email.data
                password = login_form.login_user_password.data
                user = Username.query.filter_by(email=email).first()
                if user and check_password_hash(user.password_hash, password):
                    login_user(user)
                    flash('Logged in')
                    return redirect(url_for('home'))
                else:
                    flash('Login failed. Check your email and/or password.')
                    return redirect(url_for('login'))
            else:
                return render_template('login.html', login_form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/admin")
def admin():
    pending_users = Username_Pending.query.all()
    return render_template('admin.html', pending_users=pending_users)


@app.route("/admin/approve_user/<int:id>")
def approve_user(id):
    pending_user = Username_Pending.query.get_or_404(id)
    new_user = Username()
    new_user.name = pending_user.name
    new_user.email = pending_user.email
    new_user.password_hash = pending_user.password_hash
    db.session.add(new_user)
    db.session.delete(pending_user)
    db.session.commit()
    flash('User has been approved.')
    return redirect(url_for('admin'))


@app.route("/admin/reject_user/<int:id>")
def reject_user(id):
    pending_user = Username_Pending.query.get_or_404(id)
    db.session.delete(pending_user)
    db.session.commit()
    flash('User has been rejected.')
    return redirect(url_for('admin'))


@app.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    game_form = Add_Game()
    series_form = Add_Series()
    genre_form = Add_Genre()
    if request.method == 'GET':
        return render_template('add_game.html', genre_form=genre_form, game_form=game_form, series_form=series_form)
    else:
        if game_form.validate_on_submit():
            new_game = models.Videogame()
            new_game.name = game_form.game_name.data
            new_game.release_date = game_form.game_date.data
            new_game.dev_score = game_form.game_dev_score.data
            new_game.description = game_form.game_description.data
            new_game.gameplay = game_form.game_gameplay.data
            new_game.story = game_form.game_story.data
            new_game.soundtrack = game_form.game_soundtrack.data
            new_game.reviews = game_form.game_reviews.data
            new_game.series_id = game_form.game_series.data
            filenames = []
            for game_pictures in [game_form.game_picture_1,
                                game_form.game_picture_2, game_form.game_picture_3,
                                game_form.game_picture_4, game_form.game_picture_5, game_form.game_picture_6]:
                if game_pictures.data:
                    filename = secure_filename(game_pictures.data.filename)
                    game_pictures.data.save(os.path.join(app.config['GAME_UPLOAD_FOLDER'], filename))
                    filenames.append(filename)
                else:
                    filenames.append(None)
            new_game.picture_1 = filenames[0]
            new_game.picture_2 = filenames[1]
            new_game.picture_3 = filenames[2]
            new_game.picture_4 = filenames[3]
            new_game.picture_5 = filenames[4]
            new_game.picture_6 = filenames[5]
            new_game.game_genres = Genre.query.filter(Genre.id.in_(game_form.game_genres.data)).all()
            new_game.game_directors = Director.query.filter(Director.id.in_(game_form.game_directors.data)).all()
            new_game.game_companies = Company.query.filter(Company.id.in_(game_form.game_companies.data)).all()
            db.session.add(new_game)
            db.session.commit()
            flash('Game added successfully', 'success')
            return redirect(url_for('game', game_id=new_game.id))

        elif series_form.validate_on_submit():
            new_series = models.Series()
            new_series.name = series_form.series_name.data
            db.session.add(new_series)
            db.session.commit()
            flash('Series added successfully', 'success')
            return redirect(url_for('add_game'))
        
        elif genre_form.validate_on_submit():
            new_genre = models.Genre()
            new_genre.name = genre_form.genre_name.data
            db.session.add(new_genre)
            db.session.commit()
            flash('Genre added successfully', 'success')
            return redirect(url_for('add_game'))
        else:
            # If none of the forms are valid, re-render the page with the form errors
            return render_template('add_game.html', genre_form=genre_form, game_form=game_form, series_form=series_form)


@app.route("/game/<int:game_id>", methods=['GET', 'POST'])
def game(game_id):
    game = models.Videogame.query.filter_by(id=game_id).first_or_404()
    game_companies = game.game_companies
    game_genres = game.game_genres
    game_directors = game.game_directors
    game_series = game.Series
    return render_template("game.html", game_series=game_series, game=game, game_companies=game_companies, game_genres=game_genres, game_directors=game_directors)


@app.route("/add_company", methods=['GET', 'POST'])
@login_required
def add_company():
    company_form = Add_Company()
    series_in_company_form = Add_Series()
    if request.method == 'GET':
        return render_template('add_company.html', company_form=company_form, series_in_company_form=series_in_company_form)
    else:
        if company_form.validate_on_submit():
            new_company = models.Company()
            new_company.name = company_form.company_name.data
            new_company.company_games = Videogame.query.filter(Videogame.id.in_(company_form.company_games.data)).all()
            new_company.company_directors = Director.query.filter(Director.id.in_(company_form.company_directors.data)).all()
            new_company.company_founders = Founder.query.filter(Founder.id.in_(company_form.company_founders.data)).all()
            new_company.company_series = Series.query.filter(Series.id.in_(company_form.company_series.data)).all()
            new_company.time_founded = company_form.company_time_founded.data
            new_company.headquarters = company_form.company_headquarters.data
            new_company.description = company_form.company_description.data
            filenames = []
            for company_pictures in [company_form.company_picture_1,
                                company_form.company_picture_2,]:
                if company_pictures.data:
                    filename = secure_filename(company_pictures.data.filename)
                    company_pictures.data.save(os.path.join(app.config['COMPANY_UPLOAD_FOLDER'], filename))
                    filenames.append(filename)
                else:
                    filenames.append(None)
            new_company.picture_1 = filenames[0]
            new_company.picture_2 = filenames[1]
            db.session.add(new_company)
            db.session.commit()
            flash('Company added successfully', 'success')
            return redirect(url_for('company', id=new_company.id))
        
        elif series_in_company_form.validate_on_submit():
            new_series_in_company = models.Series()
            new_series_in_company.name = series_in_company_form.series_name.data
            db.session.add(new_series_in_company)
            db.session.commit()
            flash('Series added successfully', 'success')
            return redirect(url_for('add_company'))
        else:
            return render_template('add_company.html', company_form=company_form, series_in_company_form=series_in_company_form)


@app.route("/company_list")
def company_list():
    company_list = models.Company.query.all()
    return render_template("company_list.html", company_list=company_list)


@app.route("/company/<int:id>")
def company(id):
    company = models.Company.query.filter_by(id=id).first_or_404()
    company_directors = company.company_directors
    company_founders = company.company_founders
    company_games = company.company_games
    company_series = company.company_series
    return render_template("company.html",company_series=company_series, company_games=company_games, company_founders=company_founders, company=company, company_directors=company_directors)


@app.route('/add_founder', methods=['GET', 'POST'])
@login_required
def add_founder():
    founder_form = Add_Founders()
    if request.method == 'GET':
        return render_template('add_founder.html', founder_form=founder_form)
    else:
        if founder_form.validate_on_submit():
            new_founder = models.Founder()
            new_founder.name = founder_form.founder_name.data
            new_founder.founder_companies = Company.query.filter(Company.id.in_(founder_form.founder_companies.data)).all()
            new_founder.date_of_birth = founder_form.founder_date_of_birth.data
            filenames = []
            for founder_pictures in [founder_form.founder_picture_1,
                                    founder_form.founder_picture_2,]:
                if founder_pictures.data:
                    filename = secure_filename(founder_pictures.data.filename)
                    founder_pictures.data.save(os.path.join(app.config['FOUNDER_UPLOAD_FOLDER'], filename))
                    filenames.append(filename)
                else:
                    filenames.append(None)
            new_founder.picture_1 = filenames[0]
            new_founder.picture_2 = filenames[1]
            new_founder.description = founder_form.founder_description.data
            db.session.add(new_founder)
            db.session.commit()
            flash('Founder added successfully', 'success')
            return redirect(url_for('founder', id=new_founder.id))
        else:
            return render_template('add_founder.html', founder_form=founder_form)

@app.route("/founder_list")
def founder_list():
    founder_list = models.Founder.query.all()
    return render_template("founder_list.html", founder_list=founder_list)


@app.route("/founder/<int:id>")
def founder(id):
    founder = models.Founder.query.filter_by(id=id).first_or_404()
    founder_company = founder.founder_companies
    return render_template("founder.html", founder_company=founder_company, founder=founder)


@app.route("/add_directors", methods=['GET', 'POST'])
@login_required
def add_directors():
    director_form = Add_Directors()
    if request.method == 'GET':
        return render_template('add_directors.html', director_form=director_form)
    else:
        if director_form.validate_on_submit():
            new_director = models.Director()
            new_director.name = director_form.director_name.data
            new_director.date_of_birth = director_form.director_age.data
            new_director.description = director_form.director_description.data
            new_director.videogames = Videogame.query.filter(Videogame.id.in_(director_form.director_games.data)).all()
            new_director.companies = Company.query.filter(Company.id.in_(director_form.director_companies.data)).all()
            filenames = []
            for director_pictures in [director_form.director_picture_1,
                                director_form.director_picture_2,]:
                if director_pictures.data:
                    filename = secure_filename(director_pictures.data.filename)
                    director_pictures.data.save(os.path.join(app.config['DIRECTOR_UPLOAD_FOLDER'], filename))
                    filenames.append(filename)
                else:
                    filenames.append(None)
            new_director.picture_1 = filenames[0]
            new_director.picture_2 = filenames[1]
            db.session.add(new_director)
            db.session.commit()
            flash('Director added successfully', 'success')
            return redirect(url_for('director', id=new_director.id))
        else:
            return render_template('add_directors.html', director_form=director_form)


@app.route("/director_list")
def director_list():
    director_list = models.Director.query.all()
    return render_template("director_list.html", director_list=director_list)


@app.route("/director/<int:id>")
def director(id):
    director = models.Director.query.filter_by(id=id).first_or_404()
    director_game = director.Videogame.all()
    director_company = director.Company.all()
    return render_template("director.html", director_company=director_company, director_game=director_game, director=director)