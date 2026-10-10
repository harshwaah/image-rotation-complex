import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import sys

# Configure CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def generate_demo_shape():
    """
    Generates a complex number array representing an asymmetrical shape (an 'F' block).
    Asymmetry is crucial for demonstrating rotation clearly.
    """
    # Define an 'F' shape coordinates
    points = [
        0+0j, 0+2j, 1.2+2j, 1.2+1.6j, 0.4+1.6j, 
        0.4+1.2j, 1.0+1.2j, 1.0+0.8j, 0.4+0.8j, 
        0.4+0j, 0+0j
    ]
    Z = np.array(points)
    
    # Center the shape at the origin so it rotates around its own centroid
    Z_centered = Z - np.mean(Z)
    
    # Scale it to fit nicely within a [-2, 2] plot limit
    Z_scaled = Z_centered * 1.2
    return Z_scaled

class ComplexRotationDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Complex Numbers: Image Rotation Engine")
        self.geometry("1100x650")
        self.minsize(900, 600)
        
        # Application State Variables
        self.current_angle = 0.0      # Current displayed angle in degrees
        self.target_angle = None      # Target angle for smooth lerping
        self.is_playing = False       # Continuous animation state
        self.Z_orig = generate_demo_shape()
        
        # Setup UI Layout
        self.setup_ui()
        self.setup_matplotlib()
        
        # Initial Render
        self.update_visuals(0)
        
        # Start the 60FPS animation loop
        self.animation_loop()

    def setup_ui(self):
        """Creates the grid layout and control panels for the application."""
        # Main layout configuration
        self.grid_rowconfigure(0, weight=1)    # Plot area
        self.grid_rowconfigure(1, weight=0)    # Control panel
        self.grid_columnconfigure(0, weight=1)

        # --- Plot Frame ---
        self.plot_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1E1E1E")
        self.plot_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        # --- Control & Math HUD Frame ---
        self.control_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#2B2B2B")
        self.control_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        # HUD: Mathematical Equation Display
        self.math_hud_var = ctk.StringVar(value="z' = z · e^(i · 0°) = z · (1.00 + 0.00i)")
        self.math_hud = ctk.CTkLabel(
            self.control_frame, 
            textvariable=self.math_hud_var, 
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
            text_color="#00FFCC"
        )
        self.math_hud.pack(pady=(15, 5))
        
        # Controls Container
        self.btn_container = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.btn_container.pack(pady=10)

        # Preset Buttons
        btn_style = {"width": 90, "height": 35, "corner_radius": 8}
        self.btn_30 = ctk.CTkButton(self.btn_container, text="Rotate 30°", command=lambda: self.set_target_angle(30), **btn_style)
        self.btn_30.pack(side="left", padx=10)
        
        self.btn_45 = ctk.CTkButton(self.btn_container, text="Rotate 45°", command=lambda: self.set_target_angle(45), **btn_style)
        self.btn_45.pack(side="left", padx=10)
        
        self.btn_90 = ctk.CTkButton(self.btn_container, text="Rotate 90°", command=lambda: self.set_target_angle(90), **btn_style)
        self.btn_90.pack(side="left", padx=10)
        
        # Play/Pause Animation
        self.btn_play = ctk.CTkButton(
            self.btn_container, text="Play Continuous", 
            command=self.toggle_play, fg_color="#FF6B6B", hover_color="#EE5253", **btn_style
        )
        self.btn_play.pack(side="left", padx=10)

        # Interactive Angle Slider
        slider_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        slider_frame.pack(fill="x", padx=40, pady=(5, 15))
        
        ctk.CTkLabel(slider_frame, text="0°", font=("Arial", 12)).pack(side="left")
        
        self.angle_slider = ctk.CTkSlider(
            slider_frame, from_=0, to=360, number_of_steps=360,
            command=self.on_slider_drag
        )
        self.angle_slider.set(0)
        self.angle_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        ctk.CTkLabel(slider_frame, text="360°", font=("Arial", 12)).pack(side="right")

    def setup_matplotlib(self):
        """Initializes the Matplotlib figure, subplots, and graphical objects."""
        # Create dark-themed Matplotlib Figure
        self.fig, (self.ax_argand, self.ax_shape) = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.patch.set_facecolor('#1E1E1E')
        
        # Style the subplots
        for ax in (self.ax_argand, self.ax_shape):
            ax.set_facecolor('#1E1E1E')
            ax.tick_params(colors='gray')
            for spine in ax.spines.values():
                spine.set_color('gray')
            ax.axhline(0, color='gray', linewidth=0.8, alpha=0.5)
            ax.axvline(0, color='gray', linewidth=0.8, alpha=0.5)
            ax.set_aspect('equal')

        # --- LEFT PANEL: Argand Plane ---
        self.ax_argand.set_title("Argand Plane: Rotator e^(iθ)", color="white", pad=15)
        self.ax_argand.set_xlim(-1.5, 1.5)
        self.ax_argand.set_ylim(-1.5, 1.5)
        
        # Draw Unit Circle
        theta_circle = np.linspace(0, 2*np.pi, 100)
        self.ax_argand.plot(np.cos(theta_circle), np.sin(theta_circle), 
                           color='gray', linestyle='--', alpha=0.7)
        
        # Initialize dynamic rotator vector (Line with arrowhead)
        self.rotator_line, = self.ax_argand.plot([0, 1], [0, 0], color='#FFD166', 
                                                linewidth=3, marker='o', markersize=8, markevery=[-1])
        
        # Fill arc to show swept angle
        self.angle_arc, = self.ax_argand.plot([], [], color='#FFD166', linewidth=2, alpha=0.5)

        # --- RIGHT PANEL: Shape Canvas ---
        self.ax_shape.set_title("Spatial Canvas: Z' = Z · e^(iθ)", color="white", pad=15)
        self.ax_shape.set_xlim(-2.5, 2.5)
        self.ax_shape.set_ylim(-2.5, 2.5)

        # Draw original ghost shape
        X_orig = np.real(self.Z_orig)
        Y_orig = np.imag(self.Z_orig)
        self.ax_shape.plot(X_orig, Y_orig, color='gray', linewidth=2, linestyle='--', alpha=0.5)

        # Initialize dynamic rotated shape
        self.rotated_shape_line, = self.ax_shape.plot(X_orig, Y_orig, color='#00FFCC', linewidth=3)
        
        # Initialize dynamic trails (paths swept by vertices)
        self.trail_lines = []
        # Select 3 prominent vertices to trace
        self.trace_indices = [2, 6, 8] 
        for _ in self.trace_indices:
            line, = self.ax_shape.plot([], [], color='#EF476F', linestyle=':', linewidth=1.5, alpha=0.8)
            self.trail_lines.append(line)

        # Embed into CustomTkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def update_visuals(self, angle_deg):
        """
        The core engine. Performs complex math based on current angle 
        and updates line objects for 60FPS high-performance rendering.
        """
        angle_rad = np.radians(angle_deg)
        
        # 1. Complex Multiplication Math
        rotator = np.exp(1j * angle_rad)          # e^(i * theta)
        Z_rotated = self.Z_orig * rotator         # Apply rotation to entire shape matrix
        
        # Update HUD Math Text
        cos_val, sin_val = np.real(rotator), np.imag(rotator)
        sign = "+" if sin_val >= 0 else "-"
        self.math_hud_var.set(f"z' = z · e^(i · {angle_deg:0.1f}°) = z · ({cos_val:0.2f} {sign} {abs(sin_val):0.2f}i)")
        self.angle_slider.set(angle_deg)

        # 2. Update Argand Plane (Left)
        # Update Rotator Vector
        self.rotator_line.set_data([0, cos_val], [0, sin_val])
        
        # Update Angle Sweeping Arc
        arc_thetas = np.linspace(0, angle_rad, max(10, int(angle_deg)))
        self.angle_arc.set_data(0.3 * np.cos(arc_thetas), 0.3 * np.sin(arc_thetas))

        # 3. Update Shape Canvas (Right)
        self.rotated_shape_line.set_data(np.real(Z_rotated), np.imag(Z_rotated))
        
        # Update Trails (Mathematical arcs drawn by complex phase shifting)
        for idx, trail_line in zip(self.trace_indices, self.trail_lines):
            z_point = self.Z_orig[idx]
            # Sweep this specific point from 0 to current angle
            path_complex = z_point * np.exp(1j * arc_thetas)
            trail_line.set_data(np.real(path_complex), np.imag(path_complex))

        # Blit/Draw update (faster than redrawing entire UI)
        self.fig.canvas.draw_idle()

    def animation_loop(self):
        """Handles smooth frame-by-frame updates for continuous play and lerping."""
        if self.is_playing:
            # Continuous rotation
            self.current_angle = (self.current_angle + 1.5) % 360
            self.update_visuals(self.current_angle)
            
        elif self.target_angle is not None:
            # Smooth Linear Interpolation (Lerp) towards target preset
            diff = self.target_angle - self.current_angle
            
            # Handle shortest path wrap-around for 360 degrees
            if diff > 180: diff -= 360
            elif diff < -180: diff += 360
                
            if abs(diff) < 0.5:
                # Snap to target when close enough
                self.current_angle = self.target_angle
                self.target_angle = None
            else:
                # Lerp step
                self.current_angle += diff * 0.1
                
            # Keep within 0-360 purely for UI cleanliness
            self.current_angle = self.current_angle % 360 
            self.update_visuals(self.current_angle)

        # Call this function again in 16ms (~60 FPS)
        self.after(16, self.animation_loop)

    def set_target_angle(self, angle):
        """Triggered by preset buttons to start a smooth animation to a new angle."""
        self.is_playing = False
        self.btn_play.configure(text="Play Continuous", fg_color="#FF6B6B")
        self.target_angle = angle

    def on_slider_drag(self, value):
        """Triggered by dragging the interactive slider."""
        self.is_playing = False
        self.target_angle = None
        self.btn_play.configure(text="Play Continuous", fg_color="#FF6B6B")
        self.current_angle = float(value)
        self.update_visuals(self.current_angle)
        
    def toggle_play(self):
        """Toggles the continuous rotation animation."""
        self.is_playing = not self.is_playing
        self.target_angle = None
        if self.is_playing:
            self.btn_play.configure(text="Pause Animation", fg_color="#45B7D1")
        else:
            self.btn_play.configure(text="Play Continuous", fg_color="#FF6B6B")

if __name__ == "__main__":
    try:
        app = ComplexRotationDemo()
        app.mainloop()
    except Exception as e:
        print(f"Error initializing the application: {e}")
        print("Please ensure you have installed the requirements: pip install numpy matplotlib customtkinter")
        sys.exit(1)