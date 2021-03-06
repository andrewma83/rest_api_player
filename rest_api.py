import requests
import re
import argparse

request_method=["GET", "POST", "PATCH", "PULL", "DELETE"]
tornado_info_pattern= "([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}): \[(INFO|NOTICE)\]: " \
                      "(PATCH|PUT|POST|DELETE|GET) ([a-zA-Z0-9\/\-\_]+) \(([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})\) Request Body:"
tornado_request_body_pattern="([a-zA-Z0-9\"\-\_\[\]{}:,\.\/ ]+)"


class Request:

    def __init__(self, request_type, uri, data):
        self.request_type=request_type
        self.uri=uri
        self.data=data


class Container:
    def parse_file(self,filename):
        count = 0
        file_obj = open(filename, "r")
        for line in file_obj:
            mod_count = count % 3;
            if mod_count == 0:
                match_obj = re.match(tornado_info_pattern, line)
                request_type = match_obj.group(3)
                request_uri = match_obj.group(4)
            elif mod_count == 1:
                request_data = line
            elif mod_count == 2:
                request_obj = Request(request_type, request_uri, request_data)
                self.obj_list.append(request_obj)

            count = count + 1

    def __init__(self, filename):
        self.obj_list=[]
        self.parse_file(filename)

    def dump_container_list(self):
        for container_obj in self.obj_list:
            print "Type:%-10s URI:%s" % (container_obj.request_type, container_obj.uri)


class HTTPConn:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def patch_pull_core(self, rest_uri, data):
        headers = {
            'Content-Type': 'application/json',
        }
        rest_url = 'https://' + self.host + rest_uri
        response = requests.post(rest_url, data=data, auth=(self.username, self.password), verify=False, headers=headers)
        return response.text

    def get(self, rest_uri, data):
        rest_url = 'https://' + self.host + rest_uri
        response = requests.get(rest_url, auth=(self.username, self.password), verify=False)
        return response.text

    def post(self, rest_uri, data):
        headers = {
            'Content-Type': 'application/json',
        }
        rest_url = 'https://' + self.host + rest_uri
        response = requests.post(rest_url, data=data, auth=(self.username, self.password), verify=False, headers=headers)
        return response.text

    def patch(self, rest_uri, data):
        headers = {
            'Content-Type': 'application/json',
        }
        rest_url = 'https://' + self.host + rest_uri
        response = requests.patch(rest_url, data=data, auth=(self.username, self.password), verify=False, headers=headers)
        return response.text

    def pull(self, rest_uri, data):
        headers = {
            'Content-Type': 'application/json',
        }
        rest_url = 'https://' + self.host + rest_uri
        response = requests.put(rest_url, data=data, auth=(self.username, self.password), verify=False, headers=headers)
        return response.text

    def delete(self, rest_uri, data):
        headers = {
            'Content-Type': 'application/json',
        }
        rest_url = 'https://' + self.host + rest_uri
        response = requests.delete(rest_url, headers=headers)

    def handle_request(self, api_request):
        switcher = {
            "GET": self.get,
            "POST": self.post,
            "PATCH": self.patch,
            "PULL": self.pull,
            "DELETE": self.delete
        }

        return switcher[api_request.request_type](api_request.uri, api_request.data)

    def handle_container(self, _container):
        for api_request in _container.obj_list:
            self.handle_request(api_request)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="REST API log replayer")
    parser.add_argument('-H', '--host', type=str, metavar='', required=True, help='Host/IP for device to test')
    parser.add_argument('-u', '--username', type=str, metavar='', required=True, help='Credential (username) for the API request')
    parser.add_argument('-p', '--password', type=str, metavar='', required=True, help='Credential (password) for the API request')
    parser.add_argument('--infile', type=str, metavar='', required=True, help='Input logfile name for the API request')

    cli_arg = parser.parse_args()

    # execute only if run as a script
    filename = cli_arg.infile
    host=cli_arg.host
    username=cli_arg.username
    password=cli_arg.password

    req_container = Container(filename)

    device_to_test = HTTPConn(host, username, password)
    device_to_test.handle_container(req_container)
