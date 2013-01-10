
from hal import HalDocument

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
