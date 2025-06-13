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

from dataclasses import dataclass

@dataclass(frozen=True)
class _CN:
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


def logs():
    """Returns the logs list."""
    return _logs


def level():
    """Returns current log level."""
    return _level


def status():
    """Returns current log status."""
    return _status


def is_debug():
    """Returns whether current status is DEBUG."""
    return bool(_status == CN.DEBUG)


def is_info():
    """Returns whether current status is INFO."""
    return bool(_status == CN.INFO)


def is_warn():
    """Returns whether current status is WARNING."""
    return bool(_status == CN.WARNING)


def is_error():
    """Returns whether current status is ERROR."""
    return bool(_status == CN.ERROR)


def is_fatal():
    """Returns whether current status is FATAL."""
    return bool(_status == CN.FATAL)


def tag(lvl=_level):
    """Returns preset OSlg string that matches log level."""
    try:
        lvl = int(lvl)
    except ValueError as e:
        return _tag[0]

    if not 0 <= lvl < len(_tag):
        return _tag[0]

    return _tag[lvl]


def msg(stat=_status):
    """Returns preset OSlg message that matches log status."""
    try:
        stat = int(stat)
    except ValueError as e:
        return _msg[0]

    if not 0 <= stat < len(_msg):
        return _msg[0]

    return _msg[stat]


def trim(txt="", length=60):
    """Converts object to String and trims if necessary."""
    try:
        length = int(length)
    except ValueError as e:
        length = 60

    return str(txt.strip()[:length])


def reset(lvl=CN.DEBUG):
    """Resets level, if lvl (input) is within accepted range."""
    global _level

    try:
        lvl = int(lvl)
    except ValueError as e:
        return _level

    if CN.DEBUG <= lvl <= CN.FATAL:
        _level = lvl

    return _level


def log(lvl=CN.DEBUG, message=""):
    """Logs a new entry, if provided arguments are valid."""
    global _status
    global _logs

    try:
        lvl = int(lvl)
    except ValueError as e:
        return _status

    try:
        message = str(message)
    except ValueError as e:
        return _status

    if lvl < CN.DEBUG or lvl > CN.FATAL or lvl < _level:
        return _status

    _logs.append(dict(level=lvl, message=message))

    if lvl > _status:
        _status = lvl

    return _status
