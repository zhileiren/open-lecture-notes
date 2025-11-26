#!/usr/bin/python
# coding: utf-8

import subprocess

dot_content = '''digraph G {\nnode[shape=box];\n'''

ret = subprocess.run(['git', 'log'], capture_output=True)

commits = {}
num = 0
for line in ret.stdout.decode('utf-8').splitlines():
    if not line.startswith('commit '):
        continue
    commit = line.replace('commit ', '')
    commits[commit] = num
    dot_content += f'// {commit}\n'
    dot_content += f'{num} [label="{commit}"];\n'
    num += 1

for commit in commits:
    ret = subprocess.run(['git', 'cat-file', '-p', commit], capture_output=True)
    for line in ret.stdout.decode('utf-8').splitlines():
        if not line.startswith('parent '):
            continue
        parent = line.replace('parent ', '')
        dot_content += f'{commits[parent]} -> {commits[commit]};\n'

dot_content += '}'


with open('graph.dot', 'w') as f:
    f.write(dot_content)

