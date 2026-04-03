from configparser import ConfigParser
from pathlib import Path

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()

    path = Path(file).resolve().parent / filename

    with open(path, 'r', encoding='utf-8') as f:
        parser.read_file(f)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return config