from flask import jsonify, make_response
import hashlib
import base62
import datetime
import json
from . import db
from .model import ShortUrl, Statistic


def getShort(url):
    return base62.encodebytes(hashlib.md5(url.encode('utf-8')).digest()[-5:])


def createShortUrl(origin, alias):
    shortUrl = db.session.query(ShortUrl).filter_by(
        alias=alias).one_or_none()
    if shortUrl is None:
        try:
            shortUrl = ShortUrl()
            shortUrl.alias = alias
            shortUrl.origin = origin
            db.session.add(shortUrl)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print("{}: {}".format(alias, ex))
            return make_response(json.dumps('error'), 500)
        else:
            return make_response(json.dumps('create'), 201)
    else:
        return make_response(json.dumps('Ok'), 200)


def addRedirectHitCount(alias):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    aliasStatistic = db.session().query(Statistic).filter_by(
        alias=alias).filter_by(date=today).one_or_none()
    if aliasStatistic is not None:
        try:
            aliasStatistic.count = aliasStatistic.count+1
            db.session.add(aliasStatistic)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print("{}: {}".format(alias, ex))
            return make_response(json.dumps('error1'), 500)
    else:
        try:
            statistic = Statistic()
            statistic.date = datetime.datetime.strptime(today, "%Y-%m-%d").date()
            statistic.count = 1
            statistic.alias = alias
            db.session.add(statistic)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            print("{}: {}".format(alias, ex))
            return make_response(json.dumps('error'), 500)