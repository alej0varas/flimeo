from io import StringIO
import os
import shutil
import sys
import unittest

import install


class IntallTests(unittest.TestCase):

    BASE_URL = 'http://localhost:{}/tests/ffmpeg.tar.gz'

    def setUp(self):
        import http.server
        import socketserver
        import threading

        # Silence HTTP server log
        sys.stderr = StringIO()

        class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            pass
        HOST, PORT = "localhost", 0
        self.server = ThreadedTCPServer((HOST, PORT), http.server.SimpleHTTPRequestHandler)
        ip, self.port = self.server.server_address
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        self.TEMPORARY_PATH = 'tmp'
        os.mkdir(self.TEMPORARY_PATH)
        os.environ['FFMPEG_INSTALL_PATH'] = os.path.join(self.TEMPORARY_PATH, 'local', 'bin')
        self.ffmpeg_bin = os.path.join(os.environ['FFMPEG_INSTALL_PATH'], 'ffmpeg')

    def test_main(self):
        url = self.BASE_URL.format(self.port)
        os.environ['FFMPEG_BINARY_URL'] = url

        install.main()

        self.assertTrue(os.path.exists(os.environ['FFMPEG_INSTALL_PATH']))
        self.assertTrue(os.path.exists(self.ffmpeg_bin))

    def test_download_fail(self):
        os.environ['FFMPEG_BINARY_URL'] = 'http://localhost/filenotfound'
        sys.stdout = StringIO()

        self.assertRaises(SystemExit, install.main)
        self.assertEqual(sys.stdout.getvalue(), 'Failed to download ffmpeg\n')

        sys.stdout = sys.__stdout__

    def test_cleanup(self):
        directory = 'other_tmp'
        os.mkdir(directory)

        install.cleanup(directory)

        self.assertFalse(os.path.exists(directory))

    def tearDown(self):
        self.server.shutdown()
        shutil.rmtree(self.TEMPORARY_PATH)
        sys.stderr = sys.__stderr__

if __name__ == '__main__':
    unittest.main()
