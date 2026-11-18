"""SUPPLIED browser/SQLite plumbing, not student assessment evidence.

Development server for one student's PRIVATE Codespace or localhost only.
It is not a public or multi-user hosting service. No game rules or SQL here.
"""
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
import sqlite3
import traceback
from urllib.parse import urlsplit

import game

ROOT = Path(__file__).resolve().parent
ACTIONS = {'View', 'Travel', 'Buy', 'Sell', 'New game'}
FIELD_NAMES = {'market', 'good', 'quantity'}


def make_handler(database, token, callback):
    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, body, content_type='application/json; charset=utf-8'):
            data = body.encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy',
                             "default-src 'self'; script-src 'self'; style-src 'self'; "
                             "object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)

        def fail(self, status, message):
            self.respond(status, json.dumps({'error': message}))

        def do_GET(self):
            route = urlsplit(self.path).path
            # An allowlist prevents serving database/source/other local files.
            if route == '/':
                text = (ROOT / 'web/index.html').read_text(encoding='utf-8')
                self.respond(200, text.replace('__REQUEST_TOKEN__', token), 'text/html; charset=utf-8')
            elif route in ('/app.js', '/style.css'):
                kind = 'text/javascript' if route.endswith('.js') else 'text/css'
                self.respond(200, (ROOT / 'web' / route[1:]).read_text(encoding='utf-8'),
                             kind + '; charset=utf-8')
            else:
                self.fail(404, 'Not found.')

        def do_POST(self):
            if self.path != '/action':
                self.fail(404, 'Not found.')
                return
            if self.headers.get('X-Request-Token') != token:
                self.fail(403, 'Reload this page and try again.')
                return
            if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                self.fail(415, 'Expected JSON.')
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 65536:
                    self.fail(413, 'Request too large or empty.')
                    return
                request = json.loads(self.rfile.read(length))
                if not isinstance(request, dict):
                    raise ValueError('Expected an object.')
                action, fields = request.get('action'), request.get('fields')
                if not isinstance(action, str) or action not in ACTIONS:
                    raise ValueError('Unknown button.')
                if not isinstance(fields, dict) or set(fields) != FIELD_NAMES:
                    raise ValueError('Incorrect fields.')
                if not all(isinstance(value, str) for value in fields.values()):
                    raise ValueError('Fields must contain text.')
            except (ValueError, UnicodeDecodeError):
                self.fail(400, 'The browser request was not understood. Reload and try again.')
                return
            # Above checks protect the transport, not the game's inputs/rules.
            # Blank text, negative quantities etc. are passed unchanged.
            try:
                # One button action is one transaction, including schema changes.
                # A normal text return commits; an exception rolls back.
                with database:
                    database.execute('BEGIN')
                    output = callback(action, fields, database)
                    if not isinstance(output, str):
                        raise TypeError('handle_action must return text.')
            except Exception:
                traceback.print_exc()
                self.fail(500, 'Your Python code stopped with an error. Read the terminal; '
                          'do not repeat a trade until you have checked the game state.')
                return
            self.respond(200, json.dumps({'text': output}))

    return Handler


def run(port=8000, database_path=None):
    database = sqlite3.connect(database_path or ROOT / 'game.sqlite3')
    # The shell owns per-action transactions. Students still choose their
    # schema, SQL, validation, resets and data population.
    try:
        handler = make_handler(database, secrets.token_hex(32), game.handle_action)
        # Serial request handling keeps the supplied SQLite connection on one
        # thread. One server is one game instance, not one game per browser tab.
        with HTTPServer(('127.0.0.1', port), handler) as server:
            print(f'Open http://localhost:{port} (Codespaces: Ports > Open in Browser).', flush=True)
            print('Keep port visibility PRIVATE. Press Ctrl+C to stop.', flush=True)
            server.serve_forever()
    finally:
        database.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    try:
        run(args.port)
    except KeyboardInterrupt:
        print('\nServer stopped.')
