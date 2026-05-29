#!/usr/bin/env python3
"""
Harmonic Series Square Wave Visualizer
Shows how adding odd harmonics builds a square wave
N = number of harmonics (1, 3, 5, 7, 9...)
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # Import ALL GLUT functions
import numpy as np
import math
import sys

# Initialize Pygame and OpenGL
pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Fourier Series: Square Wave Synthesis")

# Initialize GLUT (MUST be called before any GLUT functions)
glutInit(sys.argv)

# Setup orthographic projection (2D)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Enable blending for smooth drawing
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Colors (RGB, A)
WHITE = (1.0, 1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0, 1.0)
RED = (1.0, 0.0, 0.0, 0.8)
GREEN = (0.0, 1.0, 0.0, 0.8)
BLUE = (0.0, 0.0, 1.0, 0.8)
YELLOW = (1.0, 1.0, 0.0, 1.0)
CYAN = (0.0, 1.0, 1.0, 0.8)
PURPLE = (0.8, 0.0, 0.8, 0.8)
ORANGE = (1.0, 0.65, 0.0, 0.8)

# Animation parameters
x_offset = 200  # Start x position for wave
y_center = SCREEN_HEIGHT // 2  # Center y position
t = 0  # Time variable (phase)
speed = 0.02  # Animation speed
N = 1  # Current number of harmonics (using odd numbers only)
max_N = 19  # Maximum harmonics to show

# Store wave points for trace
wave_points = []
max_points = SCREEN_WIDTH - x_offset - 100

def calculate_square_wave(x, n_terms):
    """
    Calculate square wave value using Fourier series
    Square wave: f(x) = 4/π * Σ(sin((2k-1)x)/(2k-1))
    where k = 1 to n_terms (odd harmonics only)
    """
    result = 0
    for k in range(1, n_terms + 1):
        harmonic_num = 2*k - 1  # 1, 3, 5, 7...
        result += (4.0 / math.pi) * math.sin(harmonic_num * x) / harmonic_num
    return result

def calculate_harmonic_component(x, harmonic_num):
    """
    Calculate individual harmonic component
    amplitude = 4/(π * harmonic_num)
    """
    amplitude = 4.0 / (math.pi * harmonic_num)
    return amplitude * math.sin(harmonic_num * x)

def draw_circle(x, y, radius, color):
    """Draw a small circle (for harmonic visualization)"""
    glColor4f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    num_segments = max(20, int(radius * 2))  # More segments for larger circles
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    glEnd()

def draw_text(x, y, text, color=WHITE):
    """Draw text using OpenGL's bitmap fonts"""
    glColor4f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

def draw_waveform():
    """Draw the reconstructed square wave"""
    global wave_points, t
    
    # Clear points list when it gets too long
    if len(wave_points) > max_points:
        wave_points.pop(0)
    
    # Calculate current y value at x = x_offset + width
    x_val = t
    y_val = calculate_square_wave(x_val, N)
    
    # Scale and translate to screen coordinates
    screen_x = x_offset + len(wave_points)
    screen_y = y_center + y_val * 100  # Scale factor 100
    
    wave_points.append((screen_x, screen_y))
    
    # Draw the wave trace
    if len(wave_points) > 1:
        glColor4f(*YELLOW)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        for point in wave_points:
            glVertex2f(point[0], point[1])
        glEnd()
    
    # Draw individual harmonic components (epicycles style)
    harmonic_colors = [RED, GREEN, BLUE, PURPLE, CYAN, ORANGE]
    current_x = x_offset - 80
    current_y = y_center + 200  # Above main waveform
    
    for k in range(1, N + 1):
        harmonic_num = 2*k - 1
        harmonic_val = calculate_harmonic_component(t, harmonic_num)
        
        # Draw a circle representing the harmonic
        radius = abs(harmonic_val) * 50
        if radius > 2:
            draw_circle(current_x, current_y, radius, harmonic_colors[(k-1) % len(harmonic_colors)])
        
        # Draw connecting line
        glColor4f(0.5, 0.5, 0.5, 0.5)
        glLineWidth(1)
        glBegin(GL_LINES)
        glVertex2f(current_x, current_y)
        glVertex2f(current_x + harmonic_val * 80, current_y)
        glEnd()
        
        current_x += harmonic_val * 80

def draw_grid():
    """Draw background grid"""
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glLineWidth(1)
    
    # Vertical grid lines
    for x in range(x_offset, SCREEN_WIDTH - 50, 50):
        glBegin(GL_LINES)
        glVertex2f(x, 50)
        glVertex2f(x, SCREEN_HEIGHT - 50)
        glEnd()
    
    # Horizontal grid lines
    for y in range(50, SCREEN_HEIGHT - 50, 50):
        glBegin(GL_LINES)
        glVertex2f(x_offset, y)
        glVertex2f(SCREEN_WIDTH - 50, y)
        glEnd()
    
    # Draw center line (zero axis)
    glColor4f(0.5, 0.5, 0.5, 0.8)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(x_offset - 10, y_center)
    glVertex2f(SCREEN_WIDTH - 50, y_center)
    glEnd()

def draw_info():
    """Draw UI information"""
    font_y = 30
    
    # Title
    draw_text(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 40, 
              "FOURIER SERIES: SQUARE WAVE SYNTHESIS", YELLOW)
    
    # Harmonic information
    draw_text(20, font_y, f"Harmonics (odd): N = {N}", CYAN)
    font_y += 25
    
    # Expected square wave quality
    accuracy = (1.0 - 1.0/(2*N)) * 100 if N > 0 else 0
    draw_text(20, font_y, f"Approximation accuracy: {accuracy:.1f}%", GREEN)
    font_y += 25
    
    draw_text(20, font_y, "Individual harmonics (epicycles):", RED)
    font_y += 20
    
    # Show current harmonics being used
    for k in range(1, min(N, 6) + 1):
        harmonic_num = 2*k - 1
        amplitude = 4.0 / (math.pi * harmonic_num)
        draw_text(30, font_y, f"Harmonic {harmonic_num}: amplitude = {amplitude:.3f}", 
                  (0.5 + k*0.1, 0.3, 0.8, 1.0))
        font_y += 18
    
    if N > 6:
        draw_text(30, font_y, f"... and {N-5} more harmonics", (0.8, 0.8, 0.8, 1.0))
    
    # Controls
    font_y = SCREEN_HEIGHT - 100
    draw_text(20, font_y, "CONTROLS:", WHITE)
    draw_text(30, font_y - 20, "UP/DOWN: Increase/Decrease harmonics", (0.7, 0.7, 0.7, 1.0))
    draw_text(30, font_y - 38, "SPACE: Pause/Resume", (0.7, 0.7, 0.7, 1.0))
    draw_text(30, font_y - 56, "R: Reset wave trace", (0.7, 0.7, 0.7, 1.0))
    draw_text(30, font_y - 74, "ESC: Exit", (0.7, 0.7, 0.7, 1.0))
    
    # Ideal square wave reference (right side)
    draw_text(SCREEN_WIDTH - 250, y_center + 100, "Ideal Square Wave:", WHITE)
    draw_text(SCREEN_WIDTH - 250, y_center + 85, "has infinite harmonics", (0.6, 0.6, 0.6, 1.0))
    draw_text(SCREEN_WIDTH - 250, y_center + 70, "N = ∞", YELLOW)

def draw_harmonic_bars():
    """Draw frequency spectrum bar chart"""
    bar_width = 30
    start_x = SCREEN_WIDTH - 280
    start_y = y_center - 150
    
    # Draw title
    draw_text(start_x, start_y + 130, "FREQUENCY SPECTRUM", WHITE)
    
    # Draw bars for each harmonic
    max_bars = min(N, 12)  # Show up to 12 harmonics
    for k in range(1, max_bars + 1):
        harmonic_num = 2*k - 1
        amplitude = 4.0 / (math.pi * harmonic_num)
        bar_height = amplitude * 150  # Scale for visibility
        
        x = start_x + (k-1) * (bar_width + 5)
        y = start_y + bar_height
        
        # Draw bar
        glColor4f(0.0, 0.5 + amplitude * 0.5, 1.0 - amplitude, 0.8)
        glBegin(GL_QUADS)
        glVertex2f(x, start_y)
        glVertex2f(x + bar_width, start_y)
        glVertex2f(x + bar_width, y)
        glVertex2f(x, y)
        glEnd()
        
        # Draw frequency label
        draw_text(x + 5, start_y - 20, str(harmonic_num), (0.8, 0.8, 0.8, 1.0))

def main():
    global t, N, wave_points
    clock = pygame.time.Clock()
    paused = False
    running = True
    
    while running:
        dt = clock.tick(60)  # 60 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    if N + 2 <= max_N:
                        N += 2
                        wave_points = []  # Reset trace for clarity
                elif event.key == pygame.K_DOWN:
                    if N - 2 >= 1:
                        N -= 2
                        wave_points = []
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    wave_points = []
        
        if not paused:
            t += speed
            # Reset t to prevent overflow
            if t > 2 * math.pi * 10:
                t = 0
                wave_points = []
        
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
        
        # Draw all elements
        draw_grid()
        draw_harmonic_bars()
        draw_waveform()
        draw_info()
        
        # Draw a vertical line showing current phase
        if len(wave_points) > 0:
            glColor4f(1.0, 1.0, 1.0, 0.3)
            glLineWidth(1)
            glBegin(GL_LINES)
            glVertex2f(x_offset + len(wave_points), 50)
            glVertex2f(x_offset + len(wave_points), SCREEN_HEIGHT - 50)
            glEnd()
        
        # Update display
        pygame.display.flip()
        glFlush()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()