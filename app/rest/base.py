import json
from http.client import HTTPConnection
from base64 import b64encode
from typing import Optional

headers = {'Cache-Control': 'no-cache',
           'Content-Type': 'application/json',
           'X-Atlassian-Token': 'no-check',
           "Accept": "application/json,*.*;q=0.9"}


class BaseRest:
    def __init__(self, host="ultrahost", port=2990, prefix="", user="admin", password="admin"):
        self.__conn: Optional[HTTPConnection] = None
        self.__prefix: str = prefix
        self.__headers: dict = headers
        self.__host: str = host
        self.__port: int = port
        self.__headers['Authorization'] = 'Basic {}'.format(b64encode(f"{user}:{password}".encode()).decode("ascii"))
        self.__issues: list = []
        self.__schema_id: Optional[int] = None

    def connect(self):
        if self.__conn:
            self.__conn.close()
            self.__conn.connect()
        self.__conn = HTTPConnection(self.__host, self.__port)

    def disconnect(self):
        if not self.__conn:
            return
        self.__conn.close()
        self.__conn = None

    def post(self, action: str, params: dict):
        self.__conn.request("POST", self.__prefix + action, json.dumps(params), headers)
        response = self.__conn.getresponse()
        data = response.read()
        if data:
            return json.loads(data.decode())

    def get(self, action: str):
        self.__conn.request("GET", self.__prefix + action, headers=headers)
        response = self.__conn.getresponse()
        data = response.read().decode()
        if data:
            return json.loads(data)

    def delete(self, action: str):
        self.__conn.request("DELETE", self.__prefix + action, headers=headers)
        response = self.__conn.getresponse()
        data = response.read().decode()
        if data:
            return json.loads(data)
