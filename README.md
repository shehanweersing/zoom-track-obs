#  OBS Dynamic Zoom & Follow


> A Python script for OBS Studio that smoothly zooms in and follows your mouse cursor. 
> Perfect for coding tutorials, presentations, and screen recording.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![OBS](https://img.shields.io/badge/OBS-Studio-white)

##  What does this do?
Unlike standard mouse trackers that just put a dot on your screen, this script **moves the entire screen**. 
It keeps your mouse in the center and zooms in (like a magnifying glass), making it easier for viewers to see small text or code.

##  Features
* **Smooth Motion:** Uses Linear Interpolation (Lerp) for a cinematic, "weighty" camera feel.
* **Dynamic Zoom:** Adjustable zoom level (1.2x to 4.0x).
* **Inverse Panning:** Automatically calculates the screen offset to keep the target centered.

##  Installation

1.  **Download** this repo.
2.  **Open OBS Studio**:
    * Add a **Display Capture** source to your scene.
3.  **Load Script**:
    * Go to `Tools` -> `Scripts`.
    * Load `zoom_follow.py`.
4.  **Configure**:
    * Select your "Display Capture" source in the script settings.
    * Set **Zoom Level** to `1.5` and **Smoothness** to `0.08`.

##  Related Projects
Looking for a simple mouse highlighter instead? Check out my other repo: 
[**Elastic Mouse Overlay**](https://github.com/shehanweersing/obs-elastic-mouse)
#  Shehan N Weerasinghe
