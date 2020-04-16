from colorama import Fore, Back, Style
from .base_checker import BaseChecker
from ..rest import TreeRest
from ..logger import logging

log = logging.getLogger("jql checker")


class CheckJql(BaseChecker):
    def __init__(self, instance: TreeRest):
        super().__init__(instance)

    def __run_case(self, jql: str, matches: list, no_matches: list):
        log.info(f"{Back.BLUE}Start testing jql:{Back.RESET} {Fore.GREEN}{jql}{Fore.RESET}")
        issues = self.instance.search(jql)

        for matched_value in matches:
            for key in self.get_issues_for_value(matched_value):
                if key not in issues:
                    log.error(f"{Fore.RED}{key}: {matched_value} not founded, but should!!!{Style.RESET_ALL}")
                else:
                    log.info(f"{key}: {matched_value} founded")

        for not_matched_value in no_matches:
            for key in self.get_issues_for_value(not_matched_value):
                if key in issues:
                    log.error(f"{Fore.RED}{key}: {not_matched_value} founded, but should not!!!{Style.RESET_ALL}")
                else:
                    log.info(f"{key}: {not_matched_value} not founded")

    def run(self):
        for case in self.test_cases:
            jql = f"{self.single_field_jql_name} {case['operator']} \"{case['query']}\""
            self.__run_case(jql, case['matches'], case['no_matches'])
            jql = f"{self.multi_field_jql_name} {case['operator']} \"{case['query']}\""
            self.__run_case(jql, case['matches'], case['no_matches'])

            jql = f"{self.single_field_jql_name} !{case['operator']} \"{case['query']}\""
            self.__run_case(jql, case['no_matches'], case['matches'])
            jql = f"{self.multi_field_jql_name} !{case['operator']} \"{case['query']}\""
            self.__run_case(jql, case['no_matches'], case['matches'])
