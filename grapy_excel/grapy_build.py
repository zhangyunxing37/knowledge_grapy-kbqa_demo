#coding=utf-8
# 知识图neo4j python构建
from py2neo import Graph, Node, Relationship, NodeSelector 
import numpy as np
import pandas as pd
import re
import os


class IP_Graph:
    def __init__(self):
        self.feature_path = "C:\\Users\\Desktop\\IP域问答\\特性类.csv"
        self.opt_path = "C:\\Users\\Desktop\\IP域问答\\操作对象.csv"
        self.sollution = 'C:\\Users\\Desktop\\IP域问答\\问题操作类.csv'
        self.f_o = "C:\\Users\\Desktop\\IP域问答\\特性_对象.csv"
        self.o_s = "C:\\Users\\Desktop\\IP域问答\\对象_操作.csv"
        self.graph = Graph("http://localhost:7474", username="neo4j", password='10086111')
        
    # 实体、关系csv表格导入
    def read_file(self):
        feature = np.array(pd.read_csv(self.feature_path)).tolist()
        opt = pd.read_csv(self.opt_path)
        opt.drop_duplicates(inplace = True)
        opt = np.array(opt).tolist()
        sollution = np.array(pd.read_csv(self.sollution)).tolist()
        f_o = pd.read_csv(self.f_o)
        f_o.drop_duplicates(inplace = True)
        f_o = np.array(f_o).tolist()
        o_s = np.array(pd.read_csv(self.o_s)).tolist()
        return feature, opt, sollution, f_o, o_s
    
    # 后续大规模图谱构建需要修改该函数
    def creat_entity(self):
        # 实体节点及关系创建
        feat, opt, sol, r1, r2 = self.read_file()
        # 特性类实体创建
        feat_count = 0
        for p in feat:
            node = Node('feature', name=p[0], definition=p[1])
            self.graph.create(node)
            feat_count += 1
            #print(feat_count, len(feat))
        # 操作对象类实体创建
        print(feat_count,len(feat))
        opt_count = 0
        for p in opt:
            node = Node('oprate', name=p[0], content=p[1])
            self.graph.create(node)
            opt_count += 1
        print(opt_count, len(opt))      
        # 问题操作类实体创建
        sol_count=0
        for p in sol:
            node = Node('oprate2', problem=p[0], name=p[1], sollution=p[2])
            self.graph.create(node)
            sol_count += 1
        print(sol_count, len(sol))   
        # 创建关系
        count_r1 = 0
        for p in r1:
            query = "match(p:feature),(q:oprate) where p.name='%s' and q.name='%s' and q.content='%s' create (p)-[rel:opt{name:'对象'}]->(q)" % (p[0], p[1], p[2])
            try:
                self.graph.run(query)
                count_r1 += 1
            except Exception as e:
                print(e)
        print(count_r1)
        ##创建关系
        count_r2 = 0
        for p in r2:
            query = r"match(p:oprate),(q:oprate2) where p.name='%s' and p.content='%s' and q.problem='%s' and q.sollution='%s' create (p)-[rel:opt2{name:'操作'}]->(q)" % (p[0], p[1], p[2],p[3])
            try:
                self.graph.run(query)
                count_r2 += 1
            except Exception as e:
                print(e)
        print(count_r2)
		
    def create_node(self, label, nodes):
        """
        创建节点
        :param label: 标签
        :param nodes: 节点
        :return:
        """
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))
        return
        
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        """
        创建实体关系边
        :param start_node:
        :param end_node:
        :param edges:
        :param rel_type:
        :param rel_name:
        :return:
        """
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = r"match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.graph.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

