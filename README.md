# flask_event_detection

We input the key word to get the relative tweets with tweepy interface and show them on the web page, then we adopt the algorithm proposed by Aggarwal et.al. to detect the event and get the clusters. For the five most recent clusters, we choose two most relative tweets with LexRank alogrithm to show on the web page. We adopt the flask framework and redis to implement the server-send-event technology of the website with gunicorn HTTP server.  

test1/get_tweets.py : get tweets by tweepy interface  

test1/get_event_t : get event 

test1/t2.py : the main method  

test1/template/ : web template  

test1/static/ : web rendering  

embedding/google_vectors/s1.py : get embedding with rpc server  

