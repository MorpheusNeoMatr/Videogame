from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SelectMultipleField, FileField, SubmitField, PasswordField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Optional, ValidationError, Email, EqualTo, Length
import app.models
from app.models import Series,Director,Genre,Company, Videogame, Founder


class Register(FlaskForm):
    user_email = StringField('user_email', validators=[DataRequired(), Email()])
    user_name = StringField('user_name', validators=[DataRequired()])
    user_password = PasswordField('user_password', validators=[DataRequired(), EqualTo('confirm', message='Password must match'), Length(min=6, max=100)])
    confirm = PasswordField('confirm', validators=[DataRequired()])
    user_submit = SubmitField('Register')
    admin_permission = SubmitField('admin_permission')
    user_picture = FileField('picture', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])


class Login(FlaskForm):
    login_user_email = StringField('login_user_email', validators=[DataRequired(), Email()])
    login_user_password = PasswordField('login_user_password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Add_Game(FlaskForm):
    game_name = StringField('game_name', validators=[DataRequired()])
    game_dev_score = StringField('game_dev_score', validators=[DataRequired()])
    game_date = StringField('game_date', validators=[DataRequired()])
    game_description = TextAreaField('game_description', validators=[DataRequired()])
    game_gameplay = TextAreaField('game_gameplay', validators=[DataRequired()])
    game_story = TextAreaField('game_story', validators=[DataRequired()])
    game_soundtrack = TextAreaField('game_soundtrack', validators=[DataRequired()])
    game_reviews = TextAreaField('game_reviews', validators=[DataRequired()])
    game_picture_1 = FileField('game_picture_1', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    game_picture_2 = FileField('game_picture_2', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    game_picture_3 = FileField('game_picture_3', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    game_picture_4 = FileField('game_picture_4', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    game_picture_5 = FileField('game_picture_5', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    game_picture_6 = FileField('game_picture_6', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    game_series = SelectField('game_series', coerce=int, validators=[DataRequired()])
    game_genres = SelectMultipleField('game_genres', coerce=int, validators=[DataRequired()])
    game_directors = SelectMultipleField('game_directors', coerce=int, validators=[Optional()])
    game_companies = SelectMultipleField('game_companies', coerce=int, validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(Add_Game, self).__init__(*args, **kwargs)
        self.game_series.choices = [(0, 'No series')] + [(series.id, series.name) for series in Series.query.all()]
        self.game_genres.choices = [(genre.id, genre.name) for genre in Genre.query.all()]
        self.game_directors.choices = [(director.id, director.name) for director in Director.query.all()]
        self.game_companies.choices = [(company.id, company.name) for company in Company.query.all()]


class Add_Series(FlaskForm):
    series_name = StringField('series_name', validators=[DataRequired(message='Series name cannot be empty')])
    series_submit = SubmitField('Add Series')


class Add_Genre(FlaskForm):
    genre_name = StringField('genre_name', validators=[DataRequired(message='Genre name cannot be empty')])
    genre_submit = SubmitField('Add Genre')


class Add_Company(FlaskForm):
    company_name = StringField('company_name', validators=[DataRequired()])
    company_games = SelectMultipleField('company_games', coerce=int, validators=[Optional()])
    company_directors = SelectMultipleField('company_directors', coerce=int, validators=[Optional()])
    company_founders = SelectMultipleField('company_founders', coerce=int, validators=[Optional()])
    company_series = SelectMultipleField('company_series', coerce=int, validators=[DataRequired()])
    company_time_founded = StringField('company_founded_time', validators=[DataRequired()])
    company_headquarters = StringField('company_headquarters', validators=[DataRequired()])
    company_description = TextAreaField('company_description', validators=[DataRequired()])
    company_picture_1 = FileField('company_picture_1', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    company_picture_2 = FileField('company_picture_2', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])

    def __init__(self, *args, **kwargs):
        super(Add_Company, self).__init__(*args, **kwargs)
        self.company_games.choices = [(game.id, game.name) for game in Videogame.query.all()]
        self.company_directors.choices = [(director.id, director.name)for director in Director.query.all()]
        self.company_founders.choices = [(founder.id, founder.name)for founder in Founder.query.all()]
        self.company_series.choices = [(series.id, series.name)for series in Series.query.all()]


class Add_Directors(FlaskForm):
    director_name = StringField('director_name', validators=[DataRequired()])
    director_age = StringField('director_age', validators=[DataRequired()])
    director_description = TextAreaField('director_description', validators=[DataRequired()])
    director_picture_1 = FileField('director_picture_1', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    director_picture_2 = FileField('director_picture_2', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    director_games = SelectMultipleField('director_games', coerce=int, validators=[Optional()])
    director_companies = SelectMultipleField('director_companies', coerce=int, validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(Add_Directors, self).__init__(*args, **kwargs)
        self.director_games.choices = [(game.id, game.name) for game in Videogame.query.all()]
        self.director_companies.choices = [(company.id, company.name)for company in Company.query.all()]


class Add_Founders(FlaskForm):
    founder_name = StringField('founder_name', validators=[DataRequired()])
    founder_companies = SelectMultipleField('founder_companies', coerce=int, validators=[Optional()])
    founder_date_of_birth = StringField('founder_date_of_birth', validators=[DataRequired()])
    founder_description = TextAreaField('founder_description', validators=[DataRequired()])
    founder_picture_1 = FileField('founder_picture_1', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])
    founder_picture_2 = FileField('founder_picture_2', validators=[DataRequired(), FileAllowed(['jpg'], 'JPG Only!')])

    def __init__(self, *args, **kwargs):
        super(Add_Founders, self).__init__(*args, **kwargs)
        self.founder_companies.choices = [(company.id, company.name) for company in Company.query.all()]