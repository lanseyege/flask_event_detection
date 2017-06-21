import datetime
import flask
import redis
import time
from flask import render_template
from get_tweets import getTweets
from get_event_t import Event_Stream

app = flask.Flask(__name__)
app.secret_key = 'asdfb'
red = redis.StrictRedis()

special_t = '_even_and_cluster_'

def get_form(ps, ind):
    '''
    print('ind')
    print(ind)
    print('ps')
    print(ps)
    '''
    ss = ''
    for i in range(5):
        #print(ps[i][0])
        #print(ps[i][1])
        '''
        ss += '<p><font size="3">' + str(ind[i]) + '</font></p>' + \
        '<ul>' + \
           '<li>' + ps[i][0] + '</li>' + \
          '<li>' + ps[i][1] + '</li>' + \
         '</ul>'
        '''
        ss += '<p><font size="3">' + str(ind[i]) + '</font></p>' + \
                '<ul><li> 1: ' + ps[i][0] + ' 2: ' + ps[i][1] + '</li></ul>'
    print(ss)
    return ss

def event_stream_t():
    print('event_stream_t')
    pubsub = red.pubsub()
    pubsub.subscribe('tweet')
    for message in pubsub.listen():
        print(message)
        if message['type'] != 'message':
            continue
        search = message['data']
        print('search: ' + str(search))
        print('event_stream_t')
        #tweets = []
        
        event_stream = Event_Stream(5, 15)
        for tweet, inx in getTweets(search):
            print('tweet inx')
            print(tweet)
            print(inx)
            #tweets.append(tweet)
            #tweet = str(inx) + ': ' + tweet
            ps, ind = event_stream.get_tweets(tweet, inx)
            ss = get_form(ps, ind)
            ss = '<tr><td>' + ss + '</td></tr>'
            tweet = '<tr><td>' + str(inx) + '</td><td>' + tweet + '</td></tr>'
            tweet = tweet + special_t + ss
            yield 'data:%s\n\n' % tweet

            time.sleep(0.5)

@app.route('/post_t/', methods = ['POST'])
def post_t():
    print('post_t')
    search = flask.request.form['message']
    print('search: ' + search)
    print('search')
    red.publish('tweet', r'%s' % (search))
    return flask.Response(status=204)

@app.route('/stream_t')
def stream_t():
    print('stream_t')
    return flask.Response(event_stream_t(), mimetype="text/event-stream")

@app.route('/forecast/')
def home():
    return render_template('forecast_t.html' )
    
if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True)
