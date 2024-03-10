from abc import ABC, abstractmethod

class App(ABC):
    '''
    Base class for implementing and building App logic.

    '''
    
    @abstractmethod
    def connect(self):
        pass