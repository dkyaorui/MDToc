import regex as re


class MdToc(object):

    def __init__(self, config: dict):
        self.HEAD = config.get("HEAD")

    @staticmethod
    def get_file_path_and_filename(file_info: str):
        file_info_data = file_info.split('/')
        file_name = file_info_data[-1]
        file_path = "/".join(file_info_data[:-1])
        return file_path, file_name

    def process_line(self, line: str):
        for h, v in self.HEAD.items():
            m = re.search(v, line)
            if m is None:
                continue
            return m.group(0)
        return False
