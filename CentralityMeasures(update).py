# -*- coding: utf-8 -*-
"""
Created on Sun Nov 05 13:50:53 2017

@author: WZW
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import numpy as np



#n is nodes' number ,multiple is nodes'number / addnode
def addnode(graph,n,multiple,p):
    for index in range(n/multiple):
        node = []
        graph.add_node(n+index)
        aaaaaa = 0
        while (len(node) <= ((n+index) * p)):
            aaaaaa += 1
            a = random.randint(0,n-1)
            while a in node:
                a = random.randint(0,n-1)
            node.append(a)
            graph.add_edge(a,n+index) 
            
    return graph

def removenode(graph,n,multiple):
    for index in range(n/multiple):
        i = 1
        while i == 1: 
            a = random.randint(0,n-1)
            if graph.node.has_key(a):
                graph.remove_node(a)
                break
    return graph

def addedge(graph,multiple):
    for index in range(graph.number_of_edges()/multiple):
        i = 1
        while i == 1:
            a = random.randint(0,graph.number_of_nodes()-1)
            b = random.randint(0,graph.number_of_nodes()-1)
            while a == b:
                b = random.randint(0,graph.number_of_nodes()-1)
            flag = 0
            for(u,v) in graph.edges():
                if (u,v) == (a,b) or (u,v) == (b,a):
                    flag = 1
            if flag == 0:
                graph.add_edge(a,b)
                break
    return graph
        
def removeedge(graph,multiple):
    for index in range(int(graph.number_of_edges()/multiple)):
        i = 1
        for(u,v) in graph.edges():
            #this place can be better
            if(i == 1): 
                graph.remove_edge(u,v)
                i = i-1
    return graph

def method(flag,graph,n,multiple):
    if flag == 1:
        return addnode(graph,n,multiple,p)
    elif flag == 2:
        return removenode(graph,n,multiple)
    elif flag == 3:
        return addedge(graph,multiple)
    elif flag == 4:
        return removeedge(graph,multiple)

def calproperty(attrbute,graph):
    if attrbute == 1:
        return nx.degree(graph)
    elif attrbute == 2:
        return nx.betweenness_centrality(graph)
    elif attrbute == 3:
        return nx.closeness_centrality(graph)
    elif attrbute == 4:
        return nx.eigenvector_centrality(graph)

#these method to find top1，top3，top10percent。and the same node
#all g_drgree not degree but the one of (degree,betweenness,closeness,eigenvector)
def calTOP1(attrbute,flag,graph,n,multiple):
    g_degree = calproperty(attrbute,graph)
    node_max_1 = sorted(g_degree,key=lambda x:g_degree[x])[-1]
    graph1 = method(flag,graph,n,multiple)
    g1_degree = calproperty(attrbute,graph1)
    node_max_2 = sorted(g1_degree,key=lambda x:g1_degree[x])[-1]
    if node_max_1 == node_max_2:
        return 1
    else:
        return 0

def calTOP3(attrbute,flag,graph,n,multiple):
    g_degree = calproperty(attrbute,graph)
    node_max3 = []
    for i in range(1,4):
        a = sorted(g_degree,key=lambda x:g_degree[x])[-i]
        node_max3.append(a)
    graph1 = method(flag,graph,n,multiple)
    g1_degree = calproperty(attrbute,graph1)
    node_max_2 = sorted(g1_degree,key=lambda x:g1_degree[x])[-1]
    return  node_max3,node_max_2

def calTOP10percent(attrbute,flag,graph,n,multiple):
    g_degree = calproperty(attrbute,graph)
    node_max10p = []
    nodes = []
    for i in range(1,len(g_degree)/10+1):
        a = sorted(g_degree,key=lambda x:g_degree[x])[-i]
        node_max10p.append(a)
    graph1 = method(flag,graph,n,multiple)
    g1_degree = calproperty(attrbute,graph1)
    node_max10p_observed = []
    for i in range(1,len(g1_degree)/10+1):
        a = sorted(g1_degree,key=lambda x:g1_degree[x])[-i]
        node_max10p_observed.append(a)
    return  node_max10p,node_max10p_observed

def calTOP10percentfor10p(attrbute,flag,graph,n,multiple):
    g_degree = calproperty(attrbute,graph)
    node_max10p = []
    for i in range(1,len(g_degree)/10+1):
        a = sorted(g_degree,key=lambda x:g_degree[x])[-i]
        node_max10p.append(a)
    graph1 = method(flag,graph,n,multiple)
    g1_degree = calproperty(attrbute,graph1)
    node_max_2 = sorted(g1_degree,key=lambda x:g1_degree[x])[-1]
    return  node_max10p,node_max_2

def calsame(attrbute,flag,graph,n,multiple):
    g_degree = calproperty(attrbute,graph)
    graph1 = method(flag,graph,n,multiple)
    g1_degree = calproperty(attrbute,graph1)
    l = []
    list_true = []
    list_observe = []
    if flag == 2:
        for key in g1_degree:
            if key in g1_degree:
                l.append(key)
    else:
        for key in g_degree:
            if key in g_degree:
                l.append(key)
    for i in l:
        list_true.append(g_degree[i])
        list_observe.append(g1_degree[i])
    return list_true,list_observe

#these method to calculate 5 index
def calresultTOP1(attrbute,flag,n,p,multiple,cycle):
    number = 0
    for i in range(0,cycle):
        g =nx.erdos_renyi_graph(n,p)
        number += calTOP1(attrbute,flag,g,n,multiple)

    percent = float(number)/cycle
    return percent
    

def calresultTOP3(attrbute,flag,n,p,multiple,cycle):
    percent = 0
    for i in range(0,cycle):
        g =nx.erdos_renyi_graph(n,p)
        node_max3_1 = []
        node_max3_1,node_max_2 = calTOP3(attrbute,flag,g,n,multiple)
        if node_max_2 in node_max3_1:
            percent += float(1)
    percent = percent / cycle
    return percent
    
def calresultTOP10percent(attrbute,flag,n,p,multiple,cycle):
    percent = 0
    for i in range(0,cycle):
        percent_once = 0
        g =nx.erdos_renyi_graph(n,p)
        node_max10p_1 = []
        node_max10p_1,node_max_2 = calTOP10percentfor10p(attrbute,flag,g,n,multiple)
        if node_max_2 in node_max10p_1:
            percent += float(1)
    percent = percent / cycle
    
    return percent

def calresultOverlap(attrbute,flag,n,p,multiple,cycle):
    percent = 0
    for i in range(0,cycle):
        percent_once = 0
        number_intersection = 0
        number_union = 0
        g =nx.erdos_renyi_graph(n,p)
        node_max10p_1 = []
        node_max10p_2 = []
        node_max10p_1,node_max10p_2 = calTOP10percent(attrbute,flag,g,n,multiple)
        for l in node_max10p_1:
            if l in node_max10p_2:
                number_intersection += 1
        union = list(set(node_max10p_1).union(set(node_max10p_2)))
        for i in union:
            number_union += 1 
        percent_once = float(number_intersection) / number_union
        percent += percent_once
    percent = percent / cycle
    return percent

def cos(vector1,vector2):  
    dot_product = 0.0;  
    normA = 0.0;  
    normB = 0.0;  
    for a,b in zip(vector1,vector2):  
        dot_product += a*b  
        normA += a**2  
        normB += b**2  
    if normA == 0.0 or normB==0.0:  
        return None  
    else:  
        return dot_product / ((normA*normB)**0.5)  

"""!!!!!师兄，这是第三的问题，同TOP3，前百分之10的结果都和表中对不上，余弦相似性也是找不出问题，但是就是结果对不上，希望您能帮我看看"""
def calresultR(attrbute,flag,n,p,multiple,cycle):
    
    percent = 0
    for i in range(0,cycle):
        g =nx.erdos_renyi_graph(n,p)
        percent_once = 0
        list_true = []
        list_observe = []
        list_true,list_observe = calsame(attrbute,flag,g,n,multiple)
        
        x = 0
        sqrt1 = 0
        sqrt2 = 0
        percent_once = cos(list_true,list_observe)
        
        """
        s1 = 0
        s2 = 0
        sss = 0
        y_avg = 0
        for a in list_true:
            sss += a
        y_avg = float(sss) / len(list_true)
        for a,b in zip(list_true,list_observe):
            s1 += float((a-b)**2)
            
            s2 += float((a-y_avg)**2)
        percent_once = 1 - s1/s2
        percent += percent_once
        """
    percent = percent / cycle
    return percent
    
    
#n is the number of samples
#p is the density
#multiple is 1/the change of degree

"""
flag is to choose the method
1:addnode
2:removenode
3:addedge
4:removeedge
"""
"""
attrbute is to choose the Node properties
1:degree
2:betweenness
3:closeness
4:eigenvector
"""


n = 100
p = 0.5
multiple = 2
flag = 2
attrbute = 1
cycle = 1000
#output the 5 index

print calresultTOP1(attrbute,flag,n,p,multiple,cycle)
print calresultTOP3(attrbute,flag,n,p,multiple,cycle)
print calresultTOP10percent(attrbute,flag,n,p,multiple,cycle)
print calresultOverlap(attrbute,flag,n,p,multiple,cycle)
print calresultR(attrbute,flag,n,p,multiple,cycle)
