import re
from enum import Enum, auto
from typing import List, Optional

class Modifier(Enum):
    NORMAL = auto()
    BOLD = auto()          # **package**
    ITALIC = auto()        # *package*
    STRIKETHROUGH = auto() # ~~package~~
    INVALID = auto()       # Mixed styles like **~~pkg~~**

class NodeType(Enum):
    CATEGORY = auto() # Заголовки #, ##, ###
    PACKAGE = auto()  # Элементы списка - or *

class Node:
    def __init__(self, raw_line: str, level: int, node_type: NodeType):
        self.raw_content: str = raw_line
        self.level: int = level
        self.node_type: NodeType = node_type
        self.children: List['Node'] = []
        
        # Результаты парсинга
        self.name: str = ""
        self.modifier: Modifier = Modifier.NORMAL
        
        self._parse_line(raw_line)

    def _parse_line(self, line: str):
        """
        Извлекает чистое имя и определяет модификатор.
        Реализует логику: если стилей > 1, то INVALID.
        """
        # Очищаем от синтаксиса Markdown (маркеры списка и заголовков)
        clean_line = line.lstrip('#- *+').strip()
        
        # Убираем комментарии в конце строки (все что после #)
        clean_line = clean_line.split('#')[0].strip()

        # Регулярные выражения для поиска паттернов
        patterns = {
            Modifier.BOLD: r'\*\*(.*?)\*\*',
            Modifier.ITALIC: r'\*(.*?)\*',
            Modifier.STRIKETHROUGH: r'~~(.*?)~~'
        }

        found_modifiers = []
        extracted_name = clean_line

        for mod, r in patterns.items():
            match = re.search(r, clean_line)
            if match:
                found_modifiers.append(mod)
                # Извлекаем текст внутри разметки (группа 1)
                extracted_name = match.group(1)

        # Логика валидации
        if len(found_modifiers) > 1:
            self.modifier = Modifier.INVALID
            # В случае ошибки имя оставляем как есть для логов
            self.name = clean_line 
        elif len(found_modifiers) == 1:
            self.modifier = found_modifiers[0]
            self.name = extracted_name
        else:
            self.modifier = Modifier.NORMAL
            self.name = clean_line

    def add_child(self, node: 'Node'):
        self.children.append(node)

    def __repr__(self):
        return f"Node(name='{self.name}', type={self.node_type.name}, mod={self.modifier.name}, lvl={self.level})"