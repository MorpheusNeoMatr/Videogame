from app.routes import db


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())


genre_game = db.Table('genre_game',
    db.Column('videogame_id', db.Integer, db.ForeignKey('videogame.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)


game_company = db.Table('game_company',
    db.Column('videogame_id', db.Integer, db.ForeignKey('videogame.id'), primary_key=True),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'), primary_key=True))


game_director = db.Table('game_director',
    db.Column('videogame_id', db.Integer, db.ForeignKey('videogame.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('director.id'), primary_key=True))


class Videogame(db.Model):
    __tablename__ = "videogame"
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"))
    series = db.relationship("Series", backref="videogames")
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    dev_score = db.Column(db.Text())
    release_date = db.Column(db.Text())
    gameplay = db.Column(db.Text())
    story = db.Column(db.Text())
    soundtrack = db.Column(db.Text())
    reviews = db.Column(db.Text())
    picture_1 = db.Column(db.String(), nullable=True)
    picture_2 = db.Column(db.String(), nullable=True)
    picture_3 = db.Column(db.String(), nullable=True)
    picture_4 = db.Column(db.String(), nullable=True)
    picture_5 = db.Column(db.String(), nullable=True)
    picture_6 = db.Column(db.String(), nullable=True)
    game_genres = db.relationship("Genre", secondary=genre_game, backref=db.backref
                             ('videogame', lazy='dynamic'))
    game_companies = db.relationship("Company", secondary=game_company, backref=db.backref
                                ('videogame', lazy='dynamic'))
    game_directors = db.relationship("Director", secondary=game_director, backref=db.backref
                                     ('videogame', lazy='dynamic'))


company_series = db.Table('company_series',
    db.Column("series_id", db.Integer, db.ForeignKey('series.id'), primary_key=True),
    db.Column("company_id", db.Integer, db.ForeignKey('company.id'), primary_key=True))


class Series(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(5))


company_director = db.Table('company_director',
    db.Column("company_id", db.Integer, db.ForeignKey('company.id'), primary_key=True),
    db.Column("director_id", db.Integer, db.ForeignKey('director.id'), primary_key=True))


founder_company = db.Table('founder_company',
    db.Column("founder_id", db.Integer, db.ForeignKey('founder.id'), primary_key=True),
    db.Column("company_id", db.Integer, db.ForeignKey('company.id'), primary_key=True))


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    time_founded = db.Column(db.Text())
    headquarters = db.Column(db.Text())
    description = db.Column(db.Text())
    picture_1 = db.Column(db.Text())
    picture_2 = db.Column(db.Text())
    company_directors = db.relationship("Director", secondary=company_director, backref=db.backref
                                        ('company', lazy='dynamic'))
    company_founders = db.relationship("Founder", secondary=founder_company, backref=db.backref
                                       ('company', lazy='dynamic'))
    company_games = db.relationship("Videogame", secondary=game_company, backref=db.backref
                                    ('company', lazy='dynamic'))
    company_series = db.relationship("Series", secondary=company_series, backref=db.backref
                                       ('company', lazy='dynamic'))


class Founder(db.Model):
    __tablename__ = "founder"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    date_of_birth = db.Column(db.Text(15))
    description = db.Column(db.Text())
    picture_1 = db.Column(db.Text())
    picture_2 = db.Column(db.Text())
    founder_companies = db.relationship("Company", secondary=founder_company, backref=db.backref
                                       ('founder', lazy='dynamic'))

class Director(db.Model):
    __tablename__ = "director"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    date_of_birth = db.Column(db.Text(15))
    description = db.Column(db.Text())
    picture_1 = db.Column(db.Text())
    picture_2 = db.Column(db.Text())
    videogames = db.relationship("Videogame", secondary=game_director, backref=db.backref('director', lazy='dynamic'))
    companies = db.relationship("Company", secondary=company_director, backref=db.backref('director', lazy='dynamic'))