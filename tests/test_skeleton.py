# -*- coding: utf-8 -*-

import pytest
from happy_tasks.skeleton import fib

__author__ = "Garry Lachman"
__copyright__ = "Garry Lachman"
__license__ = "mit"


def test_fib() -> None:
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
