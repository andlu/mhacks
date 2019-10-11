"""mhacks development configuration."""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (
    b',{H1vY\x97\xb1\xbc\xd08\x8b\x17\xa0'
    b'\xd7\xe8\xb8\xcf\xd9\x19\xa8I\xa3\xa8'
)
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/mhacks.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'mhacks.sqlite3'
)

DEBUG = False
