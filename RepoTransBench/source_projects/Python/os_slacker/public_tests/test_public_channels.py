#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import responses

from slacker import Channels
from slacker.utilities import get_api_url


class TestChannelsPublic(unittest.TestCase):
    @responses.activate
    def test_valid_ids_return_channel_id(self):
        response = {
            'ok': 'true',
            'channels': [
                {'name': 'dev', 'id': 'C333'},
                {'name': 'support', 'id': 'C444'}
            ]
        }
        responses.add(
            responses.GET,
            get_api_url('channels.list'),
            json=response,
            status=200
        )
        channels = Channels(token='public_token')
        self.assertEqual(channels.get_channel_id('support'), 'C444')

    @responses.activate
    def test_invalid_channel_ids_return_none(self):
        response = {
            'ok': 'true',
            'channels': [
                {'name': 'dev', 'id': 'C333'},
                {'name': 'support', 'id': 'C444'}
            ]
        }
        responses.add(
            responses.GET,
            get_api_url('channels.list'),
            json=response,
            status=200
        )
        channels = Channels(token='public_token')
        self.assertEqual(channels.get_channel_id('not_a_channel'), None)