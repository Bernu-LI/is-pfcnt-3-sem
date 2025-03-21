import pygame
import math

# Initialize Pygame
pygame.init()

# Calculate velocities after collisions
def calculate_collision(m1, m2, v1, v2, p1, p2):
    # Distance vector
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.hypot(dx, dy)

    # Normalized vector
    nx = dx / dist
    ny = dy / dist

    # Velocity projection onto the collision line
    v1n = v1[0]*nx + v1[1]*ny
    v2n = v2[0]*nx + v2[1]*ny

    # Impulse rule for velocities exchange
    p1n = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    p2n = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

    # Convert back to general velocities
    v1[0] += (p1n - v1n) * nx
    v1[1] += (p1n - v1n) * ny
    v2[0] += (p2n - v2n) * nx
    v2[1] += (p2n - v2n) * ny

# Input
mass1 = float(input("Enter mass of the first body: "))
radius1 = float(input("Enter radius of the first body: "))
speed1 = float(input("Enter velocity module of the first body: "))
angle1 = float(input("Enter velocity angle of the first body (in degrees): "))
mass2 = float(input("Enter mass of the second body: "))
radius2 = float(input("Enter radius of the second body: "))
speed2 = float(input("Enter velocity module of the second body: "))
angle2 = float(input("Enter velocity angle of the second body (in degrees): "))

# Convert degrees to radians
angle1_rad = math.radians(angle1)
angle2_rad = math.radians(angle2)

# Calculate velocity components
velocity1 = [speed1 * math.cos(angle1_rad), speed1 * math.sin(angle1_rad)]
velocity2 = [speed2 * math.cos(angle2_rad), speed2 * math.sin(angle2_rad)]

# Initialize positions
pos1 = [100, 100]
pos2 = [300, 200]

# Window parameters
width, height = 700, 500

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Elastic non-center collision")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Update positions
    pos1[0] += velocity1[0]
    pos1[1] += velocity1[1]
    pos2[0] += velocity2[0]
    pos2[1] += velocity2[1]

    # Handle collisions with boundaries
    for pos, velocity, radius in zip([pos1, pos2], [velocity1, velocity2], [radius1, radius2]):
        if pos[0] <= radius or pos[0] >= width - radius:
            velocity[0] *= -1
        if pos[1] <= radius or pos[1] >= height - radius:
            velocity[1] *= -1

    # Handle collisions between bodies
    dist = math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])
    if dist <= radius1 + radius2:
        calculate_collision(mass1, mass2, velocity1, velocity2, pos1, pos2)

    # Draw
    pygame.draw.circle(screen, (255, 0, 0), [int(pos1[0]), int(pos1[1])], int(radius1))
    pygame.draw.circle(screen, (0, 0, 255), [int(pos2[0]), int(pos2[1])], int(radius2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()