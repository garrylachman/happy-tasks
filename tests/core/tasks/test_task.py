# -*- coding: utf-8 -*-

import pytest
from happy_tasks.core.tasks.task import Task, TaskStatus
from happy_tasks.core.tasks.exceptions import TaskValidationException
from happy_tasks.core.flows.flow import FlowDetails
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
    t:Task = Task[ExampleConfig]("task1", ExampleFlowDetails)
    assert t.name == "task1"
    assert t.flowDetails == ExampleFlowDetails
    assert t.flowDetails.name == "flow1"
    assert t.flowDetails.timestamp == ExampleFlowDetailsNow
    assert t.status == TaskStatus.NOT_STARTED
    
def test_config() -> None:
    config1: ExampleConfig = {
        'name': 'config1'
    }
    
    config2: ExampleConfig = {
        'name': 'config2'
    }
    
    config_bad = {
        'name_name': 'name'
    }
    
    t:Task = Task[ExampleConfig]("task1", ExampleFlowDetails)
    t.config = config1
    assert t.config == config1
    assert t.config['name'] == config1['name']
    assert t.config != config2
    t.config = config2
    assert t.config == config2
    assert t.config != config1
    assert t.config == t.config
    
def test_must_pass_no_input() -> None:
    t:Task = Task[ExampleConfig]("must_pass_no_input", ExampleFlowDetails)
    t.config = {}
    assert t.status == TaskStatus.NOT_STARTED
    t.execute()
    assert t.status == TaskStatus.COMPLETED
    
def test_must_pass_with_input() -> None:
    t:Task = Task[ExampleConfig]("must_pass_with_input", ExampleFlowDetails)
    t.config = {}
    t.appendInputData("A")
    assert t.inputData == ["A"]
    assert t.status == TaskStatus.NOT_STARTED
    t.execute()
    assert t.status == TaskStatus.COMPLETED

def test_must_pass_fail_validation_exception() -> None:
    t:Task = Task[ExampleConfig]("must_pass_fail_validation_exception", ExampleFlowDetails)
    t.config = {}
    t.appendInputData("A")
    assert t.inputData == ["A"]
    assert t.status == TaskStatus.NOT_STARTED
    with pytest.raises(TaskValidationException):
        t.riseValidationException("error")
    assert t.status == TaskStatus.ERROR