import os
import sys
from subprocess import Popen, PIPE, STDOUT

MANAGER_COUNT = 2
WORKER_COUNT = 3
NODE_LIST = []
APP_ROOT = os.path.dirname(os.path.realpath(__file__))


def exec_cmd(cmd):
    try: x = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=os.environ.copy())
    except Exception as e: print(e)
    else:
        print("executing remote cmd: [{}]".format(" ".join(cmd)))
        return x.stdout.read().decode("UTF-8") or x.stderr.read().decode("UTF-8")

def create_nodes(amount):
    for i in range(1, amount+1, 1):
        name = "node-" + str(i)
        print(exec_cmd(["docker-machine", "create", "--driver", "virtualbox", name]))
        NODE_LIST.append(name)

def init_swarm():
    manager_ip = exec_cmd(["docker-machine", "ip", NODE_LIST[0]])
    print(exec_cmd(["docker-machine", "ssh", "node-1", "docker swarm init --advertise-addr " + manager_ip]))

def add_swarm_manager(manager):
    join_string = exec_cmd(["docker", "swarm", "join-token", "manager"])
    exec_cmd(["docker-machine", "ssh", manager, join_string])

def add_swarm_worker(worker):
    join_string = exec_cmd(["docker", "swarm", "join-token", "worker"])
    exec_cmd(["docker-machine", "ssh", worker, join_string])

def set_swarm_env():
    env = exec_cmd(["docker-machine", "env", NODE_LIST[0]]).replace("export ", "").split("\n")[0:4]
    for l in env: os.environ[l.split("=")[0]] = l.split("=")[1].replace("\"","")

def install_jenkins():
    print(exec_cmd(["docker", "stack", "deploy", "-c", APP_ROOT + "/deploy_jenkins.yml", "up"]))

def create_docker_networks():
    def check_if_network_exists(network_name):
        exec_cmd(["docker", "network", "ls", "-f", "Name=" + network_name])
    if check_if_network_exists("countries"):
        exec_cmd(["docker", "network", "create", "--subnet"", 10.11.0.0/16", "--drive", "overlay", "--attachable", "--internal", "countries"])
    elif check_if_network_exists("airports"):
    exec_cmd(["docker", "network", "create", -"-subne"t "10.12.0.0/16", "--driver", "overlay", "--attachable", "--internal", "airports"])

if __name__ == "__main__":
    create_nodes(MANAGER_COUNT + WORKER_COUNT)
    set_swarm_env()
    if not "Swarm: active" in exec_cmd(["docker", "info"]): init_swarm()
    for manager in NODE_LIST[1:MANAGER_COUNT]: add_swarm_manager(manager)
    for worker in NODE_LIST[MANAGER_COUNT:]: add_swarm_worker(worker)
    install_jenkins()