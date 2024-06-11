from pathlib import Path

parquet_engine = "pyarrow"


class Paths:
    ## RISC Datastore house
    nas_hemeta_dir = Path("Z:\LI\he_metafacturing")
    nas_hemeta_dir_full = Path(r"\\risc.local\public\publicnas\LI\he_metafacturing")

    ## Main Datastore directory
    data_local = Path(__file__).parents[3] / "data"
    logs = Path(__file__).parents[1] / "logs"
    LTH_profile_data_log = logs / "lth_profile_data.log"


class NemakPaths:
    ## Nemak directory on publicnas
    nas_nemak_dir = Paths.nas_hemeta_dir / "Nemak"

    ## NEMAK local datastore house
    nemak_dir = Paths.data_local / "NEMAK"
    nemak_raw_data_dir = nemak_dir / "raw"
    nemak_raw_sample_data_csv = nemak_raw_data_dir / "example_501_502_mod.csv"
    nemak_processed_data_dir = nemak_dir / "processed"
    nemark_results_dir = nemak_dir / "results"


class FroniusPaths:
    ## Fronius directory on publicnas
    nas_dir = Paths.nas_hemeta_dir / "Fronius"
    nas_raw_sample_data = nas_dir / "sample_data_fronius"
    nas_raw_1kHz_and_10kHz_dir = nas_dir / "sample_data_fronius_1kHz_and_10kHz"
    nas_processed_down_sampled_1kHz_merged_parquet_dir = nas_dir / "down_sampled_1kHz_merged_data"
    nas_processed_upsampled_10k_merged_parquet_dir = nas_dir / "merged_1k_and_10k_parquet_20240405"

    ## FRONIUS local datastore house
    local_dir = Paths.data_local / "FRONIUS"

    local_raw_data_dir = local_dir / "raw"

    local_raw_sample_data = local_raw_data_dir / "sample_data_fronius_zipped"
    local_raw_sample_data_1kHz_and_10kHz_dir = local_raw_data_dir / "sample_data_fronius_1kHz_and_10kHz"
    local_error_codes_csv = local_raw_data_dir / "Errrolist_TPSi_V3_5_2.csv"

    local_processed_data_dir = local_dir / "processed"

    down_sampled_1kHz_merged_data_dir = local_processed_data_dir / "down_sampled_1kHz_merged_data"
    down_sampled_1kHz_merged_parquet_data_dir = down_sampled_1kHz_merged_data_dir / "parquet"
    down_sampled_1kHz_merged_image_png_dir = down_sampled_1kHz_merged_data_dir / "image_png"

    up_sampled_10kHz_merged_data_dir = local_processed_data_dir / "up_sampled_10kHz_merged_data"
    up_sampled_10kHz_merged_parquet_data_dir = up_sampled_10kHz_merged_data_dir / "parquet"
    up_sampled_10kHz_merged_image_png_dir = up_sampled_10kHz_merged_data_dir / "image_png"

    local_results_dir = local_dir / "results"

    signals_1kHz_parquet = "signals_1khz.parquet"
    signals_10kHz_parquet = "signals_10khz.parquet"


class LTHPaths:
    ## LTH directory on publicnas
    nas_dir = Paths.nas_hemeta_dir / "LTH"

    # Data Packages Directories
    nas_data_package_520020377_dir = nas_dir / "Data_package_520020377"
    nas_data_package_520020874_dir = nas_dir / "Data_package_520020874"
    nas_data_package_520021003_dir = nas_dir / "Data_package_520021003"

    ## 520020377 for 2024_02_22
    # Profile data of data package 520020377
    nas_data_package_520020377_profile_data_2024_02_22_dir = (
        nas_data_package_520020377_dir / "2024_02_22-buhler_profiles_by_serial_numbers_520020377"
    )
    # Main data for data_package 520020377 for 2024_02_22
    nas_data_package_520020377_2024_02_22_xlsx = nas_data_package_520020377_dir / "2024_02_22-520020377.xlsx"

    ## 520020377 for 2023_09_05
    # Profile data of data package 520020377 for 2023_09_05
    nas_data_package_520020377_profile_data_2023_09_05_dir = (
        nas_data_package_520020377_dir / "2023_09_05-buhler_profiles_by_serial_numbers_520020377"
    )
    # Main data for data_package 520020377 for 2023_09_05
    nas_data_package_520020377_2023_09_05_xlsx = nas_data_package_520020377_dir / "2023_09_05-520020377.xlsx"

    ## 520020874 for 2024_02_22
    # Profile data of data package 520020874
    nas_data_package_520020874_profile_data_2024_02_22_dir = (
        nas_data_package_520020874_dir / "2024_02_22-buhler_profiles_by_serial_numbers_520020874"
    )
    # Main data for data_package 520020874
    nas_data_package_520020874_2024_02_22_xlsx = nas_data_package_520020874_dir / "2024_02_22-520020874.xlsx"

    ## 520021003 for 2024_02_22
    # Profile data of data package 520021003
    nas_data_package_520021003_profile_data_2024_04_03_dir = (
        nas_data_package_520021003_dir / "2024_04_03-buhler_profiles_by_serial_numbers_520021003"
    )
    # Main data for data_package 520021003
    nas_data_package_520021003_2024_04_03_xlsx = nas_data_package_520021003_dir / "2024_04_03-520021003.xlsx"
    nas_lth_dir = Paths.nas_hemeta_dir / "LTH"
    nas_profile_data_dir = nas_lth_dir / "Buhler_profiles_by_ser_num_520020377_new"
    nas_processed_data_dir = nas_lth_dir / "processed"
    nas_result_data_dir = nas_lth_dir / "result_draft"
    nas_lth_config_dir = nas_lth_dir / "config"

    ## LTH local datastore house
    local_dir = Paths.data_local / "LTH"
    local_raw_data_dir = local_dir / "raw"
    local_processed_data_dir = local_dir / "processed"
    local_results_data_dir = local_dir / "results"

    local_raw_data_package_520020377_dir = local_raw_data_dir / "data_package_520020377"
    local_raw_data_package_520020874_dir = local_raw_data_dir / "data_package_520020874"
    local_raw_data_package_520021003_dir = local_raw_data_dir / "data_package_520021003"

    local_processed_data_package_520020377_dir = local_processed_data_dir / "data_package_520020377"
    local_processed_data_package_520020874_dir = local_processed_data_dir / "data_package_520020874"
    local_processed_data_package_520021003_dir = local_processed_data_dir / "data_package_520021003"

    local_results_data_package_520020377_dir = local_results_data_dir / "data_package_520020377"
    local_results_data_package_520020874_dir = local_results_data_dir / "data_package_520020874"
    local_results_data_package_520021003_dir = local_results_data_dir / "data_package_520021003"

    ## 520020377 for 2024_02_22
    # Profile data of raw data package 520020377
    local_raw_data_package_520020377_profile_data_2024_02_22_dir = (
        local_raw_data_package_520020377_dir / "2024_02_22-buhler_profiles_by_serial_numbers_520020377"
    )
    # Profile data of processed data package 520020377
    local_processed_data_package_520020377_profile_data_2024_02_22_dir = (
        local_processed_data_package_520020377_dir / "2024_02_22-buhler_profiles_by_serial_numbers_520020377"
    )
    # Profile data of processed data package 520020377 features
    local_processed_data_package_520020377_profile_data_2024_02_22_features_parquet = (
        local_processed_data_package_520020377_profile_data_2024_02_22_dir / "profile_features.parquet"
    )
    # Profile data of processed data package 520020377 target
    local_processed_data_package_520020377_profile_data_2024_02_22_target_parquet = (
        local_processed_data_package_520020377_profile_data_2024_02_22_dir / "target.parquet"
    )
    # Main data for data_package 520020377 for 2024_02_22
    local_raw_data_package_520020377_2024_02_22_xlsx = (
        local_raw_data_package_520020377_dir / "2024_02_22-520020377.xlsx"
    )

    ## 520020377 for 2023_09_05
    # Profile data of data package 520020377 for 2023_09_05
    local_raw_data_package_520020377_profile_data_2023_09_05_dir = (
        local_raw_data_package_520020377_dir / "2023_09_05-buhler_profiles_by_serial_numbers_520020377"
    )
    # Main data for data_package 520020377 for 2023_09_05
    local_raw_data_package_520020377_2023_09_05_xlsx = (
        local_raw_data_package_520020377_dir / "2023_09_05-520020377.xlsx"
    )

    ## 520020874 for 2024_02_22
    # Profile data of raw data package 520020874
    local_raw_data_package_520020874_profile_data_2024_02_22_dir = (
        local_raw_data_package_520020874_dir / "2024_02_22-buhler_profiles_by_serial_numbers_520020874"
    )
    # Profile data of processed data package 520020874
    local_processed_data_package_520020874_profile_data_2024_02_22_dir = (
        local_processed_data_package_520020874_dir / "2024_02_22-buhler_profiles_by_serial_numbers_520020874"
    )
    # Profile data of processed data package 520020874 features
    local_processed_data_package_520020874_profile_data_2024_02_22_features_parquet = (
        local_processed_data_package_520020874_profile_data_2024_02_22_dir / "profile_features.parquet"
    )
    # Profile data of processed data package 520020874 target
    local_processed_data_package_520020874_profile_data_2024_02_22_target_parquet = (
        local_processed_data_package_520020874_profile_data_2024_02_22_dir / "target.parquet"
    )

    # Main data for data_package 520020874
    local_raw_data_package_520020874_2024_02_22_xlsx = (
        local_raw_data_package_520020874_dir / "2024_02_22-520020874.xlsx"
    )

    ## 520021003 for 2024_02_22
    # Profile data of raw data package 520021003
    local_raw_data_package_520021003_profile_data_2024_04_03_dir = (
        local_raw_data_package_520021003_dir / "2024_04_03-buhler_profiles_by_serial_numbers_520021003"
    )
    # Profile data of processed data package 520021003
    local_processed_data_package_520021003_profile_data_2024_04_03_dir = (
        local_processed_data_package_520021003_dir / "2024_04_03-buhler_profiles_by_serial_numbers_520021003"
    )
    # Profile data of processed data package 520021003 features
    local_processed_data_package_520021003_profile_data_2024_04_03_features_parquet = (
        local_processed_data_package_520021003_profile_data_2024_04_03_dir / "profile_features.parquet"
    )
    # Profile data of processed data package 520021003 target
    local_processed_data_package_520021003_profile_data_2024_04_03_target_parquet = (
        local_processed_data_package_520021003_profile_data_2024_04_03_dir / "target.parquet"
    )
    # Main data for data_package 520021003
    local_raw_data_package_520021003_2024_04_03_xlsx = (
        local_raw_data_package_520021003_dir / "2024_04_03-520021003.xlsx"
    )

    excel_sheet_name = "Sheet1"

    # LTH conversion paths
    # lth_conversion_input_path = nas_lth_dir
    lth_conversion_input_path = local_raw_data_dir
    # lth_conversion_output_path = nas_result_data_dir
    lth_conversion_output_path = local_results_data_dir


class Paths_FRO:
    project_path = Path(__file__).parent
    data_path = Paths.data_local
    zip_input = data_path / "input"
    zip_output = data_path / "output"
    pq_output = data_path / "FRO"
    tmp_folder = data_path / "tmp"
    paths = [data_path, zip_input, zip_output, pq_output, tmp_folder]
    for folder in paths:
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)


class Paths_BEN:
    project_path = Path(__file__).parent
    data_path = Paths.data_local
    item_paths = [
        "device[1]/serialnumber",
        "device[1]/location/name",
        "device[1]/location/plant",
        "device[1]/location/hall",
    ]
    local_data_input = data_path / "ben_prod"
    local_data_output = data_path / "ben_prod_result"

    nas_dir = Paths.nas_hemeta_dir_full / "BEN_Production/FRO"
    nas_data_input = nas_dir / "Data"
    nas_data_output = nas_dir / "merged_1k_and_10k_parquet"

    data_input = nas_data_input
    data_output = nas_data_output


class Formats:
    date_time_format_in_CSVs = "%Y-%m-%d_%H.%M.%S.%f"


class File_Config:
    execpt_columns = ["Job_number"]
