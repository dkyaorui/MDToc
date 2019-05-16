from mdtoc.model import MdToc
from mdtoc.config import config
import click


@click.command()
@click.option("--file", default=None, help="The path of target *.md file.")
def start(file):
    if file is None:
        click.echo("Please use --help option read doc.")
    else:
        toc = MdToc(config)
        file_path, file_name = toc.get_file_path_and_filename(file)
        print(file_path, file_name)
        with open(file, "r") as f:
            for line in f.readlines():
                res = toc.process_line(line)
                if res:
                    print(res)
