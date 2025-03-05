from typing import Callable, Generator

import pytest

import mcp_frm.pipeline_runtime as runtime


def _actually_run_pipeline(*args: str):
    runtime.run(*args)


@pytest.fixture
def run_pipeline() -> Generator[Callable[..., None], None, None]:
    return _actually_run_pipeline
