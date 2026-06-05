from tree_sitter import Node


class SymbolExtractor:

    def extract(self, root_node):

        symbols = []

        self._walk(root_node, symbols)

        return symbols

    def _walk(self, node: Node, symbols):

        if node.type == "function_definition":

            name_node = node.child_by_field_name("name")

            if name_node:

                symbols.append(
                    {
                        "type": "function",
                        "name": name_node.text.decode(),
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                    }
                )

        elif node.type == "class_definition":

            name_node = node.child_by_field_name("name")

            if name_node:

                symbols.append(
                    {
                        "type": "class",
                        "name": name_node.text.decode(),
                        "start_line": node.start_point[0] + 1,
                        "end_line": node.end_point[0] + 1,
                    }
                )

        for child in node.children:
            self._walk(child, symbols)
