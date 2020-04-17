from colorama import Fore, Back, Style
from .base_checker import BaseChecker
from ..rest import TreeRest
from ..logger import logging

log = logging.getLogger("jql checker")


class CheckJql(BaseChecker):
    def __init__(self, instance: TreeRest):
        super().__init__(instance)

    def __run_case_jql(self, jql: str, matches: list, no_matches: list):
        log.info(f"{Back.BLUE}Jql:{Back.RESET} {Fore.GREEN}{jql}{Fore.RESET}")
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

    def __run_case(self, operator: str, query: str, matches: list, no_matches: list):
        log.info(f"{Back.BLUE}Testing single field:{Back.RESET} {self.single_field_jql_name}")
        jql = f"{self.single_field_jql_name} {operator} \"{query}\""
        self.__run_case_jql(jql, matches, no_matches)
        log.info(f"{Back.BLUE}Testing multi field:{Back.RESET} {self.multi_field_jql_name}")
        jql = f"{self.multi_field_jql_name} {operator} \"{query}\""
        self.__run_case_jql(jql, matches, no_matches)

    def run(self):
        for case in self.test_cases:
            self.__run_case(case['operator'], case['query'], case['matches'], case['no_matches'])
            self.__run_case("!{}".format(case['operator']), case['query'], case['no_matches'], case['matches'])
