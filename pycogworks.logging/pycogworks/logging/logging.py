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

import json
import datetime
import time
import platform
import sys

get_time = time.time
if platform.system() == 'Windows':
    get_time = time.clock
getTime = get_time

def getDateTimeStamp():
    d = datetime.datetime.now().timetuple()
    return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])
    
def writeHistoryFile(filename, subjectInfo):
    if 'rin' in subjectInfo:
        rin = subjectInfo['rin']
        if len(rin) != 9:
            raise Exception("The 'rin' field value must have a length of 9.")
        eid = rin2id(rin)
        if 'encrypted_rin' in subjectInfo and subjectInfo['encrypted_rin'] != eid:
            raise Exception("Invalid 'encrypted_rin' value for given 'rin'.")
        else:
            subjectInfo['encrypted_rin'] = eid
            subjectInfo['cipher'] = 'AES/CBC (RIJNDAEL) - 16Byte Key'
        history = open(filename, 'w')
        history.write(json.dumps(subjectInfo, sort_keys=True, indent=4))
        history.close()
    else:
        raise Exception("The 'subjectInfo' dict must contain a 'rin' field!")
    
class Logger():
    
    def __init__(self, header, file=None, delim="\t", newline="\n", filler="NA"):
        self.header = header
        self.delim = delim
        self.newline = newline
        self.filler = filler
        if file:
            self.file = open(file, "w")
        else:
            self.file = sys.__stdout__
        self.file.write(self.delim.join(header))
        self.file.write(self.newline)
        
    def write(self, **kwargs):
        line = [self.filler] * len(self.header)
        for k, v in kwargs.iteritems():
            if k in self.header:
                line[self.header.index(k)] = str(v)
        self.file.write(self.delim.join(line))
        self.file.write(self.newline)