import requests

from wtforms import Form, StringField, validators


class SetEstablishment(Form): # pylint: disable=R0903
    """Define the establishment registration form."""
    name = StringField('Establishment Name',
                       [validators.InputRequired()],
                       render_kw={'onFocus': 'geolocate()',
                                  'placeholder': 'Where are you listening to music?'})