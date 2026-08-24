#!/data/data/com.termux/files/usr/bin/python3

import os
import sys
import tempfile

home = "/data/data/com.termux/files/usr/share/fynqeltools/home/file"

r = '\033[91m'
y = '\033[93m'
g = '\033[92m'
x = '\033[0m'

def pct(total, cur):
    if total == 0:
        p = 100
    else:
        p = int((cur / total) * 100)
    sys.stdout.write(f'\r%{p}')
    sys.stdout.flush()

def free_space(path):
    s = os.statvfs(path)
    return s.f_bavail * s.f_frsize

def copy_file(src, dst):
    try:
        sz = os.path.getsize(src)
    except OSError:
        print(f"{r}Error: Invalid{x}")
        return False

    dst_dir = os.path.dirname(dst)

    if not os.path.isdir(dst_dir):
        print(f"{r}Invalid file copy path{x}")
        return False

    if not os.access(dst_dir, os.W_OK):
        print(f"{r}Access denied{x}")
        return False

    if free_space(dst_dir) < sz:
        print(f"{r}Operation cancelled Your memory is full{x}")
        return False

    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=dst_dir)
        os.close(fd)

        # Copy file in chunks
        with open(src, 'rb') as f1, open(tmp, 'wb') as f2:
            done = 0
            while True:
                chunk = f1.read(1048576)
                if not chunk:
                    break
                f2.write(chunk)
                done += len(chunk)
                pct(sz, done)

        os.replace(tmp, dst)
        print()
        print(f"{g}Operation completed successfully{x}")
        return True

    except PermissionError:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
        print()
        print(f"{r}Access denied{x}")
        return False

    except OSError:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)
        print()
        print(f"{r}Error: Invalid{x}")
        return False

def add_file(path):
    if os.path.isfile(path):
        name = os.path.basename(path)
        dst = os.path.join(home, name)

        if os.path.exists(dst):
            print(f"{y}This file has already been saved{x}")
            return

        copy_file(path, dst)
    elif os.path.isdir(path):
        print(f"{y}Invalid file{x}")
    else:
        print(f"{y}Error: No file exists{x}")

def list_files():
    try:
        files = os.listdir(home)
    except OSError:
        print(f"{r}Error: Invalid{x}")
        return

    real_files = [f for f in files if os.path.isfile(os.path.join(home, f))]

    if not real_files:
        print(f"{y}No file exists{x}")
        return

    for f in sorted(real_files):
        p = os.path.join(home, f)
        print(f"{f} ({os.path.getsize(p)} bytes)")

def search_file(name):
    try:
        files = os.listdir(home)
    except OSError:
        print(f"{r}Error: Invalid{x}")
        return

    for f in files:
        if f == name and os.path.isfile(os.path.join(home, f)):
            p = os.path.join(home, f)
            print(f"{f} ({os.path.getsize(p)} bytes)")
            return

    print(f"{y}File does not exist{x}")

def delete_all():
    try:
        files = os.listdir(home)
    except OSError:
        print(f"{r}Error: Invalid{x}")
        return

    real_files = [f for f in files if os.path.isfile(os.path.join(home, f))]

    if not real_files:
        print(f"{y}No file exists{x}")
        return

    print(f"{r}Are you sure? (y/n){x}")
    if input().strip().lower() != 'y':
        print(f"{y}Operation cancelled{x}")
        return

    total = len(real_files)
    i = 0
    for f in real_files:
        p = os.path.join(home, f)
        try:
            os.remove(p)
        except OSError:
            print(f"{r}Error: Invalid{x}")
            return
        i += 1
        pct(total, i)

    print()
    print(f"{g}All files deleted successfully{x}")

def delete_file(name):
    p = os.path.join(home, name)

    if os.path.isfile(p):
        print(f"{r}Are you sure? (y/n){x}")
        if input().strip().lower() != 'y':
            print(f"{y}Operation cancelled{x}")
            return

        try:
            os.remove(p)
        except OSError:
            print(f"{r}Error: Invalid{x}")
            return

        print(f"{g}File deleted successfully{x}")
    elif os.path.isdir(p):
        print(f"{y}Invalid file{x}")
    else:
        print(f"{y}No file exists{x}")

def export_file(name):
    p = os.path.join(home, name)

    if os.path.isfile(p):
        print("Where to copy (n):")
        dest = input().strip()

        if dest.lower() == 'n':
            print(f"{y}Operation cancelled{x}")
            return

        if not os.path.isdir(dest):
            print(f"{r}Invalid file copy path{x}")
            return

        dst = os.path.join(dest, name)

        if os.path.exists(dst):
            print(f"{y}This file has already been saved{x}")
            return

        copy_file(p, dst)
    elif os.path.isdir(p):
        print(f"{y}Invalid file{x}")
    else:
        print(f"{y}No file exists{x}")

def print_usage():
    print("fynq [path]           Copy file to fynqeltools")
    print("fynq list             List saved files")
    print("fynq search [name]    Search for a file")
    print("fynq delete all       Delete all files")
    print("fynq delete [name]    Delete a specific file")
    print("fynq file [name]      Export file to another path")

def main():
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    cmd = args[0]

    if cmd == "list":
        list_files()
    elif cmd == "search":
        if len(args) < 2:
            print("fynq search [name]    Search for a file")
        else:
            search_file(args[1])
    elif cmd == "delete":
        if len(args) < 2:
            print("fynq delete all       Delete all files")
            print("fynq delete [name]    Delete a specific file")
        elif args[1] == "all":
            delete_all()
        else:
            delete_file(args[1])
    elif cmd == "file":
        if len(args) < 2:
            print("fynq file [name]      Export file to another path")
        else:
            export_file(args[1])
    else:
        add_file(cmd)

if __name__ == "__main__":
    main()