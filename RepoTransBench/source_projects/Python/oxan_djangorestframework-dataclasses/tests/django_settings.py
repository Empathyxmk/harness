SECRET_KEY = "dataclasses"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}
USE_I18N = False
USE_L10N = False
USE_TZ = True