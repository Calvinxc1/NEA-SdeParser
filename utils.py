from tqdm.notebook import tqdm, trange

def build_schema(raw_data:list, tqdm_leave=False) -> dict:
    flat_data = flatten_data(raw_data, tqdm_leave)
    schema_data = parse_schema(flat_data, tqdm_leave)
    return schema_data

def parse_schema(flat_data:list, tqdm_leave=False) -> dict:
    """ Parses a flat dictionary's schema

    Utility/debugging method for parsing a flat dictionary's
    general layout by iterating over several dictionaries and
    aggregating the results in an easy-to-understand way.

    Parameters
    ----------
    flat_data: list
        List of flat dictionaries to build the schema from

    Returns
    -------
    dict
        Schema inferred from flat_data
    """

    schema = {}
    for flat_item in tqdm(flat_data, leave=tqdm_leave):
        for key, val in flat_item.items():
            val_type = type(val).__name__
            schema[key] = schema.get(key, {})
            schema[key][val_type] = schema[key].get(val_type, 0)
            schema[key][val_type] += 1

    return schema

def flatten_data(raw_data:list, tqdm_leave=False) -> list:
    """ Converts a list of dictionary items to flat format

    Takes a list of dictionaries and converts those dictionaries
    to flat format.

    Parameters
    ----------
    raw_data: list
        List of dictionaries to flatten
    tqdm_leave: bool, optional
        If verbose is True, controls whether or not the TQDM
        iterator stays after completing (default False)

    Returns
    -------
    list
        List of flattened dictionary items
    """

    flat_data = []
    for item in tqdm(raw_data, leave=tqdm_leave):
        flat_data.append(_flatten_item(item))

    return flat_data

def _flatten_item(item:dict, _header='') -> dict:
    """ Recursive dictionary flattener

    Recursively flattens dictionary items. Called from the
    flatten_data method.

    Parameters
    ----------
    item: dict or list
        Item to flatten. If called to start process should
        be called with a dict, not a list.
    _header: str
        For tracking the path of the flattener, do not use

    Returns
    -------
    dict
        Flattened dictionary item
    """
    
    flat_item = {}
    if type(item) is dict:
        for key, value in item.items():
            flat_item = {
                **flat_item,
                **_flatten_item(value, _header='%s.%s' % (_header, key))
            }
    elif type(item) is list:
        for i in range(len(item)):
            flat_item = {
                **flat_item,
                **_flatten_item(item[i], _header='%s.%s' % (_header, i))
            }
    else:
        flat_item[_header[1:]] = item

    return flat_item