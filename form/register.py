"""Establishment Registration Form Setup."""

from sqlalchemy.sql import exists
import requests

from wtforms import Form, BooleanField, IntegerField, SelectField, StringField, PasswordField, validators, ValidationError
from db.session import session as db_session
from db.tables import Establishment



def establishment_registered(form, field):
    """Validates if the establishment has already been registered."""
    form = form
    name = field.data
    session = db_session()
    result = session.query(exists().where(Establishment.name == name)).scalar()
    session.close()
    if result:
        raise ValidationError('Establishment {name} is already registered!'.format(name=name))

def verify_recaptcha(secret, response, remoteip=None):
    """Verify the Google reCAPTCHA."""
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {'secret': secret, 'response': response}
    if remoteip:
        data['remoteip'] = remoteip
    request = requests.post(verify_url, data=data)
    return request.json()['success']

class RegisterEstablishment(Form): # pylint: disable=R0903
    """Define the establishment registration form."""
    name = StringField('Establishment Name',
                       [validators.InputRequired(), establishment_registered],
                       render_kw={'onFocus': 'geolocate()',
                                  'placeholder': 'Start typing the name of your establishment...'})
    password = PasswordField('Set Music Control Password',
                             [validators.InputRequired(),
                              validators.EqualTo('confirm', message='Passwords must match.')],
                             render_kw={'placeholder': 'Needed to control the music requests.'})
    confirm = PasswordField('Confirm Password')
    request_limit = IntegerField('Requests Allowed Per Person',
                                 [validators.required()],
                                 default=3)
    repeat_limit = IntegerField('Requests To Play Before Repeats Are Allowed',
                                [validators.required()],
                                default=10)
    request_duration_limit = IntegerField('Maximum Length Of A Request In Seconds',
                                          [validators.required()],
                                          default=600)
    requester_safesearch = SelectField('Filter Out Mature Content When People Make Requests',
                                       choices=[('none', 'No Filter'),
                                                ('moderate', 'Moderate Filter'),
                                                ('strict', 'Strict Filter')],
                                       default='moderate')
    autoplay_safesearch = SelectField('Filter Out Mature Content When Music Is Randomly Selected',
                                      choices=[('none', 'No Filter'),
                                      ('moderate', 'Moderate Filter'),
                                      ('strict', 'Strict Filter')],
                                      default='moderate')
    tos_message = 'To use this service you must accept the Terms of Service.'
    tos_accepted = BooleanField('I have read and accept the Terms of Service.',
                                [validators.AnyOf([True], message=tos_message)])
