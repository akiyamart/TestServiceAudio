from abc import ABC, abstractmethod

class IHandler(ABC):
    
    @abstractmethod
    async def handle():
        raise NotImplementedError()