# ruff: noqa: E741

import pytest


def test_fronius_use_case1(run_pipeline) -> None:
    run_pipeline("mcp_use_case_fronius/fronius_use_case1.yaml")


def test_fronius_use_case1b(run_pipeline) -> None:
    run_pipeline("mcp_use_case_fronius/fronius_use_case1b.yaml")


def test_fronius_use_case2_1(run_pipeline) -> None:
    run_pipeline("mcp_use_case_fronius/fronius_use_case2.yaml", "mcp_use_case_fronius/fronius_use_case1.yaml")


def test_fronius_use_case2_1b(run_pipeline) -> None:
    run_pipeline("mcp_use_case_fronius/fronius_use_case2.yaml", "mcp_use_case_fronius/fronius_use_case1b.yaml")
