from fabric.api import local, run, env, cd
from fabric.contrib.console import confirm
from fabric.contrib.files import sed
from fabric.utils import fastprint
from fabric.state import output
from fabric.operations import prompt
from studio.settings import DATABASES
import os

BASE_DIR = os.path.dirname(__file__)
PROJECT_DIRNAME = os.path.basename(os.path.dirname(__file__))
VENVS_DIRNAME = u"{}/venvs".format(os.path.dirname(BASE_DIR))
VASSALS = u"{}/vassals".format(os.path.dirname(BASE_DIR))

output['everything'] = False
port = '22'
host = ''
env.hosts = ['%s:%s' % (host,port)]
project_dir = 'www/studio'
prod_project_dir = 'www/studio'

templates_dir = 'templates'
static_dir = 'static'
analysis_dir = 'analysis'

db_local = DATABASES['local']
db_remote = DATABASES['remote']


def configure_project():
    output[u'everything'] = True
    venv = prompt(
        u'Specifica il percorso della directory per il virtualenv oppure lascia vuoto per installarlo dentro {}'.format(
            VENVS_DIRNAME))
    if not venv:
        venv = VENVS_DIRNAME
    vassals = prompt(u'Specifica il percorso della directory per i vassals oppure lascia vuoto per usare {}'.format(
        VASSALS))
    if not vassals:
        vassals = VASSALS

    if not os.path.exists(u"{}/{}".format(venv, PROJECT_DIRNAME)):
        local(u"virtualenv {}/{}".format(venv, PROJECT_DIRNAME))
        local(u"{}/{}/bin/pip install -r {}/requirements.txt".format(venv, PROJECT_DIRNAME, BASE_DIR))
    if not os.path.exists(u'templates'):
        local(u'mkdir templates')
    if not os.path.exists(u'static'):
        local(u'mkdir static')
    if not os.path.exists(u'media'):
        local(u'mkdir media')
    if not os.path.exists(u'{}/{}.ini'.format(vassals, PROJECT_DIRNAME)):
        local(u'ln -s {}/{}.ini {}/{}.ini'.format(BASE_DIR, PROJECT_DIRNAME, vassals, PROJECT_DIRNAME))

    how_db = prompt(u'Digita 1 per creare il db, 2 per scaricarlo dal server oppure lascia vuoto per non fare nulla!')
    if how_db == "1":
        create_db()
    elif how_db == "2":
        db_from_server()


def gitclone(repository):
    output['everything'] = True
    local(u'git init')
    local(u'git add -A')
    local(u"git commit -m 'first commit'")
    local(u'git remote add origin {}'.format(repository))
    local(u'git push -u origin master')


def fastpush(message):
    output['everything'] = True
    local("git add -A")
    local("git commit -m '%s'" % message)
    local("git push")
    with cd(project_dir):
        run("git pull")


def serverpull():
    output['everything'] = True
    with cd(prod_project_dir):
        run("git pull")


def prodpull():
    output['everything'] = True
    with cd(project_dir):
        run("git pull")


def fp(message):
    output['everything'] = True
    fastpush(message=message)


def synclayout(message="Update templates and static"):
    output['everything'] = True
    local("git add -A -- %s %s" % (templates_dir, static_dir))
    local("git commit -m '%s' -- %s %s" % (message, templates_dir, static_dir))
    local("git push")
    with cd(project_dir):
        run("git pull")


def sl(message="Update templates and static"):
    output['everything'] = True
    synclayout(message=message)


def media_to_server(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Stai sovrascrivendo tutti i file contenuti in /media/ sul server con quelli in locale. Vuoi procedere? "):
        local("rsync -av --progress --inplace --rsh='ssh -p%s' %s:%s/media/ ./media/" % (port, host, project_dir))
        fastprint(u"Ricordati che sincronizzando i file media e' necessario sincronizzare anche il database con il comando 'fab db_to_server'.")


def media_from_server(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Stai sovrascrivendo tutti i file contenuti in /media/ in locale con quelli sul server. Vuoi procedere? "):
        local("rsync -av --progress --inplace --rsh='ssh -p%s' %s:%s/media/ ./media/" % (port, host, project_dir))
        fastprint(u"Ricordati che sincronizzando i file media e' necessario sincronizzare anche il database con il comando 'fab db_from_server'.")


def bkp_to_server(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Stai sovrascrivendo tutti i file contenuti in /bkp/ sul server con quelli in locale. Vuoi procedere? "):
        local("rsync -av --progress --inplace ./bkp/ %s:%s/bkp/" % (host, project_dir))
        fastprint(u"Operazione completata.")


def db_from_server(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Attenzione, in questo modo tutti i dati presenti sul database del tuo computer verranno sovrascritti con quelli del database remoto. Sei sicuro di voler procedere?"):
        with cd(project_dir):
            if "postgresql_psycopg2" in db_local['ENGINE']:
                print (u'- Engine Postgres')
                run("python dbdump.py")
                local("scp -P %s %s:%s/tempdump.sql tempdump.sql" % (port, host,project_dir))
                run("rm tempdump.sql")
                local('psql -h %s -p %s -U postgres -c "select pg_terminate_backend(pid) from pg_stat_activity where datname = \'%s\';"' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                local('dropdb --if-exists -h %s -p %s -U postgres %s' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                print (u'- Database %s eliminato' % db_local['NAME'])
                local('createdb -h %s -p %s -U postgres %s' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                print (u'- Database %s creato. carico il dump' % db_local['NAME'])
                if debug:
                    local('psql -h %s -p %s -U postgres -x -e -E -w -d %s -f tempdump.sql -L /dev/null' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                else:
                    local('psql -h %s -p %s -U postgres --output=/dev/null -q -t -w -d %s -f tempdump.sql -L /dev/null' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
                local('rm tempdump.sql')
            elif "sqlite" in db_remote['ENGINE']:
                fastprint(u'- Engine SQLite')
                local("scp -P %s %s:%s/%s %s" % (port, host, project_dir, db_remote['NAME'], db_local['NAME']))


def create_db(debug=True):
    if debug:
        output['everything'] = True
    if confirm("Attenzione, stai creando il db. Sei sicuro di voler procedere?"):
        if "postgresql_psycopg2" in db_local['ENGINE']:
            local('createdb -h %s -p %s -U postgres %s' % (db_local['HOST'], db_local['PORT'], db_local['NAME']))
            print (u'- Database %s creato. carico il dump' % db_local['NAME'])


def touch():
    with cd(project_dir):
        run("touch uwsgi.ini")