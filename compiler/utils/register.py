from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class FunctionDescriptor:
    n_arguments: int
    n_returns: int


@dataclass
class Scope:
    name: str
    parent: Optional[str]
    object_register: List[str]
    function_register: Dict[str, FunctionDescriptor]


class Register:
    def __init__(self):
        self.global_scope = Scope(parent=None, object_register=[], function_register={}, name='global')
        self.scopes = {'global': self.global_scope}

    def is_object_in_scope(self, object_name: str, scope_name: str, with_outer: bool = True) -> bool:
        if scope_name is None:
            return False
        if object_name not in self.scopes[scope_name].object_register:
            if not with_outer:
                return False
            return self.is_object_in_scope(object_name, self.parent_name(scope_name))
        return True

    def is_function_in_scope(self, function_name: str, scope_name: str) -> bool:
        if scope_name is None:
            return False
        if function_name not in self.scopes[scope_name].function_register.keys():
            return self.is_function_in_scope(function_name, self.parent_name(scope_name))
        return True

    def add_object_to_scope(self, object_name: str, scope_name: str) -> None:
        self.scopes[scope_name].object_register.append(object_name)

    def add_function_to_scope(self, function_name: str, function_descriptor: FunctionDescriptor, scope_name: str) -> None:
        self.scopes[scope_name].function_register[function_name] = function_descriptor

    def update_function_in_scope(self, function_name: str, function_descriptor: FunctionDescriptor, scope_name: str):
        if scope_name is None:
            return
        elif function_name not in self.scopes[scope_name].function_register.keys():
            self.update_function_in_scope(function_name, function_descriptor, self.parent_name(scope_name))
        else:
            self.scopes[scope_name].function_register[function_name] = function_descriptor

    def get_function_descriptor_in_scope(self, function_name: str, scope_name: str) -> Optional[FunctionDescriptor]:
        if scope_name is None:
            return None
        elif function_name not in self.scopes[scope_name].function_register.keys():
            return self.get_function_descriptor_in_scope(function_name, self.parent_name(scope_name))
        else:
            return self.scopes[scope_name].function_register[function_name]

    def parent_name(self, scope_name: str) -> str:
        return self.scopes[scope_name].parent

    def get_nearest_scope_name(self, current_scope_name: str, fun_name: str) -> str:
        if current_scope_name is None:
            raise Exception(f"Cannot find scope of function {fun_name}")
        if fun_name not in self.scopes[current_scope_name].function_register:
            return self.get_nearest_scope_name(self.parent_name(current_scope_name), fun_name)
        return current_scope_name
