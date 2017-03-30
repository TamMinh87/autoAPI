# -*- coding: utf-8 -*-
from time import sleep

import pytest

from libs import response_checker
from framework.twitch_api import twitch_api_service


@pytest.allure.feature('Reward API')
class TestRewardAPI(object):
    @pytest.allure.story('Check that response is OK(200)')
    def test_response_code_is_ok(self):
        code, response = twitch_api_service.sample_request()
        response_checker.check_code_ok(code)

    # @pytest.allure.story('Check that response is OK(200)')
    # def test_create_reward(self):
    #     json = {
    #         "name": "test",
    #         "category": "MAKE_IT_RAIN",
    #         "bot_command": "test",
    #         "price": 0,
    #         "image": "https://s3-us-west-2.amazonaws.com/revlo-public-us-west/site_images/rewards_bank/make-it-rain.svg",
    #         "description": "test!",
    #         "cooldown": "NO_COOLDOWN",
    #         "point": 10
    #     }
    #
    #     code, response = twitch_api_service.post_reward(json=json)
    #     response_checker.check_code_ok(code)
