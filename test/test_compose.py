
from simplehal import HalDocument, Links, Link

import json


def test_simple_link():
    link = Link('example', '/somewhere',
            type='text/plain',
            monkey='foobar',
            templated=True,
            name='cow')

    assert link.rel == 'example'

    link_data = link.to_dict()
    assert 'monkey' not in link_data
    assert link_data['href'] == '/somewhere'
    assert link_data['type'] == 'text/plain'
    assert link_data['templated'] == True
    assert link_data['name'] == 'cow'

def test_simple_links():
    link1 = Link('example', '/somewhere',
            type='text/plain',
            monkey='foobar',
            templated=True,
            name='cow')
    link2 = Link('self', '/somewhere-else')
    link3 = Link('example', '/other')

    links = Links()
    links.add(link1, link2, link3)

    links_info = links.structure
    assert 'example' in links_info
    assert 'self' in links_info

    assert links_info['example'][0]['href'] == '/somewhere'
    assert links_info['example'][1]['href'] == '/other'
    assert links_info['self']['href'] == '/somewhere-else'


def test_dataless_document():
    links = Links()
    links.add(Link('example', '/somewhere', type='text/plain'))

    doc = HalDocument(links)

    json_doc = doc.to_json()

    info = json.loads(json_doc)

    assert len(info) == 1
    assert '_links' in info
    assert 'example' in info['_links']
    example = info['_links']['example']
    assert example['href'] == '/somewhere'
    assert example['type'] == 'text/plain'


def test_data_document():
    links = Links()
    links.add(Link('self', '/somewhere'))

    data = {'tags': ['hello', 'goodbye'],
            'message': 'We got some new tags'}

    doc = HalDocument(links, data=data)

    json_doc = doc.to_json()
    info = json.loads(json_doc)

    assert '_links' in info
    assert 'tags' in info
    assert 'message' in info
    assert info['tags'] == ['hello', 'goodbye']


def test_embedded_document():
    links = Links()
    links.add(Link('self', '/somewhere'))

    # one embedded cow
    embed = {'cow': [{'tags': ['hello', 'goodbye'],
            'message': 'We got some new tags'}]}

    doc = HalDocument(links, embed=embed)

    json_doc = doc.to_json()
    info = json.loads(json_doc)

    assert '_links' in info
    assert '_embedded' in info

    embedded = info['_embedded']
    assert 'cow' in embedded

    cows = embedded['cow']
    assert len(cows) == 1

    cow = cows[0]
    assert 'tags' in cow
    assert 'message' in cow
    assert cow['tags'] == ['hello', 'goodbye']
