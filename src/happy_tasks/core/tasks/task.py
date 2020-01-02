# -*- coding: utf-8 -*-
"""
Task & Task related classes
---------------------------
The task implements the logic and the execution of the task.
Each task has to execute the minimal as can logic and move the output data to the next task. 
The idea behind seperating the logic to many task is the ability to catch errors, bugs & optimize performace.
When we mix many components to one task we lose the ability to monitor the process by details.
"""
from __future__ import annotations
from typing import TypeVar, Generic, List, Any
from mypy_extensions import TypedDict
from happy_tasks.core.flows.flow import FlowDetails
from happy_tasks.core.tasks.exceptions import TaskValidationException
from enum import Enum

""" Task Status
Name	      | Value	| Description
----------------------------------------------
NOT_STARTED	|   0  	| The task not started yet
RUNNING	    |   1	  | The task is executing the logic
COMPLETED	  |   2	  | The task complete the execution
ERROR	      |   3	  | The task is failure to validate the input data or the execution failure
"""
class TaskStatus(Enum):
    NOT_STARTED = 0
    RUNNING = 1
    COMPLETED = 2
    ERROR = 3
    
class TaskTriggerEvent(Enum):
    COMPLETE = 0
    ERROR = 1
    
class TaskTrigger():
    _on: TaskTriggerEvent
    _target: Any
    
    def __init__(self, on: TaskTriggerEvent, target: Any):
        self._on = on
        self._target = target
        
    @property
    def on(self) -> TaskTriggerEvent:
        return self._on
      
    @property
    def target(self) -> Any:
        return self._target

CT = TypeVar('CT')

class Task(Generic[CT]):
    _name: str
    _flowDetails: FlowDetails
    _config: CT
    _status: TaskStatus
    _input_data: List[Any]
    _dependedOn: List[Task]
    _triggers: List[TaskTrigger]
    
    """Task init
    
    Args:
      name (str): Task name
      flowDetails (FlowDetails): The owner flow details
    """
    def __init__(self, name: str, flowDetails: FlowDetails):
        self._name = name
        self._flowDetails = flowDetails
        self._status = TaskStatus.NOT_STARTED
        self._input_data = []
        self.hook_init()
        
    """Name getter
    
    Return:
      str: Task name
    """
    @property
    def name(self) -> str:
        return self._name
      
    """Task Status
    
    Return:
      TaskStatus: Task Status Enum value
    """
    @property
    def status(self) -> TaskStatus:
        return self._status
    
    """Flow Details getter
    
    Return:
      FlowDetails: Flow Deatils
    """
    @property
    def flowDetails(self) -> FlowDetails:
        return self._flowDetails
    
    """Task config getter/setter
    
    Args:
      value ([CT]): Task config
      
    Return:
      [CT]: Task config
    """
    @property
    def config(self) -> CT:
        return self._config
    @config.setter
    def config(self, value: CT) -> None:
        self.hook_config(value)
        
    """Input data getter
      
    Return:
      List[Any]: Input data
    """
    @property
    def inputData(self) -> List[Any]:
        return self._input_data
    
    """ Append Input Data
    
    Args:
      value (Any): Input data
    """
    def appendInputData(self, value: Any) -> None:
        self.hook_inputData(value)
        
    """ Execute 
    Execute hook is called in order to start the task execution. This is only wraper for ExecuteWork method
    that done the work.
    """
    def execute(self) -> None:
        self.hook_preValidate()
        self._status = TaskStatus.RUNNING
        self.executeWork()
        self.hook_postValidate()
        self._status = TaskStatus.COMPLETED
        
    """ ExecuteWork
    The tasks magic is happen here.
    """
    def executeWork(self) -> None:
        pass
    
    """ Rise a task validation exception
    Mark task status as error + rise exception
    
    Args:
      message (str): Error message
    """
    def riseValidationException(self, message: str) -> None:
      self._status = TaskStatus.ERROR
      raise TaskValidationException(message)
    
    """ HOOKS Section
    ----------------------------------
    """
    
    """ Init hook
    The hook is called when the task first created
    """
    def hook_init(self) -> None:
        pass
      
    """ Config hook
    The hook is called when new config is assigned, the configuration can be modifited inside the hook.
    
    Args:
      value ([CT]): Task config
    """
    def hook_config(self, value: CT) -> None:
        self._config = value
        
    """ Input Data hook
    Input hook is called with the task input data array as param.
    The task can receive data from one or more previous tasks so we use array.
    if this hook is implemented the data can be changed inside the hook and the modified version has to be passed to parent method
    
    Args:
      value: Input data
    """
    def hook_inputData(self, value: Any) -> None:
        self._input_data.append(value)
        
    """ Pre Validate hook
    Pre Validate hook is called in order to validate if the input data are valid, 
    in case of invalid data error(e) method will be called.
    """
    def hook_preValidate(self) -> None:
        pass
      
    """ Post Validate hook
    Pre Validate hook is called in order to validate if the ouput data are valid, 
    in case of invalid data error(e) method will be called.
    """
    def hook_postValidate(self) -> None:
        pass
      
    