def get_file_path_and_filename(file_info: str):
    file_info_data = file_info.split('/')
    file_name = file_info_data[-1]
    file_path = "/".join(file_info_data[:-1])
    return file_path, file_name
