"""Main Flask Server Program"""
from flask import Flask, flash,  make_response, redirect, request, render_template, url_for
from flask_restful import Api

import keys

from db.get_establishment import get_establishment
from db.session import session as db_session
from db.tables import Establishment, Request, AdditionalRequestInformation
from form.additional_request_information import SetAdditionalRequestInformation
from form.set_establishment import SetEstablishment
from form.register import RegisterEstablishment, verify_recaptcha
from api.player import PlayerAPI
from api.youtube_search import YouTubeSearchAPI
from request.calculate_yei_points import calculate_yei_points
from request.get_currently_playing import get_currently_playing
from request.get_all_requests import get_all_requests
from request.get_requests import get_requests
from request.new_requester_id import new_requester_id
from request.validate_request import validate_request
from request.youtube_list import youtube_list

APP = Flask(__name__)
API = Api(APP)
APP.secret_key = keys.APP_SECRET_KEY

PRODUCT_NAME = 'shitsnack'
RECAPTCHA_SECRET = keys.RECAPTCHA_SECRET
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
        establishment = get_establishment(request.cookies['establishment_id'])
    elif 'pulsepicks.net' in request.headers['Host']:
        requests = get_requests(1)
        currently_playing = get_currently_playing(1)
        establishment = get_establishment(1)
    else:
        requests = None
        currently_playing = None
        establishment = None

    page_name = 'Request Music'
    response = make_response(render_template('request_music.html',
                                             product_name=PRODUCT_NAME,
                                             page_name=page_name,
                                             currently_playing=currently_playing,
                                             requests=requests,
                                             establishment=establishment,
                                             cookies=request.cookies))

    if 'requester_id' not in request.cookies:
        response.set_cookie('requester_id', str(new_requester_id()), max_age=COOKIE_MAX_AGE)
        response.set_cookie('establishment_id', '0')
    if 'pulsepicks.net' in request.headers['Host']:
        response.set_cookie('establishment_id', '1')
    return response

@APP.route('/request/<int:establishment_id>/<string:mode>/<string:video_id>')
def submit_request(establishment_id, mode, video_id):
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
            if mode in ['karaoke']:
                flash(message, 'success')
                return redirect(url_for('additional_request_information', establishment_id=establishment_id, video_id=video_id))

            else:
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

@APP.route('/additional_request_information/<int:establishment_id>/<string:video_id>', methods=['GET', 'POST'])
def additional_request_information(establishment_id, video_id):
    """Add additional request information."""
    if request.method == 'POST':

        form = SetAdditionalRequestInformation(request.form)

        if form.validate():
            with open("/tmp/yei", "a") as yei_file:
                points = calculate_yei_points()
                yei_file.write('{points},{form_data}\n'.format(points=points, form_data=str(form.data)))
                # flash('{points} YEI points will be given to {performer}!'.format(points=points, performer=str(form.performer.data)), 'success')
            session = db_session()
            record = Request(establishment_id=establishment_id,
                             requester_id=request.cookies['requester_id'],
                             video_id=video_id,
                             state=0)
            session.add(record)
            session.flush()
            request_id = record.id
            session.add(AdditionalRequestInformation(request_id=request_id, **form.data))
            current_request_made_by_human = session.query(Request).filter(Request.establishment_id == establishment_id,
                                                                 Request.state == 1,
                                                                 Request.requester_id != 0).count()
            if not current_request_made_by_human:
                session.query(Request).filter(Request.establishment_id == establishment_id,
                                              Request.state == 1)\
                                             .update({'state': 3}, synchronize_session=False)
            session.commit()
            session.close()
            return redirect(url_for('request_music'))

        else:
            return render_template('additional_request_information.html',
                                   product_name=PRODUCT_NAME,
                                   page_name='Additional Request Information',
                                   form=form)

    else:
        return render_template('additional_request_information.html',
                               PRODUCT_NAME=PRODUCT_NAME,
                               page_name='Additional Request Information',
                               form=SetAdditionalRequestInformation())

@APP.route('/skip/<int:establishment_id>/<string:video_id>')
def skip(establishment_id, video_id):
    """Skip the request."""

    title = youtube_list([video_id])[0]['title']

    session = db_session()
    session.query(Request).filter(Request.establishment_id == establishment_id,
                                  Request.video_id == video_id,
                                  Request.state.in_((0, 1)))\
                        .update({'state': 3}, synchronize_session=False)
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
    session.query(Request).filter(Request.establishment_id == establishment_id,
                                  Request.video_id == video_id)\
                                  .update({'state': 4}, synchronize_session=False)
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

@APP.route('/requests/<int:establishment_id>')
def requests(establishment_id):
    """List Requests"""
    all_requests = get_all_requests(establishment_id)
    all_requests.sort(key=lambda k: k['title'])

    return render_template('requests.html',
                           product_name=PRODUCT_NAME,
                           page_name='Requests',
                           establishment_id=establishment_id,
                           requests=all_requests)

@APP.route('/player/<int:establishment_id>')
def player(establishment_id):
    """Loads the music player."""
    return render_template('player.html', establishment_id=establishment_id)

API.add_resource(PlayerAPI, '/player/<int:establishment_id>/<string:action>',
                 '/player/<int:establishment_id>/<string:action>/<string:video_id>')

API.add_resource(YouTubeSearchAPI, '/youtube_search/<string:search_term>')
