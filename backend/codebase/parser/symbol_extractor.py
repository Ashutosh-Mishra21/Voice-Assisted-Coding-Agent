from tree_sitter import Node


class SymbolExtractor:

    _FUNCTION_NODES = {
        "python": {
            "function_definition",
            "async_function_definition",
        },
        "javascript": {
            "function_declaration",
            "generator_function_declaration",
            "method_definition",
        },
        "typescript": {
            "function_declaration",
            "generator_function_declaration",
            "method_definition",
            "method_signature",
        },
        "tsx": {
            "function_declaration",
            "generator_function_declaration",
            "method_definition",
            "method_signature",
        },
        "java": {
            "method_declaration",
            "constructor_declaration",
        },
    }

    _CLASS_NODES = {
        "python": {"class_definition"},
        "javascript": {"class_declaration"},
        "typescript": {
            "class_declaration",
            "interface_declaration",
            "enum_declaration",
            "type_alias_declaration",
        },
        "tsx": {
            "class_declaration",
            "interface_declaration",
            "enum_declaration",
            "type_alias_declaration",
        },
        "java": {
            "class_declaration",
            "interface_declaration",
            "enum_declaration",
            "annotation_type_declaration",
        },
    }

    def extract(self, root_node, language: str = "python"):

        symbols = []

        self._walk(root_node, symbols, language)

        return symbols

    def _walk(self, node: Node, symbols, language: str):

        if node.type in self._FUNCTION_NODES.get(language, set()):
            self._append_named_symbol(node, symbols, "function")

        elif node.type in self._CLASS_NODES.get(language, set()):
            self._append_named_symbol(node, symbols, "class")

        elif language == "html" and node.type == "element":
            self._append_html_symbol(node, symbols)

        elif language == "css" and node.type in {
            "rule_set",
            "media_statement",
            "keyframes_statement",
        }:
            self._append_css_symbol(node, symbols)

        for child in node.children:
            self._walk(child, symbols, language)

    @staticmethod
    def _append_named_symbol(node: Node, symbols, symbol_type: str):
        name_node = node.child_by_field_name("name")

        if name_node:
            symbols.append(
                {
                    "type": symbol_type,
                    "name": name_node.text.decode("utf-8"),
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                }
            )

    @staticmethod
    def _append_html_symbol(node: Node, symbols):
        start_tag = node.child_by_field_name("open_tag")
        name_node = start_tag.child_by_field_name("name") if start_tag else None

        if name_node:
            symbols.append(
                {
                    "type": "component",
                    "name": name_node.text.decode("utf-8"),
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                }
            )

    @staticmethod
    def _append_css_symbol(node: Node, symbols):
        name = node.child_by_field_name("name")

        if name is None and node.named_child_count:
            name = node.named_children[0]

        if name:
            symbols.append(
                {
                    "type": "style_rule",
                    "name": name.text.decode("utf-8").strip(),
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                }
            )
