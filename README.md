# Complex Variables: Interactive Image & Shape Rotation Engine

```text
  ____ ___  __  __ ____  _     _______  __
 / ___/ _ \|  \/  |  _ \| |   | ____\ \/ /
| |  | | | | |\/| | |_) | |   |  _|  \  / 
| |__| |_| | |  | |  __/| |___| |___ /  \ 
 \____\___/|_|  |_|_|   |_____|_____/_/\_\

  ____   ___ _____  _  _____ ___ ___  _   _ 
 |  _ \ / _ \_   _|/ \|_   _|_ _/ _ \| \ | |
 | |_) | | | || | / _ \ | |  | | | | |  \| |
 |  _ <| |_| || |/ ___ \| |  | | |_| | |\  |
 |_| \_\\___/ |_/_/   \_\_| |___\___/|_| \_|
```

## Overview

An interactive, visual-first Python application demonstrating how **complex number multiplication** and **Euler's Formula** drive 2D geometric and image rotations.

Built for classroom demonstrations, academic presentations, and real-time linear algebra visual proofs using **CustomTkinter**, **Matplotlib**, and **NumPy**.

## Core Mathematics

Rotating a point $P(x, y)$ represented as a complex number $z = x + iy = r e^{i\phi}$ is performed by multiplying it with a unit complex rotator $w = e^{i\theta}$:

$$
z' = z \cdot e^{i\theta} = (r e^{i\phi}) \cdot e^{i\theta} = r e^{i(\phi + \theta)}
$$

Expanding into Cartesian coordinates using **Euler's Formula** ($e^{i\theta} = \cos\theta + i\sin\theta$):

$$
z' = (x + iy)(\cos\theta + i\sin\theta) = (x\cos\theta - y\sin\theta) + i(x\sin\theta + y\cos\theta)
$$

In NumPy, an entire array of complex coordinates $Z$ is rotated simultaneously using vectorization:

```python
Z_rotated = Z * np.exp(1j * np.radians(angle_degrees))
```

## System Architecture

```text
+-------------------------------------------------------------------------------+
|                       COMPLEX ROTATION INTERACTIVE DEMO                       |
+------------------------------------+------------------------------------------+
|  ARGAND / COMPLEX PLANE (LEFT)     | SPATIAL / SHAPE CANVAS (RIGHT)           |
|  * Unit circle overlay             | * Original ghost vector frame            |
|  * Unit rotator vector e^(iθ)      | * Dynamically rotated active shape       |
|  * Swept angle arc indicator       | * Concentric vertex trail arcs           |
+------------------------------------+------------------------------------------+
|                        CONTROL & MATHEMATICAL HUD                             |
|  [ Rotate 30° ] [ Rotate 45° ] [ Rotate 90° ] [ Play Continuous Animation ]   |
|  Angle Slider: [=======================o================] 135.0°              |
|  Equation: z' = z · e^(i · 135.0°) = z · (-0.71 + 0.71i)                     |
+-------------------------------------------------------------------------------+
```

## Key Features

* **Dual-Panel Interactive Canvas**:
  * **Argand Plane (Left):** Displays the unit rotator vector $e^{i\theta} = \cos\theta + i\sin\theta$ moving on the unit circle.
  * **Spatial Canvas (Right):** Renders the shape transforming in real time via complex scalar product multiplication.
* **Real-Time Mathematical HUD**: Dynamic readout displaying the evaluated Euler transformation formula at every frame.
* **60 FPS Vectorized Engine**: High-performance updates achieved by modifying data buffer arrays directly without canvas redraws.
* **Preset Lerping & Continuous Animation**: Smooth linear interpolation when clicking key angle presets ($30^\circ$, $45^\circ$, $90^\circ$), plus auto-spin mode.
* **Vertex Arc Trails**: Displays concentric dotted arcs highlighting the circular trajectories swept by individual coordinates.

## Getting Started

### Prerequisites

* Python 3.8 or higher
* `pip` package manager

### Installation

Install required dependencies via terminal:

```bash
pip install numpy matplotlib customtkinter
```

If using a specific Python 3 environment:

```bash
python3 -m pip install numpy matplotlib customtkinter
```

### Running the Application

Launch the demonstration application:

```bash
python main.py
```

## Interface Controls

| Component | Function |
| ----- | ----- |
| **Angle Slider** | Drag manually from $0^\circ$ to $360^\circ$ for direct manual angle sweeping. |
| **Preset Buttons** | Smoothly interpolates the rotation angle to target stops ($30^\circ$, $45^\circ$, $90^\circ$). |
| **Play Continuous** | Toggles continuous counterclockwise rotation animation loop. |

## Presentation Demo Flow

1. **Initial State ($0^\circ$)**: Point out the static orientation and ghost baseline image on the spatial canvas.
2. **Argand Plane Context**: Explain that multiplying by a unit complex number changes *only* the phase angle, keeping distance from origin $|w| = 1$ constant.
3. **Trigger $90^\circ$ Preset**: Demonstrate that $e^{i \cdot 90^\circ} = i$. Show how $(x + iy) \cdot i = -y + ix$ directly swaps coordinate axes.
4. **Continuous Drag**: Show how the red dotted vertex trails confirm that every point traces a concentric circular path around the origin.

## File Structure

```text
.
├── main.py       # Core application (CustomTkinter GUI + Matplotlib + Math engine)
└── README.md     # Technical project documentation
```

## License

Distributed under the MIT License. See `LICENSE` for more information.