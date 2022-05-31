import os
from os.path import join
import sys

import javalang


class JClass:
    def __init__(self, name, types):
        self.types = types
        self.name = name
        self.fields = []
        self.methods = []
    
    def add_field(self, field):
        self.fields.append(field)
    
    def add_method(self, method):
        self.methods.append(method)

    def __str__(self):
        return "| " + self.name + "\n---\n" + '\n'.join(self.fields) + '\n---\n' + '\n'.join(self.methods) + '\n---'
    
    def used_types(self, valid_types):
        result = self.types.intersection(self.types, valid_types)
        return '' if not result else result

def process_type(types_set, node):
    result = ''
    if hasattr(node, 'name'):        
        name = node.name
        types_set.add(name)
        result = name
    if hasattr(node, 'arguments') and node.arguments:
        result += '<'
        types = []
        for arg in node.arguments:
            types.append(process_type(types_set, arg.type))
        result += ','.join(types) + '>'
    return result


def get_modifier(node):
    m_dict = { 'private': '-', 'public': '+', 'protected': '#' }
    modifiers_list = list(node.modifiers)
    modifier_ = '' if not modifiers_list else modifiers_list[0]
    return m_dict.get(modifier_, '')
    

def process_java_code(classes_, code):
    tree = javalang.parse.parse(code)
    types = set()
    name = ''
    for path, node in tree:
        node_name = type(node).__name__
        if node_name == "FieldDeclaration":
            type_ = process_type(types, node.type)
            name_ = node.declarators[0].name
            classes_[name].add_field(' '.join([get_modifier(node), name_, ":", type_]))
        elif node_name == "MethodDeclaration":
            name_ = node.name
            r_type_ = process_type(types, node.return_type) or 'void'
            parameters_ = []
            for p in node.parameters:
                parameters_.append(p.name + ': ' + process_type(types, p.type))
            classes_[name].add_method(' '.join([get_modifier(node), name_ + '(' + ', '.join(parameters_) + ')', ":", r_type_]))
        elif node_name == "ClassDeclaration":
            name = node.name
            classes_[name] = JClass(node.name, types)


for root, dirs, files in os.walk(sys.argv[1]):
    classes_ = {}
    for name in files:
        if '.java' in name:
            process_java_code(classes_, open(join(root, name), 'r').read())


for k, v in classes_.items():
    print(v)
    print("uses:", v.used_types(classes_.keys()))
    print()
