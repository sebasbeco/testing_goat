import random
import string

from fabric.contrib.files import append, exists
from fabric.api import cd, local, run

# ssh-add ~/Documents/MyKeyPair.pem



REPO_URL = 'https://github.com/sebasbeco/testing_goat.git'


def deploy(site):
    site_folder = f'/home/ubuntu/sites/{site}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv(site)
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        run(f'python3 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')


def _create_or_update_dotenv(site):
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={site}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        secret_key = ''.join(random.SystemRandom().choices(
            string.ascii_lowercase + string.digits, k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={secret_key}')


def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput')