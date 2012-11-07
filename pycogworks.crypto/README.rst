Installation
============
``pycogworks.crypto`` can be installed with 'pip':

::

  # pip install pycogworks.crypto
  
Dependencies
============
``pycogworks.crypto`` has the following dependencies:

- `PyCrypto <http://pypi.python.org/pypi/pycrypto/2.6>`_

Documentation
=============

pycogworks.crypto.rin2id
------------------------

Generates an encrypted id from a 9 digit RIN.
::

  >>> rin2id(123456789)
  '300fe9abdca99d4a32cb2c43f2a69c5c'
  >>> rin2id('123456789')
  '300fe9abdca99d4a32cb2c43f2a69c5c'