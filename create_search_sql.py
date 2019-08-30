# coding: utf-8

import numpy as np
import pandas as pd 
from py2neo import Graph


class Aearch_answer:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="10086111")
        self.top_num = 10
		
    def transfor_to_sql(self, result, intent):
        """
        将问题转变为cypher查询语句
        :param label:实体标签
        :param entities:实体列表
        :param intent:查询意图
        :return:cypher查询语句
        """
        if not result:
            return []
        sql = []
        if intent ==0 and "feature" in result:
            sql=["match (d:feature) where d.name='{0}' return d.name,d.definition".format(e) for e in result['feature']]
        if intent == 2 and len(result) == 3:
            sql=["MATCH (a:feature)-[:opt]->(d:oprate)-[:opt2]->(s:oprate2)where a.name='{0}' and d.name='{1}' and s.problem='{2}' return s.sollution".format(result['feature'][0],result['oprate'][0],e) for e in result['oprate2']]
        if intent == 3 and "feature" in result and "oprate" in result:
            sql=["MATCH (a:feature)-[:opt]->(d:oprate)where a.name='{0}' and d.name='{1}' return d.content".format(result['feature'][0],e) for e in result['oprate']]
        if intent == 1 and "feature" in result:
            sql=["MATCH (a:feature)-[:opt]->(d:oprate)-[:opt2]->(s:oprate2) where a.name='{0}' return a.name,d.name,s.problem".format(e) for e in result['feature']]

        return sql
    def func(self, lst):
        a = ''
        for i in lst:
            a = a + str(' ') + str(i)
        return(a)
    
    def answer(self, sql):
        swer = []
        for i in sql:
            qa = self.graph.run(i).data()
            if not qa:
                continue
            for j in qa:
                sd = [j.get(key) for key in j]
                swer.append(self.func(sd))
        return(swer)
