#! /usr/bin/env python
#coding=utf-8
from __future__ import division
import math
import numpy as np
import xmlrpc.client
import copy

class Event_Stream:
    
    def __init__(self, clusters_num):
        self.clusters_num = clusters_num
        self.proxy = xmlrpc.client.ServerProxy("http://localhost:6567/")
        self.clusters_stream = []
        #self.clusters_temp = {}
        self.cosines = np.zeros(5)
        #self.cluster_ems = np.zeros(5 * 300).reshape(5, 300)
        self.cluster_ems = [[0.0 for ll in range(300)] for l in range(5)]
        self.index_ = [0, 1, 2, 3, 4]
        self.index_all = []
        self.all = 0
        self.t = 0
        self.clusters_temp = [[] for l in range(5)]
        self.clusters_temp_ems = [[] for l in range(5)]
        self.clusters_returns = []
        self.clusters_return = [[] for l in range(5)]

    def get_tweets(self, tweets):
        for inx, tweet in enumerate(tweets):
            self.get_one_tweet(inx, tweet)
            #print self.index_
            #print self.clusters_returns[inx]
        #print 'new: ' + str(self.t)
        #zeros, alls = self.proxy.num()
        #print 'all words num: ' + str(alls) + 'zeros num: ' + str(zeros)
        ps = []
        print len(self.clusters_returns)
        for returns in self.clusters_returns:
            ps1 = []
            print returns
            for ret in returns:
                ps2 = []
                if len(ret) == 0:
                    ps2.append('')
                    ps2.append('')
                else:
                    for re in ret:
                        ps2.append(tweets[re])
                    if len(ret) < 2:
                        ps2.append('')
                ps1.append(ps2)
            ps.append(ps1)
        #print self.index_all
        #print ps
        res = []
        for i in range(len(tweets)):
            res1 = []
            for j in range(5):
                res1.append([self.index_all[i][j], ps[i][j][0], ps[i][j][1]])
            res.append(res1)
        #return [self.index_all, ps]
        return res

    def get_one_tweet(self, inx, tweet):
        if tweet == '':
            pass
        tweet_l = tweet.strip().split()
        words_em = self.get_embedding(tweet_l)
        self.get_cluster(words_em, inx)
        #return self.index_

    def get_embedding(self, tweet_l):
        words_em = np.zeros(300)
        for word in tweet_l:
            words_em += self.proxy.getw(word)
        #print words_em
        return words_em
    
    def get_cluster(self, words_em, inx):
        #if self.clusters_stream == False:
        #    pass
        #res = []
        scores = []
        for i in range(self.clusters_num):
            scores.append(self.similar(words_em, self.cluster_ems[i]))
        max_v = max(scores)
        max_i = scores.index(max_v)
        #print 'all: ' + str(self.all)
        if max_v < sum(self.cosines) / self.clusters_num:
            if self.all < self.clusters_num:
                self.list_add(self.cluster_ems[self.all], words_em)
                self.clusters_temp[self.all].append(inx)
                self.clusters_temp_ems[self.all].append(words_em)
                #res.append(0)
                #res.append(inx)
                self.clusters_return[self.all].append(inx)
            else:
                self.index_.pop(0)
                self.index_.append(self.all)
                
                self.cluster_ems.pop(0)
                self.cluster_ems.append(words_em)
                self.t += 1

                self.clusters_temp.pop(0)
                self.clusters_temp.append([])
                self.clusters_temp[4].append(inx)

                self.clusters_temp_ems.pop(0)
                self.clusters_temp_ems.append([])
                self.clusters_temp_ems[4].append(words_em)
                #res = self.get_summ(clusters_temp_ems)

                self.clusters_return.pop(0)
                self.clusters_return.append([])
                self.clusters_return[4].append(inx)

            self.all += 1
            #print 'new ...'
        else:
            if self.all < self.clusters_num:
                self.list_add(self.cluster_ems[self.all], words_em)
                self.clusters_temp[self.all].append(inx)
                self.clusters_temp_ems[self.all].append(words_em)
                #res.append(0)
                #res.append(inx)
                self.clusters_return[self.all].append(inx)
                self.all += 1
                #print 'old new ...'
            else:
                t = self.index_.pop(max_i)
                self.index_.append(t)

                t = self.cluster_ems.pop(max_i)
                self.list_add(words_em, t)
                self.cluster_ems.append(words_em)

                t = self.clusters_temp.pop(max_i)
                t.append(inx)
                self.clusters_temp.append(t)

                k = self.clusters_temp_ems.pop(max_i)
                k.append(words_em)
                self.clusters_temp_ems.append(k)
                #res = self.get_summ(clusters_temp_ems)

                clus = self.clusters_return.pop(max_i)
                clus = self.get_summ(k)
                cls = []
                for cl in clus:
                    cls.append(t[cl])
                    #self.clusters_return.
                self.clusters_return.append(cls)

                #print 'old ...'
        self.cosines = scores
        self.index_all.append(copy.deepcopy(self.index_))
        #self.clusters_stream.append(clusters_temp)
        self.clusters_returns.append(copy.deepcopy(self.clusters_return))

    def list_add(self, A, B):
        for i in range(len(A)):
            A[i] += B[i]

    def similar(self,source,target):
        numerator=sum([source[word]*target[word] for word in range(len(source))])
        sourceLen=math.sqrt(sum([value*value for value in source]))
        targetLen=math.sqrt(sum([value*value for value in target]))
        denominator=sourceLen*targetLen
        if denominator==0:
            return 0
        else:
            return numerator/denominator

    def get_summ(self, A):
        m = len(A)
        if m < 3:
            if m == 2:
                return 0, 1
            if m == 1:
                return 0
        
        T = np.zeros((m, m))
        for i in range(m):
            for j in range(m):
                T[i, j] = self.similar(A[i], A[j])
        pr_results = self.pagerank(T, m)
        rc_results = self.redundance_control(T, A, m, pr_results, threshold = 0.5)
        if len(rc_results) < 2:
            return [pr_results[0], pr_results[1]]

        return [rc_results[0], rc_results[1]]

    def pagerank(self, T, m, iter_num = 10):
        Y = [1 for i in range(m)]
        NT = np.zeros((m, m))
        #normalization T
        for i in range(m):
            sumj = sum([T[i, j] for j in range(m)])
            for j in range(m):
                NT[i, j] = T[i, j] / sumj
        #pagerank process
        for t in range(iter_num):
            ty = [0 for i in range(m)]
            for i in range(m):
                ty[i] = 0.15 + 0.85 * sum([NT[j, i] * Y[j] for j in range(m) if i != j])
            Y = ty

        results = [(y, i) for i, y in enumerate(Y)]

        results.sort(reverse=True)

        return [result[1] for result in results]
        
    def redundance_control(self, T, A, m, pr_results, threshold = 0.75):
        pr_results_dict = dict([(index, sort_index) for sort_index, index in enumerate(pr_results)])
        redundance = []
        for i in range(m):
            for j in range(i+1, m):
                if T[i, j] > threshold:
                    if pr_results_dict[i] > pr_results_dict[j]:
                        redundance.append(j)
                    else:
                        redundance.append(i)
        return [i for i in pr_results if i not in set(redundance)]

