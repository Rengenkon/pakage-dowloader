from Node import Node, NodeType

class TreeSorter:
    """
    Stateless утилита для нормализации структуры дерева.
    """

    @staticmethod
    def sort_recursive(node: Node):
        """
        Рекурсивно сортирует детей узла:
        1. Сначала по уровню (level) — от меньшего к большему.
        2. Затем по имени (name) — по алфавиту.
        """
        if not node.children:
            return

        # Сортировка текущего уровня
        # В Python sort() стабильна, поэтому можно использовать кортеж для multi-key sort
        node.children.sort(key=lambda x: (x.level, x.name.lower()))

        # Рекурсивный спуск
        for child in node.children:
            TreeSorter.sort_recursive(child)

    @staticmethod
    def flatten_to_list(node: Node, path_prefix: str = "") -> list:
        """
        Вспомогательный метод: превращает дерево в плоский список путей.
        Полезно для отладки или оптимизации поиска.
        Пример: ['Core/Base/python', 'Core/Network/wget']
        """
        results = []
        # Формируем текущий путь
        current_path = f"{path_prefix}/{node.name}" if path_prefix else node.name
        
        if node.node_type == NodeType.PACKAGE:
            results.append(current_path)
        
        for child in node.children:
            results.extend(TreeSorter.flatten_to_list(child, current_path))
            
        return results