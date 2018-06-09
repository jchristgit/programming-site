from .common import *  # noqa


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['programming.im'])
SECRET_KEY = env('SECRET_KEY')
STATIC_ROOT = env('STATIC_ROOT')
