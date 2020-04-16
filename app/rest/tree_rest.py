from typing import Optional

from .base import BaseRest
from ..logger import logging

log = logging.getLogger("rest")


class TreeRest(BaseRest):
    def __init__(self, single_cf: str, multi_cf: str, schema_id: int, issue_data: dict, host="ultrahost",
                 port: int = 2990, prefix: str = "/jira", user: str = "admin", password: str = "admin"):
        super().__init__(host=host, port=port, prefix=prefix, user=user, password=password)
        self.__schema_id: int = schema_id
        self.__single_cf_id: str = single_cf
        self.__multi_cf_id: str = multi_cf
        self.__issue_data: dict = issue_data
        self.__issues: dict = {}
        self.__options: dict = {}

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect()
        for issue_key in self.__issues:
            self.__delete_issue(key=issue_key)

        for k, option in self.__options.items():
            self.__delete_option(option_id=option["id"])

        self.disconnect()

    @property
    def options(self):
        return self.__options

    @property
    def single_field_id(self):
        return self.__single_cf_id

    @property
    def multi_field_id(self):
        return self.__multi_cf_id

    @property
    def issue_data(self):
        return self.__issue_data.copy()

    def create_issue(self, issue_data) -> dict:
        log.debug(f"Create issue for {issue_data['fields']['summary']}")
        data = self.post("/rest/api/2/issue", issue_data)
        self.__issues[data['key']] = data
        return data

    def __delete_issue(self, key):
        data = self.delete(f"/rest/api/2/issue/{key}")
        return data

    def __create_option(self, option: dict):
        option["schemaId"] = self.__schema_id
        data = self.post("/rest/treecf/1.0/admin/option/update", option)
        self.__options[data["path"]] = data
        return data

    def create_option_for_name(self, option_name: str) -> dict:
        if option_name in self.__options:
            return self.__options[option_name]

        log.debug(f"create option {option_name}")

        parts = option_name.rsplit("/", 1)
        if len(parts) == 1:
            return self.__create_option({"name": parts[0]})
        else:
            parent = self.create_option_for_name(parts[0])
            opt_data = {
                "parentId": parent["id"],
                "name": parts[1]
            }

            return self.__create_option(opt_data)

    def __delete_option(self, option_id) -> dict:
        log.debug(f"delete option {option_id}")
        params = {'id': option_id}
        data = self.post("/rest/treecf/1.0/admin/option/delete", params)
        return data

    def search(self, jql) -> dict:
        params = {
            "jql": jql,
            "fields": ["id", "key", "summary", self.__single_cf_id, self.__multi_cf_id]
        }
        data = self.post("/rest/api/2/search", params)
        out = {}

        if data and "issues" in data:
            for issue in data["issues"]:
                out[issue["key"]] = issue

        return out
