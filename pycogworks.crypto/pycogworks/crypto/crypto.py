# -*- coding:    utf-8 -*-
#===============================================================================
# This file is part of PyCogWorks.
# Copyright (C) 2012 Ryan Hope <rmh3093@gmail.com>
#
# PyCogWorks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyCogWorks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyCogWorks.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from Crypto.Cipher import AES

__cipher__ = 'AES/CBC (RIJNDAEL) - 16Byte Key'

def rin2id(rin):
    if unicode(rin).isnumeric() and len(rin) == 9:
        rin = '%s%s' % (str(rin), str(rin)[:7])
        cipher = AES.new(rin, AES.MODE_CBC, "0000000000000000")
        return ''.join(["%02x" % ord(x) for x in cipher.encrypt(rin)]).strip(), __cipher__
    else:
        raise Exception("Invalid RIN.")
