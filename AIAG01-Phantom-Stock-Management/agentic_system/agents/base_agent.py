"""
Base Agent Class
Defines the interface for all autonomous agents
"""
from abc import ABC, abstractmethod
from typing import Any
from models.messages import AgentMessage

class BaseAgent(ABC):
    """Base class for all autonomous agents"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.state = {}
    
    @abstractmethod
    def receive(self, message: AgentMessage) -> None:
        """Receive input from another agent or external source"""
        pass
    
    @abstractmethod
    def process(self) -> None:
        """Process received data using agent's logic"""
        pass
    
    @abstractmethod
    def send(self) -> AgentMessage:
        """Send output to next agent"""
        pass
    
    def execute(self, input_message: AgentMessage) -> AgentMessage:
        """Execute full agent cycle: receive -> process -> send"""
        self.receive(input_message)
        self.process()
        return self.send()
    
    def get_reasoning(self) -> str:
        """Return agent's reasoning process"""
        return f"{self.name}: {self.role}"
