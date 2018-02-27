SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'e_ood_django',
    "tests",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    }
}
