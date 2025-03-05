import os
from typing import Any

import mcp_frm.pipeline_routines as routines


def write_eqe_sol1(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    outdir = routines.get_current_tmp_dir(meta)
    csv_name = os.path.join(outdir, "output_file")
    if "output_filename" in meta:
        csv_name = os.path.join(outdir, meta["output_filename"])
    df = data["df"]
    header_str = ""
    header_count = 1
    header = {
        "Header Size": 25,
        "Header version": "0,2",
        "Technique": "EQE",
        "Data type": "CSV",
        "Sample Name": "Dye cell",
        "Batch [Experiment Identification]": "Dye loading Study",
        "Sample Area [cm2]": "0,5",
        "Composition": "RKSE-5",
        "Light Source": "Xe",
        "Light modulation [Hz]": "NO",
        "Bias Light": "No",
        "Bias Light Intensity [mW/cm2]": 0,
        "Data Vector Size": 101,
        "Data rows size": 1,
        "Parameters size (#)": 1,
        "Parameters descriptor": "Integrated Current density [mA/cm2]",
        "X-Label": "Wavelength [nm]",
        "Y1-Label": "Quantum Efficiency [%]",
        "Y2-label": "Current Density [mA/cm2]",
        "Pixel's number/cells": 1,
        "Company": "UPO",
        "Operator": "Renan Escalante",
        "Aux-1": "Empty",
        "Aux-2": "Empty",
        "Aux-3": "Empty",
    }
    columns = [
        "Measurement number",
        "date",
        "time",
        "Position x",
        "Position y",
        "Position z",
        "Pixel/cell",
        "Integrated Current density [mA/cm2]",
    ]
    values = ["1", "2023-11-27", "09:01:15", "1", "1", "1", "1", "8,9"]
    for key, value in header.items():
        header_str += key + ";" + str(value)
        if header_count == 24:
            header_str += ";;;;;;;Wavelength"
        if header_count == 25:
            header_str += ";;;;;;Calibration [From fotodiode]"
            for index, row in df.iterrows():
                header_str += ";" + str(row["wavelength"])

        header_str += "\n"
        header_count += 1

    columns_str = ";".join(columns)
    values_str = ";".join(values)

    for index, row in df.iterrows():
        columns_str += ";" + str(row["integral_current_density"])
        values_str += ";" + str(row["EQE"])

    writeout = header_str + columns_str + "\n" + values_str

    with open(csv_name + ".csv", "w", newline="\n") as csvfile:
        # Create CSV writer object
        csvfile.write(writeout)
    routines.set_meta_in_data(data, meta)
    return data


def write_eqe_sol2(data: dict[str, Any]) -> dict[str, Any]:
    meta = routines.get_meta_data(data)
    outdir = routines.get_current_tmp_dir(meta)
    csv_name = os.path.join(outdir, "output_file")
    if "output_filename" in meta:
        csv_name = os.path.join(outdir, meta["output_filename"])
    df = data["df"]
    header_str = ""
    header_count = 1
    header = {
        "Header Size": 25,
        "Header version": "0,2",
        "Technique": "EQE",
        "Data type": "CSV",
        "Sample Name": "Dye cell",
        "Batch [Experiment Identification]": "Dye loading Study",
        "Sample Area [cm2]": "0,5",
        "Composition": "RKSE-5",
        "Light Source": "Xe",
        "Light modulation [Hz]": "NO",
        "Bias Light": "No",
        "Bias Light Intensity [mW/cm2]": 0,
        "Data Vector Size": 101,
        "Data rows size": 1,
        "Parameters size (#)": 1,
        "Parameters descriptor": "Integrated Current density [mA/cm2]",
        "X-Label": "Wavelength [nm]",
        "Y1-Label": "Quantum Efficiency [%]",
        "Y2-label": "Current Density [mA/cm2]",
        "Pixel's number/cells": 1,
        "Company": "UPO",
        "Operator": "Renan Escalante",
        "Aux-1": "Empty",
        "Aux-2": "Empty",
        "Aux-3": "Empty",
    }
    columns = [
        "Measurement number",
        "date",
        "time",
        "Position x",
        "Position y",
        "Position z",
        "Pixel/cell",
        "Integrated Current density [mA/cm2]",
    ]
    values = ["1", "2023-11-27", "09:01:15", "1", "1", "1", "1", "8,9"]
    for key, value in header.items():
        header_str += key + ";" + str(value)
        if header_count == 25:
            header_str += ";;;;;;;Wavelength"
        header_str += "\n"
        header_count += 1

    columns_str = ";".join(columns)
    values_str = ";".join(values)

    for index, row in df.iterrows():
        columns_str += ";" + str(row["wavelength"])
        values_str += ";" + str(row["EQE"])

    writeout = header_str + columns_str + "\n" + values_str

    with open(csv_name + ".csv", "w", newline="\n") as csvfile:
        # Create CSV writer object
        csvfile.write(writeout)

    routines.set_meta_in_data(data, meta)
    return data
