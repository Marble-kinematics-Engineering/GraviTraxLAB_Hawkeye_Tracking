# 🎯 GraviTraxLAB Hawk-Eye: Automated Trajectory Tracking

An automated computer vision tool written in Python and OpenCV to detect, track, and verify marble impacts within a GraviTrax environment with millimeter-level precision.

## 🚀 Features

* **Interactive GUI:** Built-in `tkinter` popups for zero-code parameter initialization.
* **Real-Time HSV Calibration:** Dynamic trackbars to isolate green, blue, red, or metallic grey marbles.
* **Geometric Core Isolation:** Automated 25% circular mask centering to eliminate external plastic track reflections and highlights.
* **Intelligent Auto-Scaling:** Computer vision engine that calibrates the spatial pixel-to-millimeter ratio in real time using the physical 12.7 mm marble diameter as an absolute metric anchor.
* **Interactive Precision Crosshair:** Real-time keyboard-driven adjustment matrix to align the structural pad origin center down to a single pixel.
* **Instant "Hawk-Eye" Analytics:** Automated discovery of the impact bounce frame, rendering vector trajectory lines and validation triggers.

## 🛠️ Installation

Ensure you have Python installed, then execute the following commands in your terminal:

```bash
pip install --upgrade pip
pip install opencv-python numpy
```

## 💻 Usage

1. Clone this repository or download your working script file.
2. Launch the tracking program from your console:

   ```bash
   python gravitraxlab_hawkeye.py
   ```

3. Select your experimental `.mp4` video file, input your marble color preference, adjust the HSV filtering sliders, and press the **spacebar** key to initiate the tracking loop.

### 🎮 Manual Crosshair Alignment Controls

Once the video analytics processing finishes, the viewport will pause at the impact frame. Use your keyboard to align the yellow crosshair onto the precise geometric center of your landing pad:

* **W / S:** Move crosshair center vertically (Up / Down).
* **A / D:** Move crosshair center horizontally (Left / Right).
* **Q / E:** Rotate crosshair diagonal lines orientation.
* **ENTER:** Confirm structural positioning and compute the final physical metrics.

## 🎲 Quick Calibration Cheat Sheet

If you prefer to bypass manual trackbar exploration, utilize these optimized reference values in the calibration window according to your physical GraviTrax® marble setup:

| Marble Color | H Min | H Max | S Min | S Max | V Min | V Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Red** 🔴 | 0 | 25 | 30 | 255 | 30 | 255 |
| **Blue** 🔵 | 90 | 130 | 50 | 255 | 50 | 255 |
| **Green** 🟢 | 35 | 85 | 50 | 255 | 50 | 255 |
| **Silver / Grey** ⚪ | 0 | 180 | 0 | 40 | 50 | 220 |

*Note: Always ensure that the green tracks and structural elements turn completely black, leaving only your moving marble isolated as a solid white tracking node.*

### 🪵 Understanding the HSV Color Space

Unlike standard RGB hardware models, this computer vision framework operates entirely within the **HSV** color spectrum. This mathematical separation insulates the detection algorithms from environmental light fluctuations and shadows:

* **H (Hue):** Represents the pure color wavelength along a continuous spectrum loop (0 to 180 in OpenCV).
* **S (Saturation):** Measures the absolute purity of the color (0 to 255). Lower values wash out towards grey, while higher values isolate rich neon tones.
* **V (Value):** Controls color illumination intensity (0 to 255). Essential for stripping dark shadow artifacts or bright plastic light reflections.

## 📖 Academic & Methodology Background

This software serves as the official implementation companion of **Chapter 4** of the technical textbook:  
*Vector Field of the Velocity in Projectile Motion: Mathematical Modeling and Empirical Validation (Second Edition)* available on **Amazon KDP**.

For a deep dive into kinematic trajectory equations, spatial coordinate scaling matrix computations ($E = D_{real} / D_{pixel}$), and experimental engineering setups, please refer to the complete printed textbook edition.

## 📜 License and Intellectual Property

This code constitutes Appendix 2 of the book published on Amazon KDP and is subject to the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** license. The complete work and its associated source code are registered with **Safe Creative** under the identifier:
* **Official Registration (2nd Edition - August 2026): ** 2608066660282

Any commercial use or modification of the code without the author's express authorization is prohibited.

### 📝 How to cite

If you use this code or base your own academic or technical work on this research, please cite the preprint or the official book:

Hidalgo Fernández, J. (2026). Vector Field of the Velocity in Projectile Motion: Mathematical Modeling and Empirical Validation [Open Researcher and Contributor ID]. ORCID. https://orcid.org/0009-0006-5044-9430

Hidalgo Fernández, J. (2026). Vector Field of the Velocity in Projectile Motion: Mathematical Modeling and Empirical Validation (2nd ed.). Technical Research in Kinematic Engineering. Amazon KDP. https://www.amazon.es/dp/B0H89Y5V37

## ⚖️ Legal / Trademark Notice

GraviTrax® is a registered trademark of Ravensburger. The experimental setups and physical validations presented in this technical supplement were conducted independently using these track systems as an open laboratory workbench. This academic development is not affiliated with, sponsored, or endorsed by Ravensburger.
