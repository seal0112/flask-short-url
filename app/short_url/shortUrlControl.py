from flask import request, jsonify, make_response
from ..model import (
    ShortUrl, Statistic
)
from .. import db
from . import short_url

@short_url.route('/')
def main():
    pass
    return "Hello"