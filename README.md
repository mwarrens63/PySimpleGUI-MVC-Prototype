# PySimpleGUI-MVC-Prototype
This code demonstrates using PySimpleGUI and the peewee ORM to develop an MVC flight reservations demo system.  Most of the GUI (reservationsView) code was initially written while following a very good YouTube tutorial provided by The CS Classroom (Intro To PySimpleGUI: An 8-Part Tutorial Series (with databases)).  After completing tutorials 1-6, I decided to rewrite the tutorial code as an MVC design using Python classes to implement the reservations View.  

The View is implemented as three Python classes using PySimpleGUI.  The View displays forms and tables for entering, displaying, and editing reservations data, and it validates all user input.  I have not seen other examples on the Web of using PySimpleGUI within Python classes, but I found it much more convenient than a procedural approach.

The Model is a Python module that uses the peewee ORM connected to a Sqlite database.  It uses the peewee ORM classes/methods to create and manage Sqlite tables for the reservations database.  It also implements low level CRUD methods for the reservations database.

The Controller is a Python module that connects the View and Model.  The Controller provides high-level CRUD methods connecting the View to the Model.  It converts the data retrieved from the Model to a format that is usable by the View.  For example, the PySimpleGUI tree widget requires data formatted as TreeData.  The Controller also updates the View whenever the Model has changed after an update or deletion.

A detailed description of this code is provided in the Wiki pages above.
