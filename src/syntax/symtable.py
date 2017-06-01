import pprint as pp

GLOBAL_CONTEXT = 'g'


class SymTableError(Exception):
    pass


class SymTable(object):
    _table = {GLOBAL_CONTEXT: {}}
    current_contex = GLOBAL_CONTEXT

    """docstring for SymTable."""
    def __init__(self):
        super().__init__()

    @staticmethod
    def show():
        pp.pprint(SymTable._table)

    @staticmethod
    def _formart_id_key(key):
        return f'${key}'

    @staticmethod
    def _formart_context_key(key):
        return f'{key}'

    def set(self, key, **kwargs):
        accesskey = SymTable._formart_id_key(key)
        use_context = kwargs.get('use_context', self.current_contex)

        if self.is_set(key):
            raise SymTableError(f'"{key}" is already defined.')

        record = dict(
            symbol=key,
            symtype=kwargs.get('symtype'),
            datatype=kwargs.get('datatype'),
            params=kwargs.get('params'),
            context=self.current_contex,
            extras=kwargs.get('extras')
        )

        try:
            self._table[use_context][accesskey] = record
        except KeyError:
            raise SymTableError(f'context "{use_context}" does not exist.')

        return record


    def get(self, key):
        context = self.get_context()
        accesskey = SymTable._formart_id_key(key)

        try:
            return context[accesskey]
        except KeyError:
            try:
                return self._table[GLOBAL_CONTEXT][accesskey]
            except KeyError:
                raise SymTableError(f'"{key}" is not defined.')

    def is_set(self, key):
        try:
            self.get(key)
            return True
        except SymTableError:
            return False

    def get_context(self, key=None):
        if key:
            accesskey = SymTable._formart_context_key(key)
        else:
            accesskey = self.current_contex

        try:
            return self._table[accesskey]
        except KeyError:
            raise SymTableError(f'"{key}" context is not defined.')

    def set_context(self, key):
        accesskey = self._formart_context_key(key)

        if self.is_context_set(key) or self.is_set(key):
            raise SymTableError(f'"{key}" is already defined.')

        self._table[accesskey] = {}
        self.current_contex = key

        return self._table[key]

    def is_context_set(self, key):
        accesskey = self._formart_context_key(key)

        try:
            self._table[accesskey]
            return True
        except KeyError:
            return False

    def exit_context(self):
        if self.current_contex != GLOBAL_CONTEXT:
            self.current_contex = GLOBAL_CONTEXT
