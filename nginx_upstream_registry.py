# -*- coding: utf-8 -*-
##############################################################################
# deps: docker > 18, API > 1.29, compose > 3.5
# Author: MiZo <misha3@gmail.com>
#
# Lunatech DevOps challange
#
##############################################################################

import os
import sys
from subprocess import Popen, PIPE, STDOUT
import socket

UPSTREAM_FILE_PATH = "/home/shared_drive/nginx/conf/conf.d/"
APPLICATIONS = ["countries", "airports"]

BUILD_ROOT = os.path.dirname(os.path.realpath(__file__))
KEYS_ROOT = os.path.dirname(os.path.realpath(__file__)) + "/keys"

def set_evn_vars():
    os.environ["DOCKER_API_VERSION"] = "1.29"
    os.environ["DOCKER_TLS_VERIFY"] = "1"
    os.environ["DOCKER_HOST"] = "tcp://{0}:2376".format(SWARM_MASTER_IP)
    os.environ["DOCKER_CERT_PATH"] = KEYS_ROOT
    os.environ["DOCKER_MACHINE_NAME"] = SWARM_INIT_NODE

def exec_cmd(cmd):
    try: x = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)#, env=os.environ.copy())
    except Exception as e: print(e)
    else:
        print("executing remote cmd: [{}]".format(" ".join(cmd)))
        return x.stdout.read().decode("UTF-8") or x.stderr.read().decode("UTF-8")

#1 or 2
def switch_upstream(application, int):
    if application in APPLICATIONS:
        proxy_pass_entry = "proxy_pass http://{0}_upstream_{1};".format(application, int)
        with open(UPSTREAM_FILE_PATH + application+"_proxy_pass", "r+") as f:
            for l in f.readlines():
                if proxy_pass_entry != l:
                    print("switching upstream to {0}_upstream_{1}".format(ARGS[1], ARGS[2]))
                    f.seek(0, 0)
                    f.truncate(0)
                    f.write(proxy_pass_entry)
    else: sys.exit("application is not recognized")

def reload_nginx_config(nginx_container_list):
    for n in nginx_container_list:
        task_id = n.split(" ")[0]
        node_id = n.split(" ")[1]
        cont_id = exec_cmd(["docker", "inspect",
                            "-f", "'{{.Status.ContainerStatus.ContainerID}}'", task_id])[1:12]
        r_srt = "nginx -s reload"
        r = exec_cmd(["docker-machine", "ssh", node_id, "docker exec {0} {1}".format(cont_id, r_srt)])
        yield r

def get_container_list(service_name):
    r = exec_cmd(["docker", "service", "ps", service_name,
                  "--format", "'{{.ID}} {{.Node}}'", "-f", "desired-state=Running"])
    r = [n[1:-1] for n in r.split("\n") if "such service" not in n and n != ""]
    return r if r != "" else None

def generate_upstream_config(service_name):
    def validate_ip(ip):
        try: return 1 if socket.inet_aton(ip) else 0
        except socket.error: return 0

    upstream_vip = exec_cmd(["docker", "service", "inspect", service_name,
                            "-f", "{{range .Endpoint.VirtualIPs}}{{.Addr}}{{end}}"]).split("/")[0]

    if validate_ip(upstream_vip):
        upstream_entry = "server {0}:8080;".format(upstream_vip)
        with open(UPSTREAM_FILE_PATH + service_name, "r+") as f:
            for l in f.readlines():
                if upstream_entry != l:
                    f.seek(0, 0)
                    f.truncate(0)
                    f.write(upstream_entry)

if __name__ == "__main__":
    SWARM_INIT_NODE = "node-1"
    SWARM_MASTER_STATUS = exec_cmd(["docker-machine", "status", SWARM_INIT_NODE])
    SWARM_MASTER_IP = exec_cmd(["docker-machine", "inspect", SWARM_INIT_NODE,
    "-f", "'{{.Driver.IPAddress}}'"])[1:-2]

    set_evn_vars()

    NGINX_CONTAINER_LIST = get_container_list("shared_service_nginx")
    CMD_LIST = ["switch_upstream"]
    ARGS = sys.argv[1:]

    if len(ARGS) == 3: # and ARGS[1] == "switch_upstream" and ARGS[1] in CMD_LIST :
        switch_upstream(ARGS[1], ARGS[2])

    generate_upstream_config("c_up1_countries")
    generate_upstream_config("c_up2_countries")
    generate_upstream_config("a_up1_airports")
    generate_upstream_config("a_up2_airports")

    r = [r for r in list(reload_nginx_config(NGINX_CONTAINER_LIST)) if not "process started" in r]
    if r != "":
        for line in r: print(line)





















