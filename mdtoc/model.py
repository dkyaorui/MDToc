import regex as re
import random
import os


class HeadNode(object):
    """
    标题标签节点，用于生成目录树
    """

    def __init__(self, level: int, content: str, father=None):
        """
        H1-H6 标签节点
        :param level: 节点的登记，1=>H1····
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
    """
    工具类，包含一些常用方法
    """

    def __init__(self, config: dict):
        self.HEAD = config["pattern"].get("HEAD")
        self.head_info = config["constant"].get("HEAD")
        self.md_type = config.get("type", "github")

    def process_line(self, line: str) -> list:
        """处理读取的一行内容"""
        for h, v in self.HEAD.items():
            m = re.search(v, line)
            if m is None:
                continue
            return m.group(0).split(" ", 1)
        return []

    def get_level(self, tag: str) -> int:
        """
        返回tag的优先级
        :param tag: 标题标签
        :return: 优先级，不存在返回 0
        """
        for h, val in self.head_info.items():
            if tag == val["content"]:
                return val["level"]
        return 0

    def rebuild_head(self, file: str) -> bool:
        """
        重新构建所有等级的标题
        :param file: 文件路径
        :return: 返回 bool 结果
        """
        if self.md_type == "github":
            if self.head_in_github(file):
                return True

    def head_in_github(self, file: str) -> bool:
        """
        适配 github markdown 显示规则
        :param file: 文件路径
        :return: 返回 bool 结果
        """
        temp_file = str(random.random()) + ".md"
        with open(file, "r") as f, open(temp_file, "w") as t:
            for line in f.readlines():
                res = self.process_line(line)
                if res:
                    tag, content = res
                    content = content.replace(' ', '')
                    line = tag + " " + content
                t.write(line+"\n")
        os.remove(file)
        os.rename(temp_file, file)
        return True

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
        # 生成当前节点的锚点
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
            # 写入完整目录
            for i in directory:
                _out.write(i)
            # 写入文件内容
            for i in _in.readlines():
                _out.write(i)
        # 返回文件路径
        if out_file is None:
            os.remove(file)
            os.rename(temp_file, file)
            return file
        else:
            os.rename(temp_file, out_file)
            return out_file
