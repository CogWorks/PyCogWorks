from PySide.QtCore import *
from PySide.QtGui import *

import sys

class Questionnaire( QDialog ):

	def __init__( self, app, file ):
		super( Questionnaire, self ).__init__()

		self.app = app

		self.questionsPerPage = -1

		#self.setModal( True )

		self.data = None
		self.loadFile( file )

		self.main_layout = QVBoxLayout()
		self.questions = QGridLayout()
		#self.questions.setFixedSize(800,600)
		#self.questions.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )

		self.description = None

		self.buttonGroups = []

		row = 0
		q = 1
		for v in self.data:
			if v[0] == '~':
				self.description = v[1]
			elif v[0] == 'H':
				col = 2
				for l in v[1:]:
					self.questions.addWidget( QLabel( l ), row, col )
					col += 1
				row += 1
			elif v[0] == '1':
				bg = QButtonGroup()
				col = 0
				num = QLabel( "%d." % ( q ) )
				num.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
				self.questions.addWidget( num , row, col )
				col += 1
				question = QLabel( v[1] )
				question.setWordWrap( True )
				question.setSizePolicy( QSizePolicy.MinimumExpanding, QSizePolicy.Preferred )
				self.questions.addWidget( question, row, col )
				col += 1
				for l in v[2:]:
					button = QRadioButton( l )
					bg.addButton( button )
					button.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
					self.questions.addWidget( button, row, col )
					col += 1
				QObject.connect( bg, SIGNAL( 'buttonClicked(QAbstractButton *)' ), self.questionClick )
				self.buttonGroups.append( bg )
				row += 1
				q += 1


		self.scrollArea = QScrollArea()
		self.questionsW = QWidget()

		self.questionsW.setLayout( self.questions )
		self.scrollArea.setWidget( self.questionsW )
		if self.description:
			q = QLabel( self.description )
			q.setWordWrap( True )
			self.main_layout.addWidget( q )
		self.main_layout.addWidget( self.scrollArea )
		self.doneButton = QPushButton( "Submit" )
		self.doneButton.setDisabled( True )
		QObject.connect( self.doneButton, SIGNAL( 'clicked(bool)' ), self.submit )
		self.main_layout.addWidget( self.doneButton )
		self.setLayout( self.main_layout )

		self.setWindowTitle( 'Questionnaire' )

		self.show()
		self.activateWindow()
		self.raise_()

		self.setFixedSize( 900, 700 )

		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move( ( screen.width() - size.width() ) / 2, ( screen.height() - size.height() ) / 2 )

	def questionClick( self, button ):
		for b in self.buttonGroups:
			if b.checkedId() == -1:
				self.doneButton.setDisabled( True )
				return
		self.doneButton.setDisabled( False )

	def submit( self, checked ):
		print "Done"
		self.done( 1 )

	def getResults( self ):
		if self.result():
			return map( int, [ b.checkedButton().text() for b in self.buttonGroups ] )
		else:
			return None


	def loadFile( self, file ):

		f = open( file, "rb" )
		self.data = []
		for line in f.readlines():
			self.data.append( line.strip().split( '\t' ) )


def doQuestionnaire( file ):
	app = QApplication( sys.argv )
	q = Questionnaire( app, file )
	app.exec_()
	return q.getResults()
