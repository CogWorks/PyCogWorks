import sys, os

from PySide.QtCore import *
from PySide.QtGui import *

import json
import datetime

class SubjectWindow(QDialog):
    
    def __init__(self, app, minimal=False):
        super(SubjectWindow, self).__init__()
        self.app = app
        self.minimal = minimal
        
        self.values = None
        
        self.setModal(True)
    
        self.main_layout = QVBoxLayout()
        
        self.settings_layout = QGridLayout()
        
        self.settings_layout.addWidget(QLabel('First Name'), 0, 0)
        self.first_name = QLineEdit()
        self.settings_layout.addWidget(self.first_name, 0, 1)
        
        self.settings_layout.addWidget(QLabel('Last Name'), 1, 0)
        self.last_name = QLineEdit()
        self.settings_layout.addWidget(self.last_name, 1, 1)
        
        self.settings_layout.addWidget(QLabel('RIN'), 2, 0)
        self.rin = QLineEdit()
        self.rin.setMaxLength(9)
        QObject.connect(self.rin, SIGNAL('textChanged(const QString&)'), self.rin_changed)
        self.settings_layout.addWidget(self.rin, 2, 1)
        
        if not self.minimal:
        
            self.settings_layout.addWidget(QLabel('Age'), 3, 0)
            self.age = QLineEdit()
            self.settings_layout.addWidget(self.age, 3, 1)
            
            self.settings_layout.addWidget(QLabel('Gender'), 4, 0)
            self.gender = QLineEdit()
            self.settings_layout.addWidget(self.gender, 4, 1)
            
            self.settings_layout.addWidget(QLabel('Major'), 5, 0)
            self.major = QLineEdit()
            self.settings_layout.addWidget(self.major, 5, 1)
        
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
        if len(rin) == 9:
            try:
                if int(rin) > 0:
                    self.ok.setEnabled(True)
            except ValueError:
                pass
        else:
            self.ok.setEnabled(False)
    
    def mainbutton_clicked(self, button):
        if button == self.ok:
            self.values = {'first_name': self.first_name.text(),
                           'last_name': self.last_name.text(),
                           'rin': self.rin.text()}
            if not self.minimal:
                self.values['age'] = self.age.text()
                self.values['gender'] = self.gender.text()
                self.values['major'] = self.major.text()
            self.setResult(True)
            self.done(True)
        elif button == self.cancel:
            self.setResult(False)
            self.done(True)
            
def getSubjectInfo(minimal=False):
    app = QApplication(sys.argv)
    sw = SubjectWindow(app,minimal)
    app.exec_()
    return sw.values

def makeLogFileBase(prefix):
    d = datetime.datetime.now().timetuple()
    if prefix:
        return "%s_%d-%d-%d_%d-%d-%d"%(prefix, d[0], d[1], d[2], d[3], d[4], d[5])
    else:
        return "%d-%d-%d_%d-%d-%d"%(d[0], d[1], d[2], d[3], d[4], d[5])
    

def writeHistoryFile(basename, subjectInfo):
    history = open(basename + ".history", 'w')
    history.write(json.dumps(subjectInfo, sort_keys=True, indent=4))
    history.close()

if __name__ == '__main__':
    print getSubjectInfo()