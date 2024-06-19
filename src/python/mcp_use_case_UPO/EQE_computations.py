import pandas as pd
import mcp_frm.pipeline_routines as routines
from typing import Any
from mcp_general_functions import helper
from mcp_use_case_UPO import constants as UPO_constants


def init_calc_eqe_perc(data: dict[str, Any]) -> dict[str, Any]:
    if 'df' not in data:
        data['df'] = pd.DataFrame()
        data['df']["wavelength"] = data['df_dut'][data['df_dut'].columns[0]].astype(float)
        data['loop_wavelength'] = data['df']["wavelength"].copy()
        routines.register_loop_iterator_list(data, 'loop_wavelength')
    data['df']['EQE'] = []
    return data


def init_calc_integral_current_density(data: dict[str, Any]) -> dict[str, Any]:
    if 'df' not in data:
        data['df'] = pd.DataFrame()
        data['df']["wavelength"] = data['df_dut'][df_dut.columns[0]].astype(float)
        data['loop_wavelength'] = data['df']["wavelength"].copy()
        routines.register_loop_iterator_list(data, 'loop_wavelength')
    data['last_values'] = (0, 0, 0)
    data['df']['integral_current_density'] = []
    return data


def calculate_integral_current_density(data: dict[str, Any]) -> dict[str, Any]:
    """
    Calculates the integral of current density over a given wavelength range.

    Args:
        wavelength (int): The wavelength value.
        dut_df (pd.DataFrame): DataFrame containing data related to the device under test.
        photodiode_df (pd.DataFrame): DataFrame containing data related to the photodiode.
        ref_spectral_response_help_table (pd.DataFrame): DataFrame containing reference spectral response values.
        spectral_response_help_table (pd.DataFrame): DataFrame containing spectral response values.
        last_values (tuple[float, float, float]): Tuple containing the last calculated integral current density,
            last wavelength, and last current density.

    Returns:
        tuple[float, float]: A tuple containing the integral current density and
                                current density at the given wavelength.
    """

    def calculate_electron_flux(wavelength_func):
        # Get value of the help table on wavelength
        ref_spectral_response_value = helper.vlookup(
            wavelength_func, ref_spectral_response_help_table, 1, 3
        )

        photon_flux = (
            ((ref_spectral_response_value
            * (wavelength_func * (10**-9)))
            / (conf.Constants.PLANCK * conf.Constants.LIGHT_SPEED))
            / (10**4)
        )

        try:
            electron_flux = (
                (calculate_eqe_perc(
                    wavelength_func, dut_df, photodiode_df, spectral_response_help_table
                )
                / 100)
                * photon_flux
            )
        except ZeroDivisionError:
            return 0
        return electron_flux

    iterator = routines.pop_loop_iterator(data)
    if iterator:
        data['row'] = iterator
    if 'row' in data:
        wavelength = data['row'].iloc[0]
        dut_df = data['df_dut']
        photodiode_df = data['df_fotodiode']
        spectral_response_help_table = data['help_df_hamamatsu']
        ref_spectral_response_help_table = data['help_df_referance']
        last_values = data['last_values']

        electron_flux = calculate_electron_flux(wavelength)
        current_density = (electron_flux * UPO_constants.ELECTRON_CHARGE) * 1000
        current_density_prev = last_values[2]
        current_density_wavelength = ((current_density + current_density_prev) / 2) * (
                wavelength - last_values[1]
        )
        integral_current_density = current_density_wavelength + last_values[0]

        data['df']['integral_current_density'].append(integral_current_density)
        data['last_values'] = (integral_current_density, wavelength, current_density)
    return data


def calculate_eqe_perc(data: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate the external quantum efficiency percentage (EQE%) using provided data.

    Args:
        wavelength (int): The wavelength in nanometers at which EQE% is to be calculated.
        dut_df (pd.DataFrame): DataFrame containing data for the device under test.
        photodiode_df (pd.DataFrame): DataFrame containing data for the photodiode.
        spectral_response_help_table (pd.DataFrame): DataFrame containing spectral response data.

    Returns:
        float: The calculated external quantum efficiency percentage (EQE%).
    """
    iterator = routines.pop_loop_iterator(data)
    if iterator:
        data['row'] = iterator
    try:
        if 'row' in data:
            wavelength = data['row'].iloc[0]
            dut_df = data['df_dut']
            photodiode_df = data['df_fotodiode']
            spectral_response_help_table = data['help_df_hamamatsu']

            # Look up spectral response for the photodiode
            spectral_response_photodiode = (
                    helper.vlookup(float(wavelength), spectral_response_help_table, 1, 2) / 1000
            )

            # Correcting zero spectral response
            if spectral_response_photodiode == 0:
                last_wavelength = wavelength
                while spectral_response_photodiode == 0:
                    last_wavelength -= 1
                    spectral_response_photodiode = helper.vlookup(
                        float(last_wavelength), spectral_response_help_table, 1, 2
                    )

            # Look up current DUT value
            current_dut_value = helper.vlookup(float(wavelength), dut_df, 1, 2)

            # Look up current photodiode value
            current_photodiode_value = helper.vlookup(float(wavelength), photodiode_df, 1, 2)

            # Calculate current photodiode value
            current_photodiode = current_photodiode_value  # / (10**9)

            # Calculate power
            power = current_photodiode / spectral_response_photodiode

            # Calculate DUT spectral
            dut_spectral = current_dut_value  # / (10**9)

            # Calculate spectral response
            spectral_response = dut_spectral / power

            # Calculate EQE percentage
            eqe_perc = (
                    (
                            UPO_constants.PLANCK
                            * UPO_constants.LIGHT_SPEED
                            / (UPO_constants.ELECTRON_CHARGE * (wavelength * (10 ** -9)))
                    )
                    * spectral_response
                    * 100
            )

            data['df']['EQE'].append(eqe_perc)
    except ZeroDivisionError:
        pass
    if 'row' in data:

    return data


def feedback_on_std_out(data: dict[str, Any]) -> dict[str, Any]:
    if 'row' in data:
        if 'row_nr' not in data:
            data['row_nr'] = 0
        row = data['row']
        print(f"{data['row_nr']}/{len(df) - 1} wavelength: {row.iloc[0]}")
        data['row_nr'] += 1
    return data
