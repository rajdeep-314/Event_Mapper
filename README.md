# Event Mapper

### Developed by :

- [Rajdeep (122301034)](https://github.com/rajdeep-314)
- [Raagam Hitesh Parmar (112301024)](https://github.com/Raagam-Parmar)
- [Souransu Roy (122301038)](https://github.com/Souransu-roy)

<br>

### About

Our application provides a convenient way to manage the events taking place in IIT-Palakkad, making use of the campus's map.

There are two modes available : Visitor and Organizer. <br>
The Visitor mode allows users to take a look at the various events that are taking place in the campus.<br>
The Organizer mode allows users to add or remove events at various locations, on top of the functionality that the visitors have.

 <br>
 
### How to run

Run the following command in your terminal to install Kivy :
```
pip install kivy
```
<br>

Download and extract the zip file from the repository. Open the directory in your terminal and run the following command to run `main.py` :
<br><br>

- LINUX / MacOS:
```
python3 main.py
```
<br>

- Windows:
```
python main.py
```

<br>

### How to use

The application starts with a home page, prompting the user to choose one of the two modes : Visitor or Organizer
<br><br>
<b> Visitor: </b><br><br>
The campus's map is displayed on the screen. The user is free to interact with the map. They can pan it, rotate it and zoom in and out of it as per their convenience. Various pre-defined locations are clickable on the map. Users can click on any of the locations' buttons to open a pop-up window that displays all events taking place at that location, sorted by their date and time. A short description of the event is displayed when the visitor clicks on a particular event. <br><br>
The home button takes the user back to the starting page.

<br>
<b> Organizer: </b><br><br>
Clicking on the Organizer button on the home page opens up a login page. The `i` button on the top-right corner opens a pop-up that displays the rules for making a new username or password. The login page has options to log in or sign up. Only the encrypted passwords are stored. The user can either sign in with valid credentials, or sign up with new credentials. This leads them to the map page.<br><br>
This map page has additional features to enable the organizer to manage events. Clicking on one of the pre-defined locations opens up a pop-up window. At the top is a button for the user to add a new event. Clicking on the button opens a form, where the user is prompted to add information about the event that they want to define, namely the event name, date, time and a short description. Only event names that don't already exist can be defined. A validation is performed on the entered date and time, and the new event is added to the list of events.<br><br>
Events whose names are already taken cannot be defined, and an event must be defined with timings after the current time. Apart from that, the organiser is warned if an event that they're trying to define clashes with another already defined event. The organiser then has options to go ahead with their event or change the timing.<br><br>
Events that the user is organizing are displayed below the "Add event" button, sorted by their date and time. The user has an option to remove each of these events. Below these events, the other events being organized at the venue are displayed, along with information about their date and time and a short description. These events are sorted by their date and time as well.<br><br>
The logout button logs out the user and takes them back to the starting page.

<br><br>

### Implementation details

- We have used the Python based library, Kivy, for developing our GUI.
- SHA512 has been used to encrypt the passwords. The `hashlib` module has been used for the same.
- Python's `datetime` module has been used to handle the timing aspect of the project.
- Python's `functools` module has been used to enable an efficient functionality for the landmark buttons.
- Dictionaries have been used to implement hash tables on the events to enable fast look-ups.
- Real-time input validation has been performed on all text inputs.
- Generator expressions have been used with functions to make some processes faster and more memory-efficient.
- Boolean operators have been used in some places to implement basic conditionals.

<br>

### Contributions

i) Rajdeep :
- Designed the starting and login pages, which manage the credentials database.
- Designed the functionality for adding and removing events, which manages the events database.
- Worked on the formatting of buttons, labels, and other visual elements.
- Compiled the individual portions.
<br>

ii) Raagam Parmar Hitesh :
- Designed the campus map in AutoCAD, using Google's satellite images as reference.
- Designed the map page in the application that handles the map interactions.
<br>

iii) Souransu Roy :
- Worked on the visual aspect of the landmark buttons and the displayed events.
- Designed a base framework for storing and managing events.

<br>

### Appendices

![Nila Map](images/nila_map.png)

An image of the Nila Campus made using AutoCAD
