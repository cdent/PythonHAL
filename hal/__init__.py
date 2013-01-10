"""
Classes encapsulating the structure of a HAL Document.
"""

try:
    import json
except ImportError:
    import simplejson as json

from copy import deepcopy

VALID_LINK_ATTRS = ['templated', 'type', 'name', 'profile', 'title',
    'hreflang']


class HalDocument(object):
    """
    A single HAL document, which can be nested in
    another.
    """

    def __init__(self, links, data=None, embed=None):
        if data:
            self.structure = data
        else:
            self.structure = {}
        if embed:
            self.structure['_embedded'] = embed
        self.structure['_links'] = links.structure

    def to_json(self):
        """
        Dump the structure of the document as JSON.
        """
        return json.dumps(self.structure)

    @classmethod
    def from_python(cls, structure):
        """
        Create a new document from provided structure.
        Usually decoded from JSON.
        """
        structure = deepcopy(structure)

        links = Links()
        for link in structure['_links']:
            rel = link
            target = structure['_links'][rel]
            if hasattr(target, 'append'):
                for item in target:
                    href = item['href']
                    del item['href']
                    links.add(Link(rel, href, **item))
            else:
                href = target['href']
                del target['href']
                links.add(Link(rel, href, **target))

        embedded = structure['_embedded']

        # cleanup
        del structure['_links']
        del structure['_embedded']

        return cls(links, data=structure, embed=embedded)


class Links(object):
    """
    Model of a HAL links collection.
    """

    def __init__(self):
        self.structure = {}

    def add(self, *links):
        """
        Add some link. For a new link, add it singular. If
        there is a second of the same rel, become plurar
        (that is, a list).
        """
        for link in links:
            if link.rel in self.structure:
                self.structure[link.rel] = [self.structure[link.rel]]
                self.structure[link.rel].append(link.to_dict())
            else:
                self.structure[link.rel] = link.to_dict()


class Link(object):
    """
    Model of a HAL link.
    """

    def __init__(self, rel, href, **kwargs):
        self.rel = rel
        self.href = href
        self.kwargs = kwargs

    def to_dict(self):
        """
        Turn the link into a dictionary.
        """
        result = {'href': self.href}
        for key in self.kwargs:
            if key in VALID_LINK_ATTRS:
                result[key] = self.kwargs[key]
        return result
