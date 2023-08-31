import pygame
import numpy as np
import imageio

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 60
CELL_SIZE = 15
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Create the screen
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Game of Life")


# Initialize the grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
running = True
drawing = False
simulation_running = False
show_instructions = False

# Create an empty list to store simulation frames
frames = []


def update_grid():
    new_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            neighbors = (
                np.sum(
                    grid[
                        max(0, i - 1) : min(GRID_SIZE, i + 2),
                        max(0, j - 1) : min(GRID_SIZE, j + 2),
                    ]
                )
                - grid[i, j]
            )
            if grid[i, j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0
                else:
                    new_grid[i, j] = 1
            else:
                if neighbors == 3:
                    new_grid[i, j] = 1
    return new_grid


while running:
    # Mouse and Key Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cell_x = mouse_x // CELL_SIZE
            cell_y = mouse_y // CELL_SIZE
            # Check if the click is on the button area
            if (
                0 <= mouse_x < WINDOW_SIZE[0] - 150
                and GRID_SIZE * CELL_SIZE <= mouse_y <= GRID_SIZE * CELL_SIZE + 50
            ):
                # Left-click or right-click on button
                if event.button == 1 or event.button == 3:
                    simulation_running = not simulation_running
            elif 0 <= cell_x < GRID_SIZE and 0 <= cell_y < GRID_SIZE:
                # Left-click to draw
                if event.button == 1:
                    grid[cell_y, cell_x] = 1
                # Right-click to erase
                elif event.button == 3:
                    grid[cell_y, cell_x] = 0
            elif (
                WINDOW_SIZE[0] - 150 <= mouse_x <= WINDOW_SIZE[0]
                and GRID_SIZE * CELL_SIZE <= mouse_y <= GRID_SIZE * CELL_SIZE + 50
            ):
                if event.button == 1 or event.button == 3:
                    # Left-click or right-click on Instructions button
                    show_instructions = not show_instructions
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            grid = update_grid()
    if drawing:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cell_x = mouse_x // CELL_SIZE
        cell_y = mouse_y // CELL_SIZE
        if 0 <= cell_x < GRID_SIZE and 0 <= cell_y < GRID_SIZE:
            grid[cell_y, cell_x] = 1

    if simulation_running:
        grid = update_grid()

    # Update the screen
    screen.fill(WHITE)
    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(
            screen, GRAY, (0, i * CELL_SIZE), (WINDOW_SIZE[0], i * CELL_SIZE)
        )
        pygame.draw.line(
            screen, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        )

    # Draw cells
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i, j] == 1:
                pygame.draw.rect(
                    screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    # Draw Start button
    start_button_color = GRAY if simulation_running else BLACK
    pygame.draw.rect(
        screen, start_button_color, (0, GRID_SIZE * CELL_SIZE, WINDOW_SIZE[0], 50)
    )
    start_text = "Pause" if simulation_running else "Start"
    font = pygame.font.Font(None, 36)
    text_surface = font.render(start_text, True, WHITE)
    text_rect = text_surface.get_rect(
        center=(WINDOW_SIZE[0] // 2, GRID_SIZE * CELL_SIZE + 25)
    )
    screen.blit(text_surface, text_rect)

    # Draw Instructions button
    instructions_button_color = GRAY if show_instructions else BLACK
    pygame.draw.rect(
        screen,
        instructions_button_color,
        (WINDOW_SIZE[0] - 150, GRID_SIZE * CELL_SIZE, 150, 50),
    )
    instructions_text = "Instructions"
    text_surface = font.render(instructions_text, True, WHITE)
    text_rect = text_surface.get_rect(
        center=(WINDOW_SIZE[0] - 75, GRID_SIZE * CELL_SIZE + 25)
    )
    screen.blit(text_surface, text_rect)

    # Draw Instructions overlay if show_instructions is True
    if show_instructions:
        overlay = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black overlay
        screen.blit(overlay, (0, 0))

        instructions_font = pygame.font.Font(None, 50)
        instructions_text = [
            "Left-click: Draw cells",
            "Right-click: Erase cells",
            "Click on Start to toggle simulation",
            "",
            "Simulation Rules:",
            "1. Any live cell with fewer than two",
            "live neighbors dies (underpopulation).",
            "2. Any live cell with two or three",
            "live neighbors lives on to the next generation.",
            "3. Any live cell with more than three",
            "live neighbors dies (overpopulation).",
            "4. Any dead cell with exactly three",
            "live neighbors becomes a live cell (reproduction).",
        ]
        instructions_y = 100
        for i, line in enumerate(instructions_text):
            text_surface = instructions_font.render(line, True, (128, 0, 128))
            text_rect = text_surface.get_rect(
                center=(WINDOW_SIZE[0] // 2, instructions_y + i * 35)
            )
            screen.blit(text_surface, text_rect)

    # Capture the current frame and append it to the frames list
    current_frame = pygame.surfarray.array3d(screen)
    frames.append(current_frame)

    pygame.display.flip()

    pygame.time.wait(100)  # Adjust the delay value to control speed

# Save the collected frames as a GIF
# Use duration rather fps and flipped the frames due to Pygame's coordinate system
# Comment out the line below if you want to save your generation!
imageio.mimsave("game_of_life.gif", frames, duration=4)

# Quit Pygame
pygame.quit()
