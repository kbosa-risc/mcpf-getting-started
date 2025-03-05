# ruff: noqa: E741


def test_upo_use_case1(run_pipeline) -> None:
    run_pipeline("mcp_use_case_UPO/upo_use_case1.yaml")


def test_upo_use_case2(run_pipeline) -> None:
    run_pipeline("mcp_use_case_UPO/upo_use_case2.yaml", "mcp_use_case_UPO/upo_use_case1.yaml")
