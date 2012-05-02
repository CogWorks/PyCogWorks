from setuptools import setup
from pycogworks import __version__ as version
import os.path

descr_file = os.path.join( os.path.dirname( __file__ ), 'README' )

setup( 
    name = 'PyCogWorks',
    version = version,
    
    packages = ['pycogworks'],

    description = 'Miscellaneous functions used in the CogWorks lab.',
    long_description = open( descr_file ).read(),
    author = 'Ryan Hope',
    author_email = 'rmh3093@gmail.com',
    url = 'https://github.com/CogWorks/PyCogWorks',
    classifiers = [
				'License :: OSI Approved :: GNU General Public License (GPL)',
				'Programming Language :: Python :: 2',
				'Topic :: Scientific/Engineering',
				'Topic :: Utilities',
    ],
	license = 'GPL-3',
	install_requires = [
					'setuptools',
	],
 )
