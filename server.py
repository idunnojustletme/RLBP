# server.py
# curl -X POST -H "Content-Type: application/json" -d '{"me":{"score":20}}' http://localhost:80
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import score

score_increase = 0
httpd = None


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Silence, default logger!
    def log_message(self, format, *args):
        return

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self.send_response(200, "OK")
        self.send_header("Content-type", "application/json")
        self.end_headers()

        try:
            json_data = json.loads(post_data.decode("utf-8"))
            self.get_score(json_data)
        except json.JSONDecodeError as e:
            response_message = json.dumps({"error": str(e)})
            self.wfile.write(response_message.encode("utf-8"))
            print(f"Error decoding JSON: {str(e)}")
        return

    def get_score(self, json_data):
        global score_increase
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    self.get_score(item)
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if (
                    key == "me"
                    and isinstance(value, dict)
                    and "score" in value
                ):
                    score_increase = score.calculate_score_increase(
                        value["score"]
                    )
                    return score_increase
                elif isinstance(value, (dict, list)):
                    self.get_score(value)
        return json_data


def get_score_increase():
    global score_increase
    return score_increase


def run(server_class=HTTPServer, handler_class=RequestHandler, port=80):
    global httpd
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"HTTP listener started on port {port}")
    httpd.serve_forever()


def stop():
    global httpd
    if httpd is not None:
        print("Stopping HTTP listener")
        httpd.shutdown()
        httpd.server_close()
