from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.function import Function
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.register import Register, Scope, FunctionDescriptor
from compiler.utils.error_message import ErrorMessage


class IndexingdUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator, error: ErrorMessage):
        self.output_generator = output_generator
        self.register = register
        self.error = error

        self.current_scope_name = register.global_scope.name
        self.nested_function_counter = 0
        self.function_descriptors_to_verify = {}
        self.current_function = None

    def _enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()

    def _exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def _register_diagram_creation(self, ctx):
        if self.current_function is not None:
            self.error.errors.append(f"Cannot create diagram inside the function. Line: {ctx.stop.line}")
            return

        diag_name = ctx.NAME().getText()
        self.register.add_object_to_scope(diag_name, self.current_scope_name)
        self.register.scopes[diag_name] = Scope(diag_name, self.current_scope_name, [], {})
        self._enter_scope(ctx)

    def _add_enter_ctx_to_fun(self, ctx):
        if self.current_function is not None:
            self.current_function.add_enter_ctx(ctx)

    def _add_exit_ctx_to_fun(self, ctx):
        if self.current_function is not None:
            self.current_function.add_exit_ctx(ctx)

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._register_diagram_creation(ctx)

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_scope()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._register_diagram_creation(ctx)

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_scope()

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._register_diagram_creation(ctx)

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._exit_scope()

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.nested_function_counter += 1
        if self.current_function is not None:
            self.error.errors.append(f"Functions cannot be nested. Line: {ctx.stop.line}")
            return

        fun_name = ctx.NAME().getText()

        if ctx.arg_list(1):
            argument_names = [name.getText() for name in ctx.arg_list(0).NAME()]
            return_names = [name.getText() for name in ctx.arg_list(1).NAME()]
        else:
            argument_names = []
            return_names = [name.getText() for name in ctx.arg_list(0).NAME()]

        self.current_function = Function(fun_name, argument_names, return_names)

        function_descriptor = FunctionDescriptor(len(argument_names), len(return_names))

        if fun_name in self.function_descriptors_to_verify.keys():
            for function_tuple in self.function_descriptors_to_verify[fun_name]:
                function_descriptor_to_verify = function_tuple[0]
                line = function_tuple[1]
                if function_descriptor.n_returns != function_descriptor_to_verify.n_returns:
                    self.error.errors.append(f"Wrong number of returns. Expected: {function_descriptor.n_returns}. "
                                             f"Got: {function_descriptor_to_verify.n_returns}. Line: {line}")
                if function_descriptor.n_arguments != function_descriptor_to_verify.n_arguments:
                    self.error.errors.append(f"Incorrect number of attributes was passed to \"{fun_name}\" function."
                                             f" Expected: {function_descriptor.n_arguments}. Got: {function_descriptor_to_verify.n_arguments}."
                                             f" Line: {line}")
            self.function_descriptors_to_verify.pop(fun_name)

        fun_scope = Scope(fun_name, self.current_scope_name, [], {})
        if self.register.is_function_in_scope(fun_name, self.current_scope_name):
            raise Exception(f"Function {fun_name} is already declared in scope {self.current_scope_name}. Line {ctx.start.line}")
        self.register.add_function_to_scope(fun_name, function_descriptor, self.current_scope_name)
        self.register.scopes[fun_name] = fun_scope
        self._enter_scope(ctx)
        for name in argument_names:
            self.register.add_object_to_scope(name, self.current_scope_name)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        if ctx.arg_list(1):
            return_names = [name.getText() for name in ctx.arg_list(1).NAME()]
        else:
            return_names = [name.getText() for name in ctx.arg_list(0).NAME()]
        for return_name in return_names:
            if not self.register.is_object_in_scope(return_name, self.current_scope_name, with_outer=False):
                self.error.errors.append(f"Cannot return {return_name} object "
                                         f"because it is not declared in {self.current_scope_name} function")
        self.nested_function_counter -= 1
        if self.nested_function_counter == 0:
            self._exit_scope()

            self.output_generator.add_function(self.current_scope_name, self.current_function.name, self.current_function)
            self.current_function = None

    def enterAssignment(self, ctx: dUMLeParser.AssignmentContext):
        self._add_enter_ctx_to_fun(ctx)

        for name in ctx.arg_list().NAME():
            self.register.add_object_to_scope(name.getText(), self.current_scope_name)

        ret_arg_count = len(ctx.arg_list().NAME())
        if ctx.fun_call():
            fun_name = ctx.fun_call().name().getText()
            fun_arg_count = len(ctx.fun_call().arg_list_include_scope().arg_name())
            for arg_name in ctx.fun_call().arg_list_include_scope().arg_name():
                scope = self.current_scope_name
                if arg_name.name().SCOPE_NAME():
                    scope = arg_name.name().SCOPE_NAME().getText()[:-1]
                name = arg_name.name().NAME().getText()
                if not self.register.is_object_in_scope(name, scope, with_outer=False):
                    self.error.errors.append(f"Cannot call function {fun_name} with {name} argument "
                                             f"because it does not exist in given scope. Line {ctx.start.line}")
            fun_descriptor = self.register.get_function_descriptor_in_scope(fun_name, self.current_scope_name)

            if fun_descriptor is None:
                fun_descriptor = FunctionDescriptor(fun_arg_count, ret_arg_count)
                if fun_name not in self.function_descriptors_to_verify.keys():
                    self.function_descriptors_to_verify[fun_name] = [(fun_descriptor, ctx.stop.line)]
                else:
                    self.function_descriptors_to_verify[fun_name].append((fun_descriptor, ctx.stop.line))
            else:
                if fun_descriptor.n_returns != ret_arg_count:
                    self.error.errors.append(f"Wrong number of returns. Expected: {fun_descriptor.n_returns}. "
                                             f"Got: {ret_arg_count}. Line: {ctx.stop.line}")
                if fun_descriptor.n_arguments != fun_arg_count:
                    self.error.errors.append(f"Incorrect number of attributes was passed to \"{fun_name}\" function."
                                             f" Expected: {fun_descriptor.n_arguments}. Got: {fun_arg_count}."
                                             f" Line: {ctx.stop.line}")
        elif ctx.arg_list_include_scope():
            n_values_to_assign = len(ctx.arg_list_include_scope().arg_name())
            if n_values_to_assign != ret_arg_count:
                self.error.errors.append(f"Cannot unpack {n_values_to_assign} objects to {ret_arg_count} objects. "
                                         f"Line: {ctx.stop.line}")
        else:
            if ret_arg_count > 1:
                self.error.errors.append(f"Cannot unpack list to {ret_arg_count} objects. Line: {ctx.stop.line}")

    def exitAssignment(self, ctx: dUMLeParser.AssignmentContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        self._add_enter_ctx_to_fun(ctx)
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def exitActor(self, ctx: dUMLeParser.ActorContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        self._add_enter_ctx_to_fun(ctx)
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def exitUse_case(self, ctx: dUMLeParser.Use_caseContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        self._add_enter_ctx_to_fun(ctx)
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def exitBlock(self, ctx: dUMLeParser.BlockContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        self._add_enter_ctx_to_fun(ctx)
        object_name = ctx.NAME().getText()
        if not self.register.is_object_in_scope(object_name, self.current_scope_name, with_outer=False):
            self.error.errors.append(f"Cannot add note to {object_name} object "
                                     f"because it is not present in {self.current_scope_name} scope. Line {ctx.start.line}")

    def exitNote(self, ctx: dUMLeParser.NoteContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        source, destination = ctx.name(0).getText(), ctx.name(1).getText()
        if not self.register.is_object_in_scope(source, self.current_scope_name, with_outer=False):
            self.error.errors.append(f"No {source} object in {self.current_scope_name} scope. Line {ctx.start.line}")
        if not self.register.is_object_in_scope(destination, self.current_scope_name, with_outer=False):
            self.error.errors.append(f"No {destination} object in {self.current_scope_name} scope. Line {ctx.start.line}")
        self._add_enter_ctx_to_fun(ctx)

    def exitConnection(self, ctx: dUMLeParser.ConnectionContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        self._add_enter_ctx_to_fun(ctx)
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def exitTheme(self, ctx: dUMLeParser.ThemeContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        self._add_enter_ctx_to_fun(ctx)
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def exitPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        self._add_enter_ctx_to_fun(ctx)
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def exitClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        self._add_exit_ctx_to_fun(ctx)

    def exitProgram(self, ctx: dUMLeParser.ProgramContext):
        for function_name, function_tuples in self.function_descriptors_to_verify.items():
            for function_tuple in function_tuples:
                self.error.errors.append(f"Did not find declaration of \"{function_name}\" function. Line: {function_tuple[1]}")
