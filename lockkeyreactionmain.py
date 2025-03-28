import pygame
import subprocess
import random
import time
import statistics

# Add status lights to pygame window, so windows can play too

# Global variable to store the LED mask output string.
led_mask_output = "N/A"

# Global variable for application start time; overall game time will be measured from this value.
app_start_time = time.time()

# Initialize Pygame
pygame.init()
pygame.key.set_repeat(0)  # Disable key repeat

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LED Reaction Game with Stats")

# Define colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None, 24)

###########################
# LED Reaction Game Functions
###########################
def simulate_keypress(key):
    subprocess.run(["xdotool", "key", key])

def initialize_leds():
    keys = ["Num_Lock", "Caps_Lock", "Scroll_Lock"]
    for key in keys:
        for _ in range(2):
            subprocess.run(["xdotool", "key", key])

def update_led_mask():
    """Query xset for the LED mask and update the global variable led_mask_output.
       This function only observes the mask.
    """
    global led_mask_output
    try:
        output = subprocess.check_output("xset q", shell=True).decode("utf-8")
    except Exception:
        output = ""
    for line in output.splitlines():
        if "LED mask:" in line:
            parts = line.split("LED mask:")
            if len(parts) > 1:
                mask_str = parts[1].strip()
                led_mask_output = mask_str
            break

def turn_off_leds_if_on():
    """Query xset for the LED mask and turn off any lock key that is on.
       Mapping: 0x01 – Caps Lock, 0x02 – Num Lock, 0x04 – Scroll Lock.
    """
    try:
        output = subprocess.check_output("xset q", shell=True).decode("utf-8")
    except Exception:
        output = ""
    mask = 0
    for line in output.splitlines():
        if "LED mask:" in line:
            parts = line.split("LED mask:")
            if len(parts) > 1:
                mask_str = parts[1].strip()
                try:
                    mask = int(mask_str, 16)
                except Exception:
                    mask = 0
            break
    if mask & 0x01:
        simulate_keypress("Caps_Lock")
    if mask & 0x02:
        simulate_keypress("Num_Lock")
    if mask & 0x04:
        simulate_keypress("Scroll_Lock")

def decrease_led_time(current):
    """Decrease the LED reaction time.
       - If >100ms, decrease by 5ms.
       - If >50ms, decrease by 2ms.
       - Otherwise (including under 50ms), decrease by 1ms.
       Minimum allowed value is 1ms.
    """
    if current > 100:
        return max(1, current - 5)
    elif current > 50:
        return max(1, current - 2)
    elif current > 1:
        return max(1, current - 1)
    else:
        return 1

# Reaction time helper functions
def get_led_fastest():
    return f"{min(led_reaction_times):.2f}" if led_reaction_times else "N/A"

def get_led_slowest():
    return f"{max(led_reaction_times):.2f}" if led_reaction_times else "N/A"

def get_led_average():
    return f"{(sum(led_reaction_times) / len(led_reaction_times)):.2f}" if led_reaction_times else "N/A"

def get_led_median():
    return f"{statistics.median(led_reaction_times):.2f}" if led_reaction_times else "N/A"

def get_led_stdev():
    return f"{statistics.stdev(led_reaction_times):.2f}" if len(led_reaction_times) > 1 else "N/A"

def get_led_percentile(p):
    if not led_reaction_times:
        return "N/A"
    sorted_rts = sorted(led_reaction_times)
    k = (len(sorted_rts) - 1) * (p / 100)
    f = int(k)
    c = min(f + 1, len(sorted_rts) - 1)
    if f == c:
        return f"{sorted_rts[int(k)]:.2f}"
    d0 = sorted_rts[f] * (c - k)
    d1 = sorted_rts[c] * (k - f)
    return f"{d0 + d1:.2f}"

def get_led_percentile_25():
    return get_led_percentile(25)

def get_led_percentile_75():
    return get_led_percentile(75)

def get_led_accuracy():
    if led_total_presses:
        return f"{(led_correct_presses / led_total_presses * 100):.2f}%"
    return "N/A"

def get_led_prompt_ratio():
    if led_total_prompts:
        return f"{led_correct_presses}/{led_total_prompts} ({(led_correct_presses / led_total_prompts * 100):.2f}%)"
    return "N/A"

# Define a custom event for a new LED prompt.
NEW_LED_EVENT = pygame.USEREVENT + 1

# LED game state variables.
led_mapping = {
    "Num_Lock": pygame.K_LEFT,
    "Caps_Lock": pygame.K_DOWN,
    "Scroll_Lock": pygame.K_RIGHT
}
current_led = None
led_timer_set = False
led_reaction_times = []
led_correct_presses = 0
led_wrong_presses = 0
led_total_presses = 0
led_time = 1000  # Reaction time window (ms).
led_start_time = None

# Timing variables.
led_game_start_time = time.time()      # When the game started.
# Note: overall game time will be calculated from app_start_time and is not reset.
total_pause_duration = 0.0               # Total paused time.
active_game_time = 0.0                   # Time while unpaused.

# Gameplay tracking variables.
led_missed_prompts = 0
current_streak = 0
longest_streak = 0
led_total_prompts = 0

# The game starts paused.
paused = True
pause_start = time.time()

# A set to track keys held down.
keys_down = set()

def set_new_led_timer():
    global led_timer_set
    pygame.time.set_timer(NEW_LED_EVENT, led_time, True)
    led_timer_set = True

def reset_game():
    """Reset game state to starting conditions (except overall game time)."""
    global current_led, led_timer_set, led_reaction_times, led_correct_presses, led_wrong_presses
    global led_total_presses, led_time, led_start_time, total_pause_duration, active_game_time
    global led_missed_prompts, current_streak, longest_streak, led_total_prompts
    global paused, pause_start, keys_down

    current_led = None
    led_timer_set = False
    led_reaction_times.clear()
    led_correct_presses = 0
    led_wrong_presses = 0
    led_total_presses = 0
    led_time = 1000
    led_start_time = None
    # Do NOT reset led_game_start_time (app start time remains unchanged).
    total_pause_duration = 0.0
    active_game_time = 0.0
    led_missed_prompts = 0
    current_streak = 0
    longest_streak = 0
    led_total_prompts = 0
    paused = True
    pause_start = time.time()
    keys_down.clear()
    initialize_leds()
    update_led_mask()

# At startup, ensure all LED lock keys are off.
turn_off_leds_if_on()
update_led_mask()

# Initialize timer for LED mask observation.
last_led_mask_update = time.time()

###########################
# Main Game Loop
###########################
clock = pygame.time.Clock()
running = True
fps = 60

while running:
    dt = clock.tick(fps) / 1000.0  # Seconds since last frame

    if not paused:
        active_game_time += dt


    # Update LED mask on every loop iteration.
    update_led_mask()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type == pygame.KEYUP:
            if event.key in keys_down:
                keys_down.remove(event.key)
            continue

        if event.type == pygame.KEYDOWN:
            if event.key in keys_down:
                continue
            keys_down.add(event.key)

            if event.key == pygame.K_r:
                reset_game()
                continue

            if event.key == pygame.K_SPACE:
                if paused:
                    # Exiting pause: turn off any lingering LEDs.
                    turn_off_leds_if_on()
                    total_pause_duration += time.time() - pause_start
                    paused = False
                    current_led = None
                    led_timer_set = False
                    set_new_led_timer()
                else:
                    if current_led is not None:
                        simulate_keypress(current_led)
                    turn_off_leds_if_on()
                    current_led = None
                    led_timer_set = False
                    paused = True
                    pause_start = time.time()
                continue

            if event.key not in led_mapping.values():
                continue

            if current_led is None:
                continue

            led_total_presses += 1

            if event.key == led_mapping.get(current_led):
                reaction = (time.time() - led_start_time) * 1000  # in ms.
                if reaction <= led_time:
                    simulate_keypress(current_led)
                    led_reaction_times.append(reaction)
                    current_led = None
                    led_timer_set = False
                    led_correct_presses += 1
                    current_streak += 1
                    if current_streak > longest_streak:
                        longest_streak = current_streak
                    led_time = decrease_led_time(led_time)
                else:
                    simulate_keypress(current_led)
                    led_missed_prompts += 1
                    current_streak = 0
                    current_led = None
                    led_timer_set = False
                    led_time = decrease_led_time(led_time)
            else:
                simulate_keypress(current_led)
                led_wrong_presses += 1
                led_missed_prompts += 1
                current_streak = 0
                current_led = None
                led_timer_set = False
                led_time = decrease_led_time(led_time)

        elif event.type == NEW_LED_EVENT:
            turn_off_leds_if_on()  # Clear any remaining lights.
            if current_led is not None:
                led_missed_prompts += 1
                current_streak = 0
                current_led = None
                led_timer_set = False
                led_time = decrease_led_time(led_time)
            current_led = random.choice(list(led_mapping.keys()))
            simulate_keypress(current_led)
            led_start_time = time.time()
            led_timer_set = True
            led_total_prompts += 1

    if not paused:
        if current_led is not None and (time.time() - led_start_time) * 1000 >= led_time:
            simulate_keypress(current_led)
            led_missed_prompts += 1
            current_streak = 0
            current_led = None
            led_timer_set = False
            led_time = decrease_led_time(led_time)
        if current_led is None and not led_timer_set:
            set_new_led_timer()

    overall_time = int(time.time() - app_start_time)  # Overall time always running from app start.
    active_time_display = int(active_game_time)

    # Clear the screen.
    screen.fill(WHITE)

    # Draw LED circles in the lower portion of the screen.
    # These circles represent the three LEDs: left = "Num_Lock", middle = "Caps_Lock", right = "Scroll_Lock".
    led_area_y = int(0.75 * HEIGHT)  # center Y position (e.g., 450 when HEIGHT = 600)
    led_positions = {
        "Num_Lock": (WIDTH // 6, led_area_y),
        "Caps_Lock": (WIDTH // 2, led_area_y),
        "Scroll_Lock": (5 * WIDTH // 6, led_area_y)
    }
    led_radius = 100
    for led, pos in led_positions.items():
        # Fill red if this LED is currently active; otherwise fill white.
        fill_color = RED if current_led == led else WHITE
        pygame.draw.circle(screen, fill_color, pos, led_radius)
        pygame.draw.circle(screen, BLACK, pos, led_radius, 5)

    # Prepare stats text lines.
    line1 = f"Total Key Presses: {led_total_presses} (Wrong: {led_wrong_presses})"
    line2 = f"Successful Presses: {led_correct_presses} | Accuracy: {get_led_accuracy()} | Prompts: {led_total_prompts} (Prompt Ratio: {get_led_prompt_ratio()})"
    line3 = f"Fastest: {get_led_fastest()} ms | Slowest: {get_led_slowest()} ms | Average: {get_led_average()} ms"
    line4 = f"Median: {get_led_median()} ms | Stdev: {get_led_stdev()} ms"
    line5 = f"25th Percentile: {get_led_percentile_25()} ms | 75th Percentile: {get_led_percentile_75()} ms"
    line6 = f"Current Streak: {current_streak} | Longest Streak: {longest_streak}"
    line7 = f"Missed Prompts: {led_missed_prompts}"
    line8 = f"Reaction Time Window: {led_time} ms"
    line9 = f"Active Game Time (unpaused): {active_time_display} s"
    line10 = f"Overall Game Time: {overall_time} s"
    line11 = f"LED Mask: {led_mask_output}"

    # Draw stats text at the top of the screen.
    y = 10
    for line in [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11]:
        surface = font.render(line, True, BLACK)
        screen.blit(surface, (10, y))
        y += 20

    # If paused, display pause message; if active, display current LED prompt.
    if paused:
        pause_text = "Paina avaruusnäppäintä"
        pause_surface = font.render(pause_text, True, BLACK)
        screen.blit(pause_surface, (10, y))
    else:
        if current_led:
            current_led_text = f"Press {current_led} ({pygame.key.name(led_mapping[current_led]).upper()})"
            current_led_surface = font.render(current_led_text, True, BLACK)
            screen.blit(current_led_surface, (10, y))

    pygame.display.flip()

pygame.quit()
