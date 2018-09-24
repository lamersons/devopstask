import os
import sys
from subprocess import Popen, PIPE, STDOUT

def exec_cmd(cmd):
    try: x = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)#, env=os.environ.copy())
    except Exception as e: print(e)
    else:
        print("executing remote cmd: [{}]".format(" ".join(cmd)))
        return x.stdout.read().decode("UTF-8") or x.stderr.read().decode("UTF-8")

def reload_nginx_config(nginx_node_list):
    for n in nginx_node_list:
        task_id = n.split(" ")[0]
        node_id = n.split(" ")[1]
        cont_id = exec_cmd(["docker", "inspect", "-f", "'{{.Status.ContainerStatus.ContainerID}}'", task_id])[1:12]
        r_srt = "nginx -s reload"
        r = exec_cmd(["docker-machine", "ssh", node_id, "docker exec {0} {1}".format(cont_id, r_srt)])
        yield r

def get_container_list(service_name):
    r = exec_cmd(["docker", "service", "ps", service_name, "--format", "'{{.ID}} {{.Node}}'"])
    return [n[1:-1] for n in r.split("\n") if n != ""]

COUNTRIES_SERVICE_NAME = "up_countries"
AIRPORTS_SERVICE_NAME = "up_airports"

COUNTRIES_UPSTREAM_1_PATH = "/home/shared_drive/nginx/conf/conf.d/countries_upstream_1"
COUNTRIES_UPSTREAM_2_PATH = "/home/shared_drive/nginx/conf/conf.d/countries_upstream_2"
AIRPORTS_UPSTREAM_1_PATH = "/home/shared_drive/nginx/conf/conf.d/airports_upstream_1"
AIRPORTS_UPSTREAM_2_PATH = "/home/shared_drive/nginx/conf/conf.d/airports_upstream_2"
# COUNTRIES_UPSTREAM_1_PATH = "/opt/nginx/conf/conf.d/countries_upstream_1"
# COUNTRIES_UPSTREAM_2_PATH = "/opt/nginx/conf/conf.d/countries_upstream_2"
# AIRPORTS_UPSTREAM_1_PATH = "/opt/nginx/conf/conf.d/airports_upstream_1"
# AIRPORTS_UPSTREAM_2_PATH = "/opt/nginx/conf/conf.d/airports_upstream_2"

BUILD_ROOT = os.path.dirname(os.path.realpath(__file__))
KEYS_ROOT = os.path.dirname(os.path.realpath(__file__)) + "/keys"
SWARM_INIT_NODE = "node-1"
# SWARM_MASTER_STATUS = exec_cmd(["docker-machine", "status", SWARM_INIT_NODE])
SWARM_MASTER_IP = exec_cmd(["docker-machine", "inspect", SWARM_INIT_NODE, "--format", "'{{.Driver.IPAddress}}'"])[1:-2]

os.environ["DOCKER_API_VERSION"] = "1.29"
os.environ["DOCKER_TLS_VERIFY"] = "1"
os.environ["DOCKER_HOST"] = "tcp://{0}:2376".format(SWARM_MASTER_IP)
os.environ["DOCKER_CERT_PATH"] = KEYS_ROOT
os.environ["DOCKER_MACHINE_NAME"] = SWARM_INIT_NODE


NGINX_CONTAINER_LIST = get_container_list("up_nginx")
r = [r for r in list(reload_nginx_config(NGINX_CONTAINER_LIST)) if not "signal process started" in r]
if r != "":
    for line in r: print(line)

NGINX_CONTAINER_LIST = get_container_list("up_countries")

# for l in list(r):
#     if not "signal process started" in l
# print(list(r))

# for n in NGINX_CONTAINER_LIST:
# print(NGINX_CONTAINER_LIST)

# for i in NGINX_CONTAINER_LIST.split("\n"): print(NGINX_CONTAINER_LIST)