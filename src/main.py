from utils.tools import get_file_path_and_filename
import sys

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print("请输入文件名")
    else:
        file_info = sys.argv[0]
        file_path, file_name = get_file_path_and_filename(file_info)
        print(file_path, file_name)
