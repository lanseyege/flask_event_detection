from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import gensim
import numpy as np

#server = SimpleXMLRPCServer(("localhost", 6567))
model = gensim.models.Word2Vec.load_word2vec_format('data', binary=True)
class Tes:
    def __init__(self):
        self.zeros = 0
        self.alls = 0
    def getw(self, word):
        self.alls += 1
        if word not in model:
            #return np.zeros(300)
            self.zeros += 1
            return [0.0] * 300
        return model[word].tolist()

    def is_even(self, n):
        return n % 2 == 0
    def num(self):
        return self.zeros, self.alls

server = SimpleXMLRPCServer(("localhost", 6567)) 

#server.register_instance(model)
server.register_instance(Tes())
server.serve_forever()

