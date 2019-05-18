from mdtoc.model import MdToc, HeadNode
from mdtoc.config import config
import click


@click.command()
@click.option("--file", default=None, help="The path of target *.md file.")
def start(file: str):
    """
    开始处理 markdown 文件
    Start process the markdown file
    :param file: 文件完整路径或相对路径 the path of markdown file
    :return: 处理结果 the result of process
    """
    if file is None:
        click.echo("Please use --help option read doc.")
    else:
        toc = MdToc(config)
        # 存放 H1 节点信息
        head_list = list()
        now_node = None
        file_path, file_name = toc.get_filepath_and_filename(file)
        print(file_path, file_name)
        with open(file, "r") as f:
            for line in f.readlines():
                res = toc.process_line(line)
                if res:
                    # 如果匹配到标题
                    tag, content = res
                    level = toc.get_level(tag)
                    node = HeadNode(level, content)
                    if now_node is None:
                        # 初始化第一个节点为 now_node
                        now_node = node
                        head_list.append(now_node)
                    else:
                        if node.level == -1:
                            # 将 H1 节点放入 head_list
                            head_list.append(node)
                        else:
                            if node.level < now_node.level:
                                # 如果节点等级小于当前节点，将其变为孩子
                                HeadNode.add_child(node, now_node)
                            else:
                                father = MdToc.get_father_node(node, now_node)
                                HeadNode.add_child(node, father)
                        now_node = node
        for i in head_list:
            MdToc.print_node_tree(i)
