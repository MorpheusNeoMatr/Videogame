from app import app
from flask import render_template, abort, redirect, url_for, flash, session
import os
from flask import request
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# Configure the path of the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuring the app for database, file uploads, session settings, and CSRF protection
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
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Maximum upload size set to 5 MB
app.secret_key = 'correcthorsebatterystaple'  # Secret key for session management
WTF_CSRF_ENABLED = True  # Enables CSRF protection
WTF_CSRF_SECRET_KEY = 'sup3r_secr3t_passw3rd'  # Secret key for CSRF protection
db = SQLAlchemy(app)  # Initializing the SQLAlchemy database instance


import app.models as models  # Importing models from the app.models module
from app.forms import Add_Game, Add_Series, Add_Genre, Add_Directors, Add_Company, Add_Founders, Register, Login


# home page/game_list page shows all the games.shows the names of the filters.
@app.route("/")
def home():
    genres = models.Genre.query.order_by(models.Genre.name).all()
    companies = models.Company.query.order_by(models.Company.name).all()
    directors = models.Director.query.order_by(models.Director.name).all()
    series = models.Series.query.order_by(models.Series.name).all()
    users = models.Username.query.order_by(models.Username.name).all()
    return render_template('home.html', users=users, genres=genres, companies=companies, directors=directors, series=series)


# API endpoint to filter games based on query parameters
@app.route("/api/games", methods=["GET"])
def filter_games():
    genre_id = request.args.get('Genre')
    company_id = request.args.get('Company')
    director_id = request.args.get('Director')
    series_id = request.args.get('Series')
    user_id = request.args.get('User')
    # Start with the base query for games
    query = models.Videogame.query
    # Apply filters based on the provided parameters
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
    # Execute the query
    games = query.all()
    # Prepare a list of games with their id, name, and picture
    games_list = [{"id": game.id, "name": game.name, "picture_1": game.picture_1} for game in games]
    # Return the list of games as a JSON response
    return jsonify({"games": games_list})


# About page route
@app.route("/about")
def about():
    return render_template("about.html")


# Contact page route
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Register page route with GET and POST methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        # If user is already logged in, redirect to home page with an error message
        flash('You are logged in. Cannot access register page while logged in', 'error')
        return redirect(url_for('home'))
    else:
        # Create a form instance for registration
        username_form = Register()
        if request.method == 'GET':
            return render_template(
                'register.html', username_form=username_form)
        else:
            try:
                if username_form.validate_on_submit():
                    # If form is valid, create a new user instance
                    new_username = models.Username()
                    new_username.email = username_form.user_email.data
                    new_username.name = username_form.user_name.data
                    filenames = []
                    # Save uploaded profile picture
                    for user_picture in [username_form.user_picture]:
                        if user_picture.data:
                            filename = secure_filename(user_picture.data.filename)
                            user_picture.data.save(os.path.join(app.config['USER_UPLOAD_FOLDER'], filename))
                            filenames.append(filename)
                        else:
                            filenames.append(None)
                    new_username.picture = filenames[0]
                    # Hash the user's password for security
                    new_username.password_hash = generate_password_hash(
                    username_form.user_password.data)
                    db.session.add(new_username)
                    db.session.commit()
                    flash('Username pending, wait for approval', 'success')
                    return redirect(url_for('register'))
                else:
                    # Render the register page with errors if form is not valid
                    return render_template(
                    'register.html', username_form=username_form)

            except IntegrityError:
                # Handle cases where the email already exists in the database
                db.session.rollback()  # Rollback the session to avoid partial commits
                models.Username.query.filter_by(email=username_form.user_email.data).first()
                flash('Email already exists.', 'error')
                return render_template('register.html',
                                     username_form=username_form)


# Login page route with GET and POST methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        # If user is already logged in, redirect to home page with an error message.
        flash('You are logged in.Cannot access the login page while logged in', 'error')
        return redirect(url_for('home'))
    else:
        login_form = Login()
        if request.method == 'GET':
            return render_template('login.html', login_form=login_form)
        else:
            if login_form.validate_on_submit():
                email = login_form.login_user_email.data
                password = login_form.login_user_password.data
                user = models.Username.query.filter_by(email=email).first()
                if user:
                    # Check if the account is approved
                    if user.permission != 1:
                        flash('Your account has not been approved yet.', 'error')
                        return redirect(url_for('login'))
                    # Verify password and email
                    if user and check_password_hash(user.password_hash, password):
                        session['user_id'] = user.id  # Store user ID in session
                        session['user_name'] = user.name  # Store user name in session
                        flash('Logged in successfully.', 'success')
                        return redirect(url_for('home'))
                else:
                    # Flash an error message if the email or password is wrong
                    flash('Wrong email/password.', 'error')
                    return redirect(url_for('login'))
            else:
                # Render the login page with errors if form is not valid
                return render_template('login.html', login_form=login_form)


# Dashboard route for a specific user
@app.route('/dashboard/<int:id>')
def dashboard(id):
    if 'user_id' not in session:
        # If user is not logged in, redirect to home page with an error message
        flash("Please login in order to access this page", 'error')
        return redirect(url_for('home'))
    else:
        try:
            user = models.Username.query.get_or_404(id)  # Get the user or return 404 if not found
            user_games = models.Videogame.query.filter_by(username_id=id).all()
            user_founders = models.Founder.query.filter_by(username_id=id).all()
            user_companies = models.Company.query.filter_by(username_id=id).all()
            user_directors = models.Director.query.filter_by(username_id=id).all()
            return render_template('dashboard.html',
             user_directors=user_directors,
             user_companies=user_companies,
             user=user, user_games=user_games,
             user_founders=user_founders)

        except OverflowError:
            # Handle cases where an invalid ID is entered (overflow error)
            abort(404)


# Logout route
@app.route('/logout')
def logout():
    if 'user_id' not in session:
        # If user is not logged in, flash an error message
        flash("You're not logged in to logout", 'error')
        return redirect(url_for('home'))
    else:
        # Clear the session data and log out the user
        session.pop('user_id', None)
        session.pop('user_name', None)
        flash("you logged out", 'success')
        return redirect(url_for('home'))


# Admin dashboard route
@app.route("/admin")
def admin():
    if 'user_id' not in session or session.get('user_id') != 17:
        # If user is not logged in, redirect to home page with an error message
        flash("Admin access only", 'error')
        return redirect(url_for('home'))
    else:
        pending_users = models.Username.query.filter_by(permission=0).all()
        return render_template('admin.html', pending_users=pending_users)


# Approve user route/Aprrove user button
@app.route("/admin/approve_user/<int:id>")
def approve_user(id):
    # Check if the user is logged in and if they are the admin (user_id == 17)
    if 'user_id' not in session or session.get('user_id') != 17:
        flash("Admin access only", 'error')
        return redirect(url_for('home'))
    else:
        # Fetch the user by id or return a 404 error if not found
        pending_user = models.Username.query.get_or_404(id)
        # approve the user and set the permission from 0 to 1.
        pending_user.permission = 1
        db.session.add(pending_user)
        db.session.commit()
        flash('User has been approved.', 'error')
        return redirect(url_for('admin'))


# Reject user route/Reject user button.
@app.route("/admin/reject_user/<int:id>")
def reject_user(id):
    # Check if the user is logged in and if they are the admin (user_id == 17)
    if 'user_id' not in session or session.get('user_id') != 17:
        flash("Admin access only", 'error')
        return redirect(url_for('home'))
    else:
        # Fetch the user by id or return a 404 error if not found
        pending_user = models.Username.query.get_or_404(id)
        # Reject and remove the user from the database
        db.session.delete(pending_user)
        db.session.commit()
        flash('User has been rejected.', 'error')
        return redirect(url_for('admin'))


# Add game route
@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please login in order to access this page", 'error')
        return redirect(url_for('home'))
    else:
        # Initialize forms for game, series, and genre
        game_form = Add_Game()
        series_form = Add_Series()
        genre_form = Add_Genre()
        # Handle GET request
        if request.method == 'GET':
            # Render the add game page with forms
            return render_template('add_game.html', genre_form=genre_form, game_form=game_form, series_form=series_form)
        else:
            # Handle POST request for adding a new game
            if game_form.validate_on_submit():
                # Create a new game object and assign form data to its fields
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
                # Handle image uploads for game pictures
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
                # Assign selected genres, directors, and companies to the game
                new_game.game_genres = models.Genre.query.filter(models.Genre.id.in_(game_form.game_genres.data)).all()
                new_game.game_directors = models.Director.query.filter(models.Director.id.in_(game_form.game_directors.data)).all()
                new_game.game_companies = models.Company.query.filter(models.Company.id.in_(game_form.game_companies.data)).all()
                db.session.add(new_game)
                db.session.commit()
                flash('Game added successfully', 'success')
                return redirect(url_for('game', game_id=new_game.id))

            # Handle POST request for adding a new series
            elif series_form.validate_on_submit():
                new_series = models.Series()
                new_series.name = series_form.series_name.data
                db.session.add(new_series)
                db.session.commit()
                flash('Series added successfully', 'success')
                return redirect(url_for('add_game'))

            # Handle POST request for adding a new genre
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


# Game details route
@app.route("/game/<int:game_id>", methods=['GET', 'POST'])
def game(game_id):
    try:
        # Attempt to retrieve the game by ID or get 404
        game = models.Videogame.query.filter_by(id=game_id).first_or_404()
        # Retrieve related data
        game_companies = game.game_companies
        game_genres = game.game_genres
        game_directors = game.game_directors
        game_series = game.Series
        game_user = game.Username
        # Render the template with the game details
        return render_template(
            "game.html",
            game=game,
            game_user=game_user,
            game_series=game_series,
            game_companies=game_companies,
            game_genres=game_genres,
            game_directors=game_directors
        )
    except OverflowError:
        # Handle the overflow error
        abort(404)


# Add company route
@app.route("/add_company", methods=['GET', 'POST'])
def add_company():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please login in order to access this page", 'error')
        return redirect(url_for('home'))
    else:
        # Initialize forms for company and series in company
        company_form = Add_Company()
        series_in_company_form = Add_Series()
        if request.method == 'GET':
            # Render the add company page with forms
            return render_template('add_company.html', company_form=company_form, series_in_company_form=series_in_company_form)
        else:
            # Handle POST request for adding a new company
            if company_form.validate_on_submit():
                new_company = models.Company()
                new_company.name = company_form.company_name.data
                new_company.company_games = models.Videogame.query.filter(models.Videogame.id.in_(company_form.company_games.data)).all()
                new_company.company_directors = models.Director.query.filter(models.Director.id.in_(company_form.company_directors.data)).all()
                new_company.company_founders = models.Founder.query.filter(models.Founder.id.in_(company_form.company_founders.data)).all()
                new_company.company_series = models.Series.query.filter(models.Series.id.in_(company_form.company_series.data)).all()
                new_company.time_founded = company_form.company_time_founded.data
                new_company.headquarters = company_form.company_headquarters.data
                new_company.description = company_form.company_description.data
                new_company.username_id = session['user_id']
                filenames = []
                # Handle image uploads for company pictures
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

            # Handle POST request for adding a new series in company
            elif series_in_company_form.validate_on_submit():
                new_series_in_company = models.Series()
                new_series_in_company.name = series_in_company_form.series_name.data
                db.session.add(new_series_in_company)
                db.session.commit()
                flash('Series added successfully', 'success')
                return redirect(url_for('add_company'))
            else:
                # If none of the forms are valid, re-render the page with the form errors
                return render_template('add_company.html', company_form=company_form, series_in_company_form=series_in_company_form)


# shows all companies route. query all the names of the filters for companies.
@app.route("/company_list")
def company_list():
    # Fetch all data needed for the company list page
    games = models.Videogame.query.order_by(models.Videogame.name).all()
    series = models.Series.query.order_by(models.Series.name).all()
    founders = models.Founder.query.order_by(models.Founder.name).all()
    directors = models.Director.query.order_by(models.Director.name).all()
    users = models.Username.query.order_by(models.Username.name).all()

    # Render the company list template with the fetched data
    return render_template("company_list.html",
    directors=directors, founders=founders, series=series, games=games,
    users=users)


# API endpoint to filter companies based on query parameters
@app.route("/api/companies", methods=["GET"])
def filter_companies():
    # Retrieve filter parameters from the request
    game_id = request.args.get('Game')
    founder_id = request.args.get('Founder')
    director_id = request.args.get('Director')
    series_id = request.args.get('Series')
    user_id = request.args.get('User')
    # Start with the base query for companies
    query = models.Company.query
    # Apply filters based on the provided parameters
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
    # Execute the query
    companies = query.all()
    # Prepare a list of companies with their id, name, and picture
    companies_list = [{"id": company.id, "name": company.name, "picture_1": company.picture_1} for company in companies]
    # Return the list of companies as a JSON response
    return jsonify({"companies": companies_list})


# company page route.
@app.route("/company/<int:id>")
def company(id):
    try:
        # Fetch the company by ID or return a 404 error if not found
        company = models.Company.query.filter_by(id=id).first_or_404()
        company_directors = company.company_directors
        company_founders = company.company_founders
        company_games = company.company_games
        company_series = company.company_series
        company_username = company.Username

        # Render the company details template with the fetched data
        return render_template("company.html",
        company_username=company_username,
        company_series=company_series,
        company_games=company_games,
        company_founders=company_founders,
        company=company,
        company_directors=company_directors)

    except OverflowError:
        # Handle overflow error returning a 404 page
        abort(404)


# add founder route
@app.route('/add_founder', methods=['GET', 'POST'])
def add_founder():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please login in order to access this page", 'error')
        return redirect(url_for('home'))
    else:
        # Initialize the form for adding a founder
        founder_form = Add_Founders()
        if request.method == 'GET':
            # Render the add founder template with the form
            return render_template('add_founder.html', founder_form=founder_form)
        else:
            if founder_form.validate_on_submit():
                # Create a new founder instance and set its properties
                new_founder = models.Founder()
                new_founder.name = founder_form.founder_name.data
                new_founder.founder_companies = models.Company.query.filter(models.Company.id.in_(founder_form.founder_companies.data)).all()
                new_founder.date_of_birth = founder_form.founder_date_of_birth.data
                filenames = []
                # Save founder pictures and set their filenames
                for founder_pictures in [founder_form.founder_picture_1,
                                        founder_form.founder_picture_2,]:
                    if founder_pictures.data:
                        filename = secure_filename(founder_pictures.data.filename)
                        founder_pictures.data.save(os.path.join(app.config['FOUNDER_UPLOAD_FOLDER'], filename))
                        filenames.append(filename)
                    else:
                        filenames.append(None)
                # Set additional properties and save to database
                new_founder.picture_1 = filenames[0]
                new_founder.picture_2 = filenames[1]
                new_founder.description = founder_form.founder_description.data
                new_founder.username_id = session['user_id']
                db.session.add(new_founder)
                db.session.commit()
                flash('Founder added successfully', 'success')
                return redirect(url_for('founder', id=new_founder.id))
            else:
                # If form validation fails, render the form again
                return render_template('add_founder.html', founder_form=founder_form)


# shows all founders route
@app.route("/founder_list")
def founder_list():
    # Fetch all data needed for the founder list page
    companies = models.Company.query.order_by(models.Company.name).all()
    users = models.Username.query.order_by(models.Username.name).all()
    # Render the founder list template with the fetched data
    return render_template("founder_list.html", companies=companies, users=users)


# API endpoint to filter founders based on query parameters
@app.route("/api/founders", methods=['GET'])
def filter_founders():
    # Retrieve filter parameters from the request
    company_id = request.args.get('Company')
    user_id = request.args.get('User')
    # Start with the base query for founders
    query = models.Founder.query
    # Apply filters based on the provided parameters
    if user_id and user_id != 'all':
        query = query.filter(models.Founder.username_id == user_id)
    if company_id and company_id != 'all':
        query = query.filter(models.Founder.founder_companies.any(id=company_id))
    # Execute the query
    founders = query.all()
    # Prepare a list of founders with their id, name, and picture
    founders_list = [{"id": founder.id, "name": founder.name, "picture_1": founder.picture_1} for founder in founders]
    # Return the list of founders as a JSON response
    return jsonify({"founders": founders_list})


# founder information route.
@app.route("/founder/<int:id>")
def founder(id):
    try:
        # Fetch the founder by ID or return a 404 error if not found
        founder = models.Founder.query.filter_by(id=id).first_or_404()
        founder_company = founder.founder_companies
        founder_username = founder.Username
        # Render the founder details template with the fetched data
        return render_template("founder.html",
        founder_username=founder_username,
        founder_company=founder_company,
        founder=founder)

    except OverflowError:
        # Handle overflow error returning a 404 page
        abort(404)


# Add director route.
@app.route("/add_directors", methods=['GET', 'POST'])
def add_directors():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please login in order to access this page", 'error')
        return redirect(url_for('home'))
    else:
        # Initialize the form for adding a director
        director_form = Add_Directors()
        if request.method == 'GET':
            # Render the add director template with the form
            return render_template('add_directors.html', director_form=director_form)
        else:
            if director_form.validate_on_submit():
                # Create a new director instance and set its properties
                new_director = models.Director()
                new_director.name = director_form.director_name.data
                new_director.date_of_birth = director_form.director_age.data
                new_director.description = director_form.director_description.data
                new_director.videogames = models.Videogame.query.filter(models.Videogame.id.in_(director_form.director_games.data)).all()
                new_director.companies = models.Company.query.filter(models.Company.id.in_(director_form.director_companies.data)).all()
                new_director.username_id = session['user_id']
                filenames = []
                # Save director pictures and set their filenames
                for director_pictures in [director_form.director_picture_1,
                                    director_form.director_picture_2,]:
                    if director_pictures.data:
                        filename = secure_filename(director_pictures.data.filename)
                        director_pictures.data.save(os.path.join(app.config['DIRECTOR_UPLOAD_FOLDER'], filename))
                        filenames.append(filename)
                    else:
                        filenames.append(None)
                # Set additional properties and save to database
                new_director.picture_1 = filenames[0]
                new_director.picture_2 = filenames[1]
                db.session.add(new_director)
                db.session.commit()
                flash('Director added successfully', 'success')
                return redirect(url_for('director', id=new_director.id))
            else:
                # If form validation fails, render the form again
                return render_template('add_directors.html', director_form=director_form)


# Route for showing all directors.
@app.route("/director_list")    
def director_list():
    # Query all games, companies, and users, ordering them by name
    games = models.Videogame.query.order_by(models.Videogame.name).all()
    companies = models.Company.query.order_by(models.Company.name).all()
    users = models.Username.query.order_by(models.Username.name).all()
    # Render the 'director_list.html' template with the queried data
    return render_template("director_list.html",
    companies=companies, users=users, games=games)


# API route to filter directors based on query parameters
@app.route("/api/directors", methods=["GET"])
def filter_directors():
    # Retrieve filter parameters from the request
    game_id = request.args.get('Game')
    company_id = request.args.get('Company')
    user_id = request.args.get('User')
    # Start with the base query for directors
    query = models.Director.query
    # Apply filters based on the provided parameters
    if game_id and game_id != 'all':
        query = query.filter(models.Director.videogames.any(id=game_id))
    if user_id and user_id != 'all':
        query = query.filter(models.Director.username_id == user_id)
    if company_id and company_id != 'all':
        query = query.filter(models.Director.companies.any(id=company_id))
    # Execute the query
    directors = query.all()
    # Prepare a list of users with their id, name, and picture
    director_list = [{"id": director.id, "name": director.name, "picture_1": director.picture_1} for director in directors]
    # Return the list of directors as a JSON response
    return jsonify({"directors": director_list})


# Show director page information based on its id
@app.route("/director/<int:id>")
def director(id):
    try:
        # Query for the director by ID, raising a 404 error if not found
        director = models.Director.query.filter_by(id=id).first_or_404()
        director_game = director.Videogame.all()
        director_company = director.Company.all()
        director_username = director.Username
        # Render the 'director.html' template with the queried data
        return render_template("director.html",
        director_username=director_username,
        director_company=director_company,
        director_game=director_game,
        director=director)

    except OverflowError:
        # Handle OverflowError errors returning a 404 error
        abort(404)


# Route to display all users.
@app.route("/user_list")
def user_list():
    if 'user_id' not in session:
        # If the user is not logged in, flash an error message and redirect to home
        flash("Please log in to access this page", 'error')
        return redirect(url_for('home'))
    else:
        # Query all users, games, directors, companies, and founders
        games = models.Videogame.query.all()
        directors = models.Director.query.all()
        companies = models.Company.query.all()
        founders = models.Founder.query.all()
        # Render the 'user_list.html' template with the queried data
        return render_template("user_list.html", games=games, directors=directors,
                         companies=companies, founders=founders)


# API route to filter users based on query parameters.
@app.route("/api/users", methods=["GET"])
def filter_users():
    # Retrieve filter parameters from the request
    game_id = request.args.get('Game')
    company_id = request.args.get('Company')
    director_id = request.args.get('Director')
    founder_id = request.args.get('Founder')
    # Start with the base query for users
    query = models.Username.query
    # Apply filters based on the provided parameters
    if game_id and game_id != 'all':
        query = query.join(models.Videogame).filter(models.Videogame.id == game_id)
    if company_id and company_id != 'all':
        query = query.join(models.Company).filter(models.Company.id == company_id)
    if director_id and director_id != 'all':
        query = query.join(models.Director).filter(models.Director.id == director_id)
    if founder_id and founder_id != 'all':
        query = query.join(models.Founder).filter(models.Founder.id == founder_id)
    # Execute the query
    users = query.all()
    # Prepare a list of users with their id, name, and picture
    user_list = [{"id": user.id, "name": user.name, "picture": user.picture} for user in users]
    # Return the list of users as a JSON response
    return jsonify({"users": user_list})


# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    # Render the '404.html' template when a 404 error occurs
    return render_template('404.html'), 404
