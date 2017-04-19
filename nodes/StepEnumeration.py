from .AST import AST

class StepEnumeration(AST):
    _fields = ['loop_counter','start_value','step_value','down','end_value']
