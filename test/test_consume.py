
from simplehal import HalDocument, Resolver

import json
from pprint import pprint

def test_simple_consumption():

    data = {
            u'_links': {
                u'self': {u'href': u'/hi'}
            },
            'title': 'cow list',
            '_embedded': {
                'cow': [
                    {'name': 'how'},
                    {'name': 'now'},
                    {'name': 'brown'}
                ]
            }
    }

    doc = HalDocument.from_python(data)
    info = json.loads(doc.to_json())

    assert info['_links'] == data['_links']
    assert info['title'] == data['title']
    assert info['_embedded'] == data['_embedded']

    assert doc.links == data['_links']
    assert doc.links == info['_links']

    assert doc.get_data('cow') == data['_embedded']['cow']


def test_handle_curie():
    data = {
            '_links': {
                'self': {'href': '/hi'},
                'curies': {
                    'href': 'http://example.com/barnacle/{rel}',
                    'name': 'barnacle',
                    'templated': True
                },
                'barnacle:shell': {'href': '/some/path'}
            },
            '_embedded': {
                'barnacle:cow': [
                    {'name': 'how'},
                    {'name': 'now'},
                    {'name': 'brown'}
                ]
            }
    }

    doc = HalDocument.from_python(data)
    curies = doc.get_curies()

    assert 'barnacle' in curies

    resolver = Resolver(curies)

    assert resolver.expand('barnacle:cow') == 'http://example.com/barnacle/cow'
