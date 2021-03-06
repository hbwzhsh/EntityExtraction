# coding=utf-8

# 引入外部库
from py2neo import *


# 引入内部库


class Neo4j:
    def __init__(self, ip: str, password: str, user='neo4j', http_port=7474, https_port=7473, bolt_port=7687):
        # Neo4j数据库连接
        self.graph = Graph(host=ip, password=password, user=user, http_port=http_port, https_port=https_port,
                           bolt_port=bolt_port)

    def crate_graph(self, entity_info: list, entity_rel: list)->None:
        """
        根据所传入的实体信息链表和实体关系三元组链表，构建子图，并存储到Neo4j
        注意：不考虑图谱中已经存在的相同实体
        :param entity_info: element: {type: str, property: dict}
        :param entity_rel: element: (n1_index, {name: str, property: dict}, n2_index)
        :return: None
        """
        sub_graph = None
        nodes = {}
        index = 0

        print('开始创建实体节点！')
        for info in entity_info:
            node = Node(info['type'], name=info['property']['name'])
            node.update(info['property'])
            nodes[index] = node
            index += 1
            if sub_graph is None:
                sub_graph = node
            else:
                sub_graph = sub_graph | node

        print('开始创建实体间关系！')
        for rel in entity_rel:
            relation = Relationship(nodes[rel[0]], rel[1]['name'], nodes[rel[2]])
            if 'property' in rel[1]:
                relation.update(rel[1]['property'])
            sub_graph = sub_graph | relation

        print('开始存储实体关系！')
        self.graph.create(sub_graph)

    def connect_graph(self):
        pass
