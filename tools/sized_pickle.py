# -*- coding: utf-8 -*-
"""
sized_pickle.py

store and retrieve data as a sized_pickle: a pickle with the first 4 bytes 
representing an integer size
"""

from pickle import loads, dumps
import struct

_pickle_length_format = "!I"
_pickle_length_size = struct.calcsize(_pickle_length_format)

def store_sized_pickle(data, file_object):
    """
    store structured data as a sized pickle in the file object
    """
    pickled_data = dumps(data)
    file_object.write(struct.pack(_pickle_length_format, len(pickled_data)))
    file_object.write(pickled_data)

def retrieve_sized_pickle(file_object):
    """
    return structured data from one sized pickle in the file object
    """
    length_str = file_object.read(_pickle_length_size)
    if len(length_str) == 0:
        raise EOFError()
    assert len(length_str) == _pickle_length_size, str(len(length_str))
    (pickle_length, ) = struct.unpack(_pickle_length_format, length_str)
    assert pickle_length > 0
    pickled_data = file_object.read(pickle_length)
    return loads(pickled_data)

