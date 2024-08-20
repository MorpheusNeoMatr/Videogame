from app import app
from flask import render_template, abort, redirect, url_for, flash, session
import os
from flask import request
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,
                                                                    "videogame.db")
app.config['GAME_UPLOAD_FOLDER'] = os.path.join(basedir, 'static',
                                                'games_images')
app.config['DIRECTOR_UPLOAD_FOLDER'] = os.path.join(basedir, 'static',
                                                    'directors_images')
app.config['COMPANY_UPLOAD_FOLDER'] = os.path.join(basedir, 'static',
                                                   'companies_images')
app.config['FOUNDER_UPLOAD_FOLDER'] = os.path.join(basedir, 'static',
                                                   'founders_images')
app.config['USER_UPLOAD_FOLDER'] = os.path.join(basedir, 'static',
                                                   'user_images')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_EXPIRE'] = None  # Expire when browser is closed
app.config['SESSION_PERMANENT'] = False
app.secret_key = 'correcthorsebatterystaple'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'
db = SQLAlchemy(app)


import app.models as models
from app.forms import Add_Game, Add_Series, Add_Genre, Add_Directors, Add_Company, Add_Founders, Register, Login
from app.models import Genre, Company, Director, Series, Videogame, Founder, Username


@app.route("/")
def home():
    genres = Genre.query.order_by(Genre.name).all()
    companies = Company.query.order_by(Company.name).all()
    directors = Director.query.order_by(Director.name).all()
    series = Series.query.order_by(Series.name).all()
    users = Username.query.order_by(Username.name).all()
    games = models.Videogame.query.all()  # Fetch all games initially
    return render_template('home.html', users=users, genres=genres, companies=companies, directors=directors, series=series, games=games)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/games", methods=["GET"])
def filter_games():
    genre_id = request.args.get('Genre')
    company_id = request.args.get('Company')
    director_id = request.args.get('Director')
    series_id = request.args.get('Series')
    user_id = request.args.get('User')
    query = models.Videogame.query
    if genre_id and genre_id != 'all':
        query = query.filter(models.Videogame.game_genres.any(id=genre_id))  
    if company_id and company_id != 'all':
        query = query.filter(models.Videogame.game_companies.any(id=company_id)) 
    if director_id and director_id != 'all':
        query = query.filter(models.Videogame.game_directors.any(id=director_id))
    if user_id and user_id != 'all':
        query = query.filter(models.Videogame.username_id == user_id)
    if series_id and series_id != 'all':
        query = query.filter(models.Videogame.series_id == series_id)
    games = query.all()
    # Return only names
    games_list = [{"id": game.id, "name": game.name, "picture_1": game.picture_1} for game in games]
    return jsonify({"games": games_list})


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('You are logged in. Cannot access register page while logged in')
        return redirect(url_for('home'))
    else:
        username_form = Register()
        if request.method == 'GET':
            return render_template(
                'register.html', username_form=username_form)
        else:
            try:
                if username_form.validate_on_submit():
                    new_username = models.Username()
                    new_username.email = username_form.user_email.data
                    new_username.name = username_form.user_name.data
                    filenames = []
                    for user_picture in [username_form.user_picture]:
                        if user_picture.data:
                            filename = secure_filename(user_picture.data.filename)
                            user_picture.data.save(os.path.join(app.config['USER_UPLOAD_FOLDER'], filename))
                            filenames.append(filename)
                        else:
                            filenames.append(None)
                    new_username.picture = filenames[0]
                    new_username.password_hash = generate_password_hash(
                    username_form.user_password.data)
                    db.session.add(new_username)
                    db.session.commit()
                    flash('Username pending, wait for approval')
                    return redirect(url_for('register'))
                else:
                    return render_template(
                    'register.html', username_form=username_form)
            except IntegrityError:
                db.session.rollback()  # Rollback the session to avoid partial commits
                if models.Username.query.filter_by(email=username_form.user_email.data).first():
                    flash('Email already exists.')
                elif models.Username.query.filter_by(name=username_form.user_name.data).first():
                    flash('Username already exists.')
                else:
                    flash('An unexpected error occurred.')
                return render_template('register.html',
                                     username_form=username_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('You are logged in.Cannot access the login page while logged in')
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
                if user:
                    if user.permission != 1:
                        flash('Your account has not been approved yet.')
                        return redirect(url_for('login'))
  
                    if user and check_password_hash(user.password_hash, password):
                        session['user_id'] = user.id
                        session['user_name'] = user.name
                        flash('Logged in successfully.')
                        return redirect(url_for('home'))
       
                    else:
                        flash('Login failed. Wrong email and/or password.')
                        return redirect(url_for('login'))
                else:
                    flash('Wrong email/password.')
                    return redirect(url_for('login'))
            else:
                return render_template('login.html', login_form=login_form)


@app.route('/dashboard/<int:id>')
def dashboard(id):
    if 'user_id' not in session:
        flash("Please login in order to access this page")
        return redirect(url_for('home'))
    else:
        user = Username.query.get_or_404(id)
        user_games = models.Videogame.query.filter_by(username_id=id).all()
        user_founders = models.Founder.query.filter_by(username_id=id).all()
        user_companies = models.Company.query.filter_by(username_id=id).all()
        user_directors = models.Director.query.filter_by(username_id=id).all()
        return render_template('dashboard.html', user_directors=user_directors, user_companies=user_companies, user=user, user_games=user_games, user_founders=user_founders)


@app.route('/logout')
def logout():
    if 'user_id' not in session:
        flash("You're not logged in to logout")
        return redirect(url_for('home'))
    else:
        session.pop('user_id', None)
        session.pop('user_name', None)
        return redirect(url_for('home'))


@app.route("/admin")
def admin():
    if 'user_id' not in session or session.get('user_id') != 17:
        flash("Admin access only")
        return redirect(url_for('home'))
    else:
        pending_users = Username.query.filter_by(permission=0).all()
        return render_template('admin.html', pending_users=pending_users)


@app.route("/admin/approve_user/<int:id>")
def approve_user(id):
    pending_user = Username.query.get_or_404(id)
    pending_user.permission = 1
    db.session.add(pending_user)
    db.session.commit()
    flash('User has been approved.')
    return redirect(url_for('admin'))


@app.route("/admin/reject_user/<int:id>")
def reject_user(id):
    pending_user = Username.query.get_or_404(id)
    pending_user.permission = -1
    db.session.delete(pending_user)
    db.session.commit()
    flash('User has been rejected.')
    return redirect(url_for('admin'))


@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if 'user_id' not in session:
        flash("Please login in order to access this page")
        return redirect(url_for('home'))
    else:
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
                new_game.username_id = session['user_id']
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
    game_user = game.Username
    return render_template("game.html", game_user=game_user, game_series=game_series, game=game, game_companies=game_companies, game_genres=game_genres, game_directors=game_directors)


@app.route("/add_company", methods=['GET', 'POST'])
def add_company():
    if 'user_id' not in session:
        flash("Please login in order to access this page")
        return redirect(url_for('home'))
    else:
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
                new_company.username_id = session['user_id']
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
    games = Videogame.query.order_by(Videogame.name).all()
    series = Series.query.order_by(Series.name).all()
    founders = Founder.query.order_by(Founder.name).all()
    directors = Director.query.order_by(Director.name).all()
    users = Username.query.order_by(Username.name).all()
    company_list = models.Company.query.all()
    return render_template("company_list.html",
    directors=directors, founders=founders, series=series, games=games,
    users=users, company_list=company_list)


@app.route("/api/companies", methods=["GET"])
def filter_companies():
    game_id = request.args.get('Game')
    founder_id = request.args.get('Founder')
    director_id = request.args.get('Director')
    series_id = request.args.get('Series')
    user_id = request.args.get('User')
    query = models.Company.query
    if game_id and game_id != 'all':
        query = query.filter(models.Company.company_games.any(id=game_id))
    if founder_id and founder_id != 'all':
        query = query.filter(models.Company.company_founders.any(id=founder_id))
    if director_id and director_id != 'all':
        query = query.filter(models.Company.company_directors.any(id=director_id))
    if user_id and user_id != 'all':
        query = query.filter(models.Company.username_id == user_id)
    if series_id and series_id != 'all':
        query = query.filter(models.Company.company_series.any(id=series_id))
    companies = query.all()
    # Return only names
    companies_list = [{"id": company.id, "name": company.name} for company in companies]
    return jsonify({"companies": companies_list})


@app.route("/company/<int:id>")
def company(id):
    company = models.Company.query.filter_by(id=id).first_or_404()
    company_directors = company.company_directors
    company_founders = company.company_founders
    company_games = company.company_games
    company_series = company.company_series
    company_username = company.Username
    return render_template("company.html", company_username=company_username, company_series=company_series, company_games=company_games, company_founders=company_founders, company=company, company_directors=company_directors)


@app.route('/add_founder', methods=['GET', 'POST'])
def add_founder():
    if 'user_id' not in session:
        flash("Please login in order to access this page")
        return redirect(url_for('home'))
    else:
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
                new_founder.username_id = session['user_id']
                db.session.add(new_founder)
                db.session.commit()
                flash('Founder added successfully', 'success')
                return redirect(url_for('founder', id=new_founder.id))
            else:
                return render_template('add_founder.html', founder_form=founder_form)


@app.route("/founder_list")
def founder_list():
    companies = Company.query.order_by(Company.name).all()
    users = Username.query.order_by(Username.name).all()
    founder_list = models.Founder.query.all()
    return render_template("founder_list.html", companies=companies, users=users, founder_list=founder_list)


@app.route("/api/founders", methods=['GET'])
def filter_founders():
    company_id = request.args.get('Company')
    user_id = request.args.get('User')
    query = models.Founder.query
    if user_id and user_id != 'all':
        query = query.filter(models.Founder.username_id == user_id)
    if company_id and company_id != 'all':
        query = query.filter(models.Founder.founder_companies.any(id=company_id))
    founders = query.all()
    # Return only names
    founders_list = [{"id": founder.id, "name": founder.name} for founder in founders]
    return jsonify({"founders": founders_list})


@app.route("/founder/<int:id>")
def founder(id):
    founder = models.Founder.query.filter_by(id=id).first_or_404()
    founder_company = founder.founder_companies
    founder_username = founder.Username
    return render_template("founder.html", founder_username=founder_username, founder_company=founder_company, founder=founder)


@app.route("/add_directors", methods=['GET', 'POST'])
def add_directors():
    if 'user_id' not in session:
        flash("Please login in order to access this page")
        return redirect(url_for('home'))
    else:
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
                new_director.username_id = session['user_id']
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
    games = Videogame.query.order_by(Videogame.name).all()
    companies = Company.query.order_by(Company.name).all()
    users = Username.query.order_by(Username.name).all()
    director_list = models.Director.query.all()
    return render_template("director_list.html",
    companies=companies, users=users, games=games, director_list=director_list)


@app.route("/api/directors", methods=["GET"])
def filter_directors():
    game_id = request.args.get('Game')
    company_id = request.args.get('Company')
    user_id = request.args.get('User')
    query = models.Director.query
    if game_id and game_id != 'all':
        query = query.filter(models.Director.videogames.any(id=game_id))
    if user_id and user_id != 'all':
        query = query.filter(models.Director.username_id == user_id)
    if company_id and company_id != 'all':
        query = query.filter(models.Director.companies.any(id=company_id))
    directors = query.all()
    # Return only names
    director_list = [{"id": director.id, "name": director.name} for director in directors]
    return jsonify({"directors": director_list})


@app.route("/director/<int:id>")
def director(id):
    director = models.Director.query.filter_by(id=id).first_or_404()
    director_game = director.Videogame.all()
    director_company = director.Company.all()
    director_username = director.Username
    return render_template("director.html", director_username=director_username, director_company=director_company, director_game=director_game, director=director)


@app.route("/user_list")
def user_list():
    if 'user_id' not in session:
        flash("Please log in to access this page")
        return redirect(url_for('home'))
    else:
        users = models.Username.query.all()
        return render_template("user_list.html", users=users)