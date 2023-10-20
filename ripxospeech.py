import argparse
import flask
import sys

class KeyboardServer:
    def __init__(self):
        # Create Flask app
        self.app = flask.Flask(__name__)

        # Add routes for key press and key release
        self.app.add_url_rule('/key_press', 'key_press', self.key_press, methods=['POST'])
        self.app.add_url_rule('/key_release', 'key_release', self.key_release, methods=['POST'])

    def key_press(self):
        print('Yeah buddy')
        key = flask.request.form['key']
        print('Key press received: {}'.format(key), file=sys.stderr)
        # Do something with the key press
        return 'Key press received: {}'.format(key)

    def key_release(self):
        key = flask.request.form['key']
        print('Key release received: {}'.format(key), file=sys.stdout)
        # Do something with the key release
        return 'Key release received: {}'.format(key)

    def run(self):
        # Run Flask app on all interfaces
        self.app.run(host='0.0.0.0')


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # Create KeyboardServer instance and run it
    server = KeyboardServer()
    server.run()


if __name__ == '__main__':
    main()
