# BSD 3-Clause License
#
# Copyright (c) 2022-2025, rd2
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Python implementation of the OSlg logger, in support of the OpenStudio SDK.

Original Ruby implementation/documentation: https://github.com/rd2/oslg
"""

import inspect

from dataclasses import dataclass

@dataclass(frozen=True)
class _CN:
    """
    OSlg constants (int): 'DEBUG', 'INFO', 'WARN', 'ERROR' & 'FATAL'.

    Typical usage:

        import oslg
        print(oslg.CN.FATAL)
            (-> 6)
    """
    DEBUG = 1
    INFO  = 2
    WARN  = 3
    ERROR = 4
    FATAL = 5
CN = _CN()

_tag = ("",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "FATAL")

_msg = ("",
        "Debugging ...",
        "Success! No errors, no warnings",
        "Partial success, raised non-fatal warnings",
        "Partial success, encountered non-fatal errors",
        "Failure, triggered fatal errors")

_logs   = []
_level  = CN.INFO
_status = 0


def trim(txt="", length=60) -> str:
    """
    Converts an object to a string. Strips if necessary.

    Args:
        txt:
            An object.
        length:
            Desired maximum string length.

    Returns:
        Stripped, trimmed string. Maximum string length is defaulted at 60
        if 'length' cannot be converted to an integer. Returns an empty string
        if 'txt' cannot be converted to a valid string.

    """
    try:
        length = int(length)
    except ValueError as e:
        length = 60

    try:
        txt = str(txt).strip()[:length]
    except UnicodeEncodeError:
        txt = ""
    except Exception as e:
        txt = ""

    return txt


def logs() -> list:
    """Returns generated logs."""
    return _logs


def level() -> int:
    """Returns current log level."""
    return _level


def status() -> int:
    """Returns current log status."""
    return _status


def is_debug() -> bool:
    """Returns whether current status is DEBUG."""
    return bool(_status == CN.DEBUG)


def is_info() -> bool:
    """Returns whether current status is INFO."""
    return bool(_status == CN.INFO)


def is_warn() -> bool:
    """Returns whether current status is WARNING."""
    return bool(_status == CN.WARNING)


def is_error() -> bool:
    """Returns whether current status is ERROR."""
    return bool(_status == CN.ERROR)


def is_fatal() -> bool:
    """Returns whether current status is FATAL."""
    return bool(_status == CN.FATAL)


def tag(lvl=_level) -> str:
    """
    Returns a preset string that matches a log level.

    Args:
        lvl:
            Selected log level (e.g. CN.DEBUG).

    Returns:
        Matching 'tag' string (e.g. "DEBUG"). Returns an empty string if
        'lvl' cannot be converted to an integer, or if not an OSlg constant
        (once converted).

    """
    try:
        lvl = int(lvl)
    except ValueError as e:
        return _tag[0]

    if not 0 <= lvl < len(_tag):
        return _tag[0]

    return _tag[lvl]


def msg(stat=_status) -> str:
    """
    Returns a preset string that matches a log status.

    Args:
        stat:
            Selected log status (e.g. CN.FATAL).

    Returns:
        Matching 'status' string (e.g. "Failure, triggered fatal errors").
        Returns an empty string if 'stat' cannot be converted to an integer, or
        if not an OSlg constant (once converted).

    """
    try:
        stat = int(stat)
    except ValueError as e:
        return _msg[0]

    if not 0 <= stat < len(_msg):
        return _msg[0]

    return _msg[stat]


def reset(lvl=CN.DEBUG) -> int:
    """
    Resets log level.

    Args:
        lvl:
            Selected log level (e.g. CN.DEBUG).

    Returns:
        Newly reset log level. Remains unchanged if 'lvl' cannot be converted
        to an integer, or if not an OSlg constant (once converted).

    """
    global _level

    try:
        lvl = int(lvl)
    except ValueError as e:
        return _level

    if CN.DEBUG <= lvl <= CN.FATAL:
        _level = lvl

    return _level


def log(lvl=CN.DEBUG, message="") -> int:
    """
    Logs a new entry. Overall log status is raised to the new log level, if
    the latter is greater than the former (e.g. FATAL > ERROR). Candidate log
    entry is ignored and status remains unchanged if the new level cannot be
    converted to an integer, or if not an OSlg constant (once converted).
    Relies on module method trim(): candidate entry is ignored and status
    unchanged if message is not a valid string.

    Args:
        lvl:
            Selected log level (e.g. CN.DEBUG).
        message:
            Selected log message (max. 60 chars).

    Returns:
        Current log status, potentially raised.

    """
    global _status
    global _logs

    try:
        lvl = int(lvl)
    except ValueError as e:
        return _status

    message = trim(message)

    if not message or lvl < CN.DEBUG or lvl > CN.FATAL or lvl < _level:
        return _status

    if lvl > _status:
        _status = lvl

    _logs.append(dict(level=lvl, message=message))

    return _status


def invalid(id="", mth="", ord=0, lvl=CN.DEBUG, res=None):
    """
    Logs template 'invalid object' entry, based on arguments. Relies on module
    method log(): check its own exit conditions and module-level side effects.
    Argument 'ord' is ignored unless > 0. Candidate log entry is ignored and
    status remains unchanged if 'ord' cannot be converted to an integer.

    Args:
        id:
            Object identifier string (e.g. "circle radius").
        mth:
            Method identifier string (e.g. "circle area").
        ord:
            Method call parameter index (e.g. '1' if 2nd argument).
        lvl:
            Selected log level (e.g. CN.DEBUG).
        res:
            Selected return object.

    Returns:
        Selected return object ('res').

    """
    id  = trim(id)
    mth = trim(mth)

    try:
        ord = int(ord)
    except ValueError as e:
        return res

    try:
        lvl = int(lvl)
    except ValueError as e:
        return res

    if not id or not mth or lvl < CN.DEBUG or lvl > CN.FATAL:
        return res

    msg = "Invalid '%s' " % (id)

    if ord > 0:
        msg += "arg #%d "  % (ord)

    msg += "(%s)" % (mth)
    log(lvl, msg)

    return res


def mismatch(id="", obj=None, cl=None, mth="", lvl=CN.DEBUG, res=None):
    """
    Logs template 'instance/class mismatch' entry, based on arguments. Relies
    on module method log(): check its own exit conditions and module-level
    side effects. Candidate log entry is ignored and status remains unchanged
    if 'obj' is an instance of 'cl'.

    Args:
        id:
            Object identifier string (e.g. "circle radius").
        obj:
            Mismatched object (e.g. boolean)
        cl:
            Desired target class (e.g. float)
        mth:
            Method identifier string (e.g. "circle area").
        lvl:
            Selected log level (e.g. CN.DEBUG).
        res:
            Selected return object.

    Returns:
        Selected return object ('res').

    """
    id  = trim(id)
    mth = trim(mth)

    try:
        lvl = int(lvl)
    except ValueError as e:
        return res

    if not inspect.isclass(cl) or isinstance(obj, cl):
        return res
    if not id or not mth or lvl < CN.DEBUG or lvl > CN.FATAL:
        return res

    msg  = "'%s' %s? " % (id, type(obj).__name__)
    msg += "expecting %s (%s)" % (cl.__name__, mth)
    log(lvl, msg)

    return res


def hashkey(id="", dct={}, key="", mth="", lvl=CN.DEBUG, res=None):
    """
    Logs template 'missing hash key' entry, based on arguments. Relies
    on module method log(): check its own exit conditions and module-level
    side effects. Candidate log entry is ignored and status remains unchanged
    if 'obj' is an instance of 'cl'.

    Args:
        id:
            Object identifier string (e.g. "circle radius").
        dct:
            Dictionary (or Hash) to validate.
        key:
            Missing dictionary key.
        mth:
            Method identifier string.
        lvl:
            Selected log level (e.g. CN.DEBUG).
        res:
            Selected return object.

    Returns:
        Selected return object ('res').

    """
    id  = trim(id)
    mth = trim(mth)
    ky  = trim(key)

    try:
        lvl = int(lvl)
    except ValueError as e:
        return res

    if not isinstance(dct, dict) or key in dct:
        return res
    if not id or not mth or lvl < CN.DEBUG or lvl > CN.FATAL:
        return res

    log(lvl, "Missing '%s' key in %s (%s)" % (ky, id, mth))

    return res


def empty(id="", mth="", lvl=CN.DEBUG, res=None):
    """
    Logs template 'empty' entry, based on arguments. Relies on module method
    log(): check its own exit conditions and module-level side effects.

    Args:
        id:
            Object identifier string (e.g. "circle radius").
        mth:
            Method identifier string.
        lvl:
            Selected log level (e.g. CN.DEBUG).
        res:
            Selected return object.

    Returns:
        Selected return object ('res').

    """
    id  = trim(id)
    mth = trim(mth)

    try:
        lvl = int(lvl)
    except ValueError as e:
        return res

    if not id or not mth or lvl < CN.DEBUG or lvl > CN.FATAL:
        return res

    log(lvl, "Empty '%s' (%s)" % (id, mth))

    res


def zero(id="", mth="", lvl=CN.DEBUG, res=None):
    """
    Logs template 'zero' entry, based on arguments. Relies on module method
    log(): check its own exit conditions and module-level side effects.

    Args:
        id:
            Object identifier string (e.g. "circle radius").
        mth:
            Method identifier string.
        lvl:
            Selected log level (e.g. CN.DEBUG).
        res:
            Selected return object.

    Returns:
        Selected return object ('res').

    """
    id  = trim(id)
    mth = trim(mth)

    try:
        lvl = int(lvl)
    except ValueError as e:
        return res

    if not id or not mth or lvl < CN.DEBUG or lvl > CN.FATAL:
        return res

    log(lvl, "Zero '%s' (%s)" % (id, mth))

    return res


def negative(id="", mth="", lvl=CN.DEBUG, res=None):
    """
    Logs template 'negative' entry, based on arguments. Relies on module method
    log(): check its own exit conditions and module-level side effects.

    Args:
        id:
            Object identifier string (e.g. "circle radius").
        mth:
            Method identifier string.
        lvl:
            Selected log level (e.g. CN.DEBUG).
        res:
            Selected return object.

    Returns:
        Selected return object ('res').

    """
    id  = trim(id)
    mth = trim(mth)

    try:
        lvl = int(lvl)
    except ValueError as e:
        return res

    if not id or not mth or lvl < CN.DEBUG or lvl > CN.FATAL:
        return res

    log(lvl, "Negative '%s' (%s)" % (id, mth))

    return res


def clean() -> int:
    """Resets log status and entries."""
    global _status
    global _logs

    _status = 0
    _logs   = []

    return _level
