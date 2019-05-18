import regex as re


class MdToc(object):

    def __init__(self, config: dict):
        self.HEAD = config["pattern"].get("HEAD")
        self.head_info = config["constant"].get("HEAD")

    @staticmethod
    def get_filepath_and_filename(file_info: str):
        """获取文本路径信息"""
        file_info_data = file_info.split('/')
        file_name = file_info_data[-1]
        file_path = "/".join(file_info_data[:-1])
        return file_path, file_name

    def process_line(self, line: str):
        """处理读取的一行内容"""
        for h, v in self.HEAD.items():
            m = re.search(v, line)
            if m is None:
                continue
            return m.group(0).split(" ", 1)
        return []

    def get_level(self, tag: str):
        for h, val in self.head_info.items():
            if tag == val["content"]:
                return val["level"]
        return None


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
    def add_child(node, target_node):
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

    @staticmethod
    def get_father_node(node, target_node):
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
            return HeadNode.get_father_node(node, target_node.father)

    @staticmethod
    def print_node_tree(node):
        """打印当前节点下的所有子节点"""
        print("-" * abs(node.level), node.content)
        for i in node.children:
            HeadNode.print_node_tree(i)
