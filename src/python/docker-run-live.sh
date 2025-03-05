#! /bin/sh
set -e
set -x
IMAGE=registry.risc-software.at/risc_ds/risc_dse/mcp/test
test -n "$(docker images -q $IMAGE 2> /dev/null)" || docker build -f Dockerfile-test -t $IMAGE .
docker run -it --rm --name mcp-test $({ find -mindepth 1 -maxdepth 1  \! -name mcp_use_case_UPO \! -name mcp_use_case_dot_net -printf '%P\n'; find mcp_use_case_UPO -mindepth 1 -maxdepth 1  ; find mcp_use_case_dot_net -mindepth 1 -maxdepth 1 ; } | sed 's,^.*$,-v '"$(pwd)"'/\0:/repo/\0,') $IMAGE
