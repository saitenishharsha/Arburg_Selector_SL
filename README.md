# Samplefptarburg

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Creating an Executable File](#creating-an-executable-file)
- [Usage Instructions](#usage-instructions)
- [Usage Examples](#usage-examples)
- [Contact Support](#contact-support)

---

## Introduction
Samplefptarburg is a Python application designed to simplify the process of selecting robot specifications. Users often struggle to remember their previous selections, which can lead to confusion and inefficiency. This application addresses that issue by generating a unique hexadecimal value based on the selected combinations of specifications. With the hexadecimal value, users can easily retrieve their previously chosen robot configurations.

The application encodes and decodes robot specifications into hexadecimal format.

Samplefptarburg provides a user-friendly interface for managing various aspects of robot data, including:

- **Robot Types:** Different categories of robots.
- **Robot Names:** Specific names or models within each type.
- **Gripper Types:** Various types of grippers available.
- **Communication Protocols:** Methods of communication supported by the robots.
- **Addons:** Additional features or components that can be included with the robots.

This intuitive interface makes it easy for users to configure and manage their robot specifications effectively.

---

## Features
- **Hexadecimal Code Generation:** Input robot specifications to generate a corresponding hexadecimal code.
- **Hexadecimal Code Decoding:** Input a hexadecimal code to retrieve detailed robot specifications.
- **PDF Export:** Export the generated specifications as a PDF file to a user-defined directory.
- **Clipboard Support:** Easily copy the generated hexadecimal code to the clipboard.
- **Intuitive GUI:** Built with the Tkinter library for a seamless user experience.

---

## Requirements

### To open the application as an executable:
- **Executable File:** Ensure you have the `Samplefptarburg.exe` file in your chosen directory.

### To run the GUI with the Python script:
- **Python Version:** Python 3.12.7. Download Python [here](https://www.python.org/downloads/) if not already installed.

### Dependencies:
- **Tkinter:** Usually included with Python installations (version 8.6.13).
- **pyperclip:** 1.9.0.
- **fpdf:** 1.7.2.
- **pyinstaller:** 6.10.0.

### Packages to be installed:
```bash
pip install pyperclip fpdf
pip install pyinstaller
```
## Creating an Executable File
If you want to create your own executable file `Samplefptarburg.exe` from the Python script, you can use PyInstaller.

Follow these steps:
Open a Command Prompt or Terminal: Navigate to the directory where your Python script `arburgupdated.py` is located.

Run PyInstaller: Execute the following command:
```bash
python -m PyInstaller --onefile --windowed --name "Samplefptarburg" --icon "app_icon.ico" --hidden-import pyperclip --hidden-import fpdf arburgupdated.py
```
- **python -m PyInstaller:** Runs PyInstaller as a module, helping avoid command not found issues.
- **onefile:** Packages everything into a single executable file.
- **windowed:** Prevents a console window from appearing when you run the application (useful for GUI applications).
- **name "Samplefptarburg":** Sets the name of the executable file.
- **icon "app_icon.ico":** Specifies the icon file to use for the application.
- **hidden-import pyperclip --hidden-import fpdf:** Specifies any hidden imports that PyInstaller might not automatically detect.
- **arburgupdated.py:** The name of your Python script.

- **Locate the Executable:** After the process completes, you will find the executable file in the `dist` folder within your script's directory.

- **Run the Executable:**You can now run `Samplefptarburg.exe` from the dist folder or move it to your desired directory.

## Usage Instructions for Application

- **Launch the Application:** Double-click the `Samplefptarburg.exe` file.
- **Select Robot Specifications:**
   - Choose the robot type, robot name, and gripper type from the dropdown menus.
   - Select the desired communication protocols (as many as you want) and addons (as many as you want) using checkboxes.
- **Generate Hexadecimal Code:** Click the "Get Specifications" button to generate the hexadecimal code based on your selections.
- **Decode Hexadecimal Code:** Enter a hexadecimal code in the provided input field and click "Get Specifications" to retrieve the corresponding robot specifications.
-  **Display Specifications:** Specifications are displayed in a tree view.
- **Export to PDF:** Click "Export to PDF" to save the specifications as a PDF.
- **Copy Code:** Use "Copy Code" to copy the hexadecimal code to your clipboard.
- **Clear Selections:** Click "Clear" to reset all fields and selections.

---

## Usage Instructions for GUI (Python Script)

Follow the same steps as above, starting by running the Python script to launch the GUI.

---

## Usage Examples

### Generating Hexadecimal Value

**Example 1:**

- **Input:**
  - Robot Type: Iontec
  - Robot Name: KR 20 R3100 Iontec
  - Gripper: Vacuum Gripper
  - Communication Protocols: WIFI, EtherCAT, 5G, Profinet, TCP/IP
  - Addons: FSD, AGV, Vision System, Conveyor Belt

- **Output:**
  - Hexadecimal Value: `0x100170043cc10f000`

---

**Example 2:**

- **Input:**
  - Robot Type: Cybertech nano-2
  - Robot Name: KR 6 R1840-2 Cybertech nano
  - Gripper: Magnetic
  - Communication Protocols: Bluetooth, UDP, FTP, SNMP
  - Addons: Path Planning, Palletizing, Cobot, ROS

- **Output:**
  - Hexadecimal Value: `0x3001c004211c00a60`

---

### Retrieving Robot Specifications

**Example 1:**

- **Input:**
  - Hexadecimal Value: `0x50023004701194802`

- **Output:**
  - Robot Type: KR4 und Scara
  - Robot Name: KR6 R500 Z200-2 Scara
  - Gripper: Soft Hand
  - Communication Protocols: UDP, Profinet, CAN Bus, LonWorks
  - Addons: FSD, Path Planning, Sensor Kit

---

**Example 2:**

- **Input:**
  - Hexadecimal Value: `0x4002000450c024104`

- **Output:**
  - Robot Type: Agilus-2
  - Robot Name: KR6 R900-2 AGILUS
  - Gripper: Pneumatic
  - Communication Protocols: 5G, TCP/IP, BACnet
  - Addons: FSD, Tool Changer, Gripper Kit

---
