from abc import ABC, abstractmethod


class DatabaseRepository(ABC):

    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def update(self, document_filter, updated_data):
        ...

    @abstractmethod
    def save(self, data):
        ...

    @abstractmethod
    def delete(self, document_filter):
        ...
