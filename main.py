"""Main Flask Server Program"""
from flask import Flask, flash,  make_response, redirect, request, render_template, url_for
from flask_restful import Api

import server.keys

from server.db.get_establishment import get_establishment
from server.db.session import session as db_session
from server.db.tables import Establishment, Request
from server.form.set_establishment import SetEstablishment
from server.form.register import RegisterEstablishment, verify_recaptcha
from server.api.player import PlayerAPI
from server.api.youtube_search import YouTubeSearchAPI
from server.request.get_currently_playing import get_currently_playing
from server.request.get_requests import get_requests
from server.request.new_requester_id import new_requester_id
from server.request.validate_request import validate_request
from server.request.youtube_list import youtube_list

APP = Flask(__name__)
API = Api(APP)
APP.secret_key = server.keys.APP_SECRET_KEY

PRODUCT_NAME = 'shitsnack'
RECAPTCHA_SECRET = server.keys.RECAPTCHA_SECRET
COOKIE_MAX_AGE = 60*60*3

@APP.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new establishment."""
    if request.method == 'POST':

        form = RegisterEstablishment(request.form)

        recaptcha = {'secret': RECAPTCHA_SECRET,
                     'response': request.form.get('g-recaptcha-response'),
                     'remoteip': request.remote_addr
                    }

        if form.validate() and verify_recaptcha(**recaptcha):
            session = db_session()
            session.add(Establishment(**form.data))
            session.commit()
            session.close()
            return 'OK'
        else:
            return render_template('register.html',
                                   product_name=PRODUCT_NAME,
                                   page_name='Register',
                                   form=form)

    else:
        return render_template('register.html',
                               PRODUCT_NAME=PRODUCT_NAME,
                               page_name='Register',
                               form=RegisterEstablishment())

@APP.route('/')
def request_music():
    """Request Music"""
    if 'establishment_id' in request.cookies:
        requests = get_requests(request.cookies['establishment_id'])
        currently_playing = get_currently_playing(request.cookies['establishment_id'])
    elif 'pulsepicks.net' in request.headers['Host']:
        requests = get_requests(1)
        currently_playing = get_currently_playing(1)
    else:
        requests = None
        currently_playing = None


    response = make_response(render_template('request_music.html',
                                             product_name=PRODUCT_NAME,
                                             page_name='Request Music',
                                             currently_playing=currently_playing,
                                             requests=requests,
                                             cookies=request.cookies))



    if 'requester_id' not in request.cookies:
        response.set_cookie('requester_id', str(new_requester_id()), max_age=COOKIE_MAX_AGE)
        response.set_cookie('establishment_id', '0')
    if 'pulsepicks.net' in request.headers['Host']:
        response.set_cookie('establishment_id', '1')
    return response

@APP.route('/request/<int:establishment_id>/<string:video_id>')
def submit_request(establishment_id, video_id):
    """Submits the request."""

    if 'requester_id' in request.cookies:
        if 'establishment_id' not in request.cookies or request.cookies['establishment_id'] == '0':
            response = make_response(redirect(url_for('set_establishment')))
            response.set_cookie('video_id', video_id)
            return response
        
        request_valid, message = validate_request(request.cookies['requester_id'],
                                                  establishment_id,
                                                  video_id)

        if request_valid:
            session = db_session()
            session.add(Request(establishment_id=establishment_id,
                                requester_id=request.cookies['requester_id'],
                                video_id=video_id,
                                state=0))
            session.commit()
            session.close()
            flash(message, 'success')

        else:
            flash(message, 'error')

    else:
        flash('No cookies set. Please ensure cookies are enabled!', 'error')

    return redirect(url_for('request_music'))

@APP.route('/skip/<int:establishment_id>/<string:video_id>')
def skip(establishment_id, video_id):
    """Skip the request."""

    title = youtube_list([video_id])[0]['title']

    session = db_session()
    session.query(Request).filter_by(establishment_id=establishment_id,
                                     video_id=video_id).\
                                     update({'state': 3})
    session.commit()
    session.close()
    message = u'Skipped {title}!'.format(title=title)
    flash(message, 'success')

    return redirect(url_for('request_music'))

@APP.route('/ban/<int:establishment_id>/<string:video_id>')
def ban(establishment_id, video_id):
    """Ban the request."""

    title = youtube_list([video_id])[0]['title']

    session = db_session()
    session.query(Request).filter_by(establishment_id=establishment_id,
                                     video_id=video_id).\
                                     update({'state': 4})
    session.commit()
    session.close()
    message = u'Banned {title}!'.format(title=title)
    flash(message, 'success')

    return redirect(url_for('request_music'))

@APP.route('/establishment', methods=['GET', 'POST'])
def set_establishment():
    """Set the establishment cookie"""
    if request.method == 'POST':
        form = SetEstablishment(request.form)
        if form.validate():
            establishment = get_establishment(name=form.name.data)
            if establishment:
                url = url_for('submit_request', establishment_id=establishment['id'], video_id=request.cookies['video_id'])
                response = make_response(redirect(url))
                response.set_cookie('establishment_id', str(establishment['id']), max_age=60*60*3)
                return response
    else:
        return render_template('establishment.html',
                               PRODUCT_NAME=PRODUCT_NAME,
                               page_name='Establishment',
                               form=SetEstablishment())


@APP.route('/player/<int:establishment_id>')
def player(establishment_id):
    """Loads the music player."""
    return render_template('player.html', establishment_id=establishment_id)

API.add_resource(PlayerAPI, '/player/<int:establishment_id>/<string:action>',
                 '/player/<int:establishment_id>/<string:action>/<string:video_id>')

API.add_resource(YouTubeSearchAPI, '/youtube_search/<string:search_term>')
