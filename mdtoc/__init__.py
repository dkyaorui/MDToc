from mdtoc.tools.utils import get_file_path_and_filename
from mdtoc.tools.process import process_line
from mdtoc.model import MdToc
import click


@click.command()
@click.option("--file", default=None, help="The path of target *.md file.")
def start(file):
    if file is None:
        click.echo("Please use --help option read doc.")
    else:
        file_path, file_name = get_file_path_and_filename(file)
        print(file_path, file_name)
        with open(file, "r") as f:
            for line in f.readlines():
                res = process_line(line)
                if res:
                    print(res)
