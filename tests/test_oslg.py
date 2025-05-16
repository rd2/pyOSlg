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

import sys
sys.path.append("./src/oslg")

import unittest
import oslg

class TestOSlgModuleMethods(unittest.TestCase):
    def test_pyOSlg_access(self):
        self.assertEqual(oslg.CN.DEBUG, 1)

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == "__main__":
    unittest.main()

# PACKAGE_PARENT = pathlib.Path(__file__).parent
# sys.path.append(str(PACKAGE_PARENT))

## Standalone boilerplate before relative imports
# if __package__ is None:
#     DIR = pathlib.Path(__file__).resolve().parent
#     sys.path.insert(0, str(DIR.parent))
#     __package__ = DIR.name
#
# from .. import oslg

# DBG = oslg.CONSTANTS.DEBUG
# INF = oslg.CONSTANTS.INFO
# WRN = oslg.CONSTANTS.WARN
# ERR = oslg.CONSTANTS.ERROR
# FTL = oslg.CONSTANTS.FATAL

# DBG = oslg.DEBUG
# INF = oslg.INFO
# WRN = oslg.WARN
# ERR = oslg.ERROR
# FTL = oslg.FATAL
#
#
# print(DBG)  # OK!
# DBG = 6  # NOPE
# print(DBG)  # OK!
#
# print(oslg.DEBUG)  # OK!
# oslg.DEBUG = 6  # NOPE
# print(oslg.DEBUG)  # OK!
#
# print(f"{oslg.DEBUG == 1}") # False
# print(f"{DBG == 1}")        # False
#
# print(oslg.__name__)
# print(oslg.ERROR)
# print(oslg.logs)
# # oslg.CONSTANTS.ERROR = 555
# print(oslg.ERROR)
