# AI Stress-Testing Email Tool

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge&logo=python)
![Built With](https://img.shields.io/badge/built%20with-ttkbootstrap-orange?style=for-the-badge)
[![Issues](https://img.shields.io/badge/Issues-report-brightgreen.svg?style=for-the-badge)](https://github.com/Frankwerd/ai-email-stress-tool/issues)
[![Source Code](https://img.shields.io/badge/Source-GitHub-lightgrey?style=for-the-badge&logo=github)](https://github.com/Frankwerd/ai-email-stress-tool)

</div>

<div align="center">

A powerful desktop application designed for stress-testing email-dependent systems by sending bulk emails with unique, AI-generated content using the Google Gemini API.

![Application Screenshot](<https://i.imgur.com/eecmen9.png>)
> **Note:** Screenshot of the final application. You can download the .exe in releases.

</div>


## Key Features

- **Modern User Interface:** Built with `ttkbootstrap` for a clean, modern look and feel (light and dark themes available).
- **AI-Powered Content:** Connects to the Google Gemini API to generate unique subjects and bodies for every email, ensuring realistic and varied test data.
- **Bulk Sending:** Send a specified number of emails to a target address for load testing.
- **Full Email Control:**
  - Send to `To`, `Cc`, and `Bcc` recipients.
  - Choose between **Plain Text** and **HTML** formats.
  - Attach local files to all outgoing emails.
- **Rate & Tone Control:**
  - Customize the **delay** between emails to simulate different traffic patterns.
  - Specify the **purpose** and **tone** (e.g., "Professional", "Spammy", "Casual") to guide the AI's content generation.
- **Robust & User-Friendly:**
  - Includes a **Cancel** button to safely stop the sending process mid-run.
  - Built-in threading keeps the UI responsive during long-running tasks.
  - Packaged as a standalone **`.exe`** for easy distribution and use on any Windows machine.

## How to Use (for End-Users)

No installation is needed. Just download the application and run it.

1.  Go to the **[Releases](https://github.com/Frankwerd/ai-email-stress-tool/releases)** section of this repository.
    > **Action:** Replace `Frankwerd/ai-email-stress-tool` with your actual GitHub username and repository name.
2.  Download the `main.exe` file from the latest release.
3.  Double-click `main.exe` to launch the application.

## How to Run From Source (for Developers)

If you want to run the project from the source code or contribute to its development, follow these steps.

**Prerequisites:**
- [Git](https://git-scm.com/downloads)
- [Python 3.8+](https://www.python.org/downloads/)

**Setup:**

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/Frankwerd/ai-email-stress-tool.git
    cd ai-email-stress-tool
    ```
    > **Action:** Replace `Frankwerd/ai-email-stress-tool` with your URL.

2.  **Create and activate a virtual environment:**
    ```sh
    # Create the environment
    python -m venv venv
    
    # Activate it (on Windows PowerShell)
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    python main.py
    ```

## Built With

- **Python 3**
- **Tkinter** - The standard GUI toolkit for Python.
- **ttkbootstrap** - For modern, professional theming of the Tkinter UI.
- **Google Gemini API** (`google-generativeai`) - For generating dynamic email content.
- **PyInstaller** - To package the application into a standalone Windows executable.

## How to Build the Executable

After setting up the developer environment, you can build the `.exe` file yourself using PyInstaller.

```sh
pyinstaller --onefile --windowed --icon="app_icon.ico" main.py
```

The final executable will be located in the `dist/` folder.

## License

Distributed under the MIT License. See the `LICENSE` file for more information.
> **Suggestion:** Create a new file in your repository named `LICENSE` and paste the text of the MIT license into it. You can find the text [here](https://opensource.org/licenses/MIT).

## Contact

Francis John LiButti - libutti123@gmail.com

Project Link: [https://github.com/Frankwerd/ai-email-stress-tool](https://github.com/Frankwerd/ai-email-stress-tool)
