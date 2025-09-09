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
        self.generated_python_code = ""
        self.generated_cpp_code = ""

    def generate(self, diag_name: str, mode: Mode = None, object_list: List = None, output_filename: str = None) -> None:
        diagram_generator = self.diagram_generators[diag_name]
        output = "@startuml\n"
        output += diagram_generator.generate(mode, object_list)
        output += "@enduml"
        print(output)

        if not os.path.exists("results/"):
            os.makedirs("results")

        tmp_file = "results/output.txt"
        with open(tmp_file, 'w+', encoding='utf-8') as fp:
            fp.write(output)

        if output_filename is None:
            output_filename = diag_name + "_".join(obj_name for obj_name in object_list)
        output_path = "results/" + output_filename

        self.server.processes_file(filename=tmp_file, outfile=output_path)

        py_code = self._generate_python_from_plantuml(output)
        if py_code.strip():
            self.generated_python_code += py_code + "\n\n"
            py_output_file = os.path.join("results", "python_code.py")
            with open(py_output_file, 'w+', encoding='utf-8') as fp:
                fp.write(self.generated_python_code)

        cpp_code = self._generate_cpp_from_plantuml(output)
        if cpp_code.strip():
            self.generated_cpp_code += cpp_code + "\n\n"
            cpp_output_file = os.path.join("results", "cpp_code.cpp")
            with open(cpp_output_file, 'w+', encoding='utf-8') as fp:
                fp.write(self.generated_cpp_code)

        os.remove(tmp_file)

    def _generate_python_from_plantuml(self, plantuml_code: str) -> str:
        """Convert PlantUML class diagram subset to valid Python classes with relationships."""
        class_re = re.compile(r'class\s+(\w+)\s*(\{([^}]*)\})?', re.MULTILINE)
        inherit_re = re.compile(r'(\w+)\s*<\|--\s*(\w+)')
        assoc_re = re.compile(r'(\w+)\s+([o*]?)\-?\-?[->]?\s*(\w+)\s*(:\s*([^"\n]+))?', re.MULTILINE)

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
        associations = []

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

        for m in assoc_re.finditer(plantuml_code):
            source = m.group(1)
            rel_type = m.group(2) or ''
            target = m.group(3)
            label = m.group(5)
            associations.append({'source': source, 'target': target, 'type': rel_type, 'label': label})

        py_lines = []

        for name, info in classes.items():
            bases = ", ".join(info["bases"]) if info["bases"] else "object"
            py_lines.append(f"class {name}({bases}):")

            class_associations = [a for a in associations if a['source'] == name]

            init_params = []
            init_assigns = []

            for f in info["fields"]:
                fname = re.sub(r'[^0-9a-zA-Z_]', '', f.split(':')[0].strip())
                init_params.append(f"{fname}=None")
                init_assigns.append(f"        self.{fname} = {fname}")

            for assoc in class_associations:
                target = assoc['target']
                if assoc['type'] in ['o', '*']:
                    init_assigns.append(f"        self._{target.lower()}_objects = []  # {assoc['type']}-- {target}")
                else:
                    init_params.append(f"{target.lower()}=None")
                    init_assigns.append(f"        self._{target.lower()} = {target.lower()}  # -- {target}")

            if init_params or class_associations:
                param_str = ", ".join(init_params)
                py_lines.append(f"    def __init__(self{', ' + param_str if param_str else ''}):")
                if info["bases"] and "object" not in info["bases"]:
                    py_lines.append("        super().__init__()")
                py_lines.extend(init_assigns if init_assigns else ["        pass"])
            else:
                py_lines.append("    def __init__(self):")
                if info["bases"] and "object" not in info["bases"]:
                    py_lines.append("        super().__init__()")
                py_lines.append("        pass")

            for m in info["methods"]:
                mname = re.sub(r'[^0-9a-zA-Z_]', '', m.split('(')[0].strip())
                args = m[m.find('(') + 1: m.rfind(')')].strip()
                arglist = "self" if args == "" else "self, " + args
                py_lines.append(f"    def {mname}({arglist}):")
                py_lines.append("        pass")

            for assoc in class_associations:
                target = assoc['target']
                target_var = target.lower()

                if assoc['type'] in ['o', '*']:
                    py_lines.append(f"    def add_{target_var}(self, {target_var}_object):")
                    py_lines.append(f"        \"\"\"Add {target} to {name}'s collection.\"\"\"")
                    py_lines.append(f"        self._{target_var}_objects.append({target_var}_object)")
                    py_lines.append("")
                    py_lines.append(f"    def remove_{target_var}(self, {target_var}_object):")
                    py_lines.append(f"        \"\"\"Remove {target} from {name}'s collection.\"\"\"")
                    py_lines.append(f"        self._{target_var}_objects.remove({target_var}_object)")
                    py_lines.append("")
                    py_lines.append(f"    def get_{target_var}_list(self):")
                    py_lines.append(f"        \"\"\"Get all {target} objects.\"\"\"")
                    py_lines.append(f"        return self._{target_var}_objects")
                    py_lines.append("")
                    py_lines.append(f"    def clear_{target_var}_list(self):")
                    py_lines.append(f"        \"\"\"Clear all {target} objects.\"\"\"")
                    py_lines.append(f"        self._{target_var}_objects.clear()")
                else:
                    py_lines.append(f"    def set_{target_var}(self, {target_var}_object):")
                    py_lines.append(f"        \"\"\"Set associated {target}.\"\"\"")
                    py_lines.append(f"        self._{target_var} = {target_var}_object")
                    py_lines.append("")
                    py_lines.append(f"    def get_{target_var}(self):")
                    py_lines.append(f"        \"\"\"Get associated {target}.\"\"\"")
                    py_lines.append(f"        return self._{target_var}")
                    py_lines.append("")
                    py_lines.append(f"    def clear_{target_var}(self):")
                    py_lines.append(f"        \"\"\"Clear associated {target}.\"\"\"")
                    py_lines.append(f"        self._{target_var} = None")

            py_lines.append("")

        return "\n".join(py_lines)

    def _map_type_to_cpp(self, type_str: str) -> str:
        """Map simple UML/PlantUML type names to C++ types."""
        if not type_str:
            return "std::string"
        t = type_str.strip().lower()
        if t in ("int", "integer", "long", "short"):
            return "int"
        if t in ("float", "double", "real"):
            return "double"
        if t in ("bool", "boolean"):
            return "bool"
        if t in ("str", "string", "std::string", "name"):
            return "std::string"
        return "std::string"

    def _parse_field_and_type(self, field_text: str):
        """Return (name, type_str) by parsing 'name: type' or just 'name'."""
        parts = field_text.split(':', 1)
        name = parts[0].strip()
        type_str = parts[1].strip() if len(parts) > 1 else ""
        name = re.sub(r'[^0-9a-zA-Z_]', '', name)
        return name, type_str

    def _generate_cpp_from_plantuml(self, plantuml_code: str) -> str:
        """Convert PlantUML class diagram subset to reasonable C++ class definitions."""
        class_re = re.compile(r'class\s+(\w+)\s*(\{([^}]*)\})?', re.MULTILINE)
        inherit_re = re.compile(r'(\w+)\s*<\|--\s*(\w+)')
        assoc_re = re.compile(r'(\w+)\s+([o*]?)\-?\-?[->]?\s*(\w+)\s*(:\s*([^"\n]+))?', re.MULTILINE)

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
        associations = []

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

        for m in assoc_re.finditer(plantuml_code):
            source = m.group(1)
            rel_type = m.group(2) or ''
            target = m.group(3)
            label = m.group(5)
            associations.append({'source': source, 'target': target, 'type': rel_type, 'label': label})

        cpp_lines = []
        cpp_lines.append('#include <string>')
        cpp_lines.append('#include <vector>')
        cpp_lines.append('')
        for cname in classes.keys():
            cpp_lines.append(f"class {cname};")
        cpp_lines.append('')
        cpp_lines.append("using std::string;")
        cpp_lines.append("using std::vector;")
        cpp_lines.append("")

        for name, info in classes.items():
            bases = ", ".join(f"public {b}" for b in info["bases"]) if info["bases"] else ""
            header = f"class {name}" + (f" : {bases}" if bases else "") + " {"
            cpp_lines.append(header)
            cpp_lines.append("public:")

            ctor_params = []
            ctor_inits = []
            member_lines = []

            for f in info["fields"]:
                fname, ftype = self._parse_field_and_type(f)
                cpp_type = self._map_type_to_cpp(ftype)
                member_lines.append(f"    {cpp_type} {fname};")
                ctor_params.append((cpp_type, fname))
                ctor_inits.append(f"{fname}({fname})")

            class_associations = [a for a in associations if a['source'] == name]
            for assoc in class_associations:
                target = assoc['target']
                if assoc['type'] in ['o', '*']:
                    member_lines.append(f"    vector<{target}*> {target.lower()}_list;")
                else:
                    member_lines.append(f"    {target}* {target.lower()} = nullptr;")

            if ctor_params or info["bases"]:
                param_str = ", ".join(f"{t} {n}" for t, n in ctor_params)
                cpp_lines.append(f"    {name}({param_str})")
                init_list = []
                if info["bases"]:
                    for b in info["bases"]:
                        init_list.append(f"{b}()")
                init_list.extend(ctor_inits)
                if init_list:
                    cpp_lines.append("        : " + ", ".join(init_list))
                cpp_lines.append("    {")
                cpp_lines.append("        // constructor body")
                cpp_lines.append("    }")
            else:
                cpp_lines.append(f"    {name}() {{}}")

            for m in info["methods"]:
                mname = re.sub(r'[^0-9a-zA-Z_]', '', m.split('(')[0].strip())
                args = m[m.find('(') + 1: m.rfind(')')].strip()
                cpp_args = []
                if args:
                    for arg in [a.strip() for a in args.split(',') if a.strip()]:
                        if ':' in arg:
                            aname, atype = [x.strip() for x in arg.split(':', 1)]
                            cpp_type = self._map_type_to_cpp(atype)
                            cpp_args.append(f"{cpp_type} {aname}")
                        else:
                            cpp_args.append(f"std::string {re.sub(r'[^0-9a-zA-Z_]', '', arg)}")
                cpp_lines.append(f"    void {mname}({', '.join(cpp_args)}) {{}}")

            for assoc in class_associations:
                target = assoc['target']
                tvar = target.lower()
                if assoc['type'] in ['o', '*']:
                    cpp_lines.append(f"    void add_{tvar}({target}* obj) {{ {tvar}_list.push_back(obj); }}")
                    cpp_lines.append(f"    void remove_{tvar}({target}* obj) {{ /* remove from vector - implement */ }}")
                    cpp_lines.append(f"    const vector<{target}*>& get_{tvar}_list() const {{ return {tvar}_list; }}")
                else:
                    cpp_lines.append(f"    void set_{tvar}({target}* obj) {{ {tvar} = obj; }}")
                    cpp_lines.append(f"    {target}* get_{tvar}() const {{ return {tvar}; }}")

            if member_lines:
                cpp_lines.append("")
                cpp_lines.append("private:")
                for ml in member_lines:
                    cpp_lines.append(ml)

            cpp_lines.append("};")
            cpp_lines.append("")

        return "\n".join(cpp_lines)

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
