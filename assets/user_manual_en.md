# License and Terms of Use

This software is distributed under the MIT license. You may copy, modify, and create your own versions, as long as you **credit the original developers**:

- Miguel OA4BAU
- Raquel OA4EHN

No suggestions or improvements are accepted in this official repository. You are free to create and distribute your own versions, respecting the mention of the authors.

**Disclaimer:** This software is provided "as is", without any express or implied warranties. The authors are not responsible for any damages, losses, or consequences arising from the use of the software. Use it at your own risk.

# User Manual — Logger OA

Welcome to Logger OA, the cross-platform application for OA radio amateurs in Peru. This manual guides you through all the real functions and menus of the app, designed for end users running the distributed executable (LoggerOA.exe, LoggerOA, etc.).

---

## Installation and First Start

1. Download the installer or executable for your operating system (Windows, Linux, or macOS) from the official page or repository.
2. Run the installer and follow the on-screen instructions, or simply open the provided executable file.
3. After installation, you will find a shortcut in your applications menu or desktop.
4. Double-click the Logger OA icon to start the application.

---

## Main Window and Menus

When you open Logger OA, you will see the main window with the following menus:

### File Menu
- **New** (submenu):
	- **New Operation Log**: Create a new operation log.
	- **New Contest Log**: Create a new contest log.
- **Open** (submenu):
	- **Open Operation Log**: Open an existing operation log.
	- **Open Contest Log**: Open an existing contest log.
- **Export** (submenu):
	- **Export as TXT**: Export the current log in plain text format. When finished, the folder opens and the exported file is selected.
	- **Export as CSV**: Export the current log in CSV (spreadsheet) format. When finished, the folder opens and the exported file is selected.
	- **Export as ADI**: Export the current log in ADIF format for other ham radio programs. When finished, the folder opens and the exported file is selected.
	- **Export as PDF**: Export the contest log in PDF sheet format (only available for contest logs). When finished, the folder opens and the exported file is selected.
- **Close Log**: Close the current log and return to the welcome screen.
- **Open Folder**: Quickly access the working folder.
- **Exit**: Close the application.

### Database Menu
- **Show Database**: Open the OA operators management window.
- **Import from PDF**: Import OA operators from an official PDF file. Select the PDF and the app will process the data, showing a summary (new, updated, disabled, re-enabled).
- **Import from Database**: Import operators from another database file.
- **Create Backup**: Generate a backup of the local database.
- **Restore Backup**: Restore the database from a previous backup.
- **Export to CSV**: Export the operators database to a CSV file.
- **Delete Database**: Delete the local database (confirmation required).

### Preferences Menu
- **Callsign** (submenu):
	- **Set Callsign**: Define the main callsign for operation.
	- **Save Callsign Mode**: The callsign is saved and reused automatically.
	- **Always Ask Mode**: The app requests the callsign each time a log is created or opened.
	- **Show Current Callsign**: View the currently configured callsign.
- **Appearance** (submenu):
	- **Light Theme**: Switch to light mode.
	- **Dark Theme**: Switch to dark mode.
	- **Automatic Theme**: Adapt the theme to the operating system settings.
- **Language** (submenu):
	- **Spanish**: Switch the interface to Spanish.
	- **English**: Switch the interface to English.
	- **Automatic**: Select the language according to the operating system settings.

### Help Menu
- **User Manual**: Show this manual on screen.
- **About**: Show information about the application and the development team.

---

## Main Flows

### Create a New Log

1. Go to **File > New** and select:
	- **New Operation Log**: For regular operations.
	- **New Contest Log**: For contest participation.

2. **Options when creating an operation log:**
	- Define the main callsign for operation.
	- Select the type of operation (CPS, RENER, BULLETIN).
	- Choose the frequency band and mode (HF, VHF, LSB, USB, FM, etc.).
	- Enter the frequency and, if applicable, the repeater.
	- The application automatically generates the log file and associates it with the session.

3. **Options when creating a contest log:**
	- Define the main callsign for operation.
	- Select the contest you are participating in (from a predefined list).
	- The log is associated with the contest name and the corresponding file is generated.

4. Once the log is created, the main window will display the header with the selected data and you can start registering contacts.

### Register a Contact in the Log
1. Enter the callsign in the "Enter callsign" field. If the callsign exists in the database, the associated data is auto-completed and a summary is shown instead of suggestions.
2. Complete the required fields in the form (station, energy, power, RS RX/TX, observations, etc. depending on the log type).
3. Click **Add Contact**. The system validates the data and checks for duplicates. If the contact already exists in the time block (for contests), confirmation is requested.
4. If the callsign is not in the database, you are offered to add it via a dialog. If accepted, the operator is registered and then the contact.
5. The contact is added to the log and the table is updated automatically. The callsign field is cleared for the next entry.

### Delete a Contact from the Log
1. Select the contact you want to delete in the log contacts table by selecting the corresponding row to enable the delete button.
2. Click the **Delete Contact** button.
3. The system will ask for confirmation before deleting the contact.
4. Once confirmed, the contact will be deleted from the log and the table will be updated automatically.

### How Suggestions Work
- As you type in the callsign field, suggestions of operators matching the input (minimum 2 characters) appear next to it.
- Suggestions show the callsign and operator name when hovering over them.
- You can click a suggestion to auto-complete the callsign field and load the associated data.

### How the Waiting Queue Works
- You can add callsigns to the waiting queue using the corresponding button or from the input field.
- The queue shows callsigns pending registration.
- Clicking a callsign in the queue auto-completes the input field to facilitate registration.
- You can remove callsigns from the queue using the context menu (right-click on the callsign and select "Delete").
- The system prevents duplicates in the queue and shows a message if you try to add the same callsign twice.

### Open an Existing Log
1. Go to **File > Open** and select **Open Operation Log** or **Open Contest Log**.
2. Choose the log file you want to open.

### Export Logs and Database
- To export a log: **File > Export > [Format]** (TXT, CSV, ADI, PDF). After exporting, the folder will open and the exported file will be selected automatically, regardless of your operating system (Windows, macOS, Linux). If your system does not support file selection, the folder will simply open as a fallback.
- To export the database: **Database > Export to CSV**.

### Import OA Operators from PDF
1. Go to **Database > Import from PDF**.
2. Select the official PDF file.
3. Wait for processing and review the import summary.

### Using the Operators Database Window
1. Go to **Database > Show Database** to open the OA operators management window.
2. The window displays a table with all registered operators and their main data.
	- You can add a new operator using the **Add Operator** button.
	- To edit an operator, double-click the corresponding row.
	- To delete an operator, select the row and click **Delete Operator** (confirmation required).
3. At the top, you can filter operators by any column by selecting the field in the dropdown menu and typing the text in the filter field.
	- The filter is dynamic and shows the number of results found.
	- The filter text is automatically normalized to uppercase for easier searching.
4. Below the filter, you will find a series of checkboxes for each column in the table.
	- You can show or hide columns by toggling the corresponding checkboxes.
	- The visible columns configuration is saved automatically and persists in future sessions.
5. You can adjust the column widths by dragging the edges in the table header.
	- The configured widths are saved automatically.

### Change Theme or Language
- Go to **Preferences > Appearance** to switch between light, dark, or automatic mode.
- Go to **Preferences > Language** to switch between Spanish, English, or automatic.

### Manage Callsign
- Go to **Preferences > Callsign** to define, view, or change the callsign usage mode.

### Create and Restore Backups
- **Database > Create Backup** to save a backup copy.
- **Database > Restore Backup** to recover data from a backup.

---

## Frequently Asked Questions

**Where is my data stored?**  
Your logs and operators are stored locally in a secure database (SQLite). You do not need an internet connection to use the app.

**Can I use Logger OA on any operating system?**  
Yes, download the appropriate executable for Windows, Linux, or macOS.

**How do I update the OA operators list?**  
Import the latest official PDF from the corresponding menu.

**How do I get help?**  
The only help available is provided in this user manual, accessible from the Help > User Manual menu within the application. No official support or personalized assistance is provided. But there will always be an OA colleague who can help you!

---

## Support and Contact

**Support:**
No official support or personalized assistance is provided. Use of the software is at your own risk and responsibility. All available help is contained in this user manual.

---

**Terms of Use:**
Using Logger OA implies acceptance of the MIT license and the disclaimer. If you distribute, modify, or create derivative versions, you must keep the mention of the original authors. No official support or warranty is provided regarding the operation, security, or results of the software.

Thank you for using Logger OA, 73!
