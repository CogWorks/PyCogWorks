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
import gzip

get_time = time.time
if platform.system() == 'Windows':
    get_time = time.clock
getTime = get_time

def getDateTimeStamp():
    d = datetime.datetime.now().timetuple()
    return "%d-%02.d-%02.d_%02.d-%02.d-%02.d" % (d[0], d[1], d[2], d[3], d[4], d[5])
    
def writeHistoryFile(filename, subjectInfo):
    if not 'rin' in subjectInfo:
        raise Exception("Can't write history file, 'rin' field missing.")
    elif not 'encrypted_rin' in subjectInfo:
        raise Exception("Can't write history file, 'encrypted_rin' field missing.")
    elif not 'cipher' in subjectInfo:
        raise Exception("Can't write history file, 'cipher' field missing.")
    history = open(filename, 'w')
    history.write(json.dumps(subjectInfo, sort_keys=True, indent=4))
    history.close()
    
class Logger():
    
    def __init__(self, header, delim="\t", newline="\n", filler="NA"):
        self.header = header
        self.delim = delim
        self.newline = newline
        self.filler = filler
        
    def open(self, filename, compresslevel=0):
        if file:
            if self.compresslevel:
                self.file = gzip.open("%s.gz" % filename, "w", self.compresslevel)
            else:
                self.file = open(filename, "w")
        else:
            self.file = sys.__stdout__
        self.file.write(self.delim.join(header))
        self.file.write(self.newline)
        
    def write(self, **kwargs):
        if self.file:
            line = [self.filler] * len(self.header)
            for k, v in kwargs.iteritems():
                if k in self.header:
                    line[self.header.index(k)] = str(v)
            self.file.write(self.delim.join(line))
            self.file.write(self.newline)
        
    def close(self):
        if self.file != sys.__stdout__:
            self.file.close()
            self.file = None