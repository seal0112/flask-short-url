from . import db
import datetime


class ShortUrl(db.Model):
    __tablename__ = 'short_url'
    alias = db.Column(db.String(20), primary_key=True)
    origin = db.Column(db.Text, unique=True, nullable=False)


class Statistic(db.Model):
    __tablename__ = 'statistic'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(
        db.Date, nullable=False,
        default=datetime.datetime.now().strftime("%Y-%m-%d"))
    count = db.Column(db.Integer)
    alias = db.Column(
        db.String(20), db.ForeignKey('short_url.alias'), nullable=False)