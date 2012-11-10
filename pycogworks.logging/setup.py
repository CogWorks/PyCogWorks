from setuptools import setup
import os.path

__version__ = '0.4.2'

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='pycogworks.logging',
    version=__version__,
    
    namespace_packages=['pycogworks'],
    packages=['pycogworks.logging'],

    description='Logging functions used in the CogWorks lab.',
    long_description=open(descr_file).read(),
    author='Ryan Hope',
    author_email='rmh3093@gmail.com',
    url='https://github.com/CogWorks/PyCogWorks',
    classifiers=[
                'License :: OSI Approved :: GNU General Public License (GPL)',
                'Programming Language :: Python :: 2',
                'Topic :: Scientific/Engineering',
                'Topic :: Utilities'
    ],
    license='GPL-3'
 )
