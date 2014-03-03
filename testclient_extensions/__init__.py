# -*- coding: utf-8 -*-

import mock

from django.test import client


class Client(client.Client):

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
