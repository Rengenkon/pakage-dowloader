from Node import Node, NodeType, Modifier
from TreeSorter import TreeSorter

class TreeFilter:
    @staticmethod
    def get_packages(root: Node, target_path: str = "root") -> list[str]:
        # Сортируем перед поиском для работы оптимизации
        TreeSorter.sort_recursive(root)
        
        if not target_path or target_path.lower() == "root":
            return TreeFilter._collect_packages(root)

        path_parts = target_path.strip('/').split('/')
        target_node = TreeFilter._find_node(root, path_parts)
        
        return TreeFilter._collect_packages(target_node) if target_node else []

    @staticmethod
    def _find_node(current_node: Node, path_parts: list[str]) -> Node:
        if not path_parts:
            return current_node

        target = path_parts[0].lower()
        for child in current_node.children:
            if child.node_type == NodeType.CATEGORY:
                name_low = child.name.lower()
                if name_low == target:
                    return TreeFilter._find_node(child, path_parts[1:])
                if name_low > target: # Оптимизация на отсортированном списке
                    break
        return None

    @staticmethod
    def _collect_packages(start_node: Node) -> list[str]:
        packages = []
        for child in start_node.children:
            if child.node_type == NodeType.PACKAGE:
                if child.modifier not in [Modifier.STRIKETHROUGH, Modifier.INVALID]:
                    packages.append(child.name)
            elif child.node_type == NodeType.CATEGORY and child.modifier != Modifier.INVALID:
                packages.extend(TreeFilter._collect_packages(child))
        return packages