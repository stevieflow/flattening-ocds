from __future__ import unicode_literals
from flattening_ocds.json_input import JSONParser
from flattening_ocds.schema import SchemaParser
import pytest
from collections import OrderedDict

def test_jsonparser_exceptions(tmpdir):
    test_json = tmpdir.join('test.json')
    test_json.write('{}')
    with pytest.raises(ValueError):
        JSONParser()
    with pytest.raises(ValueError):
        JSONParser(json_filename=test_json.strpath, root_json_dict={})


def test_json_filename(tmpdir):
    test_json = tmpdir.join('test.json')
    test_json.write('{"a":"b"}')
    parser = JSONParser(json_filename=test_json.strpath)
    assert parser.root_json_dict == {'a':'b'}


def test_json_filename_ordered(tmpdir):
    test_json = tmpdir.join('test.json')
    test_json.write('{"a":"b", "c": "d"}')
    parser = JSONParser(json_filename=test_json.strpath)
    assert list(parser.root_json_dict.items()) == [('a','b'), ('c','d')]


def test_parse_empty_json_dict():
    parser = JSONParser(root_json_dict={})
    parser.parse()
    assert parser.main_sheet == []
    assert parser.main_sheet_lines == []
    assert parser.sub_sheets == {}
    assert parser.sub_sheet_lines == {}


def test_parse_basic_json_dict():
    parser = JSONParser(root_json_dict=[OrderedDict([
        ('a', 'b'),
        ('c', 'd'),
    ])])
    parser.parse()
    assert parser.main_sheet == [ 'a', 'c' ]
    assert parser.main_sheet_lines == [
        {'a': 'b', 'c': 'd'}
    ]
    assert parser.sub_sheets == {}
    assert parser.sub_sheet_lines == {}


def test_parse_nested_dict_json_dict():
    parser = JSONParser(root_json_dict=[OrderedDict([
        ('a', 'b'),
        ('c', OrderedDict([('d', 'e')])),
    ])])
    parser.parse()
    assert parser.main_sheet == [ 'a', 'c/d' ]
    assert parser.main_sheet_lines == [
        {'a': 'b', 'c/d': 'e'}
    ]
    assert parser.sub_sheets == {}
    assert parser.sub_sheet_lines == {}


def test_parse_nested_list_json_dict():
    parser = JSONParser(root_json_dict=[OrderedDict([
        ('a', 'b'),
        ('c', [OrderedDict([('d', 'e')])]),
    ])])
    parser.parse()
    assert parser.main_sheet == [ 'a' ]
    assert parser.main_sheet_lines == [
        {'a': 'b'}
    ]
    assert parser.sub_sheets == {'c':['d']}
    assert parser.sub_sheet_lines == {'c':[{'d':'e'}]}


# TODO Check support for decimals, integers, booleans

# TODO Add support for cases where the eky doesn't match what the sheet name created by create_template is...
