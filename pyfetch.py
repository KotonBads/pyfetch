#!/usr/bin/env python3
import os

### COLORS ###
black = "\033[30m"
red = '\033[31m'
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"

### DISTRO ###
def distro():
    with open('/etc/os-release') as f:
        for line in f:
            if 'PRETTY_NAME' in line:
                return line.split('=')[1].translate(str.maketrans('', '', '"'))

### MEMORY ###
def mem():
    # Formula: usedmem = MemTotal + Shmem - MemFree - Buffers - Cached - SReclaimable
    # Source: https://github.com/KittyKatt/screenFetch/issues/386#issuecomment-249312716

    # current_mem = os.popen('cat /proc/meminfo | grep -E "MemTotal|Shmem|MemFree|Buffers|Cached|SReclaimable"').read().strip().split('\n')
    
    with open('/proc/meminfo') as f:
        current_mem = f.read().strip().split('\n')

        mem_total = int([i for i in current_mem if 'MemTotal' in i][0].split()[1])
        mem_shared = int([i for i in current_mem if 'Shmem' in i][0].split()[1])
        mem_free = int([i for i in current_mem if 'MemFree' in i][0].split()[1])
        mem_buffers = int([i for i in current_mem if 'Buffers' in i][0].split()[1])
        mem_cached = int([i for i in current_mem if 'Cached' in i][0].split()[1])
        mem_sreclaimable = int([i for i in current_mem if 'SReclaimable' in i][0].split()[1])

        mem_stats = {
            'total': mem_total,
            'free': mem_free,
            'buffers': mem_buffers,
            'cached': mem_cached,
            'sreclaimable': mem_sreclaimable,
            'shared': mem_shared
        }
        return {'used_mem': mem_stats['total'] + 
            mem_stats['shared'] - mem_stats['free'] - 
            mem_stats['buffers'] - mem_stats['cached'] - 
            mem_stats['sreclaimable'], 
            'total_mem': mem_stats['total']
            }

### CPU ###
def cpu():
    current_cpu = os.popen('lscpu').read().strip().split('\n')
    for line in current_cpu:
        if 'Model name' in line:
            return line.split(':')[1].strip()

### KERNEL ###
kernel = os.popen('uname -r').read().strip()

### SHELL ###
shell = os.popen('echo $SHELL').read().strip()

### VARS FOR MEM ###
x = mem()
total_mem = round(x['total_mem'] / 1024)
used_mem = round(x['used_mem'] / 1024)
free_mem = total_mem - used_mem

### OUTPUT STRING ###
fetch = f"""
{yellow}  {distro().strip()}
{red}  {cpu()}
{green}塞 {used_mem}MB / {total_mem}MB
{blue}  {kernel}
{cyan}  {shell}
"""

print(fetch)