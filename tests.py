import os
import unittest

import install


class IntallTests(unittest.TestCase):

    BASE_URL = 'http://localhost:{}/tests/ffmpeg.tar.gz'

    def setUp(self):
        import http.server
        import socketserver
        import threading

        class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            pass
        HOST, PORT = "localhost", 0
        self.server = ThreadedTCPServer((HOST, PORT), http.server.SimpleHTTPRequestHandler)
        ip, self.port = self.server.server_address
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def test_main(self):
        url = self.BASE_URL.format(self.port)
        os.environ['FFMPEG_BINARY_URL'] = url

        result = install.main()

    def tearDown(self):
        self.server.shutdown()


if __name__ == '__main__':
    unittest.main()
