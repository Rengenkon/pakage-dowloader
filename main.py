import argparse
import sys
from MarkdownParser import MarkdownParser
from TreeFilter import TreeFilter
from managers import PacmanManager, YayManager, DebugManager

def main():
    parser = argparse.ArgumentParser(
        description="Arch Linux Package Deployer (Markdown based)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("-f", "--file", required=True, 
                        help="Путь к вашему Markdown файлу с пакетами")
    
    parser.add_argument("-m", "--manager", choices=["pacman", "yay", "debug"], 
                        default="debug", 
                        help="Пакетный менеджер (по умолчанию: debug)")
    
    parser.add_argument("-c", "--category", default="root", 
                        help="Путь категории для установки (например: 'System/Core').\n"
                             "Используйте 'root' для установки всех валидных пакетов.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # 1. Реестр менеджеров
    registry = {
        "pacman": PacmanManager(),
        "yay": YayManager(),
        "debug": DebugManager()
    }
    selected_manager = registry[args.manager]

    try:
        # 2. Парсинг в дерево (статический метод)
        print(f"[*] Чтение файла: {args.file}...")
        root_node = MarkdownParser.parse(args.file)

        # 3. Получение списка пакетов через фильтр (с внутренней сортировкой)
        print(f"[*] Фильтрация по категории: '{args.category}'...")
        raw_packages = TreeFilter.get_packages(root_node, args.category)

        # 4. Превращаем в set для удаления дубликатов и обратно в список
        # Сортируем финальный список для предсказуемости вывода
        unique_packages = sorted(list(set(raw_packages)))

        if not unique_packages:
            print("[!] Список пакетов пуст. Проверьте путь категории или форматирование.")
            return

        # 5. Выполнение установки
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