import os
import shutil
from os import PathLike


def move_files(source: str, destination: str) -> None:
    if not os.path.isdir(source):
        raise ValueError(f'source has to be a directory: {source}')
    # if not os.path.isdir(destination):
    #     raise ValueError(f'destination has to be a directory: {destination}')

    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)

    source_list = os.listdir(source)
    for item in source_list:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        print(source_path)
        if os.path.isdir(source_path):
            move_files(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)
