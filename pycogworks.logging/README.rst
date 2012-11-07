Installation
============
``pycogworks.logging`` can be installed with 'pip':
::

  # pip install pycogworks.logging

Documentation
=============

pycogworks.logging.getTime, pycogworks.logging.get_time
-------------------------------------------------------

Returns the most accurate timestamp possible for the current OS.
::

  >>> getTime()
  1348684524.934422
  >>> get_time()
  1348684540.905437
    
pycogworks.logging.getDateTimeStamp
-----------------------------------

Generates a date/time stamp usefull in logs and for log filenames.
::

  >>> getDateTimeStamp()
  '2012-09-26_13-33-06'

pycogworks.logging.writeHistoryFile
-----------------------------------

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