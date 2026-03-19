import subprocess
import sys
from AbstractManager import AbstractManager

class YayManager(AbstractManager):
    """AUR helper manager."""

    @property
    def name(self) -> str:
        return "yay"

    def install(self, packages: list[str]) -> bool:
        if not packages:
            return True

        print(f"\n[Yay] Installing {len(packages)} AUR packages...")
        command = ["yay", "-S", "--needed", "--noconfirm"] + packages
        
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing yay: {e}", file=sys.stderr)
            return False