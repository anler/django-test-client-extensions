# -*- coding: utf-8 -*-
import json
import mock
import re
from functools import partial

from django.test import client


class PartialMethodCaller(object):

    def __init__(self, obj, **partial_params):
        self.obj = obj
        self.partial_params = partial_params

    def __getattr__(self, name):
        return partial(getattr(self.obj, name), **self.partial_params)


class Encoder(object):
    def __init__(self, match, encoder, predicate):
        self._match = re.compile(match)
        self._encoder = encoder
        self._predicate = predicate

    def __call__(self, *args, **kwargs):
        return self.encode(*args, **kwargs)

    def encode(self, data, **options):
        return self._encoder(data, **options)

    def accepts(self, data, **options):
        return self._predicate(data, **options)

    def match(self, content_type):
        return self._match.search(content_type)

    def match_and_accepts(self, content_type, data, **options):
        return self.match(content_type) and self.accepts(data, **options)


class Client(client.Client):

    DATA_ENCODERS = [Encoder("json", json.dumps, lambda data, **options: isinstance(data, dict))]

    @property
    def json(self):
        """Sets the content-type of the next request to 'application/json;charset="utf-8"'"""
        return PartialMethodCaller(obj=self, content_type='application/json;charset="utf-8"')

    def login(self, user=None, backend="django.contrib.auth.backends.ModelBackend", **credentials):
        """Improves default login method by accepting a user object directly.

        The passed user may have a ``raw_password`` attribute to use it as the
        login password.

        :param user: :class:`django.contrib.auth.models.User` instance.
        :param backend: name of the authentication backend to set as the one used when
        authenticating the user.
        :param credentials: credential parameters originally received by
        `django.test.client.Client.login` method.

        :return: ``True`` if login succeed, ``False`` otherwise.
        """
        if user is None:
            return super(Client, self).login(**credentials)

        with mock.patch('django.test.client.authenticate') as authenticate:
            user.backend = backend
            authenticate.return_value = user
            return super(Client, self).login(**credentials)

    def _encode_data(self, data, content_type):
        for encoder in self.DATA_ENCODERS:
            if encoder.match_and_accepts(content_type, data):
                return encoder(data)
        return super(Client, self)._encode_data(data, content_type)

    def generic(self, method, path, data='', content_type='application/octet-stream', **extra):
        data = self._encode_data(data, content_type)
        return super(Client, self).generic(method, path, data, content_type, **extra)
