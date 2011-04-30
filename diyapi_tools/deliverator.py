# -*- coding: utf-8 -*-
"""
deliverator.py

The deliverator holds the channels that will be used to deliver 
the replies that come over a resilient connection
"""

from gevent.queue import Queue

class Deliverator(object):
    """
    The deliverator holds the channels that will be used to deliver 
    the replies that come over a resilient connection
    """
    def __init__(self):
        self._active_requests = dict()

    def add_request(self, request_id):
        """
        Add a request_id
        return a channel that will deliver the reply message 
        """
        if request_id in self._active_requests:
            raise ValueError("Duplicate request '%s'" % (request_id, ))

        channel = Queue(maxsize=0)
        self._active_requests[request_id] = channel

        return channel

    def deliver_reply(self, message):
        """
        Deliver the reply nessage over the channel for its request-id
        And discard the channel
        raise KeyError if there is no channel for the request
        """
        channel = self._active_requests.pop(message["request_id"])
        channel.put(message)

