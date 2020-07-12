from . import db
import datetime
import os


class ShortUrl(db.Model):
    __tablename__ = 'short_url'
    alias = db.Column(db.String(20), primary_key=True, index=True)
    origin = db.Column(db.Text, nullable=False)

    @property
    def serialize(self):
        res = {}
        for attr, val in self.__dict__.items():
            if attr == '_sa_instance_state':
                continue
            elif attr == 'alias':
                res[attr] = 'http://'\
                    +os.getenv('IP')+':'+os.getenv('PORT')+'/'+val
            else:
                res[attr] = val
        return res


class Statistic(db.Model):
    __tablename__ = 'statistic'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(
        db.Date, nullable=False,
        default=datetime.datetime.now().strftime("%Y-%m-%d")
        ,index=True)
    count = db.Column(db.Integer)
    alias = db.Column(
        db.String(20), db.ForeignKey('short_url.alias'),
        nullable=False, index=True)
