# DotNet Use Case

## Description

It reads some *vdl* data and then uses the *Legacy Python.DoyNet Loader* (clr) to load the ITS_West.Base.dll and call the function 
*GetHashedDataInInt* to generate an anonymized internal sensor id.

## Requirements

The input file [vdl_urf_8.csv](vdl_urf_8.csv) and the corresponding dll file [ITS_West.Base.dll](ITS_West.Base.dll) must be present.

## How to Start

Assuming you are in the directory *mcp_frm*:

```
./pipeline_runtime.py ../mcp_use_case_dot_net/csharp_use_case1.yaml
```
