from graphviz import Digraph


def build_parse_tree(table, cnf_grammar, w):
    n = len(w)
    # Asegurar que la entrada y la tabla no están vacías y que la tabla tiene la dimensión adecuada
    if n == 0 or not table or len(table[0]) < n or any(not isinstance(word, str) for word in w):
        return None

    # Intentar encontrar entradas para el símbolo inicial y asegurar que todos los nodos sean válidos
    try:
        start_symbol_entries = [
            entry for entry in table[0][n - 1]
            if entry["symbol"] == cnf_grammar["startSymbol"] and entry["symbol"] in cnf_grammar["productions"]
        ]
    except (IndexError, TypeError, KeyError):
        return None  # Manejo de cualquier error en el acceso a la tabla o malformación de datos

    if start_symbol_entries:
        return start_symbol_entries[0]  # Retorna el árbol de análisis
    return None


def visualize_parse_tree(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph(comment='Parse Tree')
        graph.attr('node', shape='ellipse')

    if node is not None:
        # Crear un identificador único para cada nodo- basado en su contenido y posición para evitar duplicados
        print(f"Adding node: {node['symbol']}")  # Depuración
        node_id = str(id(node))
        graph.node(node_id, label=node['symbol'])

        if parent:
            graph.edge(parent, node_id)

        if node.get('children'):
            for child in node['children']:
                visualize_parse_tree(child, graph, node_id)

    return graph
