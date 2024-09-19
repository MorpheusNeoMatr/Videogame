from app.routes import db


# Model representing a user
class Username(db.Model):
    __tablename__ = "Username"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text(), unique=True)
    name = db.Column(db.Text())
    permission = db.Column(db.Integer, default=0)
    admin = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.Text())
    picture = db.Column(db.Text())


# Model representing a genre
class Genre(db.Model):
    __tablename__ = "Genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())


# Association table for the many-to-many relationship between Videogame and Genre
genre_game = db.Table('Genre_game',
db.Column('videogame_id', db.Integer, db.ForeignKey('Videogame.id'), primary_key=True),  # Foreign key to Videogame
db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True) # Foreign key to Genre
)

# Association table for the many-to-many relationship between Videogame and Company
game_company = db.Table('Game_company',
    db.Column('videogame_id', db.Integer, db.ForeignKey('Videogame.id'), primary_key=True),  # Foreign key to Videogame
    db.Column('company_id', db.Integer, db.ForeignKey('Company.id'), primary_key=True))  # Foreign key to Company


# Association table for the many-to-many relationship between Videogame and Director
game_director = db.Table('Game_director',
    db.Column('videogame_id', db.Integer, db.ForeignKey('Videogame.id'), primary_key=True),
    db.Column('director_id', db.Integer, db.ForeignKey('Director.id'), primary_key=True))


class Videogame(db.Model):
    __tablename__ = "Videogame"
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("Series.id"))
    Series = db.relationship("Series", backref="Videogame")
    username_id = db.Column(db.Integer, db.ForeignKey("Username.id"))
    Username = db.relationship("Username", backref="Videogame")
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    dev_score = db.Column(db.Text())
    release_date = db.Column(db.Text())
    gameplay = db.Column(db.Text())
    story = db.Column(db.Text())
    soundtrack = db.Column(db.Text())
    reviews = db.Column(db.Text())
    picture_1 = db.Column(db.Text(), nullable=True)
    picture_2 = db.Column(db.Text(), nullable=True)
    picture_3 = db.Column(db.Text(), nullable=True)
    picture_4 = db.Column(db.Text(), nullable=True)
    picture_5 = db.Column(db.Text(), nullable=True)
    picture_6 = db.Column(db.Text(), nullable=True)
    game_genres = db.relationship("Genre", secondary=genre_game, backref=db.backref
                             ('Videogame', lazy='dynamic'))
    game_companies = db.relationship("Company", secondary=game_company, backref=db.backref
                                ('Videogame', lazy='dynamic'))
    game_directors = db.relationship("Director", secondary=game_director, backref=db.backref
                                     ('Videogame', lazy='dynamic'))


company_series = db.Table('Company_series',
    db.Column("series_id", db.Integer, db.ForeignKey('Series.id'), primary_key=True),
    db.Column("company_id", db.Integer, db.ForeignKey('Company.id'), primary_key=True))


class Series(db.Model):
    __tablename__ = "Series"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())


company_director = db.Table('Company_director',
    db.Column("company_id", db.Integer, db.ForeignKey('Company.id'), primary_key=True),
    db.Column("director_id", db.Integer, db.ForeignKey('Director.id'), primary_key=True))


founder_company = db.Table('founder_company',
    db.Column("founder_id", db.Integer, db.ForeignKey('Founder.id'), primary_key=True),
    db.Column("company_id", db.Integer, db.ForeignKey('Company.id'), primary_key=True))


class Company(db.Model):
    __tablename__ = "Company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    time_founded = db.Column(db.Text())
    username_id = db.Column(db.Integer, db.ForeignKey("Username.id"))
    Username = db.relationship("Username", backref="Company")
    headquarters = db.Column(db.Text())
    description = db.Column(db.Text())
    picture_1 = db.Column(db.Text())
    picture_2 = db.Column(db.Text())
    company_directors = db.relationship("Director", secondary=company_director, backref=db.backref
                                        ('Company', lazy='dynamic'))
    company_founders = db.relationship("Founder", secondary=founder_company, backref=db.backref
                                       ('Company', lazy='dynamic'))
    company_games = db.relationship("Videogame", secondary=game_company, backref=db.backref
                                    ('Company', lazy='dynamic'))
    company_series = db.relationship("Series", secondary=company_series, backref=db.backref
                                       ('Company', lazy='dynamic'))


class Founder(db.Model):
    __tablename__ = "Founder"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    date_of_birth = db.Column(db.Text(15))
    username_id = db.Column(db.Integer, db.ForeignKey("Username.id"))
    Username = db.relationship("Username", backref="Founder")
    description = db.Column(db.Text())
    picture_1 = db.Column(db.Text())
    picture_2 = db.Column(db.Text())
    founder_companies = db.relationship("Company", secondary=founder_company, backref=db.backref
                                       ('Founder', lazy='dynamic'))


class Director(db.Model):
    __tablename__ = "Director"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    date_of_birth = db.Column(db.Text(15))
    username_id = db.Column(db.Integer, db.ForeignKey("Username.id"))
    Username = db.relationship("Username", backref="Director")
    description = db.Column(db.Text())
    picture_1 = db.Column(db.Text())
    picture_2 = db.Column(db.Text())
    videogames = db.relationship("Videogame", secondary=game_director, backref=db.backref('Director', lazy='dynamic'))
    companies = db.relationship("Company", secondary=company_director, backref=db.backref('Director', lazy='dynamic'))