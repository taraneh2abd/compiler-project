from enum import Enum, auto
from copy import deepcopy
from typing import List
from plantuml import PlantUML
import os

from compiler.utils.exceptions import ObjectNotDeclaredException
from compiler.utils.function import Function
from compiler.utils.object import Object


class Mode(Enum):
    """
    dosc for Mode
    """
    ALL = auto()
    BRIEF = auto()


class OutputGenerator:
    """ docs for OutputGenerator"""

    def __init__(self):
        self.server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        self.global_objects = {}
        self.diagram_generators = {}
        self._functions = {}

    def generate(self, diag_name: str, mode: Mode = None, object_list: List = None, output_filename: str = None) -> None:
        diagram_generator = self.diagram_generators[diag_name]
        output = "@startuml\n"
        output += diagram_generator.generate(mode, object_list)
        output += "@enduml"
        if not os.path.exists("results/"):
            os.makedirs("results")
        with open("results/output.txt", 'w+') as fp:
            fp.write(output)
        if output_filename is None:
            output_filename = diag_name + "_".join(obj_name for obj_name in object_list)
        output_filename = "results/" + output_filename
        self.server.processes_file(filename="results/output.txt", outfile=output_filename)
        os.remove("results/output.txt")

    def add_function(self, scope_name: str, function_name: str, function: Function) -> None:
        self._functions[scope_name + "&" + function_name] = function

    def get_function(self, scope_name: str, function_name: str) -> Function:
        return self._functions[scope_name + "&" + function_name]

    def _get_scope_if_exists(self, name: str):
        if "&" in name:
            return name.split("&")[0], name.split("&")[1]
        return None, name

    def get_object(self, name: str, current_scope_name: str) -> Object:
        scope_name, object_name = self._get_scope_if_exists(name)
        if scope_name is None:
            scope_name = current_scope_name

        if scope_name == "global":
            try:
                return self.global_objects[object_name]
            except KeyError:
                raise ObjectNotDeclaredException(name)
        else:
            return self.diagram_generators[scope_name].get_object(object_name)

    def get_objects(self, names: List[str], is_deep_copy: List[bool], current_scope_name: str) -> List[Object]:
        result = []
        for object_name, is_deep_copy in zip(names, is_deep_copy):
            obj = deepcopy(self.get_object(object_name, current_scope_name))
            if not is_deep_copy:
                obj.connections = {}
            result.append(obj)
        return result

    def debug(self):
        print(f"Global objects({len(self.global_objects)}):")
        print(f"Objects: {[arg.__str__() for arg in self.global_objects.values()]}")

        print()

        print(f"Diagram generators({len(self.diagram_generators)}): ")
        for diag_name, diag_gen in self.diagram_generators.items():
            print(f"Diagram generator name: {diag_name}")
            print(f"Objects: {[arg.__str__() for arg in diag_gen.objects]}")
            print()

        print(f"Function generators({len(self._functions)}): ")
        for fun_name, fun_gen in self._functions.items():
            print(f"Function generator name: {fun_name} arg count: {fun_gen.n_arguments} return count: {fun_gen.n_returns}")
            print(f"Fixed objects: {[arg.__str__() for arg in fun_gen.fixed_objects]}")
            print(f"Modifiable args: {fun_gen.modifiable_args}")
            print(f"Modifiable arg names: {fun_gen.modifiable_arg_names}")
            print(f"Return object names: {fun_gen.return_object_names}")
            print()
