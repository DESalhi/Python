# Currency Converter Program
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from pathlib import Path

# Function to get the conversion value
def getVal(cont1, cont2):
    cont1val = cont1.split("-")[1].strip()
    cont2val = cont2.split("-")[1].strip()
    url = f"https://free.currconv.com/api/v7/convert?q={cont1val}_{cont2val}&compact=ultra&apiKey=b43a653672c4a94c4c26"
    r = requests.get(url)
    if r.status_code != 200:
        print("Error fetching data.")
        exit()
    try:
        data = r.json()
        valCurr = data[f"{cont1val}_{cont2val}"]
    except KeyError:
        print("Server response invalid.")
        exit()
    return valCurr

# Application configuration
app = QApplication([])

# Define the base directory and file paths
base_dir = Path.cwd() / "currency converter"
ui_path = base_dir / "gui.ui"
country_file_path = base_dir / "country.txt"

# Load the user interface
window = uic.loadUi(ui_path)

# Read the country file
with open(country_file_path, "r") as f:
    country_data = f.readlines()

# Populate the dropdowns
window.dropDown1.addItem("Select")
window.dropDown2.addItem("Select")
for line in country_data:
    line = line.strip()
    if line:
        window.dropDown1.addItem(line)
        window.dropDown2.addItem(line)

# Add a validator for the input
intOnly = QDoubleValidator()
window.lineEdit.setValidator(intOnly)

# Main function to connect the button
def main():
    window.pushButton.clicked.connect(changeBtn)

# Callback function for the button
def changeBtn():
    val = window.lineEdit.text()
    cont1 = window.dropDown1.currentText()
    cont2 = window.dropDown2.currentText()
    if cont1 == "Select" or cont2 == "Select":
        print("Please select valid currencies.")
        return
    try:
        valCurr = getVal(cont1, cont2)
        window.lcdpanel.display(float(val) * valCurr)
    except Exception as e:
        print(f"Error: {e}")

# Run the application
main()
window.show()
app.exec()
