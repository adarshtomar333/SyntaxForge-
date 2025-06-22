import re

token_specification = [
    ('EQ',        r'=='),
    ('NE',        r'!='),
    ('LE',        r'<='),
    ('GE',        r'>='),
    ('ASSIGN',    r'='),
    ('LT',        r'<'),
    ('GT',        r'>'),
    ('JAB_TAK',   r'jab_tak'),
    ('KARO',      r'karo'),
    ('NUMBER',    r'\d+'),
    ('STRING',    r'"[^"]*"'),
    ('CHAR',      r"'[^']'"),
    ('TOH',       r'Toh'),
    ('TU_INT',    r'tu_int'),
    ('TU_CHAR',   r'tu_char'),
    ('TU_STRING', r'tu_string'),
    ('TU_BOOL',   r'tu_bool'),
    ('TRUE',      r'true'),
    ('FALSE',     r'false'),
    ('AGAR',      r'agar'),
    ('NAHI_TO',   r'nahi_to'),
    ('CHAP_REE',  r'chap_ree'),
    ('SUN_OYEE',  r'sun_oyee'),
    ('PLUS',      r'\+'),
    ('MINUS',     r'-'),
    ('TIMES',     r'\*'),
    ('DIVIDE',    r'/'),
    ('MOD',       r'%'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
    ('IDENT',     r'[A-Za-z_][A-Za-z_0-9]*'),
    ('MISMATCH',  r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'CHAR':
            value = value[1:-1]
        elif kind == 'STRING':
            value = value[1:-1]
        elif kind == 'NEWLINE' or kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected char: {value!r}')
        yield (kind, value)