import regex as re
import random
import os


class HeadNode(object):
    def __init__(self, level: int, content: str, father=None):
        """
        H1-H6 标签节点
        :param level: 节点的登记，1=》H1····
        :param content: 标题内容
        :return: None
        """
        self.level = level
        self.content = content
        self.father = father
        self.children = list()

    @staticmethod
    def add_child(node, target_node) -> bool:
        """
        在 self.children 中添加子节点
        :param node: Node，标签节点
        :param target_node: 父亲节点
        :return:
        """
        if isinstance(node, HeadNode):
            node.father = target_node
            target_node.children.append(node)
            return True
        return False


class MdToc(object):

    def __init__(self, config: dict):
        self.HEAD = config["pattern"].get("HEAD")
        self.head_info = config["constant"].get("HEAD")

    def process_line(self, line: str) -> list:
        """处理读取的一行内容"""
        for h, v in self.HEAD.items():
            m = re.search(v, line)
            if m is None:
                continue
            return m.group(0).split(" ", 1)
        return []

    def get_level(self, tag: str) -> int:
        for h, val in self.head_info.items():
            if tag == val["content"]:
                return val["level"]
        return 0

    @staticmethod
    def print_node_tree(node: HeadNode) -> None:
        """打印当前节点下的所有子节点"""
        print("-" * abs(node.level), node.content)
        for i in node.children:
            MdToc.print_node_tree(i)

    @staticmethod
    def get_father_node(node: HeadNode, target_node: HeadNode) -> HeadNode:
        """
        找到 node 的父亲
        :param node: 没有父亲的节点
        :param target_node: 目标节点家族
        :return:
        """
        if node.level == target_node.level:
            return target_node.father
        elif node.level < target_node.level:
            return target_node
        else:
            return MdToc.get_father_node(node, target_node.father)

    @staticmethod
    def create_directory(node: HeadNode) -> list:
        directory = []
        # 生成当前节点到锚点
        temp = " " * abs(node.level + 1) * 2 + \
               "* [" + node.content.replace(' ', '') + "]" + \
               "(#" + node.content + ")\n\n"
        directory.append(temp)
        for n in node.children:
            directory += MdToc.create_directory(n)
        return directory

    @staticmethod
    def write_into_file(directory, file, out_file=None) -> str:
        """
        生成目标文件
        :param directory: 目录信息
        :param file: 源文件完整路径
        :param out_file: 目标文件完整路径
        :return: 结果文件完整路径
        """
        temp_file = str(random.random()) + ".md"
        with open(temp_file, "a") as _out, open(file, "r") as _in:
            # 获取H1
            while True:
                line = _in.readline()
                if re.search(r"^#{1}\s.*", line):
                    break
            # 写入 H1 和 目录（H2）
            _out.write(line + '\n')
            _out.write("#" * 2 + " " + "目录\n\n")
            for i in directory:
                _out.write(i)
            for i in _in.readlines():
                _out.write(i)
        if out_file is None:
            os.remove(file)
            os.rename(temp_file, file)
            return file
        else:
            os.rename(temp_file, out_file)
            return out_file
