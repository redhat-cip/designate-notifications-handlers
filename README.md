Introduction
============

:warning: Now that
[multi-backend](https://blueprints.launchpad.net/designate/+spec/multi-backend)
and [nsd4slave-backend](https://blueprints.launchpad.net/designate/+spec/nsd4-slave-backend)
have merged, dnh is obsolete :warning:

Designate-notifications-handlers (dnh) is a daemon that listens to AMQP
notifications emitted by
[Designate](http://designate.readthedocs.org/en/latest). It comes with a NSD4
handler that reacts to domain creations and deletions by sending nsd-control
commands to a NSD4 server. If you want to write your own handler, take a look
at the BaseHandler class to understand how notifications are dispatched.
