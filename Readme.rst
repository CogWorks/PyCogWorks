==========
PyCogWorks
==========

``pycogworks`` is a Python package with miscellaneous functions used in the CogWorks lab.

Installation
============
``pycogworks`` can be installed using 'pip'.
::

  # pip install pycogworks
  
Dependencies
============
``pycogworks`` has the following dependencies:

- `PyCrypto <http://pypi.python.org/pypi/pycrypto/2.6>`_
- `PySide <http://qt-project.org/wiki/PySideDownloads>`_

GUI Functions
=============

pycogworks.getSubjectInfo
-------------------------
Creates a GUI dialog to collect subject information. The default dialog collects subjects
first name, last name and RIN. Additional fields can be collected by passing an array
of field names to ``getSubjectInfo``. ``getSubjectInfo`` returns a dict of subject information
where the keys are the field names converted to lower case and spaces replaced with underscores.
The RIN field is automatically encrypted using ``pycogworks.rin2id`` and stored in the 'encrypted_rin' field.
::

  >>> getSubjectInfo(["Age"])
  {'rin': u'123456789', 'first_name': u'Foo', 'last_name': u'Bar', 'age': u'18'}
  
.. image:: http://ompldr.org/vZm5ldw


Logging Functions
=================

pycogworks.getDateTimeStamp
---------------------------
Returns the most accurate timestamp possible for the current OS.
::

  >>> get_time()
  1348684540.905437

pycogworks.getDateTimeStamp
---------------------------

Generates a date/time stamp usefull in logs and for log filenames.
::

  >>> getDateTimeStamp()
  '2012-9-26_13-33-6'

pycogworks.rin2id
-----------------

Generates an encrypted id from a 9 digit RIN.
::

  >>> rin2id(123456789)
  '300fe9abdca99d4a32cb2c43f2a69c5c'
  >>> rin2id('123456789')
  '300fe9abdca99d4a32cb2c43f2a69c5c'

pycogworks.writeHistoryFile
---------------------------

Takes a ``dict`` of subject information and writes a history file.
The subject information dict must contain a field called 'rin' with a value that contains a valid 9 digit RIN.
If the subject information dict does not already contain an 'encrypted_rin' field, the RIN will be enrypted and
added to the subject information dict under the field 'encrypted_rin'. The subject information dict is then encoded 
as a JSON string and written to a file.
::

  >>> writeHistoryFile("test.history",{"foo":"bar","rin":"123456789"})

::
  
  # cat test.history
  {
    "cipher": "AES/CBC (RIJNDAEL) - 16Byte Key", 
    "encrypted_rin": "300fe9abdca99d4a32cb2c43f2a69c5c", 
    "foo": "bar", 
    "rin": "123456789"
  }