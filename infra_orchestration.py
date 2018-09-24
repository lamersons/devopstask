import os
from subprocess import Popen, PIPE, STDOUT

MANAGER_COUNT = 2
WORKER_COUNT = 3
NODE_LIST = []

def exec_cmd(cmd):
    try: x = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=os.environ.copy())
    except Exception as e: print(e)
    else:
        print("executing remote cmd: [{}]".format(" ".join(cmd)))
        return x.stdout.read().decode("UTF-8") or x.stderr.read().decode("UTF-8")

def create_nodes(amount):
    for i in range(1, amount+1, 1):
        name = "node-" + str(i)
        c = ["docker-machine", "create", "--driver", "virtualbox", name]
        print(exec_cmd(c))
        NODE_LIST.append(name)

def init_swarm():
    manager_ip = exec_cmd(["docker-machine", "ip", NODE_LIST[0]])
    c = ["docker-machine", "ssh", "node-1", "docker swarm init --advertise-addr " + manager_ip]
    print(exec_cmd(c))

def add_swarm_manager(manager):
    join_string = exec_cmd(["docker", "swarm", "join-token", "manager"])
    c = ["docker-machine", "ssh", manager, join_string]
    exec_cmd(c)

def add_swarm_worker(worker):
    join_string = exec_cmd(["docker", "swarm", "join-token", "worker"])
    c = ["docker-machine", "ssh", worker, join_string]
    exec_cmd(c)

def set_swarm_env():
    env = exec_cmd(["docker-machine", "env", NODE_LIST[0]]).replace("export ", "").split("\n")[0:4]
    for l in env: os.environ[l.split("=")[0]] = l.split("=")[1].replace("\"","")

def install_jenkins():
    c = ["docker", "stack", "deploy", "-c deploy_jenkins.yml", "up"]
    print(exec_cmd(c))

if __name__ == "__main__":
    create_nodes(MANAGER_COUNT + WORKER_COUNT)
    set_swarm_env()
    if not "Swarm: active" in exec_cmd(["docker", "info"]): init_swarm()
    for manager in NODE_LIST[1:MANAGER_COUNT]: add_swarm_manager(manager)
    for worker in NODE_LIST[MANAGER_COUNT:]: add_swarm_worker(worker)
    install_jenkins()