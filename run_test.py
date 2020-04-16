#!/usr/bin/python3

import random
from app.rest import TreeRest
from app import test_cases
from app.checkers import CheckJql


single_customfield = "customfield_10000"
multiple_customfield = "customfield_10001"
schema_id = 2

issue_data = {
    "fields": {
        "project": {"key": "TR"},
        "issuetype": {"id": "10000"},
        "description": "autogenerated"
    }
}


def main():
    with TreeRest(single_customfield, multiple_customfield, schema_id, issue_data) as inst:
        checker = CheckJql(inst)
        checker.prepare_data(test_cases.eq_simple_cases)
        checker.run()

        checker.prepare_data(test_cases.like_simple_cases)
        checker.run()

        input("press any key")


if __name__ == "__main__":
    main()
