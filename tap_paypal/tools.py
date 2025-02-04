"""Tools."""
# -*- coding: utf-8 -*-
from functools import reduce
from typing import Optional


def clear_currently_syncing(state: dict) -> dict:
    """Clear the currently syncing from the state.

    Arguments:
        state (dict) -- State file

    Returns:
        dict -- New state file
    """
    return state.pop('currently_syncing', None)


def get_stream_state(state: dict, start_date: str, tap_stream_id: str) -> dict:
    """Return the state of the stream.

    Arguments:
        state {dict} -- The state
        start_date {str} -- default date
        tap_stream_id {str} -- The id of the stream

    Returns:
        dict -- The state of the stream, if no bookmark was found return default start_date
    """
    return state.get(
        'bookmarks',
        {tap_stream_id: {
            "start_date": start_date
        }},
    ).get(tap_stream_id)


def retrieve_bookmark_with_path(path: str, row: dict) -> Optional[str]:
    """Bookmark exists in the row of data which is an dictionary.

    The bookmark can either be a key such as row[key] but also a subkey such as
    row[key][subkey]. In the streams definition file, the key can be saved as
    a string, but [key][subkey] cannot. Therefore, in the streams file, if we
    want to use a subkey as bookmark, we save it in the format 'key.subkey',
    which is our path in the dictionary.
    This helper function parses the string and checks whether it has a dot.
    If it has one, it returns the value of the subkey in the row of data, e.g.
    row[key][subkey]. If not it returns the alue of the key, e.g row[path].

    Arguments:
        path {str} -- Path in the dictionary
        row {dict} -- Data row

    Returns:
        Optional[str] -- The value or from the key or subkey
    """
    # If the path has a dot, then parse it as key and subkeys
    if '.' in path:
        return str(reduce(dict.get, path.split('.'), row))  # type: ignore
    # Else if the path is just a key, parse it as a normal key
    elif path:
        return row[path]
    return None
