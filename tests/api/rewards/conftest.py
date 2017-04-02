import pytest
from framework.reward_api.models.create_reward_model import CreateRewardModel
from libs.common import generators


@pytest.fixture(scope="function")
def random_reward():
    reward = CreateRewardModel(**{
        "name": generators.get_random_name(),
        "point": generators.get_random_number_by_range(0, 10000),
    })
    return reward.model

