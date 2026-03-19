from abc import ABC, abstractmethod

class AbstractManager(ABC):
    """
    Base interface for all package managers.
    Equivalent to a Java Interface with default property behavior.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the binary name of the manager."""
        pass

    @abstractmethod
    def install(self, packages: list[str]) -> bool:
        """
        Executes the installation command.
        :param packages: List of package names to install.
        :return: True if successful, False otherwise.
        """
        pass