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
        self.name = name
        self.ctx = []
        self.argument_names = argument_names
        self.return_names = return_names

        self.current_recursion_depth_count = 0
        self.max_recursion_depth_count = 0
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
        parameters = Object.change_names(parameters, self.argument_names)

        walker = ParseTreeWalker()

        from compiler.ContentdUMLeListener import ContentdUMLeListener
        listener = ContentdUMLeListener(register, output_generator)
        listener.set_function_listener(parameters, scope_name, self.name)

        for single_ctx_tuple in self.ctx:
            if single_ctx_tuple[0] == RuleType.ENTER:
                walker.enterRule(listener, single_ctx_tuple[1])
            elif single_ctx_tuple[0] == RuleType.EXIT:
                walker.exitRule(listener, single_ctx_tuple[1])

        returned_objects = []
        for returned_object in listener.created_objects:
            if returned_object.name in self.return_names:
                returned_objects.append(returned_object)

        return Object.change_names(returned_objects, returned_object_names)

    def add_enter_ctx(self, enter_rule):
        self.ctx.append((RuleType.ENTER, enter_rule))

    def add_exit_ctx(self, exit_rule):
        self.ctx.append((RuleType.EXIT, exit_rule))
