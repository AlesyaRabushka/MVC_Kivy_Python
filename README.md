<h1 align="center">Vet Clinic</h1>

# Description
**Vet Clinic** is a simple interface application that was inspired by registration database

It contains add, search and delete dialogs to communicate with the data

## MVC pattern
The application has been created as an example of [MVC](https://developer.mozilla.org/en-US/docs/Glossary/MVC) pattern
with [Kivy](https://kivy.org/doc/stable/) and [KivyMD](https://kivymd.readthedocs.io/en/latest/) Python

It contains model, controller and view classes 
- **Model**:
    Contains one class Model that is responsible for XML parsing 
- **Controller**:
    Is one class that filters the input data and provides communication between Model and View classes
- **View**:
    Is presented by a set of classes each of which is responsible for the presentation of each dialog window
    + *MainScreen* - the main screen of the App from which all other windows are called
    + *AddPopup* - adds new pet records
    + *SearchPopup* - searches for particular records by the given parameters
    + *DeletePopup* - deletes particular records by the given parameters
    + *EmailLetterPopup* - is called from DeletePopup and provides a choice of sending an email to pet owner (opens *default browser* on [mail.ru](https://e.mail.ru/drafts/) page), *but only if one record has been found* 
  ````
  import webbrowser
      def open_mail(self):
        # opens default browser
        webbrowser.open_new('https://e.mail.ru/drafts/')
  ````
    + *FoundPopup* - is opened from SearchPopup and is used for show the table with searched data records
    + *HandlerPopup* - adds pet handler information (is called after correct registration in AddPopup)
    + *InformationPopup* - shows more pet records information by clicking on checkbox on the main screen table
    + *WarningPopup* - appears as a result of XML Parsing Error 
    + *HelperPopup* - has no methods, just shows the **Vet Clinic** contact info
    
## Interface
The whole interface of the App is placed in *[myscreen.kv](https://github.com/AlesyaRabushka/MVC_Kivy_Python/blob/main/View/myscreen.kv)* file and is written in special [Kivy Language](https://kivy.org/doc/stable/guide/lang.html)

Here is the example of Main Screen

<img src="https://github.com/AlesyaRabushka/MVC_Kivy_Python/blob/main/src/MainScreen.jpg">

## XML Parsing

- In this App is used [Minimal DOM implementation](https://docs.python.org/3/library/xml.dom.minidom.html) for fill the XML file with information
- [SAX Parser](https://docs.python.org/3/library/xml.sax.handler.html) is used for reading XML file, it is placed in [Model/sax_parser.py](https://github.com/AlesyaRabushka/MVC_Kivy_Python/blob/main/Model/sax_parser.py)

There are three XML files, to use one of them you should change the name of parsed file in [Model/myscreen.py](https://github.com/AlesyaRabushka/MVC_Kivy_Python/blob/main/Model/myscreen.py) where *'pet.xml'* - is the name of the file you want to use
````
# line 274
file = open('pet.xml', 'w')

# line 330
file = open('pet.xml', 'w')

# line 345
parser.parse('pet.xml')
````
First two lines are parts of [Minimal DOM implementation](https://docs.python.org/3/library/xml.dom.minidom.html) parsing
The third one - [SAX Parser](https://docs.python.org/3/library/xml.sax.handler.html)

## How to use

To use this App it is required to install **kivy** and **kivymd** libraries

You can do it in a way provided by PyCharm (File -> Settings -> Project: your_project_name -> Python Interpreter)
or on your own using Terminal
````
pip install "kivy[base] @https://github.com/kivy/kivy/archive/master.zip"    
pip install https://github.com/kivymd/KivyMD/archive/master.zip
````
