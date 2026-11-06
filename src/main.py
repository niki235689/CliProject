"""Главный скрипт для запуска инструмента визуализации."""
from cli import parse_args
from graph import build_graph, print_ascii
from visualize import generate_graphviz, print_load_order


def main() -> None:
    """Точка входа в программу."""
    args = parse_args()

    # Этап 1: вывод параметров
    print("=== Параметры запуска ===")
    for key, value in vars(args).items():
        print(f"{key}: {value}")

    # Этапы 2 и 3: сбор данных и построение графа (DFS)
    graph = build_graph(args.pkg, args.ver, args.url, args.test)

    print("\n--- Прямые зависимости ---")
    print(graph.get(args.pkg, []))

    if args.ascii:
        print("\n--- Вывод ASCII-дерева ---")
        print_ascii(graph, args.pkg)

    # Этап 4: порядок загрузки
    print("\n--- Порядок загрузки ---")
    print_load_order(graph, args.pkg)

    # Этап 5: визуализация через Graphviz
    generate_graphviz(graph, args.out)


if __name__ == "__main__":
    main()