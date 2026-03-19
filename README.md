# Arch Package Deployer (APD)

> [🇷🇺 Русский](#russian) | [🇺🇸 English](#english)

---

<a name="russian"></a>
## 🇷🇺 Russian Version

**Описание:** Консольная утилита для декларативного управления пакетами Arch Linux через иерархические Markdown-списки с поддержкой логики форматирования.

### Пример конфигурации (`packages.md`)
```markdown
# System
## Core
- **linux** # Жирный: Обязательный
- base               # Обычный: Стандартный
- *intel-ucode* # Курсив: Опциональный
- ~~test-pkg~~       # Зачеркнутый: Игнорировать

# Software
## Dev
- python
- **neovim**
```

### Команда запуска
```bash
# Проверка структуры (режим отладки) для конкретной категории
python main.py --file packages.md --manager debug --category "System/Core"

# Реальная установка всей системы через yay
python main.py -f packages.md -m yay -c root
```

### Поддерживаемые пакетные менеджеры
- pacman
- yay

<a name="english"></a>
## 🇺🇸 English Version

**Description:** : A CLI utility for declarative Arch Linux package management using hierarchical Markdown lists with formatting-based logic.

### Config Example (packages.md)
```Markdown
# Desktop
## Browsers
- firefox            # Normal: Standard
- **chromium** # Bold: Mandatory
- *opera* # Italic: Optional
- ~~edge-bin~~       # Strikethrough: Blacklisted

# Media
- mpv
- **gimp**
```

### Execution Command
```Bash
# Dry run (debug mode) for a specific category path
python main.py --file packages.md --manager debug --category "Desktop/Browsers"

# Actual installation of the entire tree via pacman
python main.py -f packages.md -m pacman -c root
```

### Supported pakage managers
- pacman
- yay


## Аргументы / Arguments
| Flag | Description |
| ---: | :--- |
| -f | Путь к файлу / Path to .md file |
| -m | Менеджер / Manager (pacman, yay, debug) |
| -c | Путь или 'root' / Category path or 'root' |
