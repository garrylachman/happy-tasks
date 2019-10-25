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
from datetime import datetime
from mypy_extensions import TypedDict

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
    details: FlowDetails
    
    """Flow init
    
    Args:
      name (str): Flow name 
    """
    def __init__(self, name: str):
        self.details = FlowDetails({
            'name': name,
            'timestamp': datetime.now()
        })
        