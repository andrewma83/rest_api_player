import rest_api


def driver_test (filename):
    request_container = rest_api.rest_api_container(filename)
    request_container.dump_container_list()


if __name__ == "__main__":
    # execute only if run as a script
    filename = "./tornado_config_log"
    driver_test(filename)
