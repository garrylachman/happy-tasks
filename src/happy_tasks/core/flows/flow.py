# -*- coding: utf-8 -*-
"""
Flow & Flow related classes
---------------------------
If the Task is the micro - the job itself, the Flow is the macro plan.
Here we design the sequence of tasks, their inputs, configs, the triggers.
The Flow is in charge of how when running when and the result of each action.

The Flow handle the dependencies between the tasks and the triggers of each 
Task in case of successful run or exception.
"""
from __future__ import annotations
from datetime import datetime
from mypy_extensions import TypedDict
from typing import Any, Dict, Optional
from happy_tasks.core.flows.exceptions import FlowConfigException, FlowConfigFileNotFoundException

Loader: Any = None
from yaml import load, YAMLError, YAMLObject
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader as Loader


"""FlowDetailsTyping (TypedDict) checks Flow Details Typing
"""
class FlowDetailsTyping(TypedDict):
    name: str
    timestamp: datetime

"""Flow Details
"""
class FlowDetails():
    details: FlowDetailsTyping
    
    """Flow Details init
    
    Args:
      details (FlowDetailsTyping): The flow details with typing check 
    """
    def __init__(self, details: FlowDetailsTyping):
        self.details = details
        
    """ Flow name
    Returns:
      str: Flow name
    """
    @property
    def name(self) -> str:
        return self.details['name']
    
    """ Flow timestamp
    Returns:
      datetime: Flow timestamp
    """
    @property
    def timestamp(self) -> datetime:
        return self.details['timestamp']


"""Flow class
"""
class Flow:
    _details: FlowDetails
    _config: Optional[Dict[Any, Any]]
    
    """Flow init
    
    Args:
      name (str): Flow name 
    """
    def __init__(self, name: str, config: Dict=None):
        if len(name) < 1:
            raise FlowConfigException("Empty flow name")
        self._config = config
        self._details = FlowDetails({
            'name': name,
            'timestamp': datetime.now()
        })
        
    @property
    def details(self) -> FlowDetails:
        return self._details
      
    @classmethod
    def initFromYAML(cls, filePath: str) -> Flow:
        try:
            with open(filePath, 'r') as stream:
                try:
                    configYAML:Dict = load(stream, Loader=Loader)
                    if configYAML["name"]:
                        return Flow(configYAML["name"], configYAML)
                    else:
                        raise FlowConfigException("Flow name is missing in YAML config")
                except YAMLError:
                    raise FlowConfigException("YAML config parsing error")
        except EnvironmentError:
            raise FlowConfigFileNotFoundException(filePath)
                    