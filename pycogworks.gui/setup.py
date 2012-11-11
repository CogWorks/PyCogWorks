from setuptools import setup
import os.path

__version__ = '0.4.1'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='pycogworks.gui',
    version=__version__,
    
    namespace_packages=['pycogworks'],
    packages=['pycogworks.gui'],

    description='GUI functions used in the CogWorks lab.',
    long_description=open(descr_file).read(),
    author='Ryan Hope',
    author_email='rmh3093@gmail.com',
    url='https://github.com/CogWorks/PyCogWorks',
    classifiers=[
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Programming Language :: Python :: 2',
                'Topic :: Scientific/Engineering',
                'Topic :: Utilities',
                'Environment :: X11 Applications :: Qt'
    ],
    license='GPL-3',
	install_requires=[
					'pyside',
                    'pycogworks.crypto'
	]
 )
