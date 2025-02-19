# ruff: noqa: E741

import pytest


def test_duckdb(run_pipeline) -> None:
    run_pipeline("mcp_use_case_testing_duckdb/testing_duckdb_use_case.yaml")
