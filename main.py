import argparse
import sys
import os
from MarkdownParser import MarkdownParser
from TreeFilter import TreeFilter
from managers import PacmanManager, YayManager, DebugManager

def check_not_root():
    """
    Проверка прав доступа. 
    UID 0 всегда принадлежит root.
    """
    if os.getuid() == 0:
        print("[!] Ошибка: Скрипт нельзя запускать от имени root или через sudo.")
        print("    Используйте запуск от обычного пользователя. Менеджеры сами запрясят пароль.")
        sys.exit(1)

def main():
    # Проверка на root перед любыми действиями
    check_not_root()

    parser = argparse.ArgumentParser(
        description="Arch Linux Package Deployer (Markdown based)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-f", "--file", required=True, 
                        help="Путь к вашему Markdown файлу с пакетами")
    
    parser.add_argument("-m", "--manager", choices=["pacman", "yay", "debug"], 
                        default="yay", 
                        help="Пакетный менеджер (по умолчанию: yay)")
    
    parser.add_argument("-c", "--category", default="root", 
                        help="Путь категории для установки (например: 'System/Core').\n"
                             "Используйте 'root' для установки всех валидных пакетов.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    registry = {
        "pacman": PacmanManager(),
        "yay": YayManager(),
        "debug": DebugManager()
    }
    selected_manager = registry[args.manager]

    try:
        print(f"[*] Чтение файла: {args.file}...")
        root_node = MarkdownParser.parse(args.file)

        print(f"[*] Фильтрация по категории: '{args.category}'...")
        # Внутри TreeFilter.get_packages происходит автоматическая сортировка
        raw_packages = TreeFilter.get_packages(root_node, args.category)

        # Удаление дубликатов и сортировка
        unique_packages = sorted(list(set(raw_packages)))

        if not unique_packages:
            print("[!] Список пакетов пуст. Проверьте путь категории или форматирование.")
            return

        print(f"[*] Подготовлено уникальных пакетов: {len(unique_packages)}")
        success = selected_manager.install(unique_packages)

        if not success:
            print("\n[!] Произошла ошибка во время работы менеджера.", file=sys.stderr)
            sys.exit(1)
            
        print("\n[+] Операция успешно завершена.")

    except FileNotFoundError:
        print(f"Error: Файл '{args.file}' не найден.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()