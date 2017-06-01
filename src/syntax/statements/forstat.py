from lexer import lang
from ..tree import Node

FOR_CONDITIONS = dict(
    can_break=True,
    can_continue=True
)

class ForStat(Node):
    """docstring for ForStat."""
    def __init__(self, initializer, condition, step, stats, token):
        super().__init__(None, token)

        self.initializer = initializer or Node(None, token)
        self.condition = condition or Node(None, token)
        self.step = step or Node(None, token)
        self.stats = stats

    def process_semantic(self, **cond):
        self.condition.process_semantic()
        self.initializer.process_semantic()
        self.step.process_semantic()

        cond = self.condition
        init = self.initializer
        step = self.step
        datatype = lang.SEMANTIC_VOID_TYPE

        if init.right.datatype != lang.SEMANTIC_INT_TYPE:
            Node.raise_error(f'Step must be of type {lang.SEMANTIC_INT_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')

        if cond.right.datatype != lang.SEMANTIC_INT_TYPE:
            Node.raise_error(f'Limit must be of type {lang.SEMANTIC_INT_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')
            datatype = lang.SEMANTIC_ERROR_TYPE

        if cond and cond.datatype != lang.SEMANTIC_LOGIC_TYPE:
            Node.raise_error(f'Condition must be of type {lang.SEMANTIC_LOGIC_TYPE}. Line: {self.token.line_index} - Col: {self.token.col_index}')
            datatype = lang.SEMANTIC_ERROR_TYPE

        Node.proccess_traversal_semantics(self.stats, **FOR_CONDITIONS)

        self.datatype = datatype

    def generate_code(self, **cond):
        true_label = Node.get_unique_label('true')
        false_label = Node.get_unique_label('false')
        for_label = Node.get_unique_label('for')
        form_incr_label = Node.get_unique_label('form_incr')

        array, _ = Node.assignated_array()
        cond = dict(break_to=false_label, continue_to=form_incr_label)

        self.initializer.generate_code()
        _, line = Node.assignated_array()
        Node.code_labels.append(f'{for_label},I,I,{line},0,#,')

        self.condition.generate_code()
        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMC V, {true_label}')
        line +=1
        Node.array_append(array, f'{line} JMP 0, {false_label}')

        _, line = Node.assignated_array()
        Node.code_labels.append(f'{form_incr_label},I,I,{line},0,#,')

        self.step.generate_code()
        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMP 0, {for_label}')

        _, line = Node.assignated_array()
        Node.code_labels.append(f'{true_label},I,I,{line},0,#,')

        Node.cascade_code(self.stats, **cond)
        _, line = Node.assignated_array()
        Node.array_append(array, f'{line} JMP 0, {form_incr_label}')

        line += 1
        Node.code_labels.append(f'{false_label},I,I,{line},0,#')
