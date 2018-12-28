from abc import ABC, abstractmethod


class AbstractHook(ABC):
    @abstractmethod
    def builder(self) -> str:
        pass

    @abstractmethod
    def event(self) -> str:
        pass

    @abstractmethod
    def patch(self, container, operating_system, arch, version, distribution) -> None:
        pass
