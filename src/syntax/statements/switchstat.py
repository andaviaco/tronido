from ..tree import Node

SWITCH_COND = dict(
    can_break=True,
    is_switch=True
)

class SwitchStat(Node):
    """docstring for SwitchStat."""
    def __init__(self,  exp, cases, token):
        super().__init__(None, token)

        self.exp = exp or Node(None, token)
        self.cases = cases

    def validate_default_case(self, cases):
        current_case = cases
        has_default = False

        while current_case:
            if has_default:
                Node.raise_error(f'Only one default statement is allow. Line: {self.init.token.line_index} - Col: {self.init.token.col_index}')
            has_default = not current_case.cond
            current_case = current_case.next

    def process_semantic(self, **cond):
        self.exp.process_semantic()
        conditions = SWITCH_COND
        conditions['datatype'] = self.exp.datatype

        self.validate_default_case(self.cases)

        Node.proccess_traversal_semantics(self.cases, **conditions)


    def generate_code(self, **cond):
        cases_labels = []

        default_label = Node.get_unique_label('default_case')
        end_switch_label = Node.get_unique_label('end_switch')

        array, _ = Node.assignated_array()

        default_pos = 0
        current_case = self.cases
        line = 0
        i = 0

        while current_case:
            if not current_case.cond:
                default_pos = True
                current_case = current_case.next

                continue

            self.exp.generate_code()
            current_case.cond.generate_code()
            cases_labels.append(Node.get_unique_label('case'))
            _, line = Node.assignated_array()
            Node.array_append(array, f'{line} OPR 0, 14')
            line += 1
            cases_label = cases_labels[i]
            Node.array_append(array, f'{line} JMC V, {cases_label}')
            current_case = current_case.next
            i += 1

        _, line = Node.assignated_array()

        if default_pos:
            Node.array_append(array, f'{line} JMP 0, {default_label}')

        current_case = self.cases
        i = 0

        while current_case:
            _, line = Node.assignated_array()

            if current_case.cond:
                label = cases_labels[i]
            else:
                label = default_label

            Node.code_labels.append(f'{label},I,I,{line},0,#,')
            Node.cascade_code(current_case.stats, **{'break_to': end_switch_label})
            current_case = current_case.next
            i += 1

        _, line = Node.assignated_array()
        Node.array_append(array, f'JMP 0, {end_switch_label}')
        line += 1
        Node.code_labels.append(f'{end_switch_label},I,I,{line},0,#,')
