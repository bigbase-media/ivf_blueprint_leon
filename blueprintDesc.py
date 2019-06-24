# -*- coding: utf-8 -*-

def create(name, author=None, version=None, topic=None, label=None, brief=None):
    desc = dict()
    desc['name'] = name
    if (author is not None):
        desc['author'] = author
    if (version is not None):
        desc['version'] = version
    if (topic is not None):
        desc['topic'] = topic
    if (label is not None):
        desc['label'] = label
    if (brief is not None):
        desc['brief'] = brief
    return desc
