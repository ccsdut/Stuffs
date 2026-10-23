#!/usr/bin/env python3
"""Serve this folder on http://localhost:8080 with the headers the game needs.

Opening index.html by double-click (file://) fails the "secure page" and
"threads" checks. localhost counts as a secure page, and these headers make
it cross-origin isolated, so run this and open http://localhost:8080 instead.
"""
import http.server
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.wasm': 'application/wasm', '.js': 'text/javascript'}

    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
        super().end_headers()


if __name__ == '__main__':
    print(f'Open http://localhost:{PORT}')
    http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
