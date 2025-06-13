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

DBG = oslg.CN.DEBUG
INF = oslg.CN.INFO
WRN = oslg.CN.WARN
ERR = oslg.CN.ERROR
FTL = oslg.CN.FATAL

class TestOSlgModuleMethods(unittest.TestCase):
    def test_oslg_constants(self):
        self.assertEqual(DBG, 1)

    def test01_oslg_initialized(self):
        self.assertEqual(len(oslg.logs()), 0)
        self.assertEqual(oslg.level(), INF)
        self.assertEqual(oslg.status(), 0)
        self.assertNotEqual(oslg.level(), DBG)
        self.assertNotEqual(oslg.status(), ERR)
        self.assertEqual(oslg.tag(), "INFO")
        self.assertEqual(oslg.msg(), "")
        self.assertEqual(oslg.tag(WRN), "WARNING")
        self.assertEqual(oslg.msg(FTL), "Failure, triggered fatal errors")
        self.assertNotEqual(oslg.msg(FTL), "Debugging ...")
        self.assertEqual(oslg.trim("   oslg  "), "oslg")
        self.assertEqual(oslg.trim("   oslg  ", 3), "osl")
        self.assertEqual(oslg.trim("   oslg  ", 64), "oslg")

    def test02_oslg_resets(self):
        self.assertEqual(oslg.level(), INF)
        self.assertEqual(oslg.reset(10), INF)
        self.assertEqual(oslg.reset(FTL), FTL)
        self.assertEqual(oslg.reset(), DBG)
        self.assertEqual(oslg.reset(INF), INF)
        self.assertEqual(oslg.level(), INF)

    def test03_oslg_logging(self):
        self.assertEqual(oslg.log(FTL, oslg.msg(FTL)), FTL)
        self.assertEqual(len(oslg.logs()), 1)

if __name__ == "__main__":
    unittest.main()
