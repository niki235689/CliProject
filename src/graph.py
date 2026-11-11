"""Модуль построения графа зависимостей и обхода дерева."""
from fetcher import fetch_real, fetch_test


def build_graph(start: str, ver: str, url: str, is_test: bool) -> dict:
    """Строит граф зависимостей обходом DFS без рекурсии."""
    graph = {}
    stack = [(start, ver)]
    visited = set()

    while stack:
        pkg, curr_ver = stack.pop()
        if pkg in visited:
            continue

        visited.add(pkg)
        if is_test:
            deps = fetch_test(pkg, url)
        else:
            deps = fetch_real(pkg, curr_ver, url)

        graph[pkg] = deps

        for dep in deps:
            if dep not in visited:
                stack.append((dep, "*"))
    return graph


def print_ascii(graph: dict, start: str) -> None:
    """Итеративный вывод дерева зависимостей в формате ASCII."""
    stack = [(start, 0, "")]
    visited_on_path = set()

    while stack:
        node, depth, indent = stack.pop()
        if depth > 0:
            print(f"{indent}└── {node}")
        else:
            print(node)

        if node in visited_on_path:
            continue
        visited_on_path.add(node)

        children = graph.get(node, [])
        for child in reversed(children):
            stack.append((child, depth + 1, indent + "    "))