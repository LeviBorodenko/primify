# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for primify.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

from PIL import Image
import pytest


@pytest.fixture()
def test_image() -> Image.Image:
    return Image.open("tests/gauss.png")


@pytest.fixture(params=[10, 100, 1000, 10000])
def test_max_digits(request) -> int:
    return request.param
