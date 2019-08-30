# coding: utf-8

'''
问题类型
*是什么？
*的*是什么？
*的*的*是什么？
*的*怎么显示？
'''
# 意图识别还有什么改进
import numpy as np
from bert_serving.client import BertClient
# 先要在CMD界面上启动bert_server: bert-serving-start -model_dir dict/chinese_L-12_H-768_A-12 -num_worker=1

class Question_intent:
    def __init__(self):
        self.question_demo = {0:"*是什么", 1:"*常见问题有哪些", 2:"*问题怎么解决", 3:"*的*是什么"}
        self.threshold = 0.825
		
    def query_intent(self,question):
        """句子相似度匹配"""
        from bert_serving.client import BertClient
        bc = BertClient(ip='localhost')
        query_vec = bc.encode([question])[0]
        demo_vec = bc.encode([self.question_demo.get(i) for i in self.question_demo])
        ss = np.linalg.norm(query_vec)
        cosin_sim = np.sum(query_vec *demo_vec, axis=1) / (ss*np.linalg.norm(demo_vec, axis=1))
        topk_idx = np.argsort(cosin_sim)[-1]
        print(cosin_sim)
        if(cosin_sim[topk_idx] > self.threshold):
            return (self.question_demo[topk_idx])
        else: return ('')
		
    def dict_intent(self,question):
        """字典的精准匹配"""
        pass

