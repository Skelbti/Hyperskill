import argparse
import os
import sys
import hashlib


class File:
    def __init__(self, path: str,) -> None:
        self.path = path
        self.name = os.path.basename(path)
        self.size = os.path.getsize(path)
        self.ext = path[path.find(".")]
        self.count = None
        self.hash = None

    def __repr__(self) -> str:
        return f"{self.name}"

    def set_hash(self) -> None:
        m = hashlib.md5()
        with open(self.path, "rb") as f:
            m.update(f.read())
            self.hash = m.hexdigest()



def get_path() -> str:
    parser = argparse.ArgumentParser()
    if len(sys.argv) <= 1:
        print("Directory is not specified")
    else:
        parser.add_argument("path")
        args = parser.parse_args()
        return args.path


def fileformat() -> str:
    return input("Enter file format:\n")


def sort_opt() -> str:
    print("\nSize sorting options:\n1. Descending\n2. Ascending\n")
    sort = input("Enter a sorting option:")
    while sort not in "12":
        print("Wrong option\n")
        sort = input("Enter a sorting option:")
    return sort


def get_files(path: str, fileformat: str) -> list:
    all_files = []
    for p, d, f in os.walk(path):
        for file in f:
            if fileformat in file:
                new_file = File(p + "\\" + file)
                all_files.append(new_file)
    return all_files


def files_by_size(all_files: list) -> dict:
    di_size_file = {}
    for f in all_files:
        if f.size not in di_size_file:
            di_size_file[f.size] = [f]
        else:
            di_size_file[f.size].append(f)
    return di_size_file


def keep_duplicate(di: dict) -> dict:
    return {k: v for (k, v) in di.items()if len(v) > 1}


def read_order(di: dict, sort: str) -> list:
    read_order = sorted(di)
    if sort == "1":
        read_order = read_order[::-1]
    return read_order


def print_dup_f_by_size(read_order: list, di_size_file: dict) -> None:
    for size in read_order:
        print(f"\n{size} bytes")
        for file in di_size_file[size]:
            print(file.path)


def give_duplicate() -> bool:
    user = input("Check for duplicates?\n")
    while user not in ["yes", "no"]:
        print("Wrong option")
        user = input("Check for duplicates?\n")
    return user == "yes"


def hash_for_dupl(files: dict) -> None:
    for file_list in files.values():
        for file in file_list:
            file.set_hash()


def files_by_hash(files: dict) -> dict:
    di_hash_files = {}
    for file_list in files.values():
        for file in file_list:
            if file.hash not in di_hash_files:
                di_hash_files[file.hash] = [file]
            else:
                di_hash_files[file.hash].append(file)
    return di_hash_files


def group_hash_by_size(di_hash_files: dict) -> dict:
    dupl_by_size_n_hash = {}
    for hash, files_list in di_hash_files.items():
        if files_list[0].size not in dupl_by_size_n_hash:
            dupl_by_size_n_hash[files_list[0].size] = {hash:files_list}
        else:
            dupl_by_size_n_hash[files_list[0].size][hash] = files_list
    return dupl_by_size_n_hash


def print_hash_by_size(read_order: list, hash_dupl_by_size: dict) -> int:
    count = 0
    for size in read_order:
        print(size, "bytes")
        for hash, files_list in hash_dupl_by_size[size].items():
            print("Hash:", hash)
            for file in files_list:
                count += 1
                file.count = count
                print(f"{file.count}. {file.path}")
    return count

def want_delete() -> bool:
    user = ("Delete files?\n")
    while user not in ["yes", "no"]:
        print("Wrong option")
        user = input("Delete files?\n")
    return user == "yes"

def what_delete(count: int) -> list[int]:
    while True:
        user = input("Enter file numbers to delete:\n")
        try:
            user = [int(i) for i in user.split(" ")]
            if set(user).issubset(set(range(1, count + 1))):
                return user
            else:
                raise ValueError
        except ValueError:
            print("Wrong format")


def deleting(list: list[int], files: dict) -> None:
    del_size = []
    for files_list in files.values():
        for file in files_list:
            if file.count in list:
                del_size.append(file.size)
                os.remove(file.path)
    print(f"Total freed up space: {sum(del_size)} bytes")


if __name__ == "__main__":
    d_path = get_path()
    f_format = fileformat()
    sort = sort_opt()
    all_files = get_files(d_path, f_format)
    di_size_file = files_by_size(all_files)
    di_size_file = keep_duplicate(di_size_file)
    r_order = read_order(di_size_file, sort)
    print_dup_f_by_size(r_order, di_size_file)
    if give_duplicate():
        hash_for_dupl(di_size_file)
        di_hash_files = files_by_hash(di_size_file)
        di_hash_files = keep_duplicate(di_hash_files)
        hash_dupl_by_size = group_hash_by_size(di_hash_files)
        count = print_hash_by_size(r_order, hash_dupl_by_size)
        if want_delete():
            list_to_del = what_delete(count)
            deleting(list_to_del, di_hash_files)
