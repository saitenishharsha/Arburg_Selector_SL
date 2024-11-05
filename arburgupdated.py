# This program encodes and decodes robot specifications, such as robot type, robot name, gripper type, communication protocols, and addons into binary and hexadecimal representations using a seperate interface
# It allows users to either:
# 1. Input robot specifications to generate a hexadecimal code, or
# 2. Input a hexadecimal code to retrieve the robot's specifications.
# The generated results can be exported as a PDF to a user-specified directory for future reference.

import tkinter as tk # Import tkinter library for GUI
from tkinter import ttk # Import themed tkinter widgets
from tkinter import messagebox # Import messagebox for displaying alerts
import pyperclip #  Import pyperclip library for clipboard operations
from fpdf import FPDF # Import FPDF for PDF generation
from tkinter import filedialog # Import filedialog for file saving dialogs 

class RobotInterface:
    def select_robot(self):
        self.robot_combobox.config(state="readonly") # Set robot type combobox to readonly
        self.color_combobox.config(state="readonly") # Set robot name combobox to readonly
        self.gripper_combobox.config(state="readonly") # Set gripper combobox to readonly
        self.communication_protocols_frame.config(state="normal") # Enable communication protocols frame
        self.addons_frame.config(state="normal") # Enable addons frame
        self.hexadecimal_entry.config(state="readonly") # Set hexadecimal entry to readonly
        self.hexadecimal_button.config(state="normal") # Enable hexadecimal button
        self.robot_button.config(state="disabled") # Disable robot button
    
    def select_hexadecimal(self):
        self.robot_combobox.config(state="readonly") # Set robot type combobox to readonly
        self.color_combobox.config(state="readonly") # Set robot name combobox to readonly
        self.gripper_combobox.config(state="readonly") # Set gripper combobox to readonly
        for widget in self.communication_protocols_checkbuttons_frame.winfo_children():
            widget.config(state="normal") # Enable all communication protocol checkbuttons
        for widget in self.addons_checkbuttons_frame.winfo_children():
            widget.config(state="normal") # Enable all addons checkbuttons
        self.hexadecimal_entry.config(state="normal") # Enable hexadecimal entry
        self.robot_button.config(state="disabled") # Disable robot button
        self.hexadecimal_button.config(state="normal") # Enable hexadecimal button
    
    def export_to_pdf(self):
        hex_value = self.hexadecimal_entry.get() # Get the hexadecimal value from the entry
        if hex_value:
            try:
                # Decode hexadecimal value to retrieve robot specifications
                decoded_robot, decoded_color, decoded_gripper, decoded_communication_protocols, decoded_addons = self.decode_hexadecimal(hex_value)
                data = [
                    ["Robot", decoded_robot],
                    ["Color", decoded_color],
                    ["Gripper", decoded_gripper],
                    ["Communication Protocols", ', '.join(decoded_communication_protocols)],
                    ["Addons", ', '.join(decoded_addons)],
                    ["Hexadecimal Value", hex_value]
                ]
            except Exception as e:
                messagebox.showerror("Error", "Invalid hexadecimal value") # Show error, if decoding fails
                return
        else:
            # Retrieve specifications directly from GUI fields if no hex value is provided
            robot = self.robot_combobox.get()
            color = self.color_combobox.get()
            gripper = self.gripper_combobox.get()
            communication_protocols = [protocol for protocol, var in self.communication_protocols_checkbuttons.items() if var.get()]
            addons = [addon for addon, var in self.addons_checkbuttons.items() if var.get()]
            
            # Check if all required fields are filled
            if robot != "No selection" and color != "No selection" and gripper != "No selection" and communication_protocols and addons:
                data = [
                    ["Robot", robot],
                    ["Color", color],
                    ["Gripper", gripper],
                    ["Communication Protocols", ', '.join(communication_protocols)],
                    ["Addons", ', '.join(addons)],
                    ["Hexadecimal Value", self.hexadecimal_entry.get()]
                ]
            else:
                messagebox.showerror("Error", "Please enter a hexadecimal value or select all options") # Show error, if fields are missing
                return

        # Open a file dialog to save the PDF
        file_name = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_name:
            pdf = FPDF() # Create a PDF Object
            pdf.add_page()  # Add a new page to the PDF
            pdf.set_font("Arial", size=15) # Set font for the PDF title
            pdf.cell(200, 10, txt="Robot Specifications", ln=True, align='C') # Add title
            pdf.ln(10) # Add a blank line
            pdf.set_font("Arial", size=12) # Set font size for the content
            for row in data:
                pdf.cell(200, 10, txt=row[0] + ": " + row[1], ln=True, align='L') # Add each row of data to the PDF
            pdf.output(file_name) # Save the PDF to the specified file

            messagebox.showinfo("Success", "Robot specifications exported to " + file_name) # Show success message after export
            
    def __init__(self, root):
        self.root = root # Store the root window
        self.root.title("Robot Specifications") # Set the window title
        self.cleared = False # Flag to track if the interface has been cleared

        # Dictionaries mapping robot names, colors, grippers, communication protocols, and addons to their 16-bit binary representations.
        # These dictionaries enable easy lookup for encoding and decoding robot specifications.
        
        # Robot types dictionary
        self.robot_dict = {
            "Iontec": "0000000000000001",
            "Cybertech-2": "0000000000000010",
            "Cybertech nano-2": "0000000000000011",
            "Agilus-2": "0000000000000100",
            "KR4 und Scara": "0000000000000101",
            "KR12 Scara": "0000000000000110",
            # "Robot 7": "0000000000000111",
            # "Robot 8": "0000000000001000",
            # "Robot 9": "0000000000001001",
            # "Robot 10": "0000000000001010",
            # "Robot 11": "0000000000001011",
            # "Robot 12": "0000000000001100",
            # "Robot 13": "0000000000001101",
            # "Robot 14": "0000000000001110",
            # "Robot 15": "0000000000001111",
            # "Robot 16": "0000000000010000"
        }

        # Robot names dictionary 
        self.color_dict = {
            "KR 20 R3100 Iontec": "0000000000010111",
            "KR 30 R2100 Iontec": "0000000000011000",
            "KR 08 R2010 Cybertech-2": "0000000000011001",
            "KR 12 R1810 Cybertech-2": "0000000000011010",
            "KR 16 R1610 Cybertech-2": "0000000000011011",
            "KR 6 R1840-2 Cybertech nano": "0000000000011100",
            "KR 8 R1640-2 Cybertech nano": "0000000000011101",
            "KR 10 R1440-2 Cybertech nano": "0000000000011110",
            "KR6 R700-2 AGILUS": "0000000000011111",
            "KR6 R900-2 AGILUS": "0000000000100000",
            "KR10 R900-2 AGILUS": "0000000000100001",
            "KR4 R600 Agilus": "0000000000100010",
            "KR6 R500 Z200-2 Scara": "0000000000100011",
            "KR12 R650 Z400 Scara": "0000000000100100",
            "KR12 R750 Z400 Scara": "0000000000100101",
            "KR12 R850 Z400 Scara": "0000000000100110"
        }

        # Gripper types dictionary
        self.grippers_dict = {
            "Hydraulic": "0000000001000001",
            "Magnetic": "0000000001000010",
            "Vacuum Gripper": "0000000001000011",
            "Sys Parallel Gripper": "0000000001000100",
            "Pneumatic": "0000000001000101",
            "Electric": "0000000001000110",
            "Soft Hand": "0000000001000111",
            "Needle": "0000000001001000",
            "Three-Finger": "0000000001001001",
            "Angled": "0000000001001010",
            "Adhesive": "0000000001001011",
            "Suction Cup": "0000000001001100",
            "Clamp": "0000000001001101",
            "Hook": "0000000001001110",
            "Screwdriver": "0000000001001111",
            "Welding Torch": "0000000001010000"
        }

        # Communication protocols dictionary
        self.communication_protocols_dict = {
            "WIFI": "0000000001010101",
            "EtherCAT": "0000000001010110",
            "Hardwiring": "0000000001010111",
            "Bluetooth": "0000000001011000",
            "5G": "0000000001011001",
            "TCP/IP": "0000000001011010",
            "OPC UA": "0000000001011011",
            "UDP": "0000000001011100",
            "FTP": "0000000001011101",
            "SNMP": "0000000001011110",
            "SPI/I2C": "0000000001011111",
            "Profinet": "0000000001100000",
            "CAN Bus": "0000000001100001",
            "Modbus": "0000000001100010",
            "BACnet": "0000000001100011",
            "LonWorks": "0000000001100100"
        }
        
        # Addons dictionary
        self.addons_dict = {
            "Conveyor Belt": "0000000001100101",
            "FSD": "0000000001100110",
            "AGV": "0000000001100111",
            "Vision System": "0000000001101000",
            "Path Planning": "0000000001101001",
            "Safety System": "0000000001101010",
            "Palletizing": "0000000001101011",
            "Tool Changer": "0000000001101100",
            "Robot Controller": "0000000001101101",
            "Cobot": "0000000001101110",
            "ROS": "0000000001101111",
            "Data Storage": "0000000001110000",
            "Robot Arm": "0000000001110001",
            "Gripper Kit": "0000000001110010",
            "Sensor Kit": "0000000001110011",
            "Actuator Kit": "0000000001110100"
        }
        
        # Create a dictionary to map binary values to robots
        self.binary_to_robot = {}
        for robot, binary in self.robot_dict.items():
            self.binary_to_robot[binary] = robot # Map binary values to robot names
            
        # Create a main frame to hold all the widgets
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)  # Expand the main frame to fill the window

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.TOP, fill="x") # Pack the button frame at the top

        # Create a frame to hold the top buttons
        self.top_button_frame = tk.Frame(self.button_frame)
        self.top_button_frame.pack(side=tk.TOP, fill="x") # Pack the top button frame

        # Create a frame to hold the top buttons in the middle
        self.top_button_frame_middle = tk.Frame(self.top_button_frame)
        self.top_button_frame_middle.pack(side=tk.TOP, fill="x", expand=True) # Expand the middle frame

        # Create a frame to hold the top buttons in the middle left
        self.top_button_frame_middle_left = tk.Frame(self.top_button_frame_middle)
        self.top_button_frame_middle_left.pack(side=tk.LEFT, fill="x", expand=True)  # Left side frame

        # Create a frame to hold the top buttons in the middle right
        self.top_button_frame_middle_right = tk.Frame(self.top_button_frame_middle)
        self.top_button_frame_middle_right.pack(side=tk.RIGHT, fill="x", expand=True) # Right side frame

        # Create a frame to hold the top buttons in the middle center
        self.top_button_frame_middle_center = tk.Frame(self.top_button_frame_middle)
        self.top_button_frame_middle_center.pack(side=tk.LEFT, fill="x", expand=True)  # Center side frame
        
        # # Create a frame to hold the company logos
        # self.company_logos_frame = tk.Frame(self.top_button_frame, width=400, height=100)
        # self.company_logos_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Frame for placing the company logos

        # # Load the company logos
        # self.company_logo = tk.PhotoImage(file="fptlogo.png")
        # self.partnered_company_logo = tk.PhotoImage(file="arburglogo.png") # Load the company logos from the specific directory

        # # Create labels to display the company logos
        # self.company_logo_label = tk.Label(self.company_logos_frame, image=self.company_logo)
        # self.company_logo_label.place(relx=0.2, rely=0.5, anchor=tk.CENTER) # Display main company logo

        # self.partnered_company_logo_label = tk.Label(self.company_logos_frame, image=self.partnered_company_logo)
        # self.partnered_company_logo_label.place(relx=0.8, rely=0.5, anchor=tk.CENTER) # Display  partnered company logo

        # Create a button to select robot
        self.robot_button = tk.Button(self.top_button_frame_middle_center, text="New Order", command=self.select_robot, font=('Helvetica', 12), width=10, height=1)
        self.robot_button.pack(side=tk.LEFT, padx=10) # Pack the button with padding

        # Create a button to select hexadecimal
        self.hexadecimal_button = tk.Button(self.top_button_frame_middle_center, text="Code", command=self.select_hexadecimal, font=('Helvetica', 12), width=10, height=1)
        self.hexadecimal_button.pack(side=tk.LEFT, padx=10) # Pack the button with padding
        
        # Create a frame to hold the labels and comboboxes
        frame = tk.Frame(self.main_frame)
        frame.pack(fill="both", expand=True) # Expand the frame to fill the main frame

        # Create a label and combobox for selecting the robot type
        self.robot_label = tk.Label(frame, text="Robot Type")
        self.robot_label.grid(row=0, column=0, padx=10, pady=10) # Place the label in the grid

        self.robot_combobox = ttk.Combobox(frame, values=["All"] + list(self.robot_dict.keys()), state="readonly")
        self.robot_combobox.grid(row=0, column=1, padx=10, pady=10) # Place the combobox in the grid
        self.robot_combobox.set("All") # Set default value

        # Create a label and combobox for selecting the robot name
        self.color_label = tk.Label(frame, text="Robot Name")
        self.color_label.grid(row=1, column=0, padx=10, pady=10) # Place the label in the grid

        self.color_combobox = ttk.Combobox(frame, values=["All"] + list(self.color_dict.keys()), state="readonly")
        self.color_combobox.grid(row=1, column=1, padx=10, pady=10) # Place the combobox in the grid
        self.color_combobox.set("All") # Set default value

        # Create a label and combobox for selecting the gripper type
        self.gripper_label = tk.Label(frame, text="Select Gripper")
        self.gripper_label.grid(row=2, column=0, padx=10, pady=10) # Place the label in the grid

        # Create a combobox to select the gripper
        self.gripper_combobox = ttk.Combobox(frame, values=["All"] + list(self.grippers_dict.keys()), state="readonly")
        self.gripper_combobox.grid(row=2, column=1, padx=10, pady=10) # Place the combobox in the grid
        self.gripper_combobox.set("All") # Set default value
        
        # Create a frame for communication protocols
        self.communication_protocols_frame = tk.Frame(frame)
        self.communication_protocols_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew") # Place the frame in the grid

        # Create a label to display the text "Select Communication Protocols"
        self.communication_protocols_label = tk.Label(self.communication_protocols_frame, text="Select Communication Protocols")
        self.communication_protocols_label.pack()

        # Create a dictionary to store the communication protocols checkbuttons
        self.communication_protocols_checkbuttons = {}

        # Create a frame to hold the communication protocols checkbuttons
        self.communication_protocols_checkbuttons_frame = tk.Frame(self.communication_protocols_frame)
        self.communication_protocols_checkbuttons_frame.pack(fill="x")
        
        # Create checkbuttons for the communication protocols
        for protocol in self.communication_protocols_dict.keys():
            var = tk.IntVar() # Create a variable to track the state of the checkbutton
            checkbutton = tk.Checkbutton(self.communication_protocols_checkbuttons_frame, text=protocol, variable=var, state="normal")
            checkbutton.pack(side=tk.LEFT) 
            self.communication_protocols_checkbuttons[protocol] = var # Store the variable in the dictionary

        # Create a frame for addons
        self.addons_frame = tk.Frame(frame)
        self.addons_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")  # Place the frame in the grid

        # Create a label to display the text "Select Addons"
        self.addons_label = tk.Label(self.addons_frame, text="Select Addons")
        self.addons_label.pack()

        # Create a dictionary to store the addons checkbuttons
        self.addons_checkbuttons = {}

        # Create a frame to hold the addons checkbuttons
        self.addons_checkbuttons_frame = tk.Frame(self.addons_frame)
        self.addons_checkbuttons_frame.pack(fill="x")

        # Create checkbuttons for the addons
        for addon in self.addons_dict.keys():
            var = tk.IntVar() # Create a variable to track the state of the checkbutton
            checkbutton = tk.Checkbutton(self.addons_checkbuttons_frame, text=addon, variable=var, state="normal")
            checkbutton.pack(side=tk.LEFT)
            self.addons_checkbuttons[addon] = var # Store the variable in the dictionary

        # Create a label to display the text "Hexadecimal Value"
        self.hexadecimal_label = tk.Label(frame, text="Hexadecimal Value")
        self.hexadecimal_label.grid(row=2, column=2, padx=10, pady=10)

        # Create an entry for hexadecimal input
        self.hexadecimal_entry = tk.Entry(frame, state="readonly")
        self.hexadecimal_entry.grid(row=3, column=2, padx=10, pady=10)

        # Create a frame to hold the buttons and treeview
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(side=tk.TOP, fill="both", expand=True)

        # Create a frame to hold the middle buttons
        self.middle_button_frame = tk.Frame(self.bottom_frame)
        self.middle_button_frame.pack(side=tk.TOP, fill="x")

        # Create a frame to hold the middle buttons in the middle
        self.middle_button_frame_middle = tk.Frame(self.middle_button_frame)
        self.middle_button_frame_middle.pack(side=tk.TOP, fill="x", expand=True)

        # Create a frame to hold the middle buttons in the middle center
        self.middle_button_frame_middle_center = tk.Frame(self.middle_button_frame_middle)
        self.middle_button_frame_middle_center.pack(side=tk.LEFT, fill="x", expand=True)

        # Create a button to get the specifications
        self.button = tk.Button(self.middle_button_frame_middle_center, text="Get Specifications", command=self.get_specs)
        self.button.pack(side=tk.LEFT, padx=10) # Alignment of Get Specifications button in the interface
        
        # Create a button to copy the code
        self.copy_button = tk.Button(self.middle_button_frame_middle_center, text="Copy Code", command=self.copy_code)
        self.copy_button.pack(side=tk.LEFT, padx=10) # Alignment of Copy Code button in the interface

        # Create a button to clear the table
        self.clear_button = tk.Button(self.middle_button_frame_middle_center, text="Clear", command=self.clear_table)
        self.clear_button.pack(side=tk.LEFT, padx=10) # Alignment of Clear button in the interface

        # Create a frame to hold the treeview
        self.tree_frame = tk.Frame(self.bottom_frame)
        self.tree_frame.pack(side=tk.TOP, fill="both", expand=True) #  Alignment of Treeview to display the specifications, providing a structured view of selected robot's attributes and values

        # Create a treeview to display the specifications
        self.tree = ttk.Treeview(self.tree_frame, columns=("Attribute", "Value"), show="headings")
        self.tree.heading("Attribute", text="Attribute")  # Set the column headings
        self.tree.heading("Value", text="Value")   # Set the column headings

        # Use pack to layout the treeview
        self.tree.pack(side=tk.TOP, fill="both", expand=True)
        
        # Create a button to export the output to a PDF file
        self.export_button = tk.Button(self.middle_button_frame_middle_center, text="Export to PDF", command=self.export_to_pdf) # Specify the function to call when the button is pressed
        self.export_button.pack(side=tk.LEFT, padx=10) # Align the Export to PDF button in the interface 

        # Bind the combobox selected event to their respective functions
        self.robot_combobox.bind("<<ComboboxSelected>>", self.on_robot_type_selected)  # Event for when robot type is selected
        self.color_combobox.bind("<<ComboboxSelected>>", self.on_color_selected)  # Event for when robot name is selected
        self.gripper_combobox.bind("<<ComboboxSelected>>", lambda event: self.root.after(100, self.on_gripper_selected))  # Event for when gripper type is selected; uses a delay to ensure the UI updates
        # Loop through each protocol and bind their state change to a function
        for protocol, var in self.communication_protocols_checkbuttons.items():
            var.trace("w", lambda name, index, mode, var=var: self.on_communication_protocol_selected()) # Trace changes in the variable's state (checked/unchecked) to trigger the protocol selection handler
    
    # Copies the current hexadecimal value from the entry field to the clipboard
    def copy_code(self):
        hex_value = self.hexadecimal_entry.get()  # Get the current hexadecimal value from the entry field
        if hex_value: # Check if there is a value to copy
            pyperclip.copy(hex_value) # Copy the hexadecimal value to the clipboard
            messagebox.showinfo("Success", "Hexadecimal value copied to clipboard") # Show a success message
        else: # If there is no value to copy
            messagebox.showerror("Error", "No hexadecimal value to copy") # Show an error message

    # Function handles the selection of a robot type from the robot_combobox.
    def on_robot_type_selected(self, event):
        robot_type = self.robot_combobox.get() # Get the selected robot type
        if robot_type != "All":  # If a specific robot type is selected
            # Set the values of the robot_name_combobox based on the selected robot type
            if robot_type == "Iontec":
                self.color_combobox['values'] = ["All", "KR 20 R3100 Iontec", "KR 30 R2100 Iontec"]
            elif robot_type == "Cybertech-2":
                self.color_combobox['values'] = ["All", "KR 08 R2010 Cybertech-2", "KR 12 R1810 Cybertech-2", "KR 16 R1610 Cybertech-2"]
            elif robot_type == "Cybertech nano-2":
                self.color_combobox['values'] = ["All", "KR 6 R1840-2 Cybertech nano", "KR 8 R1640-2 Cybertech nano", "KR 10 R1440-2 Cybertech nano"]
            elif robot_type == "Agilus-2":
                self.color_combobox['values'] = ["All", "KR6 R700-2 AGILUS", "KR6 R900-2 AGILUS", "KR10 R900-2 AGILUS"]
            elif robot_type == "KR4 und Scara":
                self.color_combobox['values'] = ["All", "KR4 R600 Agilus", "KR6 R500 Z200-2 Scara"]
            elif robot_type == "KR12 Scara":
                self.color_combobox['values'] = ["All", "KR12 R650 Z400 Scara", "KR12 R750 Z400 Scara", "KR12 R850 Z400 Scara"]
            self.color_combobox.set("All")
        else: # If "All" is selected, display all color option
            self.color_combobox['values'] = ["All"] + list(self.color_dict.keys())
            self.color_combobox.set("All")  # Reset to "All"
            
        # Set combobox states to readonly if not already set
        if self.color_combobox['state'] != 'readonly':
            self.color_combobox.config(state="readonly")
        if self.gripper_combobox['state'] != 'readonly':
            self.gripper_combobox.config(state="readonly")
        self.gripper_combobox.config(state="readonly")
        # Enable frames for communication protocols and addons
        self.communication_protocols_frame.config(state="normal")
        self.addons_frame.config(state="normal")

    # Function handles the selection of a robot name from the robot_name_combobox
    def on_color_selected(self, event):
        color = self.color_combobox.get() # Get the selected robot name
        if color != "All": # If a specific robot name is selected
            # Set the robot_combobox to the corresponding robot type based on the selected robot name
            if "Iontec" in color:
                self.robot_combobox.set("Iontec")
            elif "Cybertech-2" in color:
                self.robot_combobox.set("Cybertech-2")
            elif "Cybertech nano" in color:
                self.robot_combobox.set("Cybertech nano-2")
            elif "AGILUS" in color:
                self.robot_combobox.set("Agilus-2")
            elif "Agilus" in color and "Scara" not in color:
                self.robot_combobox.set("KR4 und Scara")
            elif "Scara" in color:
                if "KR12" in color:
                    self.robot_combobox.set("KR12 Scara")
                else:
                    self.robot_combobox.set("KR4 und Scara")
        else: 
            self.robot_combobox.set("All") # Reset robot selection if "All" is selected
        if self.gripper_combobox['state'] != 'readonly': # Ensure the gripper_combobox is readonly
            self.gripper_combobox.config(state="readonly")
        # Enable frames for communication protocols and addons
        self.communication_protocols_frame.config(state="normal")
        self.addons_frame.config(state="normal")

    # Function handles the selection of a gripper and enables associated options
    def on_gripper_selected(self):
        # Enable all communication protocol checkbuttons
        for widget in self.communication_protocols_checkbuttons_frame.winfo_children():
            widget.config(state="normal")
        # Enable all addons checkbuttons
        for widget in self.addons_checkbuttons_frame.winfo_children():
            widget.config(state="normal")
        # Ensure the communication protocols and addons frames are enabled
        self.communication_protocols_frame.config(state="normal")
        self.addons_frame.config(state="normal")
        # Set the communication protocol checkbuttons based on previously decoded protocols
        for protocol, var in self.communication_protocols_checkbuttons.items():
            if protocol in decoded_communication_protocols:
                var.set(1) # Set to checked if the protocol is in the list
            else:
                var.set(0) # Set to unchecked if not

    # Function handles changes to the selected communication protocols
    def on_communication_protocol_selected(self):
        # Gather selected protocols based on the checkbutton states
        selected_protocols = [protocol for protocol, var in self.communication_protocols_checkbuttons.items() if var.get()]
        if selected_protocols: # If any protocols are selected
            # Enable addons checkbuttons
            for widget in self.addons_checkbuttons_frame.winfo_children():
                if widget['state'] != 'normal':
                    widget.config(state="normal")
        else:
            # Disable addons checkbuttons if no protocols are selected
            for widget in self.addons_checkbuttons_frame.winfo_children():
                if widget['state'] != 'normal':
                    widget.config(state="normal")
                var.set(0) # Ensure the variable is unchecked
    
    # Function clears the selection in the specified combobox and resets its state
    def clear_text(self, combobox):
        combobox.set("No selection") # Reset the combobox to indicate no selection
        if combobox['state'] != 'disabled':
            combobox.config(state="normal") 

    # Function clears all input fields, selections and outputs
    def clear_table(self):
        self.robot_combobox.set("All") # Reset robot type selection to "All"
        self.color_combobox.set("All") # Reset robot name selection to "All"
        self.color_combobox['values'] = ["All"] + list(self.color_dict.keys()) # Reset robot name selection to "All"
        self.gripper_combobox.set("All")  # Reset gripper selection to "All"
        self.gripper_combobox['values'] = ["All"] + list(self.grippers_dict.keys()) # Reset gripper options
        self.hexadecimal_entry.config(state="normal") # Make hexadecimal entry editable
        self.hexadecimal_entry.delete(0, tk.END) # Clear any text in the entry
        self.hexadecimal_entry.config(state="readonly") # Set back to readonly

        # Clear the outputs
        self.tree.delete(*self.tree.get_children()) # Remove all items from the treeview

        # Reset the checkbuttons for communication protocols and addons
        for var in self.communication_protocols_checkbuttons.values():
            var.set(0) # Uncheck all protocols
            for widget in self.communication_protocols_checkbuttons_frame.winfo_children():
                if widget['state'] != 'normal':
                    widget.config(state="normal") # Enable all protocol checkbuttons
        for var in self.addons_checkbuttons.values():
            var.set(0) # Uncheck all addons
            for widget in self.addons_checkbuttons_frame.winfo_children():
                if widget['state'] != 'normal':
                    widget.config(state="normal") # Enable all addon checkbuttons
                
        # Enable the buttons for further actions
        self.robot_button.config(state="normal")
        self.hexadecimal_button.config(state="normal")
        
        # Enable all input options
        self.robot_combobox.config(state="readonly")
        self.color_combobox.config(state="readonly")
        self.gripper_combobox.config(state="readonly")
        self.communication_protocols_frame.config(state="normal") # Keep communication protocols frame enabled
        self.addons_frame.config(state="normal") # Keep addons frame enabled

    # Function handles the generate hexadecimal 
    def generate_hexadecimal(self, robot, color, gripper, communication_protocols, addons):
        # Convert selected robot, color and gripper from binary string to integer for bit manipulation
        robot_binary = int(self.robot_dict[robot], 2)
        color_binary = int(self.color_dict[color], 2)
        gripper_binary = int(self.grippers_dict[gripper], 2)

        # Shift robot's binary value by 32 bits to the left to create space for color and gripper data
        robot_binary_shifted = robot_binary << 32
        color_binary_shifted = color_binary << 16

        # Combine robot, color and gripper binaries using OR operation
        robot_color_gripper_binary = robot_binary_shifted | color_binary_shifted | gripper_binary

        # Convert the combined 48-bit binary value to a string format
        robot_color_gripper_binary_str = format(robot_color_gripper_binary, '048b')

        # Generate 16-bit binary string for selected communication protocols
        communication_protocols_binary = ['0'] * 16 # Initialize all bits to 0
        for i, protocol in enumerate(self.communication_protocols_dict.keys()):
            # Set the corresponding index to '1' if the protocol is selected by the user
            if protocol in communication_protocols:
                communication_protocols_binary[i] = '1'
        # Join the list into a single binary string
        communication_protocols_binary_str = ''.join(communication_protocols_binary)

        # Generate 16-bit binary string for selected addons
        addons_binary = ['0'] * 16 # Initialize all bits to 0
        for i, addon in enumerate(self.addons_dict.keys()):
            # Set the corresponding index to '1' if the addon is selected by the user
            if addon in addons:
                addons_binary[i] = '1'
        # Join the list into a single binary string
        addons_binary_str = ''.join(addons_binary)

        # Convert the protocol and addon binary strings to integers and apply bitwise shifts
        communication_protocols_binary_shifted = int(communication_protocols_binary_str, 2) << 16
        addons_binary_shifted = int(addons_binary_str, 2)

        # XOR operation between communication protocols and addons
        communication_addons_binary = bin(communication_protocols_binary_shifted ^ addons_binary_shifted)[2:].zfill(32)

        # Combine robot_color_gripper_binary and communication_addons_binary
        final_binary = robot_color_gripper_binary_str + communication_addons_binary

        # Convert the final binary value to hexadecimal without padding
        final_hex = int(final_binary, 2)

        return final_binary, final_hex
    
    # Function handles hexadecimal input to decode and retrieve robot specifications 
    def decode_hexadecimal(self, hex_value):
        try:
            # Convert the hexadecimal value to a binary string, ensure it's 80 bits long
            binary_value = bin(int(hex_value, 16))[2:].zfill(80)
        except ValueError:
            messagebox.showerror("Error",  "Invalid hexadecimal value") # Show error message if the entered hexadecimal value is invalid
            return 
        
        # Check if the binary value is valid
        if len(binary_value) != 80:
            messagebox.showerror("Error", "Invalid hexadecimal value") # Show error message if the generated binary value is invalid
            return None

        # # Split binary string
        # robot_color_gripper_binary = binary_value[:48]
        # communication_addons_binary = binary_value[48:]

        # Split binary strings to represent robot type, robot name, gripper and communication_addons
        robot_binary = binary_value[:16]
        color_binary = binary_value[16:32]
        gripper_binary = binary_value[32:48]
        communication_addons_binary = binary_value[48:]
        
        #  Split communication_addons_binary into two parts:  communication and addons
        communication_protocols_binary = communication_addons_binary[:16]
        addons_binary = communication_addons_binary[16:]

        # Decode robot, color and gripper using dictionary lookups
        decoded_robot = [robot for robot, binary in self.robot_dict.items() if binary == robot_binary]
        decoded_color = [color for color, binary in self.color_dict.items() if binary == color_binary]
        decoded_gripper = [gripper for gripper, binary in self.grippers_dict.items() if binary == gripper_binary]

        # Decode communication protocols and addons
        # communication_addons_binary_list = list(communication_addons_binary)
        # communication_protocols_binary = communication_addons_binary_list[:16]
        # addons_binary = communication_addons_binary_list[16:]

        # Decode the selected communication protocols
        decoded_communication_protocols = []
        for i, protocol in enumerate(self.communication_protocols_dict.keys()):
            if communication_protocols_binary[i] == '1':
                decoded_communication_protocols.append(protocol)

        # Decode the selected addons
        decoded_addons = []
        for i, addon in enumerate(self.addons_dict.keys()):
            if addons_binary[i] == '1':
                decoded_addons.append(addon)
                
        # Check if any of the decoded values are missing        
        if not decoded_robot or not decoded_color or not decoded_gripper or not decoded_communication_protocols or not decoded_addons:
            messagebox.showerror("Error", "Invalid hexadecimal value") # If any decoded value is invalid or missing, show an error message
            return
        
        # If all decoded values are valid, return the robot type, robot name,  gripper, communication protocols and addons
        return decoded_robot[0], decoded_color[0], decoded_gripper[0], decoded_communication_protocols, decoded_addons
    
    # Function handles to display output
    def get_specs(self):
        # Clear the existing items in the tree view
        self.tree.delete(*self.tree.get_children())
        hex_value = self.hexadecimal_entry.get() # Clear the existing items in the tree view
        # if self.robot_combobox['state'] == 'disabled':
        
        # Check if a hexadecimal value has been entered
        if hex_value:
            # try:
            # Attempt to decode the hexadecimal value
            decoded_values = self.decode_hexadecimal(hex_value)
            # If decoding failed, exit the function
            if decoded_values is None:
                return
        
            # Unpack the decoded values into individual variables
            decoded_robot, decoded_color, decoded_gripper, decoded_communication_protocols, decoded_addons = self.decode_hexadecimal(hex_value)
            # Insert the decoded values into the tree view for display
            self.tree.insert('', 'end', values=("Robot Type", decoded_robot))
            self.tree.insert('', 'end', values=("Robot Name", decoded_color))
            self.tree.insert('', 'end', values=("Gripper", decoded_gripper))
            self.tree.insert('', 'end', values=("Communication Protocols", ', '.join(decoded_communication_protocols)))
            self.tree.insert('', 'end', values=("Addons", ', '.join(decoded_addons)))
            self.tree.insert('', 'end', values=("Hexadecimal Value", hex_value))
            
            # Set the comboboxes to the decoded values
            self.robot_combobox.set(decoded_robot)
            self.color_combobox.set(decoded_color)
            self.gripper_combobox.set(decoded_gripper)
            # Check the communication protocols and addons, setting their respective checkbuttons
            for protocol, var in self.communication_protocols_checkbuttons.items():
                if protocol in decoded_communication_protocols:
                    var.set(1)
                else:
                    var.set(0)
            for addon, var in self.addons_checkbuttons.items():
                if addon in decoded_addons:
                    var.set(1)
                else:
                    var.set(0)
            
            # Enable all the relevant options and frames
            self.robot_combobox.config(state="normal")
            self.color_combobox.config(state="normal")
            self.gripper_combobox.config(state="normal")
            self.communication_protocols_frame.config(state="normal")
            self.addons_frame.config(state="normal")
            # Make all checkbuttons in the communication protocols and addons frames active
            for widget in self.communication_protocols_checkbuttons_frame.winfo_children():
                widget.config(state="normal")
            for widget in self.addons_checkbuttons_frame.winfo_children():
                widget.config(state="normal")
            for widget in self.communication_protocols_checkbuttons_frame.winfo_children():
                widget.config(state="normal")
            # self.gripper_combobox.config(state="normal")
            # self.gripper_combobox.set(decoded_gripper)
            # self.on_gripper_selected()
            # Call the function to handle communication protocol selections
            self.on_communication_protocol_selected()
        #     except Exception as e:
        #         messagebox.showerror("Error", "Invalid hexadecimal value")
        else:
            # If no hexadecimal value is entered, get the selected values from the comboboxes and checkbuttons
            robot = self.robot_combobox.get()
            color = self.color_combobox.get()
            gripper = self.gripper_combobox.get()
            communication_protocols = [protocol for protocol, var in self.communication_protocols_checkbuttons.items() if var.get()]
            addons = [addon for addon, var in self.addons_checkbuttons.items() if var.get()]

            # Check for any missing selections and collect them into a list
            missing_options = []
            if robot == "All":
                missing_options.append("Robot Type")
            if color == "All":
                missing_options.append("Robot Name")
            if gripper == "All":
                missing_options.append("Gripper")
            if not communication_protocols:
                missing_options.append("Communication Protocols")
            if not addons:
                missing_options.append("Addons")

            # If any options are missing, display an error message to the user
            if missing_options:
                messagebox.showerror("Error", "Please select the following options: " + ", ".join(missing_options) + " or Hexadecimal Value")
            else:
                # Generate hexadecimal value based on selected options
                binary_result, hex_result = self.generate_hexadecimal(robot, color, gripper, communication_protocols, addons)
                # Update the hexadecimal entry field with the new value
                self.hexadecimal_entry.config(state="normal")
                self.hexadecimal_entry.delete(0, tk.END)
                self.hexadecimal_entry.insert(0, hex(hex_result))
                self.hexadecimal_entry.config(state="readonly")

                # Insert the selected options into the tree view for display
                self.tree.insert('', 'end', values=("Robot Type", robot))
                self.tree.insert('', 'end', values=("Robot Name", color))
                self.tree.insert('', 'end', values=("Gripper", gripper))
                self.tree.insert('', 'end', values=("Communication Protocols", ', '.join(communication_protocols)))
                self.tree.insert('', 'end', values=("Addons", ', '.join(addons)))
                self.tree.insert('', 'end', values=("Hexadecimal Value", hex(hex_result)))

# Main execution
if __name__ == "__main__":
    try:
        root = tk.Tk() # Create the main application window
        app = RobotInterface(root) # Create an instance of the RobotInterface class
        root.mainloop() # Keep the application running until the user closes it
    except Exception as e:
        print(f"An error occurred: {e}") # Return error if there is any mistake 
        