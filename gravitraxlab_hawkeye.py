# ============================================================================
# AUTHOR: Javier Hidalgo Fernández
# DATE: July 28, 2026
# ASSOCIATED DOCUMENT: [Vector field 'Velocity' in projectile motion:
# Mathematical modeling and empirical validation - Second Edition]
#
# LICENSE: Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International
# LICENSE URL: https://creativecommons.org/licenses/by-nc-nd/4.0/
# ============================================================================

import cv2 
import numpy as np 
import tkinter as tk 
from tkinter import messagebox, filedialog, simpledialog

def request_initial_data(): 
    """Opens GUI popups to capture the initial configuration parameters.""" 
    root = tk.Tk() 
    root.withdraw() 
    
    messagebox.showinfo("Configuration", "Welcome to the GraviTraxLAB Automation Software.\nSelect the MP4 video file to analyze.") 
    video_path = filedialog.askopenfilename(filetypes=[("MP4 Videos", "*.mp4"), ("All Files", "*.*")])
    if not video_path: 
        exit() 
    
    marble_color = simpledialog.askstring("Marble Color", "Type the marble color (green, blue, red, grey):").strip().lower() 
    return video_path, marble_color 

# --- SCIENTIFIC CONFIGURATION CONSTANTS --- 
REAL_MARBLE_DIAMETER_MM = 12.7  # Fixed standard physical marble sizing calibration
TOLERANCE_THRESHOLD_MM = 5.0    # Success margin for experiment validation

# --- CORE PROGRAM INITIALIZATION --- 
video_path, selected_color = request_initial_data() 

# Setup baseline HSV spectrum boundaries depending on user input
if selected_color == "green":
    h_min, s_min, v_min, h_max, s_max, v_max = 35, 50, 50, 85, 255, 255
elif selected_color == "blue":
    h_min, s_min, v_min, h_max, s_max, v_max = 90, 50, 50, 130, 255, 255
elif selected_color == "red":
    h_min, s_min, v_min, h_max, s_max, v_max = 0, 30, 30, 25, 255, 255
else:  # Metallic grey (Low saturation, medium-high brightness)
    h_min, s_min, v_min, h_max, s_max, v_max = 0, 0, 50, 180, 40, 220

# Initialize video processing engine and properties
cap = cv2.VideoCapture(video_path) 
fps = cap.get(cv2.CAP_PROP_FPS) 
if fps == 0: fps = 30.0 

# Create graphical layout sliders for masking adjustments
cv2.namedWindow("Color Calibration") 
cv2.createTrackbar("H Min", "Color Calibration", h_min, 179, lambda x: None) 
cv2.createTrackbar("H Max", "Color Calibration", h_max, 179, lambda x: None) 
cv2.createTrackbar("S Min", "Color Calibration", s_min, 255, lambda x: None) 
cv2.createTrackbar("S Max", "Color Calibration", s_max, 255, lambda x: None) 
cv2.createTrackbar("V Min", "Color Calibration", v_min, 255, lambda x: None) 
cv2.createTrackbar("V Max", "Color Calibration", v_max, 255, lambda x: None) 

print("INSTRUCTIONS: Adjust trackbars. Press 'Space' to begin analysis.") 

# Operational coordinate pointers
piece_center_x = None
piece_center_y = None
piece_radius = 100

# PRELIMINARY RUN: Real-time user filtering window
while True: 
    ret, frame = cap.read() 
    if not ret: 
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
        continue 
    
    # Scale frame natively to optimize hardware interface resolution
    frame = cv2.resize(frame, (640, 480)) 
    h_min = cv2.getTrackbarPos("H Min", "Color Calibration") 
    h_max = cv2.getTrackbarPos("H Max", "Color Calibration") 
    s_min = cv2.getTrackbarPos("S Min", "Color Calibration") 
    s_max = cv2.getTrackbarPos("S Max", "Color Calibration") 
    v_min = cv2.getTrackbarPos("V Min", "Color Calibration") 
    v_max = cv2.getTrackbarPos("V Max", "Color Calibration") 
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    # Dual-pass masking to safely isolate the full spectrum of red hues
    if selected_color == "red":
        mask1 = cv2.inRange(hsv, np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max]))
        mask2 = cv2.inRange(hsv, np.array([170, s_min, v_min]), np.array([180, s_max, v_max]))
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max])) 
    
    # Crop mask with an internal geometric circle to protect edges from environment noises
    height, width, _ = frame.shape 
    center_x, center_y = int(width / 2), int(height / 2) 
    roi_radius = int(min(width, height) * 0.25) 
    
    geometric_mask = np.zeros(mask.shape, dtype=np.uint8) 
    cv2.circle(geometric_mask, (center_x, center_y), roi_radius, 255, -1) 
    mask = cv2.bitwise_and(mask, geometric_mask) 
    
    cv2.imshow("Color Calibration", mask) 
    cv2.imshow("Original Video (Press Spacebar to Confirm)", frame) 
    
    # Key listener: pressing Space locks properties and continues
    if cv2.waitKey(30) & 0xFF == 32: 
        final_h_min = h_min 
        final_h_max = h_max 
        final_s_min = s_min 
        final_s_max = s_max 
        final_v_min = v_min 
        final_v_max = v_max 
        
        # Set central pixel estimates as starting point for the target crosshair
        piece_center_x, piece_center_y = int(width / 2), int(height / 2)
        break 

cv2.destroyWindow("Color Calibration") 
cap.set(cv2.CAP_PROP_POS_FRAMES, 1)  # Rewind digital footage to trigger mathematical analytics

position_history = [] 
radius_history = []  
current_frame = 0 

# SECONDARY RUN: Main computational tracking loop
while True: 
    ret, frame = cap.read() 
    if not ret: break 
    
    current_frame += 1 
    frame = cv2.resize(frame, (640, 480)) 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    
    if selected_color == "red":
        mask1 = cv2.inRange(hsv, np.array([final_h_min, final_s_min, final_v_min]), np.array([final_h_max, final_s_max, final_v_max]))
        mask2 = cv2.inRange(hsv, np.array([170, final_s_min, final_v_min]), np.array([180, final_s_max, final_v_max]))
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, np.array([final_h_min, final_s_min, final_v_min]), np.array([final_h_max, final_s_max, final_v_max])) 
    
    # Apply standard geometric ROI filtering inside calculation loops
    height, width, _ = frame.shape 
    center_x, center_y = int(width / 2), int(height / 2) 
    roi_radius = int(min(width, height) * 0.25) 
    
    geometric_mask = np.zeros(mask.shape, dtype=np.uint8) 
    cv2.circle(geometric_mask, (center_x, center_y), roi_radius, 255, -1) 
    mask = cv2.bitwise_and(mask, geometric_mask) 
    
    # Clean micro background noise artifacts via morphology open techniques
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8)) 
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    # Store analytical path history parameters
    for c in contours: 
        area = cv2.contourArea(c) 
        if 5 < area < 2000: 
            ((x, y), radius) = cv2.minEnclosingCircle(c) 
            if radius > 1: 
                position_history.append((x, y, current_frame)) 
                radius_history.append(radius)

# POST-PROCESSING ENGINE: Metric calculations and manual fine-tuning canvas
if len(position_history) > 0: 
    # Locate lower bounding impact target via structural path history
    final_bounce_point = max(position_history, key=lambda p: p) 
    x_pixel_bounce, y_pixel_bounce, bounce_frame_index = final_bounce_point 
    
    # Automated pixel-to-millimeter scaling based on the median diameter of the marble
    avg_pixel_radius = np.median(radius_history)
    px_diameter_marble = avg_pixel_radius * 2
    mm_per_pixel = REAL_MARBLE_DIAMETER_MM / px_diameter_marble  
    
    exact_seconds = bounce_frame_index / fps 
    cap.set(cv2.CAP_PROP_POS_FRAMES, bounce_frame_index - 1) 
    _, base_impact_frame = cap.read() 
    
    if base_impact_frame is not None: 
        base_impact_frame = cv2.resize(base_impact_frame, (640, 480)) 
        angle_deg = 45 
        
        print("\n=== MANUAL ALIGNMENT ASSISTANT ACTIVE ===")
        print("Center the yellow crosshair onto the physical landing pad surface:")
        print("W/S: Move Center Up/Down | A/D: Move Center Left/Right")
        print("Q/E: Rotate Crosshair Lines Orientation")
        print("ENTER: Confirm Positioning and Compute Final Metrics\n")
        
        # Interactive keyboard correction loop
        while True:
            impact_frame = base_impact_frame.copy()
            
            # Map trigonometric vector parameters to allow crosshair rotations
            rad = np.radians(angle_deg)
            cos_a, sin_a = np.cos(rad), np.sin(rad)
            length = int(piece_radius * 0.8)
            
            # Draw diagonal axis vector 1
            p1_x = int(piece_center_x - length * cos_a)
            p1_y = int(piece_center_y - length * sin_a)
            p2_x = int(piece_center_x + length * cos_a)
            p2_y = int(piece_center_y + length * sin_a)
            
            # Draw perpendicular diagonal axis vector 2 (+90 degrees offset)
            rad2 = np.radians(angle_deg + 90)
            p3_x = int(piece_center_x - length * np.cos(rad2))
            p3_y = int(piece_center_y - length * np.sin(rad2))
            p4_x = int(piece_center_x + length * np.cos(rad2))
            p4_y = int(piece_center_y + length * np.sin(rad2))
            
            # Overlay crosshair metrics and indicators
            cv2.line(impact_frame, (p1_x, p1_y), (p2_x, p2_y), (0, 255, 255), 2)
            cv2.line(impact_frame, (p3_x, p3_y), (p4_x, p4_y), (0, 255, 255), 2)
            
            cv2.circle(impact_frame, (piece_center_x, piece_center_y), 4, (255, 255, 255), -1)
            cv2.circle(impact_frame, (int(x_pixel_bounce), int(y_pixel_bounce)), 12, (0, 0, 255), -1) 
            cv2.circle(impact_frame, (int(x_pixel_bounce), int(y_pixel_bounce)), 15, (255, 255, 255), 2) 
            cv2.line(impact_frame, (piece_center_x, piece_center_y), (int(x_pixel_bounce), int(y_pixel_bounce)), (0, 255, 0), 2)
            
            cv2.putText(impact_frame, "Adjust: W,A,S,D | Rotate: Q,E | ENTER: Finish", (15, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow("GraviTraxLAB Hawk-Eye - Manual Calibration", impact_frame)
            
            # Capture standard keystroke values
            key = cv2.waitKey(0) & 0xFF

            if key == ord('w'): piece_center_y -= 1
            elif key == ord('s'): piece_center_y += 1
            elif key == ord('a'): piece_center_x -= 1
            elif key == ord('d'): piece_center_x += 1
            elif key == ord('q'): angle_deg -= 1
            elif key == ord('e'): angle_deg += 1
            elif key == 13 or key == 141: # Enter key codes
                break

        # Apply Euclidean 2D distance algorithms between user verified coordinates
        distance_pixels = np.sqrt((x_pixel_bounce - piece_center_x)**2 + (y_pixel_bounce - piece_center_y)**2)
        distance_mm = distance_pixels * mm_per_pixel 

        # Build graphical overlay indicators
        within_range = 0.0 <= distance_mm <= 0.5 
        result_text = f"Pad Center Dist: {distance_mm:.3f} mm -> {'WITHIN RANGE' if within_range else 'OUT OF RANGE'}"
        time_text = f"Bounce Timestamp: {exact_seconds:.3f} s (Frame: {bounce_frame_index})"
        
        cv2.putText(impact_frame, result_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if within_range else (0, 0, 255), 2) 
        cv2.putText(impact_frame, time_text, (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) 

        # Display operational status to the user using window messaging alerts
        root = tk.Tk() 
        root.withdraw() 
        messagebox.showinfo("AUTOMATED EXPERIMENTAL RESULT", f"Verification Complete:\n\n-{time_text}\n-{result_text}") 
        
        cv2.imshow("GraviTraxLAB Hawk-Eye - Impact Frame Display", impact_frame) 
        cv2.waitKey(0) 
else: 
    root = tk.Tk() 
    root.withdraw() 
    messagebox.showerror("Error", "Failed to resolve marble trajectory paths.") 

cap.release() 
cv2.destroyAllWindows()