#!/usr/bin/env python
import datetime
import flask
import redis


app = flask.Flask(__name__)
app.secret_key = 'asdfa'
red = redis.StrictRedis()


def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('chat')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        print(message['type'])
        if message['type'] != 'message':
            continue
            #pass
        print(message)
        yield 'data: %s\n\n' % message['data']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        flask.session['user'] = flask.request.form['user']
        return flask.redirect('/')
    return '<form action="" method="post">user: <input name="user">'


@app.route('/post', methods=['POST'])
def post():
    print('post')
    message = flask.request.form['message']
    print('mmmm: ' + message)
    user = flask.session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    red.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return flask.Response(status=204)


@app.route('/stream')
def stream():
    print('hehe')
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


@app.route('/')
def home():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    return """
        <!doctype html>
        <title>chat</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        <p><b>hi, % s!</b></p>
        <p>Message: <input id="in" /></p>
        <pre id="out"></pre>
        <script>
            function sse() {
                var source = new EventSource('/stream');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    // XSS in chat is fun
                    out.innerHTML =  e.data + '\\n' + out.innerHTML;
                    //out.innerHTML = 'abcn';
                };
            }
            $('#in').keyup(function(e){
                if (e.keyCode == 13) {
                    $.post('/post', {'message': $(this).val()});
                    $(this).val('');
                }
            });
            sse();
        </script>
    """ % flask.session['user']


if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)

