import regex as re
from mdtoc.tools.match import HEAD


def process_line(line: str):
    for h, v in HEAD.items():
        m = re.search(v, line)
        if m is None:
            continue
        return m.group(0)
    return False
