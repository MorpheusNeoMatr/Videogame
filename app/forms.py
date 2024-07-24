from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField,SelectField, SelectMultipleField, FileField, SubmitField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models
from app.models import Series,Director,Genre,Company
from datetime import datetime


class Add_Game(FlaskForm):
    game_name = StringField('game_name', validators=[DataRequired()])
    game_dev_score = StringField('game_dev_score', validators=[DataRequired()])
    game_date = StringField('game_date', validators=[DataRequired()])
    game_description = TextAreaField('game_description', validators=[DataRequired()])
    game_gameplay = TextAreaField('game_gameplay', validators=[DataRequired()])
    game_story = TextAreaField('game_story', validators=[DataRequired()])
    game_soundtrack = TextAreaField('game_soundtrack', validators=[DataRequired()])
    game_reviews = TextAreaField('game_reviews', validators=[DataRequired()])
    game_picture_1 = FileField('game_picture_1', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    game_picture_2 = FileField('game_picture_2', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    game_picture_3 = FileField('game_picture_3', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    game_picture_4 = FileField('game_picture_4', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    game_picture_5 = FileField('game_picture_5', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    game_picture_6 = FileField('game_picture_5', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
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


class Add_series(FlaskForm):
    series_name = StringField('series_name', validators=[DataRequired()])
    submit = SubmitField('Add series')

class Add_Directors(FlaskForm):
    director_name = StringField('director_name', validators=[DataRequired()])
    director_age = StringField('director_age', validators=[DataRequired()])
    director_resume = TextAreaField('director_resume', validators=[DataRequired()])
    director_description = TextAreaField('director_description', validators=[DataRequired()])
    director_picture_1 = FileField('director_picture_1', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    director_picture_2 = FileField('director_picture_2', validators=[FileAllowed(['jpg', 'png'], 'Images Only!')])
    