"""Модуль для визуализации графа с помощью Graphviz."""
import os
import subprocess


def print_load_order(graph: dict, start_node: str) -> None:
    """Выводит порядок загрузки зависимостей (топологический порядок)."""
    visited = set()
    visiting = set()
    order = []

    def dfs(node: str) -> None:
        if node in visiting:
            return
        if node in visited:
            return
        visiting.add(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
        visiting.remove(node)
        visited.add(node)
        order.append(node)

    dfs(start_node)
    print(" -> ".join(order))


def generate_graphviz(graph: dict, out_file: str) -> None:
    """Формирует DOT-описание и компилирует его в PNG."""
    dot_path = f"{out_file}.dot"
    with open(dot_path, "w", encoding="utf-8") as file:
        file.write("digraph G {\n")
        for node, edges in graph.items():
            for edge in edges:
                file.write(f'  "{node}" -> "{edge}";\n')
        file.write("}\n")

    dot_cmd = "dot"
    possible_paths = [
        r"C:\Program Files\Graphviz\bin\dot.exe",
        r"C:\Program Files (x86)\Graphviz\bin\dot.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            dot_cmd = path
            break

    try:
        subprocess.run(
            [dot_cmd, "-Tpng", dot_path, "-o", out_file],
            check=True
        )
        print(f"Успех: Граф сохранен в {out_file}")
    except FileNotFoundError:
        print("Внимание: Утилита 'dot' не найдена.")
        print(f"Текстовый DOT-файл сохранен: {dot_path}")
    except subprocess.CalledProcessError as err:
        print(f"Ошибка вызова Graphviz: {err}")