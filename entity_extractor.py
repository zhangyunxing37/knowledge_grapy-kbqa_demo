# coding: utf-8

import os
import ahocorasick
import jieba
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class EntityExtractor:
    def __init__(self):
        self.feature_path = 'C:\\Users\\Desktop\\IP域问答\\ip域dict\\特性.txt'
        self.oprate_path = 'C:\\Users\\Desktop\\IP域问答\\ip域dict\\操作对象.txt'
        self.oprate2_path = 'C:\\Users\\Desktop\\IP域问答\\ip域dict\\问题操作.txt'
        self.vocab_path = 'C:\\Users\\Desktop\\IP域问答\\ip域dict\\vocab.txt'
        
        self.feature_entities = [w.strip() for w in open(self.feature_path, encoding='utf-8-sig') if w.strip()]
        self.oprate_entities = [w.strip() for w in open(self.oprate_path, encoding='utf-8-sig') if w.strip()]
        self.oprate2_entities = [w.strip() for w in open(self.oprate2_path, encoding='utf-8-sig') if w.strip()]
        
        # 构造领域actree
        self.feature_tree = self.build_actree(list(set(self.feature_entities)))
        self.oprate_tree = self.build_actree(list(set(self.oprate_entities)))
        self.oprate2_tree = self.build_actree(list(set(self.oprate2_entities)))
    def build_actree(self, wordlist):
        """
        构造actree--存成词典
        :param wordlist:
        :return:
        """
        actree = ahocorasick.Automaton()
        # 向树中添加单词
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree
    # 全匹配构建
    def entity_reg(self, question):
        """
        模式匹配, 得到匹配的词和类型。
        :param question:str
        :return:
        """
        self.result = {}

        for i in self.feature_tree.iter(question):
            word = i[1][1]
            if "feature" not in self.result:
                self.result["feature"] = [word]
            else:
                self.result["feature"].append(word)

        for i in self.oprate_tree.iter(question):
            word = i[1][1]
            if "oprate" not in self.result:
                self.result["oprate"] = [word]
            else:
                self.result["oprate"].append(word)

        for i in self.oprate2_tree.iter(question):
            wd = i[1][1]
            if "oprate2" not in self.result:
                self.result["oprate2"] = [wd]
            else:
                self.result["oprate2"].append(wd)
        if "feature" not in self.result:
            self.result = self.find_sim_words(question, "feature")
        if "oprate" not in self.result:
            self.result = self.find_sim_words(question, "oprate")
        if "oprate2" not in self.result:
            self.result = self.find_sim_words(question, "oprate2")
        return self.result
    def find_sim_words(self, question,flag):
        import re
        import string
        from gensim.models import KeyedVectors
        stop_word_path = "C:\\Users\\z50004593\\Desktop\\词库\\停用词库\\stop_words.utf8"
        stopwords = [w.strip() for w in open(stop_word_path, 'r', encoding='utf8') if w.strip().strip('\n')]

        jieba.load_userdict(self.vocab_path)
        
        sentence = re.sub("[，。‘’；：？、！【】]", " ", question)
        sentence = sentence.strip()

        words = [w.strip() for w in jieba.cut(sentence) if w.strip() not in stopwords and len(w.strip()) >= 2]
        print(words)

        for word in words:
            alist = []
            temp = [self.feature_entities, self.oprate_entities, self.oprate2_entities]
            if flag == "feature":
                i=0
            elif flag == "oprate":
                i=1
            elif flag == "oprate2":
                i=2
            scores = self.simCal(word, temp[i], flag)
            alist.extend(scores)
            temp1 = sorted(alist, key=lambda k: k[1], reverse=True)
            if temp1:
                self.result[temp1[0][2]] = [temp1[0][0]]
        return self.result
    def simCal(self, word, entities, flag):
        """
        计算词语和字典中的词的相似度
        相同字符的个数/min(|A|,|B|)   +  余弦相似度
        :param word: str
        :param entities:List
        :return:
        """
        import synonyms as sy
        a = len(word)
        scores = []
        for entity in entities:
            sim_num = 0
            b = len(entity)
            c = len(set(entity + word))
            temp = []
            try:
                if not np.isnan(sy.compare(word, entity)):
                    score2 = sy.compare(word, entity)  
                    temp.append(score2)
            except:
                pass
            score3 = 1 - self.editDistanceDP(word, entity) / (a + b) 
            if score3 > 0.5:
                temp.append(score3)

            score = sum(temp) / len(temp)
            if score >= 0.7:
                scores.append((entity, score, flag))

        scores.sort(key=lambda k: k[1], reverse=True)
        return scores
    def editDistanceDP(self, s1, s2):
        """
        采用DP方法计算编辑距离
        :param s1:
        :param s2:
        :return:
        """
        m = len(s1)
        n = len(s2)
        solution = [[0 for j in range(n + 1)] for i in range(m + 1)]
        for i in range(len(s2) + 1):
            solution[0][i] = i
        for i in range(len(s1) + 1):
            solution[i][0] = i

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    solution[i][j] = solution[i - 1][j - 1]
                else:
                    solution[i][j] = 1 + min(solution[i][j - 1], min(solution[i - 1][j],
                                                                     solution[i - 1][j - 1]))
        return solution[m][n]

