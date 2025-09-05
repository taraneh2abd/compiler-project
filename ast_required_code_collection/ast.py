class AST:
    def __init__(self):
        self.root = None
        self.current_number = 0

    def traverse_ast(self, root_node):
        traversal = []
        if len(root_node.children) > 0:
            for child in root_node.children:
                traversal.extend(self.traverse_ast(child))
        node_dict = dict()
        node_dict['text'] = root_node.value
        node_dict['attributes_dictionary'] = root_node.attributes_dictionary
        traversal.append(node_dict)
        return traversal

    class TreeNode:
        def __init__(self, value, children, number):
            self.value = value
            self.children = children
            self.number = number
            self.attributes_dictionary = dict()

        def add_attribute_to_node(self, attribute_name, attribute_value):
            self.attributes_dictionary[attribute_name] = attribute_value

    def make_node(self, value, children):
        tree_node = self.TreeNode(value, children, self.current_number)
        self.current_number += 1
        return tree_node
