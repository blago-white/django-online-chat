from abc import ABCMeta, abstractmethod


class BaseService(metaclass=ABCMeta):
    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass
