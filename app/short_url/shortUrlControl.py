from flask import request, jsonify, make_response, redirect
from ..model import ShortUrl, Statistic
from ..core import getShort, createShortUrl, addRedirectHitCount
from .. import db
from . import short_url
import os
import datetime
import json
from sqlalchemy.sql import func


@short_url.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        data = json.loads(request.data)
        origin = data['origin']
        if 'alias' not in data:
            alias = getShort(origin)
            return createShortUrl(origin, alias)
        else:
            alias = data['alias']
            shortUrl = db.session.query(ShortUrl).filter_by(
                alias=alias).one_or_none()
            if shortUrl is not None:
                return make_response(json.dumps('alias collision'), 400)
            else:
                return createShortUrl(origin, alias)
    else:
        shortUrls = db.session().query(ShortUrl).all()
        shortUrls = [url.serialize for url in shortUrls]
        return jsonify(shortUrls)


@short_url.route('/<token>')
def getRedirect(token):
    origin = db.session.query().with_entities(
        ShortUrl.origin.label('origin')).filter_by(alias=token).one_or_none()
    if origin is not None:
        addRedirectHitCount(token)
        return redirect(origin[0])
    else:
        return make_response(
            json.dumps("Couldn't find long url for {}".format(token)), 404)


@short_url.route('/top-three-visited')
def getTop3Alias():
    subq = db.session\
        .query(
            Statistic.alias.label('alias'),
            func.sum(Statistic.count).label('count'))\
        .group_by(Statistic.alias)\
        .order_by(Statistic.count.desc())\
        .limit(3).subquery()
    top3HitCount = db.session\
        .query(
            (
                'http://'+os.getenv('IP')+
                ':'+os.getenv('PORT')+'/'+ShortUrl.alias
            ).label('alias'),
            ShortUrl.origin,
            subq.c.count)\
        .join(subq)\
        .order_by(subq.c.count).all()

    top3HitCount = [row._asdict() for row in top3HitCount]
    return jsonify(top3HitCount)


@short_url.route('/hit-count/<token>')
def getHitCount(token):
    subq = db.session\
        .query(
            Statistic.alias.label('alias'),
            func.sum(Statistic.count).label('count'))\
        .group_by(Statistic.alias)\
        .having(Statistic.alias==token).subquery()

    hitCount = db.session\
        .query(
            (
                'http://'+os.getenv('IP')+
                ':'+os.getenv('PORT')+'/'+ShortUrl.alias
            ).label('alias'),
            ShortUrl.origin,
            subq.c.count)\
        .join(subq).one_or_none()
    if hitCount is not None:
        hitCount = hitCount._asdict()
        return jsonify(hitCount)
    else:
        return jsonify(hitCount)


@short_url.route('/hit-count-group-by-date')
def getHitCountGroupByDate():
    date = db.session().query(Statistic.date).group_by(Statistic.date).all()
    result = []
    for d in date:
        subq = db.session().query()
        values = db.session()\
            .query(ShortUrl)\
            .with_entities(
                (
                    'http://'+os.getenv('IP')+
                    ':'+os.getenv('PORT')+'/'+ShortUrl.alias
                ).label('alias'),
                Statistic.count,
                ShortUrl.origin)\
            .join(Statistic)\
            .filter_by(date=d[0])\
            .order_by(Statistic.count).all()
        values = [vaule._asdict() for vaule in values]
        data = {
            'Date': d[0].strftime("%Y-%m-%d"),
            'Values': values
        }
        result.append(data)
    return jsonify(result)
