from AbstractManager import AbstractManager

class DebugManager(AbstractManager):
    """Менеджер для отладки: просто печатает список пакетов."""
    
    @property
    def name(self) -> str:
        return "debug"

    def install(self, packages: list[str]) -> bool:
        if not packages:
            print("[Debug] Список пакетов пуст.")
            return True
        
        print(f"\n[Debug] Имитация установки {len(packages)} пакетов:")
        for i, pkg in enumerate(packages, 1):
            print(f"  {i}. {pkg}")
        
        print("\n[Debug] Процесс завершен (имитация).")
        return True