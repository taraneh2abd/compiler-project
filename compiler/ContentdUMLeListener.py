from copy import deepcopy
from enum import Enum, auto
from typing import Tuple, List

from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.exceptions import RecursionDepthException, ObjectNotDeclaredException, WrongDiagramTypeException
from compiler.utils.register import Register
from compiler.utils.object import Object, Actor, UseCase, Class, Connection, Block, Note, Package
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.diagram_generator import DiagGenerator, DiagType
from compiler.utils.object import Theme


class ContentdUMLeListenerMode(Enum):
    NOT_ACTIVE = auto()
    FUNCTION = auto()
    MAIN = auto()


class ContentdUMLeListener(dUMLeListener):
    shared_themes = {}
    def __init__(self, register: Register, output_generator: OutputGenerator):
        self.output_generator = output_generator
        self.register = register
        self.current_scope_name = None
        self.current_function_name = None

        self.is_in_diagram = None
        self.is_in_function = None
        self.is_in_global_scope = None
        self.current_diagram_type = None
        self.current_diagram_name = None

        self.created_objects = None

        self.mode = ContentdUMLeListenerMode.NOT_ACTIVE
    
    def _enter_diag(self, ctx, diag_type: DiagType):
        self._enter_scope(ctx)
        self.is_in_diagram = True
        self.current_diagram_name = ctx.NAME().getText()
        self.current_diagram_type = diag_type
        self.output_generator.diagram_generators[self.current_diagram_name] = DiagGenerator(diag_type)

    def _exit_diag(self):
        self.current_diagram_name = ""
        self.current_diagram_type = None
        self.is_in_diagram = False
        self._exit_scope()

    def _enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()
        if self.mode is ContentdUMLeListenerMode.MAIN and self.current_scope_name != 'global':
            self.is_in_global_scope = False

    def _exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)
        if self.mode is ContentdUMLeListenerMode.MAIN and self.current_scope_name == 'global':
            self.is_in_global_scope = True

    def _get_scope_if_exists(self, name: str) -> Tuple[str | None, str]:
        if "&" in name:
            return name.split("&")[0], name.split("&")[1]
        return None, name

    def _add_object(self, object: Object):
        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                self.output_generator.diagram_generators[self.current_diagram_name].add_object(object)
            elif not self.is_in_function:
                self.output_generator.global_objects[object.name] = object
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            self._add_to_function_objects(object)
        else:
            raise Exception("Content listener is not activated. Specify the source of the code")

    def _add_to_function_objects(self, object_to_add: Object):
        for existing_object in self.created_objects:
            if object_to_add.name == existing_object.name:
                self.created_objects.remove(existing_object)
                break
        self.created_objects.append(object_to_add)

    def set_global_listener(self):
        if self.mode != ContentdUMLeListenerMode.NOT_ACTIVE:
            raise Exception("Cannot activate content listener. Content listener is already activated")

        self.current_scope_name = self.register.global_scope.name
        self.is_in_diagram = False
        self.is_in_global_scope = True
        self.is_in_function = False
        self.current_diagram_type = None
        self.current_function_name = ""
        self.current_diagram_name = ""
        self.mode = ContentdUMLeListenerMode.MAIN

    def set_function_listener(self, parameters: List[Object], scope_name: str, function_name: str):
        if self.mode != ContentdUMLeListenerMode.NOT_ACTIVE:
            raise Exception("Cannot activate content listener. Content listener is already activated")

        self.created_objects = parameters
        self.current_scope_name = scope_name
        self.current_function_name = function_name
        self.mode = ContentdUMLeListenerMode.FUNCTION

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self._enter_scope(ctx)
        self.is_in_function = True
        self.current_function_name = ctx.NAME().getText()

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.current_function_name = ""
        self._exit_scope()

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._enter_diag(ctx, DiagType.CLASS)

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_diag()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._enter_diag(ctx, DiagType.USE_CASE)

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_diag()

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._enter_diag(ctx, DiagType.SEQUENCE)

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._exit_diag()

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.USE_CASE:
            raise Exception(f"You cannot define actor in {self.current_diagram_type}. Line: {ctx.stop.line}")
        actor = Actor(ctx)
        self._add_object(actor)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.USE_CASE:
            raise Exception(f"You cannot define use case in {self.current_diagram_type}. Line: {ctx.stop.line}")
        use_case = UseCase(ctx)
        self._add_object(use_case)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.SEQUENCE:
            raise Exception(f"You cannot define block in {self.current_diagram_type}. Line: {ctx.stop.line}")
        block = Block(ctx)
        self._add_object(block)

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.CLASS:
            raise Exception(f"You cannot define class in {self.current_diagram_type}. Line: {ctx.stop.line}")
        class_object = Class(ctx)
        self._add_object(class_object)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        note = Note(ctx)

        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                for object in self.output_generator.diagram_generators[self.current_diagram_name].objects:
                    if object.name == note.object_name:
                        object.add_note(note)
                        break
            elif not self.is_in_function:
                self.output_generator.global_objects[note.object_name].add_note(note)
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            for object in self.created_objects:
                if object.name == note.object_name:
                    object.add_note(note)
                    break

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        connection = Connection(ctx)

        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                for object in self.output_generator.diagram_generators[self.current_diagram_name].objects:
                    if object.name == connection.source_object_name:
                        object.add_connection(connection)
                        break
                if self.current_diagram_type == DiagType.SEQUENCE:
                    self.output_generator.diagram_generators[self.current_diagram_name].sequences.append(connection)
            elif not self.is_in_function:
                self.output_generator.global_objects[connection.source_object_name].add_connection(connection)
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            for object in self.created_objects:
                if object.name == connection.source_object_name:
                    object.add_connection(connection)
                    break

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        object_names = [name.getText() for name in ctx.NAME()]
        object_names.pop(0)
        is_deep_copy = [True for _ in enumerate(object_names)]
        objects = []
        try:
            if self.mode is ContentdUMLeListenerMode.MAIN:
                if not self.is_in_function:
                    objects = self._get_arg_copy_from_diagram(object_names, is_deep_copy)
            elif self.mode is ContentdUMLeListenerMode.FUNCTION:
                objects = self._get_arg_copy_from_function(object_names, is_deep_copy)
            else:
                raise Exception("Wrong mode. Cannot call the function")
        except ObjectNotDeclaredException as e:
            raise Exception(f"{e} Line: {ctx.stop.line}")

        try:
            package = Package(ctx, objects)
        except WrongDiagramTypeException as e:
            raise Exception(f"{e} Line {ctx.stop.line}")

        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                self.output_generator.diagram_generators[self.current_diagram_name].add_object(package)
                for o in package.objects:
                    objects = self.output_generator.diagram_generators[self.current_diagram_name].objects
                    for existing_object in objects:
                        if existing_object.name == o.name:
                            objects.remove(existing_object)
                            break
            elif not self.is_in_function:
                self.output_generator.global_objects[package.name] = package
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            self._add_to_function_objects(package)
            for o in package.objects:
                for existing_object in self.created_objects:
                    if existing_object.name == o.name:
                        self.created_objects.remove(existing_object)
                        break


    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        theme = Theme(ctx)
        ContentdUMLeListener.shared_themes[theme.name] = theme
        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                self.output_generator.diagram_generators[self.current_diagram_name].add_object(theme)
            elif not self.is_in_function:
                self.output_generator.global_objects[theme.name] = theme
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            self._add_to_function_objects(theme)
    def enterUseTheme(self, ctx: dUMLeParser.UseThemeContext):
        theme_name = ctx.NAME().getText()
        
        if theme_name not in ContentdUMLeListener.shared_themes:
            raise Exception(f"Theme {theme_name} not declared. Line: {ctx.start.line}")
        
        theme = ContentdUMLeListener.shared_themes[theme_name]
        
        self.active_theme = theme
        
        if self.is_in_diagram:
            self.output_generator.diagram_generators[self.current_diagram_name].add_object(theme)


    def _get_arg_copy_from_diagram(self, arg_names: List[str], is_deep_copy: List[bool]):
        return self.output_generator.get_objects(arg_names, is_deep_copy, self.current_scope_name)

    def _get_arg_copy_from_function(self, arg_names: List[str], is_deep_copy: List[bool]):
        arg_list = []
        for object_name, is_deep_copy in zip(arg_names, is_deep_copy):
            found_object = None
            for function_object in self.created_objects:
                if function_object.name == object_name:
                    found_object = function_object
                    break

            if found_object is None:
                raise Exception(f"Object {object_name} was not declared in this scope")

            copied_object = deepcopy(found_object)
            if not is_deep_copy:
                copied_object.connections = {}
            arg_list.append(copied_object)

        return arg_list

    def _call_function(self, fun_ctx, returned_arg_names: List[str], line):
        arg_names = [arg_name.name().getText() for arg_name in fun_ctx.arg_list_include_scope().arg_name()]
        is_deep_copy = [True if arg_name.DEEP_COPY() else False for arg_name in
                        fun_ctx.arg_list_include_scope().arg_name()]

        scope_name, fun_name = self._get_scope_if_exists(fun_ctx.name().getText())
        if scope_name is None:
            scope_name = self.register.get_nearest_scope_name(self.current_scope_name, fun_name)

        if self.mode is ContentdUMLeListenerMode.MAIN:
            arg_list = self._get_arg_copy_from_diagram(arg_names, is_deep_copy)
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            arg_list = self._get_arg_copy_from_function(arg_names, is_deep_copy)
        else:
            raise Exception("Wrong mode. Cannot call the function")

        function = self.output_generator.get_function(scope_name, fun_name)
        max_depth = 1
        if fun_ctx.NUMBER():
            max_depth = int(fun_ctx.NUMBER().getText())
        function.set_max_depth(max_depth)
        function.activate()
        returned_objects = function.call(self.output_generator, self.register, arg_list, returned_arg_names, self.current_scope_name)
        function.release()

        if self.is_in_diagram:
            allowed_types = self.output_generator.diagram_generators[self.current_diagram_name].available_object_types
            for returned_object in returned_objects:
                if type(returned_object) not in allowed_types:
                    raise Exception(f"You cannot create {returned_object.__class__.__name__} object in {self.current_diagram_type}. Line {fun_ctx.stop.line}")

        return returned_objects

    def enterAssignment(self, ctx: dUMLeParser.AssignmentContext):
        returned_arg_names = [name.getText() for name in ctx.arg_list().NAME()]
        returned_objects = []

        if ctx.list_declaration():
            raise Exception(f"List declaration not supported. Line: {ctx.stop.line}")
        elif ctx.fun_call():
            try:
                if self.mode is ContentdUMLeListenerMode.MAIN and self.is_in_function:
                    return
                returned_objects = self._call_function(ctx.fun_call(), returned_arg_names, ctx.stop.line)
            except RecursionDepthException:
                return
        elif ctx.arg_list_include_scope():
            arg_names = [arg_name.name().getText() for arg_name in ctx.arg_list_include_scope().arg_name()]
            is_deep_copy = [True if arg_name.DEEP_COPY() else False for arg_name in
                            ctx.arg_list_include_scope().arg_name()]

            if self.mode is ContentdUMLeListenerMode.MAIN:
                arg_list = self._get_arg_copy_from_diagram(arg_names, is_deep_copy)
            elif self.mode is ContentdUMLeListenerMode.FUNCTION:
                arg_list = self._get_arg_copy_from_function(arg_names, is_deep_copy)
            else:
                raise Exception("Wrong mode. Cannot call the function")

            returned_objects = Object.change_names(arg_list, returned_arg_names)

        if self.mode is ContentdUMLeListenerMode.MAIN:
            for object in returned_objects:
                if self.is_in_diagram:
                    if object.is_package and object.type != self.current_diagram_type:
                        raise Exception(f"You cannot add package of type {object.type} to {self.current_diagram_type}")
                    self.output_generator.diagram_generators[self.current_diagram_name].add_object(object)
                elif not self.is_in_function:
                    self.output_generator.global_objects[object.name] = object
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            for object in returned_objects:
                self._add_to_function_objects(object)
        else:
            raise Exception("Wrong mode. Cannot call the function")

    def enterExecution(self, ctx: dUMLeParser.ExecutionContext):
        if self.is_in_function:
            raise Exception(f"Cannot execute diagram inside the function. Line: {ctx.stop.line}")

        if not self.is_in_diagram and not self.is_in_global_scope:
            raise Exception(f"Exec can only be called in global scope or in diagram. Line: {ctx.stop.line}")

        if not self.is_in_diagram and not ctx.NAME(0):
            raise Exception(f"Diagram name is required in global execution. "
                            f"Please provide the name of the diagram that you want to execute. "
                            f" Line: {ctx.stop.line}")

        diag_name = self.current_diagram_name
        file_name = self.current_diagram_name + ".png"
        mode = None
        object_list = None

        if ctx.NAME(0):
            diag_name = ctx.NAME(0).getText()

        if ctx.TEXT():
            file_name = ctx.TEXT().getText()[1:-1]
            if file_name[-4:] != ".png":
                raise Exception(f"The only supported extension is png. Please provide the png file. "
                                f"Line: {ctx.stop.line}")

        if ctx.MODE():
            mode = ctx.MODE().getText()

        if ctx.list_declaration():
            object_list = [name.getText() for name in ctx.list_declaration().name()]
        elif ctx.list_access():
            raise Exception(f"List access is not supported. Line: {ctx.stop.line}")
        elif ctx.NAME(1):
            raise Exception(f"List name is not supported. Line: {ctx.stop.line}")

        self.output_generator.generate(diag_name, mode, object_list, file_name)
