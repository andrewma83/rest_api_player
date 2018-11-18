import rest_api


def driver_test (filename):
    request_container = rest_api.Container(filename)
    request_container.dump_container_list()


if __name__ == "__main__":
    # execute only if run as a script
    filename = "./tornado_config_log.test"
    host="10.50.22.36"
    username="admin"
    password="admin123A!!"

#    driver_test(filename)
    req_container = rest_api.Container(filename)

    device_to_test = rest_api.HTTPConn(host, username, password)
    device_to_test.handle_container(req_container)
