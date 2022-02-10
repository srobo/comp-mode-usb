"""
json.py - A JSON parser.

A fairly small pure python json parser for use on circuitpython boards that
don't include the C-based json library.

Written by Will Barber
"""
import gc


def loads(s):
    """Load an object from a JSON string."""
    if s[0] != '{':
        raise ValueError("Invalid JSON object")
    try:
        return _parse_object(s, 1)[0]
    except IndexError:
        raise ValueError("Incomplete JSON object")


def _parse_object(data, start):
    """Parse JSON object {}, returns a dict and the index beyond the last character."""
    idx = _skip_whitespace(data, start)
    obj = {}
    if data[idx] == '}':
        return obj, idx + 1

    while True:
        idx = _skip_whitespace(data, idx)

        if data[idx] != '"':
            raise ValueError("Object key is not a string, index: {}".format(idx))
        key, idx = _parse_string(data, idx + 1)
        idx = _skip_whitespace(data, idx)

        if data[idx] != ':':
            raise ValueError("Invalid key value pair")
        value, idx = _parse_value(data, idx + 1)

        obj[key] = value
        if data[idx] != ',':
            break
        idx += 1

    if data[idx] == '}':
        return obj, idx + 1

    raise ValueError("Incomplete JSON object")


def _skip_whitespace(data, idx):
    """Return the next index with a non-whitespace character."""
    while data[idx].isspace():
        idx += 1
    return idx


def _parse_value(data, start):
    """Parse a JSON value, returns any of the following parsers and the index beyond the last character."""
    init_idx = _skip_whitespace(data, start)

    if data[init_idx] == '{':
        value, idx = _parse_object(data, init_idx + 1)
    elif data[init_idx] == '[':
        value, idx = _parse_array(data, init_idx + 1)
    elif data[init_idx] == '"':
        value, idx = _parse_string(data, init_idx + 1)
    elif data[init_idx] in ['t', 'f', 'n']:
        value, idx = _parse_bool(data, init_idx)
    elif data[init_idx] in '-0123456789':
        value, idx = _parse_number(data, init_idx)
    else:
        raise ValueError("Invalid value starting character: '{}', index: {}".format(data[init_idx], init_idx))

    idx = _skip_whitespace(data, idx)
    return value, idx


def _parse_array(data, start):
    """Parse JSON object [], returns a list and the index beyond the last character."""
    idx = _skip_whitespace(data, start)
    obj = []
    if data[idx] == ']':
        return obj, idx + 1

    while True:
        value, idx = _parse_value(data, idx)

        obj.append(value)
        if data[idx] == ',':
            idx += 1
        else:
            break

    if data[idx] == ']':
        return obj, idx + 1

    raise ValueError("Incomplete JSON object")


def _parse_bool(data, start):
    """Parse JSON bool/null, returns a bool or None and the index beyond the last character."""
    if data[start:start + 4] == 'true':
        return True, start + 4
    elif data[start:start + 5] == 'false':
        return False, start + 5
    elif data[start:start + 4] == 'null':
        return None, start + 4
    raise ValueError('Malformed JSON data at index {}'.format(start))


def _parse_string(data, start):
    """Parse JSON string, returns a string and the index beyond the last character."""
    idx = start
    value = ''
    while not data[idx] == '"':
        if data[idx] == '\\':
            value += data[start:idx]
            c = data[idx + 1]
            if c in ['"', '\\', '/']:
                value += c
            elif c == 'b':
                value = value[:-1]
            elif c == 'f':
                value += '\f'
            elif c == 'n':
                value += '\n'
            elif c == 'r':
                value += '\r'
            elif c == 't':
                value += '\t'
            elif c == 'u':
                raise NotImplementedError("json.py does not support unicode")
            idx += 2
            start = idx
            continue
        idx += 1

    value += data[start:idx]

    return value, idx + 1


def _parse_number(data, start):
    """Parse JSON number, returns an int or float and the index beyond the last character."""
    idx = start
    is_float = False
    # Use loose validation since we're using int()/float()
    while data[idx] in '+-0123456789.eE':
        idx += 1
        if data[idx] in '.e':
            is_float = True

    if is_float:
        return float(data[start:idx]), idx
    else:
        return int(data[start:idx]), idx


def dumps(data):
    """convert a dict to a JSON string."""
    if not isinstance(data, dict):
        raise ValueError("The outer container must be a dict")
    gc.collect()  # do some garbage collection
    output = _dump_object(data)
    gc.collect()
    return output


def _dump_object(data):
    elements = []
    for key, value in data.items():
        elements.append("{}: {}".format(_dump_string(key), _dump_value(value)))

    return '{' + ', '.join(elements) + '}'


def _dump_value(data):
    if data is True:
        return 'true'
    elif data is False:
        return 'false'
    elif data is None:
        return 'null'
    elif isinstance(data, dict):
        return _dump_object(data)
    elif isinstance(data, list):
        return _dump_array(data)
    elif isinstance(data, str):
        return _dump_string(data)
    elif isinstance(data, int) or isinstance(data, float):
        return str(data)

    raise ValueError("Unsupported object type")


def _dump_array(data):
    elements = []
    for value in data:
        elements.append(_dump_value(value))

    return '[' + ', '.join(elements) + ']'


def _dump_string(data):
    output = ''
    start = 0
    idx = 0
    for idx, c in enumerate(data):
        if c in ['"', '\\', '\f', '\n', '\r', '\t']:
            output += data[start:idx]
            if c == '"':
                output += '\\"'
            elif c == '\\':
                output += '\\\\'
            elif c == '\f':
                output += '\\f'
            elif c == '\n':
                output += '\\n'
            elif c == '\r':
                output += '\\r'
            elif c == '\t':
                output += '\\t'

            start = idx + 1

    output += data[start:idx + 1]
    return '"' + output + '"'
