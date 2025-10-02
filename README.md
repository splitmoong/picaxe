# Picaxe 🖼️⛏️

Picaxe is a modern, minimalist image compression and conversion tool built for the GNOME desktop. Designed to be fast, efficient, and seamlessly integrated with your system's look and feel, Picaxe helps you reduce image file sizes without compromising quality, or convert them to different formats with ease.

* **Effortless Compression:** Reduce image file sizes for faster sharing and storage.
* **Intuitive Conversion:** Easily change image formats (e.g., PNG to JPG, etc.).
* **Modern GNOME Integration:** Built with GTK4 and Libadwaita for a native, adaptive user experience.
* **Seamless UI:** Respects your system's light/dark mode and accent colors.

<p align="center">
  <img src="https://github.com/user-attachments/assets/31afd1e5-b68e-4f45-99b2-cb9eb31a1592" alt="Picaxe in Light Mode" width="49%" style="display: inline-block; margin: 0 0.5%;" />
  <img src="https://github.com/user-attachments/assets/c260ad70-11b3-4c29-815d-92e07c8c00c9" alt="Picaxe in Dark Mode" width="49%" style="display: inline-block; margin: 0 0.5%;" />
</p>

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