from enum import Enum, auto
from typing import List
from antlr4 import ParseTreeWalker

from compiler.utils.exceptions import RecursionDepthException
from compiler.utils.object import Object


class RuleType(Enum):
    ENTER = auto()
    EXIT = auto()


class Function:
    def __init__(self, name: str, argument_names: List[str], return_names: List[str]):
        self.name = name  # the name of the function
        self.ctx = []  # the list that contains ctx objects that have to be called sequentially
        self.argument_names = argument_names
        self.return_names = return_names

        # flags for recursion
        self.current_recursion_depth_count = 0
        self.max_recursion_depth_count = 0  # this value should be set before calling the method call
        self.was_max_reached = False

    def set_max_depth(self, max_depth: int):
        if self.current_recursion_depth_count > 0:
            return
        else:
            self.max_recursion_depth_count = max_depth

    def activate(self):
        if self.was_max_reached:
            raise RecursionDepthException(self.max_recursion_depth_count)

        self.current_recursion_depth_count += 1
        if self.max_recursion_depth_count <= self.current_recursion_depth_count:
            self.was_max_reached = True

    def release(self):
        self.current_recursion_depth_count -= 1
        if self.current_recursion_depth_count == 0:
            self.was_max_reached = False

    def call(self, output_generator, register, parameters: List[Object], returned_object_names: List[str], scope_name: str) -> List:
        # changing name of the parameters
        parameters = Object.change_names(parameters, self.argument_names)

        # creating walker for the function
        walker = ParseTreeWalker()

        # creating new listener for the function
        from compiler.ContentdUMLeListener import ContentdUMLeListener
        listener = ContentdUMLeListener(register, output_generator)
        listener.set_function_listener(parameters, scope_name, self.name)

        # executing function code
        for single_ctx_tuple in self.ctx:
            if single_ctx_tuple[0] == RuleType.ENTER:
                walker.enterRule(listener, single_ctx_tuple[1])
            elif single_ctx_tuple[0] == RuleType.EXIT:
                walker.exitRule(listener, single_ctx_tuple[1])

        # renaming result and returning proper objects
        returned_objects = []
        for returned_object in listener.created_objects:
            if returned_object.name in self.return_names:
                returned_objects.append(returned_object)

        return Object.change_names(returned_objects, returned_object_names)

    def add_enter_ctx(self, enter_rule):
        self.ctx.append((RuleType.ENTER, enter_rule))

    def add_exit_ctx(self, exit_rule):
        self.ctx.append((RuleType.EXIT, exit_rule))
