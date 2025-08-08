# Generated from /Users/hania/Desktop/komp22-dumle/grammar/dUMLe.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .dUMLeParser import dUMLeParser
else:
    from dUMLeParser import dUMLeParser

# This class defines a complete listener for a parse tree produced by dUMLeParser.
class dUMLeListener(ParseTreeListener):

    # Enter a parse tree produced by dUMLeParser#program.
    def enterProgram(self, ctx:dUMLeParser.ProgramContext):
        pass

    # Exit a parse tree produced by dUMLeParser#program.
    def exitProgram(self, ctx:dUMLeParser.ProgramContext):
        pass


    # Enter a parse tree produced by dUMLeParser#diagcreation.
    def enterDiagcreation(self, ctx:dUMLeParser.DiagcreationContext):
        pass

    # Exit a parse tree produced by dUMLeParser#diagcreation.
    def exitDiagcreation(self, ctx:dUMLeParser.DiagcreationContext):
        pass


    # Enter a parse tree produced by dUMLeParser#class_diagram.
    def enterClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        pass

    # Exit a parse tree produced by dUMLeParser#class_diagram.
    def exitClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        pass


    # Enter a parse tree produced by dUMLeParser#seq_diagram.
    def enterSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        pass

    # Exit a parse tree produced by dUMLeParser#seq_diagram.
    def exitSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        pass


    # Enter a parse tree produced by dUMLeParser#use_case_diagram.
    def enterUse_case_diagram(self, ctx:dUMLeParser.Use_case_diagramContext):
        pass

    # Exit a parse tree produced by dUMLeParser#use_case_diagram.
    def exitUse_case_diagram(self, ctx:dUMLeParser.Use_case_diagramContext):
        pass


    # Enter a parse tree produced by dUMLeParser#instruction.
    def enterInstruction(self, ctx:dUMLeParser.InstructionContext):
        pass

    # Exit a parse tree produced by dUMLeParser#instruction.
    def exitInstruction(self, ctx:dUMLeParser.InstructionContext):
        pass


    # Enter a parse tree produced by dUMLeParser#obj_declaration.
    def enterObj_declaration(self, ctx:dUMLeParser.Obj_declarationContext):
        pass

    # Exit a parse tree produced by dUMLeParser#obj_declaration.
    def exitObj_declaration(self, ctx:dUMLeParser.Obj_declarationContext):
        pass


    # Enter a parse tree produced by dUMLeParser#list_declaration.
    def enterList_declaration(self, ctx:dUMLeParser.List_declarationContext):
        pass

    # Exit a parse tree produced by dUMLeParser#list_declaration.
    def exitList_declaration(self, ctx:dUMLeParser.List_declarationContext):
        pass


    # Enter a parse tree produced by dUMLeParser#list_access.
    def enterList_access(self, ctx:dUMLeParser.List_accessContext):
        pass

    # Exit a parse tree produced by dUMLeParser#list_access.
    def exitList_access(self, ctx:dUMLeParser.List_accessContext):
        pass


    # Enter a parse tree produced by dUMLeParser#assignment.
    def enterAssignment(self, ctx:dUMLeParser.AssignmentContext):
        pass

    # Exit a parse tree produced by dUMLeParser#assignment.
    def exitAssignment(self, ctx:dUMLeParser.AssignmentContext):
        pass


    # Enter a parse tree produced by dUMLeParser#fun_declaration.
    def enterFun_declaration(self, ctx:dUMLeParser.Fun_declarationContext):
        pass

    # Exit a parse tree produced by dUMLeParser#fun_declaration.
    def exitFun_declaration(self, ctx:dUMLeParser.Fun_declarationContext):
        pass


    # Enter a parse tree produced by dUMLeParser#fun_call.
    def enterFun_call(self, ctx:dUMLeParser.Fun_callContext):
        pass

    # Exit a parse tree produced by dUMLeParser#fun_call.
    def exitFun_call(self, ctx:dUMLeParser.Fun_callContext):
        pass


    # Enter a parse tree produced by dUMLeParser#execution.
    def enterExecution(self, ctx:dUMLeParser.ExecutionContext):
        pass

    # Exit a parse tree produced by dUMLeParser#execution.
    def exitExecution(self, ctx:dUMLeParser.ExecutionContext):
        pass


    # Enter a parse tree produced by dUMLeParser#loop.
    def enterLoop(self, ctx:dUMLeParser.LoopContext):
        pass

    # Exit a parse tree produced by dUMLeParser#loop.
    def exitLoop(self, ctx:dUMLeParser.LoopContext):
        pass


    # Enter a parse tree produced by dUMLeParser#connection.
    def enterConnection(self, ctx:dUMLeParser.ConnectionContext):
        pass

    # Exit a parse tree produced by dUMLeParser#connection.
    def exitConnection(self, ctx:dUMLeParser.ConnectionContext):
        pass


    # Enter a parse tree produced by dUMLeParser#obj_access.
    def enterObj_access(self, ctx:dUMLeParser.Obj_accessContext):
        pass

    # Exit a parse tree produced by dUMLeParser#obj_access.
    def exitObj_access(self, ctx:dUMLeParser.Obj_accessContext):
        pass


    # Enter a parse tree produced by dUMLeParser#class_declaration.
    def enterClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        pass

    # Exit a parse tree produced by dUMLeParser#class_declaration.
    def exitClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        pass


    # Enter a parse tree produced by dUMLeParser#class_declaration_line.
    def enterClass_declaration_line(self, ctx:dUMLeParser.Class_declaration_lineContext):
        pass

    # Exit a parse tree produced by dUMLeParser#class_declaration_line.
    def exitClass_declaration_line(self, ctx:dUMLeParser.Class_declaration_lineContext):
        pass


    # Enter a parse tree produced by dUMLeParser#note.
    def enterNote(self, ctx:dUMLeParser.NoteContext):
        pass

    # Exit a parse tree produced by dUMLeParser#note.
    def exitNote(self, ctx:dUMLeParser.NoteContext):
        pass


    # Enter a parse tree produced by dUMLeParser#actor.
    def enterActor(self, ctx:dUMLeParser.ActorContext):
        pass

    # Exit a parse tree produced by dUMLeParser#actor.
    def exitActor(self, ctx:dUMLeParser.ActorContext):
        pass


    # Enter a parse tree produced by dUMLeParser#theme.
    def enterTheme(self, ctx:dUMLeParser.ThemeContext):
        pass

    # Exit a parse tree produced by dUMLeParser#theme.
    def exitTheme(self, ctx:dUMLeParser.ThemeContext):
        pass


    # Enter a parse tree produced by dUMLeParser#package_declaration.
    def enterPackage_declaration(self, ctx:dUMLeParser.Package_declarationContext):
        pass

    # Exit a parse tree produced by dUMLeParser#package_declaration.
    def exitPackage_declaration(self, ctx:dUMLeParser.Package_declarationContext):
        pass


    # Enter a parse tree produced by dUMLeParser#arg_list.
    def enterArg_list(self, ctx:dUMLeParser.Arg_listContext):
        pass

    # Exit a parse tree produced by dUMLeParser#arg_list.
    def exitArg_list(self, ctx:dUMLeParser.Arg_listContext):
        pass


    # Enter a parse tree produced by dUMLeParser#arg_list_include_scope.
    def enterArg_list_include_scope(self, ctx:dUMLeParser.Arg_list_include_scopeContext):
        pass

    # Exit a parse tree produced by dUMLeParser#arg_list_include_scope.
    def exitArg_list_include_scope(self, ctx:dUMLeParser.Arg_list_include_scopeContext):
        pass


    # Enter a parse tree produced by dUMLeParser#block.
    def enterBlock(self, ctx:dUMLeParser.BlockContext):
        pass

    # Exit a parse tree produced by dUMLeParser#block.
    def exitBlock(self, ctx:dUMLeParser.BlockContext):
        pass


    # Enter a parse tree produced by dUMLeParser#use_case.
    def enterUse_case(self, ctx:dUMLeParser.Use_caseContext):
        pass

    # Exit a parse tree produced by dUMLeParser#use_case.
    def exitUse_case(self, ctx:dUMLeParser.Use_caseContext):
        pass


    # Enter a parse tree produced by dUMLeParser#name.
    def enterName(self, ctx:dUMLeParser.NameContext):
        pass

    # Exit a parse tree produced by dUMLeParser#name.
    def exitName(self, ctx:dUMLeParser.NameContext):
        pass


    # Enter a parse tree produced by dUMLeParser#arg_name.
    def enterArg_name(self, ctx:dUMLeParser.Arg_nameContext):
        pass

    # Exit a parse tree produced by dUMLeParser#arg_name.
    def exitArg_name(self, ctx:dUMLeParser.Arg_nameContext):
        pass



del dUMLeParser