import random
from unittest.mock import MagicMock, patch
from .utils import sample_payload, MockBigQuery
from unittest.mock import MagicMock, patch


@patch('google.cloud.bigquery.Client.__init__', MagicMock(return_value=MockBigQuery()))
@patch('src.helpers.streamer.stream_to_bigquery', MagicMock(return_value=True))
def test_without_entry_payload(build_request, to_json):

    data, status_code, headers = main(build_request(
        {'hook': {'event': None}, 'data': None}))
    json = to_json(data)
    assert status_code == 400
    assert 'details' in json
    assert 'slug' in json and json['slug'] == 'invalid-event-name'
    assert headers == {'Content-Type': 'application/json'}


@patch('google.cloud.bigquery.Client.__init__', MagicMock(return_value=MockBigQuery()))
@patch('src.helpers.streamer.stream_to_bigquery', MagicMock(return_value=True))
def test_real_payload(build_request, to_json):

    data, status_code, headers = main(build_request(sample_payload))
    json = to_json(data)

    assert status_code == 200
    assert 'fields' in json
    assert 'together' in json['fields']
    assert 'Hello World' in json['fields']['together']
    assert headers == {'Content-Type': 'application/json'}
