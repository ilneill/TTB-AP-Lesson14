# Using an Arduino with Python LESSON 14: Model a Moving Marble in a Room Using Parameters.
# https://www.youtube.com/watch?v=JA4UbI2v0EA
# https://toptechboy.com/

# Internet References:
# https://www.glowscript.org/docs/VPythonDocs/index.html

from vpython import *
import numpy as np

# vPython refresh rate.
vPythonRefreshRate = 100

# A place on which to put our things...
canvas(title = "<b><i>Arduino with Python - Connected boxes containing bouncing balls!</i></b>", background = color.cyan, width = 800, height = 600)

# A function to draw an arena box.
def buildBox(rPos = vector(0, 0, 0), boxSize = 1):
    boxY = boxSize      # Height.
    boxX = boxSize * 3  # Width.
    boxZ = boxSize * 2  # Depth.
    wallThickness = (boxZ + boxX + boxY) / 200
    wallLeft   = box(color = color.gray(0.5), opacity = 0.75, pos = vector(-boxX / 2,  0, 0) + rPos, size = vector(wallThickness, boxY, boxZ + wallThickness))
    wallRight  = box(color = color.gray(0.5), opacity = 0.75, pos = vector( boxX / 2,  0, 0) + rPos, size = vector(wallThickness, boxY, boxZ + wallThickness))
    wallTop    = box(color = color.gray(0.5), opacity = 0.75, pos = vector( 0,  boxY / 2, 0) + rPos, size = vector(boxX, wallThickness, boxZ + wallThickness))
    wallBottom = box(color = color.gray(0.5), opacity = 0.75, pos = vector( 0, -boxY / 2, 0) + rPos, size = vector(boxX, wallThickness, boxZ + wallThickness))
    wallRear   = box(color = color.gray(0.5), opacity = 0.75, pos = vector( 0, 0, -boxZ / 2) + rPos, size = vector(boxX, boxY, wallThickness))
    wallFront  = box(color = color.gray(0.5), opacity = 0.10, pos = vector( 0, 0,  boxZ / 2) + rPos, size = vector(boxX, boxY, wallThickness))
    topleftCornerTrim     = cylinder (color = color.gray(0.5), opacity = 0.75, radius = wallThickness / 2, pos = vector(-boxX / 2,  boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    toprightCornerTrim    = cylinder (color = color.gray(0.5), opacity = 0.75, radius = wallThickness / 2, pos = vector( boxX / 2,  boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    bottomleftCornerTrim  = cylinder (color = color.gray(0.5), opacity = 0.75, radius = wallThickness / 2, pos = vector(-boxX / 2, -boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    bottomrightCornerTrim = cylinder (color = color.gray(0.5), opacity = 0.75, radius = wallThickness / 2, pos = vector( boxX / 2, -boxY / 2, -(boxZ + wallThickness) / 2) + rPos, axis = vector(0, 0, boxZ + wallThickness))
    # Return the box boundaries -> [x-left, x-right, y-bottom, y-top, z-back, z-front].
    return([(-boxX / 2 + wallThickness / 2 + rPos.x), (boxX / 2 - wallThickness / 2 + rPos.x),
            (-boxY / 2 + wallThickness / 2 + rPos.y), (boxY / 2 - wallThickness / 2 + rPos.y),
            (-boxZ / 2 + wallThickness / 2 + rPos.z), (boxZ / 2 - wallThickness / 2 + rPos.z)])

# A function to draw a tunnel box.
def buildTunnel(rPos = vector(0, 0, 0), tunnelSize = 1):
    tunnelY = tunnelSize        # Height.
    tunnelX = tunnelSize / 1.00 # Width.
    tunnelZ = tunnelSize / 1.00 # Depth.
    wallThickness = (tunnelX + tunnelY + tunnelZ) / 200
    wallLeft  = box(color = color.gray(0.5), opacity = 0.75, pos = vector(-tunnelX / 2,  0, 0) + rPos, size = vector(wallThickness, tunnelY, tunnelZ))
    wallRight = box(color = color.gray(0.5), opacity = 0.75, pos = vector( tunnelX / 2,  0, 0) + rPos, size = vector(wallThickness, tunnelY, tunnelZ))
    wallRear  = box(color = color.gray(0.5), opacity = 0.75, pos = vector( 0, 0, -tunnelZ / 2) + rPos, size = vector(tunnelX, tunnelY, wallThickness))
    wallRear  = box(color = color.gray(0.5), opacity = 0.10, pos = vector( 0, 0,  tunnelZ / 2) + rPos, size = vector(tunnelX, tunnelY, wallThickness))
    backleftCornerTrim  = cylinder (color = color.gray(0.5), opacity = 0.75, radius = wallThickness / 2, pos = vector(-tunnelX / 2, -tunnelY / 2, -(tunnelZ) / 2) + rPos, axis = vector(0, tunnelY, 0))
    backrightCornerTrim = cylinder (color = color.gray(0.5), opacity = 0.75, radius = wallThickness / 2, pos = vector( tunnelX / 2, -tunnelY / 2, -(tunnelZ) / 2) + rPos, axis = vector(0, tunnelY, 0))
    # Return the box boundaries -> [x-left, x-right, y-bottom, y-top, z-back, z-front].
    return([(-tunnelX / 2 + wallThickness / 2 + rPos.x), (tunnelX / 2 - wallThickness / 2 + rPos.x),
            (-tunnelY / 2 + rPos.y),                     (tunnelY / 2 + rPos.y),
            (-tunnelZ / 2 + wallThickness / 2 + rPos.z), (tunnelZ / 2 - wallThickness / 2 + rPos.z)])

# Upper arena.
arena1Size = 10
arena1Centre = vector(0, arena1Size, 0) # Positive Y, above the Z plane.
arena1 = buildBox(arena1Centre, arena1Size)
ball1Radius = 0.05 * arena1Size
ball1 = sphere(color = color.green, opacity = 1, radius = ball1Radius, pos = arena1Centre, make_trail = True, retain = arena1Size * 10)
# A random position change vector for ball1.
ball1Change = vector((np.random.rand() - 0.5) / (arena1Size / 2), (np.random.rand() - 0.5) / (arena1Size / 2), (np.random.rand() - 0.5) / (arena1Size / 2))

# Lower arena.
arena2Size = 15
arena2Centre = vector(0, -arena2Size, 0) # Negative Y, below the Z plane.
arena2 = buildBox(arena2Centre, arena2Size)
ball2Radius = 0.05 * arena2Size
ball2 = sphere(color = color.blue, opacity = 1, radius = ball2Radius, pos = arena2Centre, make_trail = True, retain = arena2Size * 10)
# A random position change vector for ball2.
ball2Change = vector((np.random.rand() - 0.5) / (arena2Size / 2), (np.random.rand() - 0.5) / (arena2Size / 2), (np.random.rand() - 0.5) / (arena2Size / 2))

# Linking tunnel - tunnel size and position related to the size and position of arena1 and arena2.
tunnelSize = abs(arena1[2]) + abs(arena2[3]) # Related to the arenas.
tunnelCentre = vector(0, (arena1[2] + arena2[3]) / 2, 0)
tunnel = buildTunnel(tunnelCentre, tunnelSize)

# Preping for the bouncing balls - not yet able to get them to leave their starting arena if they have a radius!
ball1Radius = 0
ball2Radius = 0

# An infinite loop: When is True, True? It is always True!
while True:
    rate(vPythonRefreshRate) # The vPython rate command is obligatory in animation loops.

    # Check where ball1 is going, and update the boundaries.
    if ((arena1[0] + ball1Radius) <= (ball1.pos.x + ball1Change.x) and (ball1.pos.x + ball1Change.x) <= (arena1[1] - ball1Radius)
        and (arena1[2] + ball1Radius) <= (ball1.pos.y + ball1Change.y) and (ball1.pos.y + ball1Change.y) <= (arena1[3] - ball1Radius)
        and (arena1[4] + ball1Radius) <= (ball1.pos.z + ball1Change.z) and (ball1.pos.z + ball1Change.z) <= (arena1[5] - ball1Radius)):
        bounds1 = arena1
    if ((arena2[0] + ball1Radius) <= (ball1.pos.x + ball1Change.x) and (ball1.pos.x + ball1Change.x) <= (arena2[1] - ball1Radius)
        and (arena2[2] + ball1Radius) <= (ball1.pos.y + ball1Change.y) and (ball1.pos.y + ball1Change.y) <= (arena2[3] - ball1Radius)
        and (arena2[4] + ball1Radius) <= (ball1.pos.z + ball1Change.z) and (ball1.pos.z + ball1Change.z) <= (arena2[5] - ball1Radius)):
        bounds1 = arena2
    if ((tunnel[0] + ball1Radius) <= (ball1.pos.x + ball1Change.x) and (ball1.pos.x + ball1Change.x) <= (tunnel[1] - ball1Radius)
        and (tunnel[2] + ball1Radius) <= (ball1.pos.y + ball1Change.y) and (ball1.pos.y + ball1Change.y) <= (tunnel[3] - ball1Radius)
        and (tunnel[4] + ball1Radius) <= (ball1.pos.z + ball1Change.z) and (ball1.pos.z + ball1Change.z) <= (tunnel[5] - ball1Radius)):
        bounds1 = tunnel

    # Check where ball2 is going, and update the boundaries.
    if ((arena1[0] + ball2Radius) <= (ball2.pos.x + ball2Change.x) and (ball2.pos.x + ball2Change.x) <= (arena1[1] - ball2Radius)
        and (arena1[2] + ball2Radius) <= (ball2.pos.y + ball2Change.y) and (ball2.pos.y + ball2Change.y) <= (arena1[3] - ball2Radius)
        and (arena1[4] + ball2Radius) <= (ball2.pos.z + ball2Change.z) and (ball2.pos.z + ball2Change.z) <= (arena1[5] - ball2Radius)):
        bounds2 = arena1
    if ((arena2[0] + ball2Radius) <= (ball2.pos.x + ball2Change.x) and (ball2.pos.x + ball2Change.x) <= (arena2[1] - ball2Radius)
        and (arena2[2] + ball2Radius) <= (ball2.pos.y + ball2Change.y) and (ball2.pos.y + ball2Change.y) <= (arena2[3] - ball2Radius)
        and (arena2[4] + ball2Radius) <= (ball2.pos.z + ball2Change.z) and (ball2.pos.z + ball2Change.z) <= (arena2[5] - ball2Radius)):
        bounds2 = arena2
    if ((tunnel[0] + ball2Radius) <= (ball2.pos.x + ball2Change.x) and (ball2.pos.x + ball2Change.x) <= (tunnel[1] - ball2Radius)
        and (tunnel[2] + ball2Radius) <= (ball2.pos.y + ball2Change.y) and (ball2.pos.y + ball2Change.y) <= (tunnel[3] - ball2Radius)
        and (tunnel[4] + ball2Radius) <= (ball2.pos.z + ball2Change.z) and (ball2.pos.z + ball2Change.z) <= (tunnel[5] - ball2Radius)):
        bounds2 = tunnel

    # Move ball1.
    ball1.pos += ball1Change
    # Check if ball1 has hit a boundary, and reverse the direction if it has.
    if ((bounds1[0] + ball1Radius) >= ball1.pos.x or ball1.pos.x >= (bounds1[1] - ball1Radius)):
        ball1Change.x = -ball1Change.x
    if ((bounds1[2] + ball1Radius) >= ball1.pos.y or ball1.pos.y >= (bounds1[3] - ball1Radius)):
        ball1Change.y = -ball1Change.y
    if ((bounds1[4] + ball1Radius) >= ball1.pos.z or ball1.pos.z >= (bounds1[5] - ball1Radius)):
        ball1Change.z = -ball1Change.z

    # Move ball2.
    ball2.pos += ball2Change
    # Check if ball2 has hit a boundary, and reverse the direction if it has.
    if ((bounds2[0] + ball2Radius) >= ball2.pos.x or ball2.pos.x >= (bounds2[1] - ball2Radius)):
        ball2Change.x = -ball2Change.x
    if ((bounds2[2] + ball2Radius) >= ball2.pos.y or ball2.pos.y >= (bounds2[3] - ball2Radius)):
        ball2Change.y = -ball2Change.y
    if ((bounds2[4] + ball2Radius) >= ball2.pos.z or ball2.pos.z >= (bounds2[5] - ball2Radius)):
        ball2Change.z = -ball2Change.z

# EOF
