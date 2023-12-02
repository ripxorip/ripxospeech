import subprocess
from utils.constants import *

def run_command_over_ssh(command, server):
    print("Running command: {} on {}".format(command, server))
    ssh = subprocess.Popen(["ssh", "{}@{}".format(LINUX_USER, server), command],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    stderr = ssh.stderr.readlines()
    if stderr != []:
        err = "[Error] "
        for line in stderr:
            err += line.decode("utf-8")
        print(err)
    res = ""
    for line in result:
        res += line.decode("utf-8")
    print(res)
    return res

def tmux_run(command, server):
    run_command_over_ssh("tmux send-keys -t {} '{}' C-m".format(TMUX_SESSION_NAME, command), IP_ADDR[server])

def tmux_abort_command(server):
    run_command_over_ssh("tmux send-keys -t {} C-c".format(TMUX_SESSION_NAME), IP_ADDR[server])

def verify_tmux_session(server):
    print("Verifying tmux session for {}".format(server))
    sessions = run_command_over_ssh("tmux ls", IP_ADDR[server])
    # check if the session exists in the sessions
    if TMUX_SESSION_NAME in sessions:
        print("Session already exists")
    else:
        print("Spawning a new tmux session")
        run_command_over_ssh("tmux new -d -s {}".format(TMUX_SESSION_NAME), IP_ADDR[server])

def tmux_kill():
    for c in CLIENTS:
        if IP_ADDR[c] != "":
            verify_tmux_session(c)
            tmux_abort_command(c)