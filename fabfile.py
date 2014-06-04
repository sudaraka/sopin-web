#  fabfile.py: Fabric script for deploying sopin
#
#  Copyright 2014 Sudaraka Wijesinghe <sudaraka.org/contact>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""" Fabric script for deploying sopin """

import random
import re
import sys

from fabric.api import local, run, hide, env
from fabric.contrib.files import sed


REPO = 'https://github.com/sudaraka/sopin-web'


def deploy(version=''):
    """ Execute complete deployment process """

    if env.key_filename is None:
        env.key_filename = '~/.keys/private/ssh-sopin-deploy.key'

    git_ref = _verify_local_version(version)

    site_root = '/home/%s/%s' % (env.user, env.host)

    _init_directories(site_root)

    _backup_current_site(site_root)

    _get_source_from_git(site_root + '/src', git_ref)

    _install_dependencies(site_root)

    _setup_site(site_root, git_ref)


def _setup_site(root, ref):
    """ Initialize static content, database and configuration """

    run('%s/bin/python %s/src/manage.py collectstatic --noinput' %
        (root, root))
    run('%s/bin/python %s/src/manage.py syncdb --migrate --noinput' %
        (root, root))

    http_conf = '%s/src/httpd.conf' % root
    sed(http_conf, '%ROOT%', root)
    sed(http_conf, '%SITE_PACKAGES%',
        run('find %s/lib -type d -name site-packages' % root))
    sed(http_conf, '%USER%', env.user)
    sed(http_conf, '%HOST_NAME%', env.host)
    sed(http_conf, '%IP_ADDR%',
        run('dig %s +short|tail -n1' % env.host))

    ver = re.split(r'[-.]', ref[1:])

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-='
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))

    settings_file = '%s/src/app/settings.py' % root
    sed(settings_file, 'DEBUG =.+$', 'DEBUG = False')
    sed(settings_file, 'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % env.host)
    sed(settings_file, 'SECRET_KEY =.+$', 'SECRET_KEY = "%s"' % key)
    sed(settings_file, 'VERSION =.+$', 'VERSION = (%s, %s, "%s")' % tuple(ver))


def _install_dependencies(root):
    """
    Setup python virtual environment and install modules from requirements.txt

    """

    run('virtualenv -p python3 %s' % root)
    run('%s/bin/pip install -r %s/src/requirements.txt' % (root, root))


def _get_source_from_git(source_dir, ref):
    """ Clone or pull the latest source code from remote git repository """

    run('rm -fr %s' % source_dir)
    run('git clone %s %s' % (REPO, source_dir))
    run('cd %s && git reset --hard %s' % (source_dir, ref))

    # Remove source that is not required by production server
    run('rm -fr %s/{{ui,data}/tests,ft,.git}' % source_dir)
    run('rm -f %s/{.coveragerc,.gitignore,fabfile.py,requirements-dev.txt}' %
        source_dir)


def _backup_current_site(root):
    """ Create a backup of current source, configuration and data """

    run('tar zcf %s/var/backup/replaced-`date "+%%Y%%m%%d%%H%%M%%S"`.tar.gz \
        %s/{src,var/{www,db}}' % (root, root))


def _init_directories(root):
    """ Create the base directory structure for the application """

    run('mkdir -p %s/{src,var/{www,db,backup}}' % root)


def _verify_local_version(version):
    """
    If a version number (git tag) is given, verify it, or return the latest tag
    from local git tree.
    Abort if version information is not found.

    """

    with hide('running'):
        git_ref = local('git tag -l "%s"' % version, capture=True)

        if 1 > len(git_ref):
            git_ref = local('git tag -l --sort=-v:refname "v*"|head -n1',
                            capture=True)

    if 1 > len(git_ref):
        print('Failed to identify the version to be installed on local tree.')
        sys.exit(1)

    return git_ref
