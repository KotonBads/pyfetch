#!/usr/bin/env python3
import os
import sys

### COLORS ###
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"

### COLOR BLOCKS ###
def color_blocks():

    # Thin
    c1 = "\033[7;30m  \033[0;1;30m"
    c2 = "\033[7;31m  \033[0;1;31m"
    c3 = "\033[7;32m  \033[0;1;32m"
    c4 = "\033[7;33m  \033[0;1;33m"
    c5 = "\033[7;34m  \033[0;1;34m"
    c6 = "\033[7;35m  \033[0;1;35m"
    c7 = "\033[7;36m  \033[0;1;36m"
    c8 = "\033[7;37m  \033[0;1;37m"

    # Thick
    _c1 = "\033[7;30m    \033[0;1;30m"
    _c2 = "\033[7;31m    \033[0;1;31m"
    _c3 = "\033[7;32m    \033[0;1;32m"
    _c4 = "\033[7;33m    \033[0;1;33m"
    _c5 = "\033[7;34m    \033[0;1;34m"
    _c6 = "\033[7;35m    \033[0;1;35m"
    _c7 = "\033[7;36m    \033[0;1;36m"
    _c8 = "\033[7;37m    \033[0;1;37m"

    return {
        "thin": f"{c1}{c2}{c3}{c4}{c5}{c6}{c7}{c8}",
        "thick": f"{_c1}{_c2}{_c3}{_c4}{_c5}{_c6}{_c7}{_c8}\n{_c1}{_c2}{_c3}{_c4}{_c5}{_c6}{_c7}{_c8}",
    }


### DISTRO ###
def distro():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if "PRETTY_NAME" in line:
                    return (
                        line.split("=")[1].translate(str.maketrans("", "", '"'))
                    ).strip()

    except FileNotFoundError:
        return "Unknown"


### MEMORY ###
def mem():
    # Formula: usedmem = MemTotal + Shmem - MemFree - Buffers - Cached - SReclaimable
    # Source: https://github.com/KittyKatt/screenFetch/issues/386#issuecomment-249312716
    try:
        with open("/proc/meminfo") as f:
            current_mem = f.read().strip().split("\n")

        mem_total = int([i for i in current_mem if "MemTotal" in i][0].split()[1])
        mem_shared = int([i for i in current_mem if "Shmem" in i][0].split()[1])
        mem_free = int([i for i in current_mem if "MemFree" in i][0].split()[1])
        mem_buffers = int([i for i in current_mem if "Buffers" in i][0].split()[1])
        mem_cached = int([i for i in current_mem if "Cached" in i][0].split()[1])
        mem_sreclaimable = int(
            [i for i in current_mem if "SReclaimable" in i][0].split()[1]
        )

        return {
            "used_mem": mem_total
            + mem_shared
            - mem_free
            - mem_buffers
            - mem_cached
            - mem_sreclaimable,
            "total_mem": mem_total,
        }

    except FileNotFoundError:
        return {"used_mem": 0, "total_mem": 0}


### CPU ###
def cpu():
    try:
        with open("/proc/cpuinfo") as f:
            current_cpu = f.read().strip().split("\n")

            cpu_model = (
                [i for i in current_cpu if "model name" in i][0].split(":")[1].strip()
            )
            # cpu_cores = [i for i in current_cpu if 'cpu cores' in i][0].split(':')[1].strip()
            # cpu_siblings = [i for i in current_cpu if 'siblings' in i][0].split(':')[1].strip()
            # flags = [i for i in current_cpu if 'flags' in i][0].split(':')[1].strip().split(' ')

            return {
                "model": cpu_model,
                # 'cores': cpu_cores,
                # 'threads': cpu_siblings,
                # 'flags': flags
            }
    except FileNotFoundError:
        return {
            "model": "Unknown",
            # 'cores': 0,
            # 'threads': 0,
            # 'flags': []
        }


### KERNEL ###
def kernel():
    try:
        with open("/proc/version") as f:
            return f.read().split()[2]
    except FileNotFoundError:
        return "Unknown"


### WEATHER ###
# def weather():
#     return os.popen('curl -s wttr.in/?format="%c%C%20%t"').read()

### POWER CONSUMPTION ###
# def power():
# only works on battery power
# try:
#     with open('/sys/class/power_supply/BAT0/power_now') as f:
#         return int(f.read().strip()) / 1000000
# except:
#     return 'N/A'

### SHELL ###
try:
    shell = os.environ["SHELL"]
except KeyError:
    shell = "Unknown"

### WM/DE ###
try:
    wm = os.environ["XDG_CURRENT_DESKTOP"]
except KeyError:
    wm = "Unknown"

### HOSTNAME AND USER ###
try:
    with open("/etc/hostname") as f:
        hostname = f.read().strip()
    user = os.environ["USER"]
except (FileNotFoundError, KeyError):
    hostname = "Unknown"
    user = "Unknown"
### VARS FOR MEM ###
x = mem()
total_mem = round(x["total_mem"] / 1024)
used_mem = round(x["used_mem"] / 1024)
free_mem = total_mem - used_mem

### VARS FOR CPU ###
y = cpu()
cpu_model = y["model"]
# cpu_cores = y['cores']
# cpu_threads = y['threads']
# cpu_flags = y['flags']

### VARS FOR COLOR BLOCKS ###
try:
    if sys.argv[1] == "--thin" or sys.argv[1] != "--thick":
        col_blocks = color_blocks()["thin"]
    else:
        col_blocks = color_blocks()["thick"]
except IndexError:
    col_blocks = color_blocks()["thin"]

### OUTPUT STRING ###
fetch = f"""
               {blue}{user}@{hostname}{reset}
{black}     .--.      {reset}======================{reset}
{black}    |{white}o{yellow}_{white}o{black} |     {yellow}???  {distro()}{reset}
{black}    |{yellow}:_/{black} |     {red}???  {cpu_model}{reset}
{black}   /{white}/   \\{black} \\    {purple}???  {wm}{reset}
{black}  ({white}|     |{black} )   {blue}???  {kernel()}{reset}
{yellow} /'{white}\\_   _/{yellow}`\\   {cyan}???  {shell}{reset}
{yellow} \\___){black}={yellow}(___/   {green}??? {used_mem}MB / {total_mem}MB{reset}

{col_blocks}
"""

print(fetch)
