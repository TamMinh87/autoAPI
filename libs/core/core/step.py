import allure

from contextlib2 import ContextDecorator


class step(ContextDecorator):

    def __init__(self, step_description=""):
        self.step_description = step_description

    def __enter__(self):
        try:
            with allure.step(self.step_description):
                return self
        except AttributeError:
            return self

    def __exit__(self, *exc):
        pass
