import pprint

from maya import cmds

import controllerLibrary
reload(controllerLibrary)
from PySide2 import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The controller library UI is a dialog that lets us save and import controllers.
    """

    def __init__(self):
        # Same as typing QTWidgets.QDialogue.__init__(self). but if you changed what you inherit from you have to change the instances as well.
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')
        # The library variable point to an instance of our controller library.
        self.library = controllerLibrary.ControllerLibrary()
        # Every time we create a new instance we will automatically build our UI and populate it.
        self.buildUI()
        self.populate()

    def buildUI(self):
        """This method builds out the UI"""
        # This is the master layout. add all widgets to this main vertical layout.
        layout = QtWidgets.QVBoxLayout(self)

        # Here we create the first child horizontal widget.
        saveWidget = QtWidgets.QWidget()
        # This is the horizontal layout for Save (it does not mean save the Layout). HBoxLayout must get a widget to apply to = (saveWidget).
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        # Saves layout to QVBoxLayout
        layout.addWidget(saveWidget)

        # First item in saveLayout. It is a line to enter text. We put self in front of it so we can access it in later code.
        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        # This just creates a button, it wont do anything yet.
        saveBtn = QtWidgets.QPushButton('save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # These are the parameters for our thumbnail size.
        size = 64
        buffer = 12
        # This creates an area to view our controls
        self.listWidget = QtWidgets.QListWidget()
        # Displays view a icon mode instead.
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        # Set icon size. QSize gets an (x,y) parameter. Our size = 64 pixels. = 64 x 64 square thumb
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        # Make thumbs adjust to UI size
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        layout.addWidget(self.listWidget)

        # This creates a new widget to hold new buttons at bottom of our UI.
        btnWidget = QtWidgets.QWidget()
        # Assigning layout to (btnWidget)
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        # Adds above to master layout.
        layout.addWidget(btnWidget)

        # now we make the 3 buttons:
        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        # Created a button layout and we must assign it to the widget we made above.
        btnLayout.addWidget(importBtn)

        refreshBtn = QtWidgets.QPushButton('Refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)

    def populate(self):
        """ ^^This clears the list widget and then repopulates it with the contents of our library."""
        self.listWidget.clear()
        # Finds all existing controllers
        self.library.find()

        # Goes through controllers and adds them to UI.
        for name, info in self.library.items():
            # Creating a list
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

            # Adds screenshot to each item. gets screenshot from the info dictionary we made.
            screenshot = info.get('screenshot')
            if screenshot:
                # Icon class is in QtGui.
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return

        name = currentItem.text()
        self.library.load(name)

    def save(self):
        name = self.saveNameField.text()
        if not name.strip():
            cmds.warning("You must give a name.")
            return

        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

def showUI():
    """
    This shows and returns a handle to the UI.
    Returns:
        QDialog
    """
    ui = ControllerLibraryUI()
    ui.show()
    return ui



"""With the Controller Library complete, there's still more that you can do to improve it if you like:
If a controller has no icon, it currently looks out of place in our UI. 
You could have a default image that is displayed when there is no screenshot.
Controllers are simply loaded into the scene. 
It might be nice if they are positioned to any currently selected object in the scene.
 You could do this by constraining them after loading them, and then delete the constraint.
If I save a controller with the same name as an existing one, it just overwrites it. 
You could check if there is a controller with that name already and provide a warning to the user if there is.
"""

