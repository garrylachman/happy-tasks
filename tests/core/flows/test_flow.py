# -*- coding: utf-8 -*-
from __future__ import annotations

import pytest
from happy_tasks.core.flows.flow import FlowDetails, Flow
from happy_tasks.core.flows.exceptions import FlowConfigException, FlowConfigFileNotFoundException

from datetime import datetime

from mypy_extensions import TypedDict

"""Example config generic
"""
class ExampleConfig(TypedDict):
    name: str
    
ExampleFlowDetailsNow: datetime = datetime.now()
ExampleFlowDetails: FlowDetails = FlowDetails({
    'name': 'flow1',
    'timestamp': ExampleFlowDetailsNow
})

def test_base() -> None:
    f:Flow = Flow("flow1")
    assert f.details.name == "flow1"
    
def test_empty_name() -> None:
    with pytest.raises(FlowConfigException):
        Flow("")

def test_missing_yaml_config_file() -> None:
    with pytest.raises(FlowConfigFileNotFoundException):
        Flow.initFromYAML("tests/missing_file.yaml")   

def test_yaml_config_file() -> None:
    f:Flow = Flow.initFromYAML("tests/flow1.yaml")
    assert f.details.name == "usersUsageFlow"
    