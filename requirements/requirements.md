# General Overview

Generate a GUI for the command-line password manager `pass` using GTK4 for the Gnome Desktop Environment. 
This project should call the `pass` command as child processes to retrieve data. 
It must not make any changes to the saved passwords. 

# Features
The UI should consist of two main elements:
* A list of all password folder on the left, displaying nested folders in a tree structure.
* A list of all password files in in the selected folder. For every file, show:
    * the file name as `username`
    * the password as a read-only text field masked with asterisks.
    * a button to copy the password to the clipboard. (make call to `pass -c`) next to the password field
    * a button to unmask the password next to the password field

# Packaging
Generate a PKGBUILD file so that this tool can be installed on arch linux by calling `makepkg` in the root directory.