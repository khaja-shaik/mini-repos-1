from collections import defaultdict
from hashlib import sha1
from os import (
    path as os_path,
    walk as os_walk
)
from sys import argv as sys_argv


def read_file_bytes(file_name, bytes_size=1024):
    while True:
        file_1k_bytes = file_name.read(bytes_size)
        if not file_1k_bytes:
            return
        yield file_1k_bytes


def retrieve_hash(filename, first_part=False, hash=sha1):
    hash_instance = hash()
    file_instance = open(filename, 'rb')

    if first_part:
        hash_instance.update(file_instance.read(1024))
    else:
        for block in read_file_bytes(file_instance):
            hash_instance.update(block)
    hashed = hash_instance.digest()

    file_instance.close()
    return hashed


def list_duplicates(path, hash=sha1):
    duplicate_files = []
    duplicate_files_dictionary = {}
    counter = 0
    hash_byte_size = defaultdict(list)  # dict to store files by size in bytes
    hash_1k_bytes = defaultdict(list)  # dict of 1k bytes files
    total_hash = {}   # dict of total hash and file

    for dirpath, dirnames, filenames in os_walk(path):
        for filename in filenames:
            try:
                file_path = os_path.realpath(os_path.join(dirpath, filename))
                file_size = os_path.getsize(file_path)
                hash_byte_size[file_size].append(file_path)
            except OSError:
                continue

    for byte_size, files in hash_byte_size.items():
        if len(files) < 2:
            # To skip files of unique size
            continue

        for filename in files:
            try:
                hash_1k = retrieve_hash(filename, first_part=True)
                hash_1k_bytes[(hash_1k, byte_size)].append(filename)
            except OSError:
                continue

    for __, files_list in hash_1k_bytes.items():
        if len(files_list) < 2:
            # Skip files whose first part bytes are not same
            continue

        for filename in files_list:
            try:
                complete_hash = retrieve_hash(filename, first_part=False)
                duplicates = total_hash.get(complete_hash)
                if duplicates:
                    duplicate_files.append(filename)
                    duplicate_files.append(duplicates)
                else:
                    total_hash[complete_hash] = filename
            except (OSError,):
                continue

        duplicate_files_dictionary.setdefault(counter, set(duplicate_files))
        counter += 1
        duplicate_files = []

    print("List of duplicate files:")
    for key, value in duplicate_files_dictionary.items():
        print(f"{key}:{value}")


if __name__ == "__main__":
    directory_path = sys_argv[1]
    if directory_path:
        list_duplicates(directory_path)
    else:
        print("Parameter directory_path missing")
