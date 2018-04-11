# -*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals
from functools import partial
from celery.platforms import detached, maybe_drop_privileges
from celery.bin.base import Command, daemon_options

__all__ = ['beat']

HELP = __doc__


class beat(Command):
    """Start the beat periodic task scheduler.

    Examples:
        .. code-block:: console

            $ celery beat -l info
            $ celery beat -s /var/run/celery/beat-schedule --detach
            $ celery beat -S django

    The last example requires the :pypi:`django-celery-beat` extension
    package found on PyPI.
    """

    doc = HELP
    enable_config_from_cmdline = True
    supports_args = False

    def run(self, detach=False, logfile=None, pidfile=None, uid=None,
            gid=None, umask=None, workdir=None, **kwargs):
        if not detach:
            maybe_drop_privileges(uid=uid, gid=gid)
        kwargs.pop('app', None)
        beat = partial(self.app.Beat,
                       logfile=logfile, pidfile=pidfile, **kwargs)

        if detach:
            with detached(logfile, pidfile, uid, gid, umask, workdir):
                return beat().run()
        else:
            return beat().run()

    def add_arguments(self, parser):
        c = self.app.conf
        bopts = parser.add_argument_group('Beat Options')
        bopts.add_argument('--detach', action='store_true', default=False)
        bopts.add_argument(
            '-s', '--schedule', default=c.beat_schedule_filename)
        bopts.add_argument('--max-interval', type=float)
        bopts.add_argument('-S', '--scheduler')
        bopts.add_argument('-l', '--loglevel', default='WARN')

        daemon_options(parser, default_pidfile='celerybeat.pid')

        user_options = self.app.user_options['beat']
        if user_options:
            uopts = parser.add_argument_group('User Options')
            self.add_compat_options(uopts, user_options)


def main(app=None):
    beat(app=app).execute_from_commandline()


if __name__ == '__main__':      # pragma: no cover
    main()
