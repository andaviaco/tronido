GLOBAL_CONTEXT = 'g'

class SymTableError(Exception):
    pass


class SymTable(object):
    _table = {GLOBAL_CONTEXT: {}}
    current_contex = GLOBAL_CONTEXT

    """docstring for SymTable."""
    def __init__(self):
        super().__init__()

    def _formart_id_key(self, key):
        return f'${key}'

    def _formart_context_key(self, key):
        return f'@{key}'

    def set(self, key, **kwargs):
        accesskey = self._formart_id_key(key)

        try:
            self.get(accesskey):

            raise SymTableError(f'"{key}" is already defined.')
        except SymTableError:
            self._table[self.current_contex][accesskey] = record

            return record


    def get(self, key):
        context = self.get_context()

        try:
            return context[key]
        except KeyError:
            raise SymTableError(f'"{key}" is not defined.')

    def is_set(self, key):
        accesskey = self._formart_id_key(key)

        try:
            self.get(accesskey):
            return True
        except SymTableError:
            return False

    def get_context(self, key=GLOBAL_CONTEXT):
        try:
            return self._table[self.current_contex]
        except KeyError:
            raise SymTableError(f'"{key}" is not defined.')

    def set_context(self, key):
        accesskey = self._formart_context_key(key)

        if self.get_context(accesskey):
            raise SymTableError(f'"{key}" is already defined.')

        self._table[accesskey] = {}

        return self._table[key]

    def exit_context(self):
        if self.current_contex != GLOBAL_CONTEXT:
            self._table.pop(self.current_contex, None)

            self.current_contex = GLOBAL_CONTEXT
