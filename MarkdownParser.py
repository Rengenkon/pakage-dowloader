import re
from Node import Node, NodeType

class MarkdownParser:
    @staticmethod
    def parse(file_path: str) -> Node:
        root = Node("Root", level=-1, node_type=NodeType.CATEGORY)
        stack = [root]

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line:
                    continue

                # Логика определения Категории
                header_match = re.match(r'^(#+)\s+(.*)', clean_line)
                if header_match:
                    level = len(header_match.group(1))
                    new_node = Node(line, level, NodeType.CATEGORY)
                    
                    while len(stack) > 1 and stack[-1].level >= level:
                        stack.pop()
                    
                    stack[-1].add_child(new_node)
                    stack.append(new_node)
                    continue

                # Логика определения Пакета
                if clean_line.startswith(('-', '*', '+')):
                    parent_category = stack[-1]
                    pkg_node = Node(line, parent_category.level + 1, NodeType.PACKAGE)
                    parent_category.add_child(pkg_node)

        return root