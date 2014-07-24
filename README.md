django-test-client-extensions
=============================

Extensions to Django's built-in test client.

## Features ##

* `client.login` - Accepts an user instance instead of having to pass the username and the password.
* `client.json` - Sets the content-type of the next request to json.

## Examples ##

### Setup ###

Define a base test case for your tests:
```python
from django import test import TestCase as BaseTestCase

import testclient_extensions


class TestCase(test.TestCase):
    client_class = testclient_extensions.Client

```

or use a pytest fixture:
```python
@pytest.fixture
def client():
    from testclient_extensions import Client
    return Client()
```

### client.login ###

```python
# ...
user = my_factories.create_user()
self.client.login(user)
# ...
```

### client.json ###
Automatically encode json-data and set the proper content-type.

```python
# ...
data = {"complex": ["piece", "of", "data"]}
response = self.client.json.post(url, data)
# ...
```

## Installation ##

`pip install django-restclient-extensions`
