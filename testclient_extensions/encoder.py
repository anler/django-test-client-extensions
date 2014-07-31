# -*- coding: utf-8 -*-
import re


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
