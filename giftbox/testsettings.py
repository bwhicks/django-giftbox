GIFTBOX_SETTINGS = {
    'type': 'prod',
    'doc_root': 'foo',
    'sendfile_url': '/protected/',
}

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

SECRET_KEY = 'foooooo'
