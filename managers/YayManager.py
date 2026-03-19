import subprocess
import sys
import shutil
import os
import tempfile
from AbstractManager import AbstractManager

class YayManager(AbstractManager):
    """AUR helper manager with auto-bootstrap capabilities."""

    @property
    def name(self) -> str:
        return "yay"

    def install(self, packages: list[str]) -> bool:
        if not packages:
            return True

        # Проверяем наличие yay перед работой
        if not self._is_installed():
            print("[Yay] Менеджер не найден. Запуск процесса автоматической установки...")
            if not self._bootstrap_yay():
                print("[!] Не удалось установить yay автоматически.", file=sys.stderr)
                return False

        print(f"\n[Yay] Installing {len(packages)} AUR packages...")
        command = ["yay", "-S", "--needed", "--noconfirm"] + packages
        
        try:
            subprocess.run(command, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing yay: {e}", file=sys.stderr)
            return False

    def _is_installed(self) -> bool:
        """Проверяет, доступен ли бинарник yay в системе."""
        return shutil.which("yay") is not None

    def _bootstrap_yay(self) -> bool:
        """
        Процесс ручной установки yay из AUR.
        Требует наличия git и base-devel.
        """
        try:
            # 1. Устанавливаем зависимости для сборки через pacman
            print("[*] Установка зависимостей для сборки (git, base-devel)...")
            subprocess.run(["sudo", "pacman", "-S", "--needed", "--noconfirm", "git", "base-devel"], check=True)

            # 2. Создаем временную директорию для сборки
            with tempfile.TemporaryDirectory() as tmpdir:
                print(f"[*] Клонирование репозитория yay в {tmpdir}...")
                subprocess.run(["git", "clone", "https://aur.archlinux.org/yay.git", tmpdir], check=True)
                
                # 3. Сборка и установка (makepkg)
                # Флаг -s устанавливает зависимости, -i устанавливает пакет
                print("[*] Сборка пакета (makepkg)...")
                # Важно: makepkg нельзя запускать от root, поэтому вызываем напрямую (он сам запросит sudo для установки)
                subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=tmpdir, check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при бутстрапе yay: {e}", file=sys.stderr)
            return False