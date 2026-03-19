import subprocess
import sys
from AbstractManager import AbstractManager

class PacmanManager(AbstractManager):
    """Official Arch Linux repository manager."""

    @property
    def name(self) -> str:
        return "pacman"

    def install(self, packages: list[str]) -> bool:
        if not packages:
            return True

        print(f"\n[Pacman] Installing {len(packages)} packages...")
        command = ["sudo", "pacman", "-S", "--needed", "--noconfirm"] + packages
        
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing pacman: {e}", file=sys.stderr)
            return False