import os
import re

from fabric.api import local, task, lcd
from babel.messages.pofile import read_po, write_po


@task
def manage(command):
    """Run ./manage.py command"""

    local('./manage.py {}'.format(command))


@task
def run(host='127.0.0.1', port=8000):
    """Start uwsgi development server"""

    manage('runserver {}:{}'.format(host, port))


@task
def clear():
    """Clear temporary files"""

    local(
        "find . -name '~*' -or -name '*.pyo' -or -name '*.pyc' "
        "-or -name '__pycache__' -or -name 'Thubms.db' "
        "| xargs -I {} rm -vrf '{}'")


@task
def subl():
    """Start sublime editor"""

    local('subl project.sublime-project')


@task
def install():
    """Install pip requirements"""

    with lcd('requirements'):
        local('pip install -r development.txt')


def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)


@task
def locale(action='make', lang='en'):
    """Make messages, and compile messages for listed apps"""

    apps = []
    apps = local('cd app/components/ && ls -d */', capture=True)
    apps = apps.split()
    apps = map(lambda a: 'app.components.{}'.format(a), apps)

    if action == 'make':
        for app, app_path in apps:
            app_path = os.path.join(*app.split('.'))

            with lcd(app_path):
                po_path = os.path.join(
                    app_path, 'locale', lang, 'LC_MESSAGES', 'django.po')
                if not os.path.exists(po_path):
                    local('django-admin.py makemessages -l {}'.format(lang))

                with open(po_path, 'rb') as f:
                    catalog = read_po(f)
                    for message in catalog:
                        message.id = lreplace(
                            '{}:'.format(app), '', message.id)

                with open(po_path, 'wb') as f:
                    write_po(f, catalog, include_previous=True)
                local('django-admin.py makemessages -l {}'.format(lang))

                with open(po_path, 'rb') as f:
                    catalog = read_po(f)
                    for message in catalog:
                        if lang == 'en':
                            message.string = str(message.id)
                        message.id = '{}:{}'.format(app, message.id)
                with open(po_path, 'wb') as f:
                    write_po(f, catalog, include_previous=True)
    elif action == 'compile':
        for app, app_path in apps:
            with lcd(app_path):
                local('django-admin.py compilemessages -l {}'.format(lang))
    else:
        print(
            'Invalid action: {}, available actions: "make"'
            ', "compile"'.format(action))


@task
def bootstrap_db():
    """ Bootstrap initial database with project user and permissions """
    local('sh scripts/bootstrap_db.sh')


@task
def init():
    """ Create postgres database, migrate and create user """

    bootstrap_db()

    manage('migrate')
    manage('createsuperuser')
