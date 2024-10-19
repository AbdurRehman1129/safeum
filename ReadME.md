
---

# SafeUM Account Creation Script

This project is a Python-based script designed to automate the creation of SafeUM accounts. The script uses WebSocket connections and multi-threading to register multiple accounts efficiently. The generated accounts are saved in a `SafeUM.txt` file in the format `Username:password`.

## Features
- Creates SafeUM accounts automatically
- Saves accounts in `Username:password` format
- Multi-threaded execution for faster performance

## Installation

### For Termux

1. Update your package list and upgrade installed packages:
   ```bash
   apt update && apt upgrade
   ```

2. Install Python and Git:
   ```bash
   pkg install python && pkg install git
   ```

3. Clone the repository:
   ```bash
   git clone https://codeberg.org/AbdurRehman1/safeum.git
   ```

4. Navigate to the project folder:
   ```bash
   cd safeum
   ```

5. Install the required Python modules:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the script:
   ```bash
   python main.py
   ```

### For Windows (CMD)

1. Open the command prompt and install Git and Python (if not installed). You can download them from their official websites:
   - [Python](https://www.python.org/downloads/)
   - [Git](https://git-scm.com/)

2. Clone the repository:
   ```bash
   git clone https://codeberg.org/AbdurRehman1/safeum.git
   ```

3. Navigate to the project folder:
   ```bash
   cd safeum
   ```

4. Install the required Python modules:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the script:
   ```bash
   python main.py
   ```

---

Feel free to modify any part of the description to suit your preferences or add more details if necessary!