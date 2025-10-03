# Picaxe

A minimalist image compression and conversion tool built for the GNOME desktop that helps you reduce image file sizes or convert them to different formats with ease.

<img width="3945" height="1500" alt="Group 1" src="https://github.com/user-attachments/assets/7e5883eb-f83d-44e2-b94a-5803e93a011f" />

### Prerequisites

* Python 3.8+
* GTK 4 and Libadwaita development files.
    * **Fedora:** `sudo dnf install python3-gobject python3-gobject-cairo gtk4-devel libadwaita-devel`
    * **Debian/Ubuntu:** `sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/splitmoong/picaxe.git
    cd picaxe
    ```
2.  **Set up a virtual environment (recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Run the application:**
    ```bash
    python3 src/main.py
    ```
