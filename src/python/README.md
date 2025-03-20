
# Introduction into the Minimalist Configurable (Code) Pipeline  *(mcp)* Framework

---

The main purpose of the mcp framework is to minimize the effort to re-implement the similar issues over and over again for various use cases. To achieve this, it provides the following:
 - A framework which is able to execute specified python functions in a pipeline/workflow defined in a yaml configuration file. 
	- The composed code pipeline can be decomposed to child-pipelines, 
which may in turn include further child-pipelines or python functions.
 	- A child-pipeline may be executed repetitively in loops.
   - For given python functions maybe some sort of additional function arguments can be specified in the yaml configuration.
   - A (child-)pipeline can be refactored in another yaml file and adapted to another use case.
 - Some general logic is already implemented in order to facilitate the usage of the mcp framework.
 - Some coding templates and best practices are presented as well in order to support the user to be able entirely use the capability of this tiny tool.

This directory contains the following:
- the source of mcp framework, see the directory [**mcp_frm**](mcp_frm/README.md);
- some coding guidelines/templates, see the directory as well as 
a tiny collection of some generally (re-)usable functions (read/write csv/parquet etc.),
see the directory [**mcp_general_functions**](mcp_general_functions/README.md);
- a very simple pipeline configuration for getting started, see the directory [**mcp_use_case_getting_started**](mcp_use_case_getting_started/README.md);
- re-implemented fronius use case (re-sampling csv/parquet data and write into parquet), see the directory [**mcp_use_case_fronius**](mcp_use_case_fronius/README.md);
- re-implemented UPO use case, see the directory [**mcp_use_case_UPO**](mcp_use_case_UPO/README.md);
- re-implemented sim2influx use case (writing csv data into influx/timescale db), see the directory [**mcp_use_case_sim2infux**](mcp_use_case_sim2influx/README.md);
- the source of the santub use case (converting data on excel worksheet to parquet), see the directory [**mcp_santub**](mcp_santub/README.md); and
- the source tiny dotnet use case to demonstrate how to wrapped and re-use c# code (e.g.: from the EVIS project), see the directory [**mcp_use_case_dot_net**](mcp_use_case_dot_net/README.md)

## Synopsis

>      mcp_frm/pipeline_runtime.py  
>         [adapted_use_case_configuration.yaml] basic_use_case_configuration.yaml

### Examples

Assuming you are in the directory `mcp/src/python`:

```sh
mcp_frm/pipeline_runtime.py mcp_use_case_fronius/fronius_use_case1.yaml
```
or
```sh
mcp_frm/pipeline_runtime.py \
	mcp_use_case_fronius/fronius_use_case2.yaml \
	mcp_use_case_fronius/fronius_use_case1.yaml
```

## Getting Started

To Execute your first pipeline issue the following statement from the directory `mcp/src/python`, which will print the content of the parent directory 
and of its sub-directories of the parent directory to the standard output:

```sh
mcp_frm/pipeline_runtime.py mcp_use_case_getting_started/first_use_case.yaml
```

For particular yaml configuration examples, see the use cases. For coding guidelines and best practices, see [mcp_general_functions/README.md](mcp_general_functions/README.md)

## Running with poetry

To run it with poetry:
```sh
cd .../risc_dse/mcp/src/python/
poetry env use "path_with_python_interpreter_binary"
poetry shell
poetry install
python3.10 mcp_frm/pipeline_runtime.py mcp_use_case_getting_started/first_use_case.yaml
exit
```

## Building example files container

In order to have reproducable tests all binary test data is contained in a dedicated docker image

```
registry.risc-software.at/risc_ds/risc_dse/mcp/examples:0.1
```

To rebuild this image from scratch the following steps have to be performed.

> **_NOTE:_** Building the image has to be done only once or whenever test data changes. Consider incremental updates, i.e. base off on a lower version of the `examples` image if you only have to add new data.

> **_NOTE:_** If marked with `(wsl2)`, the step is to be performed in a WLS2 environment. If marked with `(local)`, the step is to be performed under Windows in a GitBash console.

### Prepare Docker build environment

1. Install Docker desktop on the Windows host or Docker CE within WSL2. You need a working docker installation in WSL2.
2. Create working directory hierarchy
```sh
# (wsl2)
mkdir -p /tmp/mcp-testabb/data_{sim,santub/excel_files/{tunnels,bridges}}
```

### Copy test data files from authoritative locations

All data will be collected from their related network shares if available.

```sh
# (local)
# Santub
cp -av '\\risc.local\projects\LI\neuron_santub\Content\Data'/InspB_{Ebel*2024.07.23_neu,J6*2024.07.23_new,*hlbacherbr*_2024.07.23_neu}.xlsx -t '\\wsl.localhost\Ubuntu-20.04'/tmp/mcp-testabb/data_santub/excel_files/bridges
cp -av '\\risc.local\projects\LI\neuron_santub\Content\Data'/InspB_Neumarkttunnel*2024.06.27.xlsx -t '\\wsl.localhost\Ubuntu-20.04'/tmp/mcp-testabb/data_santub/excel_files/tunnels

# Fresgo Sim
(cd '\\publicnas\publicnas\LI\ffg_opt1mus/sim/fresgo' && cp -av data_1ce37cb2-ddf9-4ebe-8085-aea4704ee291 data_26cca20d-f2cf-43b1-8652-bf5b1152daaa data_3c558e73-e65e-468f-a383-dd79be249864 data_5b8e82f9-44b3-4b53-ab3e-bae56cdf8cb2 -t '\\wsl.localhost\Ubuntu-20.04'/tmp/mcp-testabb/data_sim )
```

If data is not available in authoritative locations, it must be put under the artificial authoritative location `\\publicnas\publicnas\LI\risc_dataengineering\mcp\test`.

The hierarchy under test already matches the final directory layout in the `examples` image, i.e.

```
├── data_fronius
│   └── input_files
├── data_fronius2
│   └── input_files
├── data_santub
│   └── coordinates.csv
└── repo
    ├── mcp_use_case_UPO
    │   └── data
    └── mcp_use_case_dot_net
        ├── ITS_West.Base.dll
        ├── ITS_West.Base.pdb
        └── vdl_urf_8.csv
```

The directory `repo` in the docker image is the equivalent of the locally checked out directory `mcp/src/python`. Later build stages will populate the `repo` directory with the related repository artefacts.

```sh
# (local) Copy all data not stored elsewhere from the artificial authoritative location
(cd '\\publicnas\publicnas\LI\risc_dataengineering'/mcp/test && cp -a * -t '\\wsl.localhost\Ubuntu-20.04'/tmp/mcp-testabb)
```

### Create build instructions and build image

```sh
# (wsl2) Pack data into docker image
cd /tmp/mcp-testabb
 cat <<"EOF" > .dockerignore
*
!data_*
!repo
EOF
cat <<"EOF" > Dockerfile
FROM debian:stable-slim

COPY . /
EOF

# Define version number. Bump minor version if data added/changed.
EXAMPLES_VERSION=0.1

# Build examples image.
docker build -t registry.risc-software.at/risc_ds/risc_dse/mcp/examples:$EXAMPLES_VERSION .
```

Optionally you can run the locally built image to check it.

```sh
# (wsl2)
docker run -it --rm --name matlab-bsp registry.risc-software.at/risc_ds/risc_dse/mcp/examples:$EXAMPLES_VERSION
```

Push image to registry
```sh
# (wsl2) Optionally logon to registry
docker login registry.risc-software.at
docker push registry.risc-software.at/risc_ds/risc_dse/mcp/examples:$EXAMPLES_VERSION
```

## Using test image for testing and development

### Build test image locally

In order to run `pytest` test cases as well as running the mcp pipeline on test data, we need to build a test docker image first.

> **_NOTE:_** The test image is based on `registry.risc-software.at/risc_ds/risc_dse/mcp/examples:(some_version)`. If you updated the version number, don't forget to update the version number within `Dockerfile-test` before you build.

```sh
# (wsl2)
cd /path/to/checked/out/mcp/src/python
docker build -f Dockerfile-test -t registry.risc-software.at/risc_de/mcp/mcp/test .
```

### Run tests within test image

You can run the `pytest` test cases locally completely isolated within the test container.

```sh
# (wsl2)
docker run -it --rm --name mcp-test registry.risc-software.at/risc_de/mcp/mcp/test pytest
```

To inspect the image (get a bash) use instead:
```sh
# (wsl2)
docker run -it --rm --name mcp-test registry.risc-software.at/risc_de/mcp/mcp/test
```

### Develop within test image

You can mount your source directory into the test container and run `pytest` or invoke the pipeline script from within the container while using your latest code and configuration changes.

> **_NOTE:_** We bind mount each directory individually into the container's `/repo` base directory. Otherwise, the test files from the `examples` image would be shadowed by the bind mount.

```sh
cd /path/to/checked/out/mcp/src/python
docker run -it --rm --name mcp-test $({ find -mindepth 1 -maxdepth 1  \! -name mcp_use_case_UPO \! -name mcp_use_case_dot_net -printf '%P\n'; find mcp_use_case_UPO -mindepth 1 -maxdepth 1  ; find mcp_use_case_dot_net -mindepth 1 -maxdepth 1 ; } | sed 's,^.*$,-v '"$(pwd)"'/\0:/repo/\0,') registry.risc-software.at/risc_de/mcp/mcp/test
```

Alternatively, invoke the script

```sh
./docker-run-live.sh
```

It will build the test image if it doesn't exist yet.

Then run `pytest` from within the docker container or run any python script.


