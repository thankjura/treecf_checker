from abc import ABC, abstractmethod
from ..rest import TreeRest
from ..logger import logging

log = logging.getLogger("checker")


class BaseChecker(ABC):
    def __init__(self, instance: TreeRest):
        self.__instance: TreeRest = instance
        self.__test_cases: list = []
        self.__value_issues: dict = {}

    @property
    def instance(self):
        return self.__instance

    @property
    def options(self) -> dict:
        return self.__instance.options

    @property
    def test_cases(self) -> list:
        return self.__test_cases

    @property
    def single_field_jql_name(self):
        return "cf[{}]".format(self.__instance.single_field_id.replace("customfield_", ""))

    @property
    def multi_field_jql_name(self):
        return "cf[{}]".format(self.__instance.multi_field_id.replace("customfield_", ""))

    def get_issues_for_value(self, value):
        # TODO: make many issues for value
        return [self.__value_issues[value]]

    def prepare_data(self, test_cases: dict):
        self.__test_cases = test_cases
        self.__create_options()
        self.__create_issues()

    def __create_issues(self):
        log.debug("Start create issues")
        for val, opt in self.options.items():
            if val in self.__value_issues:
                continue
            issue_data = self.__instance.issue_data
            issue_data["fields"][self.__instance.single_field_id] = {
                "id": str(opt['id'])
            }
            issue_data["fields"][self.__instance.multi_field_id] = [{
                "id": str(opt['id'])
            }]
            issue_data["fields"]["summary"] = val
            data = self.__instance.create_issue(issue_data)
            self.__value_issues[val] = data["key"]
        log.debug("Issues created")

    def __create_options(self):
        log.debug("Start create options")
        option_name_set: set = set()
        for c in self.__test_cases:
            option_name_set.update(c['matches'])
            option_name_set.update(c['no_matches'])

        for option_name in option_name_set:
            self.__instance.create_option_for_name(option_name)

        log.debug("Options created")

    @abstractmethod
    def run(self):
        pass
