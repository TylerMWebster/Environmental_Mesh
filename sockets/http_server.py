from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json, random

hostName = "192.168.43.28"
hostName = "172.28.120.37"
serverPort = 42069
def generate_data(length):
    data = {}
    for i in range(0, length):
        data[f'address{i}'] =  round(random.uniform(30.5, 95.5), 2)
    data = json.dumps(data)
    return data


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(f"{generate_data(4)}", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")