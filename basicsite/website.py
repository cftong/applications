import nginx
import os

from arkos.system import users, groups
from arkos.websites import Site
from arkos.languages import php


class Website(Site):
    addtoblock = []

    def pre_install(self, extra_vars):
        if extra_vars.get('php', False):
            self.addtoblock = [
                nginx.Location(
                    '~ ^(.+?\.php)(/.*)?$',
                    nginx.Key('include', 'fastcgi_params'),
                    nginx.Key('fastcgi_param',
                              'SCRIPT_FILENAME $document_root$1'),
                    nginx.Key('fastcgi_param', 'PATH_INFO $2'),
                    nginx.Key('fastcgi_pass',
                              'unix:/run/php-fpm/php-fpm.sock'),
                    nginx.Key('fastcgi_read_timeout', '900s'),
                )
            ]

    def post_install(self, extra_vars, dbpasswd=""):
        # Write a basic index file showing that we are here
        if extra_vars.get('php'):
            php.enable_mod('apcu', config_file="/etc/php/conf.d/apcu.ini")

        index_ext = 'php' if extra_vars.get('php') else 'html'
        index_path = os.path.join(self.path, 'index.{0}'.format(index_ext))
        with open(index_path, 'w') as f:
            f.write(
                '<html>\n'
                '<body>\n'
                '<h1>Genesis - Custom Site</h1>\n'
                '<p>Your site is online and available at {0}</p>\n'
                '<p>Feel free to paste your site files here</p>\n'
                '</body>\n'
                '</html>\n'
                .format(self.path)
            )

        # Give access to httpd
        uid, gid = users.get_system("http").uid, groups.get_system("http").gid
        for r, d, f in os.walk(self.path):
            for x in d:
                os.chown(os.path.join(r, x), uid, gid)
            for x in f:
                os.chown(os.path.join(r, x), uid, gid)

    def pre_remove(self):
        pass

    def post_remove(self):
        pass

    def enable_ssl(self, cfile, kfile):
        pass

    def disable_ssl(self):
        pass

    def update(self, pkg, ver):
        pass
