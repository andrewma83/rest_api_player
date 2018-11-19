import rest_api
import argparse


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

    req_container = rest_api.Container(filename)

    device_to_test = rest_api.HTTPConn(host, username, password)
    device_to_test.handle_container(req_container)
