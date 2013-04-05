from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from gevent import monkey
from flask import Flask, Response, request, render_template

monkey.patch_all()
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_socketio():
    return render_template('index.html')


class FooNamespace(BaseNamespace):

    def on_event_from_client(self, data):
        msg = 'Server Received: %s' % data
        self.emit('event_from_server', msg)
        return True


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    socketio_manage(request.environ, {'/foo': FooNamespace}, request)

    return Response()

if __name__ == '__main__':
    app.run()
