"""Additional Request Information"""

from wtforms import Form, StringField, PasswordField, HiddenField



class SetAdditionalRequestInformation(Form): # pylint: disable=R0903
    """Add additional request information."""
    performer = StringField('Performer (Optional)',
                               render_kw={'placeholder': 'The person who will be performing karaoke...'})
    requested_by = StringField('Music Requester (Optional)',
                               render_kw={'placeholder': 'The person who requested the music...'})
    '''dedicated_to = StringField('Dedicated To (Optional)',
                               render_kw={'placeholder': 'The person who this song is dedicated to...'})'''