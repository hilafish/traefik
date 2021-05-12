#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
import os
from time import sleep
from concurrent.futures import ThreadPoolExecutor

app_instances = int(os.environ.get("app_instances"))
app_container_name = "traefik_whoami_"


class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        tasks = []
        with ThreadPoolExecutor(max_workers=app_instances) as pool:
            for i in range(app_instances):
                container_name = app_container_name + str(i + 1)
                task = pool.submit(self.post_to_one_container(container_name, post_data))
                tasks.append(task)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def post_to_one_container(self, container_name, post_data):
        req = self.actual_post(container_name, post_data)
        status_code = req.status_code
        num_retries = 0
        while status_code != 201:
            time_to_wait = self.calculate_backoff_seconds(num_retries)
            sleep(time_to_wait)
            req = self.actual_post(container_name, post_data)
            status_code = req.status_code
            num_retries += 1
        return status_code

    @staticmethod
    def actual_post(container_name, post_data):
        result = requests.post('http://' + container_name, data=post_data.decode('utf-8'))
        logging.info("POST request forwarded to %s, status code: %s" % (container_name, result.status_code))
        return result

    @staticmethod
    def calculate_backoff_seconds(num_retries):
        """ arguments are ints in seconds """
        return 2 ** num_retries  # in seconds


def run(server_class=HTTPServer, handler_class=S, port=8081):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    run()

