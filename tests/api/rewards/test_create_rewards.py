import pytest
from libs import response_checker
from framework.reward_api import reward_api_service
from data.reward_api.json_schema import create_rewards


@pytest.allure.feature('Rewards API. Test create rewards handler')
class TestCreateRewards:
    @pytest.allure.story('Check that response code is OK(200)')
    def test_response_code_is_ok(self, random_reward):
        code, _ = reward_api_service.create_rewards(random_reward)
        response_checker.check_code_ok(code)

    @pytest.allure.story('Check create rewards json structure')
    def test_json_structure_is_ok(self, random_reward):
        _, response = reward_api_service.create_rewards(random_reward)
        response_checker.validate_json_schema(response, create_rewards.schema)
