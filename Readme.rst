==========
PyCogWorks
==========

``pycogworks`` is a Python package with miscellaneous functions used in the CogWorks lab.

Logging Functions
=================

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
The RIN is enrypted and added to the subject information dict under the field 'encrypted_rin'. The new
subject information dict is then encoded as a JSON string and written to a file.
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