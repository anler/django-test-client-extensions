django-test-client-extensions
=============================

Extensions to Django's built-in test client.

## Features ##

* `client.login` - Accepts an user instance instead of having to pass the username and the password.

## Examples ##

Define a base test case for your tests:
```python
from django import test import TestCase as BaseTestCase

import testclient_extensions


class TestCase(test.TestCase):
    client_class = testclient_extensions.Client

```

The just use the client as usual:
```python
# ...
class MyTest:
    def test_something(self):
	    user = my_factories.create_user()
	    self.client.login(user)
		# ...
```
