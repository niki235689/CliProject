"""Главный скрипт для запуска инструмента визуализации."""
from cli import parse_args
from graph import build_graph, print_ascii
from visualize import generate_graphviz, print_load_order


def main() -> None:
    """Точка входа в программу."""
    args = parse_args()

    print("Параметры запуска")
    for key, value in vars(args).items():
        print(f"{key}: {value}")

    graph = build_graph(args.pkg, args.ver, args.url, args.test)

    print("\nПрямые зависимости")
    print(graph.get(args.pkg, []))

    if args.ascii:
        print("\nВывод ASCII-дерева")
        print_ascii(graph, args.pkg)

    print("\nПорядок загрузки")
    print_load_order(graph, args.pkg)

    generate_graphviz(graph, args.out)


if __name__ == "__main__":
    main()