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

import sys

from PySide.QtCore import *
from PySide.QtGui import *

from pycogworks.crypto import rin2id

class SubjectWindow(QDialog):
    
    def __init__(self, app, custom_fields=None):
        super(SubjectWindow, self).__init__()
        self.app = app
        
        self.fields = ['First Name', 'Last Name', 'RIN']
        if custom_fields:
            self.fields += custom_fields 
        
        self.values = None
        
        self.setModal(True)
    
        self.main_layout = QVBoxLayout()
        
        self.settings_layout = QGridLayout()
        
        self.field_widgets = {}
        row = 0
        for field in self.fields:
            self.settings_layout.addWidget(QLabel(field), row, 0)
            self.field_widgets[field] = QLineEdit()
            self.settings_layout.addWidget(self.field_widgets[field], row, 1)
            if field == 'RIN':
                self.field_widgets[field].setMaxLength(9)
                QObject.connect(self.field_widgets[field], SIGNAL('textChanged(const QString&)'), self.rin_changed)
            row += 1
        
        self.mainButtons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.ok = self.mainButtons.button(QDialogButtonBox.StandardButton.Ok)
        self.ok.setEnabled(False)
        self.cancel = self.mainButtons.button(QDialogButtonBox.StandardButton.Cancel)
        QObject.connect(self.mainButtons, SIGNAL('clicked(QAbstractButton *)'), self.mainbutton_clicked)
        
        self.main_layout.addLayout(self.settings_layout)
        self.main_layout.addWidget(self.mainButtons)
        
        self.setLayout(self.main_layout)
        
        self.setWindowTitle('Participant Information')
        
        self.show()
        self.activateWindow()
        self.raise_()
        
        self.setMinimumWidth(self.geometry().width()*1.2)
        
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
        
    def rin_changed(self, rin):
        self.ok.setEnabled(unicode(rin).isnumeric() and len(rin) == 9)
        
    def mainbutton_clicked(self, button):
        if button == self.ok:
            self.values = {}
            for field in self.field_widgets:
                self.values[field.lower().replace(" ","_")] = self.field_widgets[field].text()
            self.values['encrypted_rin'], self.values['cipher'] = rin2id(self.values['rin'])
            self.setResult(True)
            self.done(True)
        elif button == self.cancel:
            self.setResult(False)
            self.done(True)
            
def getSubjectInfo(custom_fields=['Age']):
    app = QApplication(sys.argv)
    sw = SubjectWindow(app,custom_fields)
    app.exec_()
    return sw.values

if __name__ == '__main__':
    print getSubjectInfo()