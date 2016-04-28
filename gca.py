#!/usr/bin/python
# __author__ = 'darklinden'

import os
import subprocess
import sys
import shutil

def run_cmd(cmd):
    print("\trunning cmd: " + " ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print("\t\t" + err)

    if len(out) == 0:
        return ""

    outline = out.split("\n")
    ret = ""
    idx = 0
    while idx < len(outline):
        line = outline[idx]
        line = line.strip()
        line = line.strip("\t")
        ret += "\t\t" + line + "\n"
        idx += 1

    return ret

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def check_git():
    answer = run_cmd(['git', 'status', '-s'])
    return answer

def checkout_and_pull(branch):
    # git branch --track $2 $1/$2\n
    command = 'git status -s'
    answer = subprocess.check_output([command])
    return answer

def list_remote_branches():
    commands = ['git', 'branch', '-a']
    answer = run_cmd(commands)
    tmp_list = answer.split("\n")
    new_list = []
    for line in tmp_list:
        new_key = line.strip()
        if len(new_key) > 0:
            if -1 != new_key.find('remote'):
                if -1 == new_key.find('HEAD'):
                    new_list.append(new_key)

    return new_list

def branch_key(line):
    ls = line.split("/")
    key = ls[-1]
    if len(ls) > 1:
        key += "0"
    else:
        key += "1"
    return key

def __main__():

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("gca.py", "/usr/local/bin")
        return

    check = check_git()
    print(check)
    if len(check):
        print("git repository is not clean")
        print(check)
        return

    remote_branches = list_remote_branches()
    for branch in remote_branches:
        print("working on remote: " + branch + " ...")
        bl = branch.split('/')
        if "local" in bl:
            continue
        bn = bl[-1]
        print(run_cmd(['git', 'clean', '-d', '-f', '-q']))
        print(run_cmd(['git', 'branch', '--track', "" + bn, "" + branch]))
        print(run_cmd(['git', 'checkout', "" + bn]))
        print(run_cmd(['git', 'branch', '--set-upstream-to=' + bl[1] + "/" + bn]))
        print(run_cmd(['git', 'pull']))
        print(run_cmd(['git', 'push', 'local', "" + bn]))

    print("gca Done")

__main__()
