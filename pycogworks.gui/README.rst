Installation
============
``pycogworks.gui`` can be installed with 'pip':
::

  # pip install pycogworks.gui
  
Dependencies
============
``pycogworks.gui`` has the following dependencies:

- `PySide <http://qt-project.org/wiki/PySideDownloads>`_

Documentation
=============

pycogworks.gui.getSubjectInfo
-----------------------------
Creates a GUI dialog to collect subject information. The default dialog collects subjects
first name, last name and RIN. Additional fields can be collected by passing an array
of field names to ``getSubjectInfo``. ``getSubjectInfo`` returns a dict of subject information
where the keys are the field names converted to lower case and spaces replaced with underscores.
The RIN field is automatically encrypted using ``pycogworks.rin2id`` and stored in the 'encrypted_rin' field.
::

  >>> getSubjectInfo(["Age"])
  {'rin': u'123456789', 'first_name': u'Foo', 'last_name': u'Bar', 'age': u'18'}
  
.. image:: http://ompldr.org/vZm5ldw

pycogworks.gui.doQuestionnaire
------------------------------
THIS NEED DOCUMENTATION AND AN EAMPLE!!!