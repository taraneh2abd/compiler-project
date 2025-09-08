from enum import Enum, auto
from copy import deepcopy
from typing import List
from plantuml import PlantUML
import os
import re

from compiler.utils.exceptions import ObjectNotDeclaredException
from compiler.utils.function import Function
from compiler.utils.object import Object


class Mode(Enum):
    """doc for Mode"""
    ALL = auto()
    BRIEF = auto()


class OutputGenerator:
    """docs for OutputGenerator"""

    def __init__(self):
        self.server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        self.global_objects = {}
        self.diagram_generators = {}
        self._functions = {}
        self.generated_python_code = ""  # نگهداری کل کد پایتون

    def generate(self, diag_name: str, mode: Mode = None, object_list: List = None, output_filename: str = None) -> None:
        diagram_generator = self.diagram_generators[diag_name]
        output = "@startuml\n"
        output += diagram_generator.generate(mode, object_list)
        output += "@enduml"
        print(output)

        if not os.path.exists("results/"):
            os.makedirs("results")

        # نوشتن موقت فایل plantuml
        tmp_file = "results/output.txt"
        with open(tmp_file, 'w+', encoding='utf-8') as fp:
            fp.write(output)

        if output_filename is None:
            output_filename = diag_name + "_".join(obj_name for obj_name in object_list)
        output_path = "results/" + output_filename

        # generate image
        self.server.processes_file(filename=tmp_file, outfile=output_path)

        # generate Python code
        py_code = self._generate_python_from_plantuml(output)

        if py_code.strip():  # فقط اگر کد پایتون تولید شده غیرخالی بود
            self.generated_python_code += py_code + "\n\n"
            py_output_file = os.path.join("results", "python_code.py")
            with open(py_output_file, 'w+', encoding='utf-8') as fp:
                fp.write(self.generated_python_code)

        # حذف فایل موقت
        os.remove(tmp_file)

    def _generate_python_from_plantuml(self, plantuml_code: str) -> str:
        """Convert PlantUML class diagram subset to valid Python classes."""
        class_re = re.compile(r'class\s+(\w+)\s*(\{([^}]*)\})?', re.MULTILINE)
        inherit_re = re.compile(r'(\w+)\s*<\|\-\-\s*(\w+)')

        def parse_body(body):
            fields, methods = [], []
            if not body:
                return fields, methods
            for line in body.splitlines():
                line = line.strip()
                if not line:
                    continue
                if '(' in line and ')' in line:
                    methods.append(line)
                else:
                    fields.append(line)
            return fields, methods

        classes = {}
        for m in class_re.finditer(plantuml_code):
            name = m.group(1)
            body = m.group(3) or ""
            fields, methods = parse_body(body)
            classes[name] = {"fields": fields, "methods": methods, "bases": []}

        for m in inherit_re.finditer(plantuml_code):
            parent, child = m.group(1), m.group(2)
            if child in classes:
                classes[child]["bases"].append(parent)
            else:
                classes.setdefault(child, {"fields": [], "methods": [], "bases": [parent]})
            classes.setdefault(parent, {"fields": [], "methods": [], "bases": []})

        py_lines = []
        for name, info in classes.items():
            bases = ", ".join(info["bases"]) if info["bases"] else "object"
            py_lines.append(f"class {name}({bases}):")

            if info["fields"]:
                params = []
                assigns = []
                for f in info["fields"]:
                    # پاک کردن علامت‌های UML مثل + - # و کاراکترهای غیرمجاز
                    fname = re.sub(r'[^0-9a-zA-Z_]', '', f.split(':')[0].strip())
                    params.append(f"{fname}=None")
                    assigns.append(f"        self.{fname} = {fname}")
                py_lines.append(f"    def __init__(self, {', '.join(params)}):")
                if info["bases"] and "object" not in info["bases"]:
                    py_lines.append("        super().__init__()")
                py_lines += assigns if assigns else ["        pass"]
            elif info["methods"]:
                py_lines.append("    def __init__(self):")
                if info["bases"] and "object" not in info["bases"]:
                    py_lines.append("        super().__init__()")
                py_lines.append("        pass")
            else:
                py_lines.append("    pass")

            for m in info["methods"]:
                # پاک کردن علامت‌های UML و ساخت اسم معتبر پایتون
                mname = re.sub(r'[^0-9a-zA-Z_]', '', m.split('(')[0].strip())
                args = m[m.find('(')+1 : m.rfind(')')].strip()
                arglist = "self" if args == "" else "self, " + args
                py_lines.append(f"    def {mname}({arglist}):")
                py_lines.append("        pass")
            py_lines.append("")

        return "\n".join(py_lines)

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
