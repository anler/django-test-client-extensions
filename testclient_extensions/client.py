# -*- coding: utf-8 -*-
import json
import mock
from functools import partial

from django.test import client

from .encoder import Encoder


class PartialMethodCaller(object):

    def __init__(self, obj, **partial_params):
        self.obj = obj
        self.partial_params = partial_params

    def __getattr__(self, name):
        return partial(getattr(self.obj, name), **self.partial_params)


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
