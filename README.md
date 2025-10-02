# Picaxe 🖼️⛏️

A minimalist image compression and conversion tool built for the GNOME desktop that helps you reduce image file sizes or convert them to different formats with ease.

<img width="622" height="722" alt="Screenshot From 2025-10-03 01-58-51" src="https://github.com/user-attachments/assets/32ffc682-f59a-4540-8946-9a9519abc813" />

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
