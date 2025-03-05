# ruff: noqa: E741


def test_santub_use_case1(run_pipeline) -> None:
    run_pipeline("mcp_santub/santub_use_case1.yaml")


def test_santub_use_case2(run_pipeline) -> None:
    run_pipeline("mcp_santub/santub_use_case2.yaml", "mcp_santub/santub_use_case1.yaml")
