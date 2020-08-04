def get_content_from_file(file_path):
    file = open(file_path, 'r')
    file_content = file.readlines()
    file.close()
    return file_content


def get_sanitized_content_from_file(file_path):
    file_content = get_content_from_file(file_path)

    sanitized_file_content = []
    for line in file_content:
        sanitized_file_content.append(line.strip())
    return sanitized_file_content
