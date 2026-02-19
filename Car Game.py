# Car game
# Press Q or Esc to Quit

# import LIB
import pygame
import random


pygame.init()

# Initialize audio once; if unavailable, run silently.
AUDIO_ENABLED = True
try:
    pygame.mixer.init()
except pygame.error:
    AUDIO_ENABLED = False

icon = pygame.image.load('Car_gif.gif')
pygame.display.set_icon(icon)


# VAR num (int, float, ...)
width = 500
height = 500
speed = 2
score = 0
high_score = 0
fps = 120
marker_width = 10
marker_height = 50
left_lane = 150
center_lane = 250
right_lane = 350
lane_marker_move_y = 0
player_x = 250
player_y = 400

# Create screen
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')


# ========== UI MODULE SECTION: Palette, Fonts, Helper Functions ==========

# Consistent color palette
GRASS_COLOR = (41, 133, 74)
ROAD_COLOR = (58, 63, 74)
ROAD_EDGE_COLOR = (245, 205, 68)
LANE_MARKER_COLOR = (235, 238, 245)

UI_PANEL_BG = (16, 22, 30, 185)
UI_PANEL_BORDER = (108, 128, 152, 220)
UI_OVERLAY_BG = (8, 12, 18, 170)

TEXT_PRIMARY = (244, 247, 252)
TEXT_SECONDARY = (189, 201, 218)
TEXT_ACCENT = (106, 187, 255)

# Keep original color names used by gameplay drawing.
gray = ROAD_COLOR
green = GRASS_COLOR
white = TEXT_PRIMARY
yellow = ROAD_EDGE_COLOR
black = (0, 0, 0)


def load_font(size, bold=False):
    """Load a readable UI font with safe fallback to pygame default."""
    font_candidates = ["segoeui", "verdana", "dejavusans", "arial"]
    for name in font_candidates:
        font_path = pygame.font.match_font(name, bold=bold)
        if font_path:
            return pygame.font.Font(font_path, size)
    return pygame.font.Font(pygame.font.get_default_font(), size)


HUD_FONT = load_font(18)
BIG_FONT = load_font(44, bold=True)
SMALL_FONT = load_font(16)
TITLE_FONT = load_font(22, bold=True)


def draw_text(surface, text, font, color, x, y, align="topleft"):
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect()

    if hasattr(text_rect, align):
        setattr(text_rect, align, (x, y))
    else:
        text_rect.topleft = (x, y)

    surface.blit(text_surf, text_rect)
    return text_rect


def draw_panel(surface, rect, bg_color, border_color, border_radius=12):
    panel_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel_rect = panel_surface.get_rect()

    pygame.draw.rect(
        panel_surface,
        bg_color,
        panel_rect,
        border_radius=border_radius,
    )
    pygame.draw.rect(
        panel_surface,
        border_color,
        panel_rect,
        width=2,
        border_radius=border_radius,
    )

    surface.blit(panel_surface, rect.topleft)


def draw_hud(surface, score_value, high_score_value, speed_value, fps_value):
    hud_rect = pygame.Rect(12, 12, 210, 126)
    draw_panel(surface, hud_rect, UI_PANEL_BG, UI_PANEL_BORDER, border_radius=14)

    padding_x = 14
    line_y = hud_rect.top + 12

    draw_text(surface, "HUD", TITLE_FONT, TEXT_ACCENT, hud_rect.left + padding_x, line_y)

    line_y += 30
    draw_text(
        surface,
        f"Score: {score_value}",
        HUD_FONT,
        TEXT_PRIMARY,
        hud_rect.left + padding_x,
        line_y,
    )

    line_y += 24
    draw_text(
        surface,
        f"High Score: {high_score_value}",
        HUD_FONT,
        TEXT_PRIMARY,
        hud_rect.left + padding_x,
        line_y,
    )

    line_y += 24
    draw_text(
        surface,
        f"Level: {max(1, speed_value - 1)}",
        SMALL_FONT,
        TEXT_SECONDARY,
        hud_rect.left + padding_x,
        line_y,
    )

    draw_text(
        surface,
        f"FPS: {int(fps_value)}",
        SMALL_FONT,
        TEXT_SECONDARY,
        hud_rect.right - 14,
        hud_rect.bottom - 10,
        align="bottomright",
    )


def draw_center_message(surface, title, subtitle_lines):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill(UI_OVERLAY_BG)
    surface.blit(overlay, (0, 0))

    panel_rect = pygame.Rect(0, 0, 420, 240)
    panel_rect.center = (width // 2, height // 2)
    draw_panel(surface, panel_rect, (12, 18, 26, 225), UI_PANEL_BORDER, border_radius=18)

    draw_text(
        surface,
        title,
        BIG_FONT,
        TEXT_PRIMARY,
        panel_rect.centerx,
        panel_rect.top + 24,
        align="midtop",
    )

    line_y = panel_rect.top + 112
    for line in subtitle_lines:
        draw_text(
            surface,
            line,
            HUD_FONT,
            TEXT_SECONDARY,
            panel_rect.centerx,
            line_y,
            align="midtop",
        )
        line_y += 30


# VAR bool (True, False)
game_over = False
running = True
game_started = False
paused = False
crash_sound_played = False

# list
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)
lanes = [left_lane, center_lane, right_lane]

# game loop
clock = pygame.time.Clock()

# Audio cache
_sound_cache = {}


# def
def Play_Music(music_name, vol):
    if not AUDIO_ENABLED:
        return

    sound = _sound_cache.get(music_name)
    if sound is None:
        try:
            sound = pygame.mixer.Sound(music_name)
            _sound_cache[music_name] = sound
        except pygame.error:
            return

    sound.set_volume(vol)
    sound.play()


# class
class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Scale the image down so it fits in the lane.
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('Images/car.png').convert_alpha()
        super().__init__(image, x, y)


# create the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load the other vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('Images/' + image_filename).convert_alpha()
    vehicle_images.append(image)

# sprite group for vehicles
vehicle_group = pygame.sprite.Group()

crash = pygame.image.load('Images/crash.png').convert_alpha()
crash_rect = crash.get_rect()


def trigger_game_over(crash_center=None):
    global game_over, crash_sound_played

    game_over = True
    if crash_center is not None:
        crash_rect.center = crash_center

    if not crash_sound_played:
        Play_Music('Crash.mp3', 0.2)
        crash_sound_played = True


while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False

            if not game_started:
                if event.key == pygame.K_SPACE:
                    game_started = True
                continue

            if game_over:
                if event.key == pygame.K_SPACE:
                    speed = 2
                    score = 0
                    lane_marker_move_y = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                    game_over = False
                    paused = False
                    crash_sound_played = False
                continue

            if event.key == pygame.K_p:
                paused = not paused
                continue

            if paused:
                continue

            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.rect.center[0] > left_lane:
                player.rect.x -= 100

            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.rect.center[0] < right_lane:
                player.rect.x += 100

            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.rect.left = vehicle.rect.right
                        trigger_game_over(
                            (player.rect.left, int((player.rect.center[1] + vehicle.rect.center[1]) / 2))
                        )
                        break

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.rect.right = vehicle.rect.left
                        trigger_game_over(
                            (player.rect.right, int((player.rect.center[1] + vehicle.rect.center[1]) / 2))
                        )
                        break

    # Draw the grass
    screen.fill(green)

    # Draw the road
    pygame.draw.rect(screen, gray, road)

    # Draw edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # Draw lane markers
    if game_started and not game_over and not paused:
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0

    for y in range(marker_height * (-2), height, marker_height * 2):
        pygame.draw.rect(
            screen,
            LANE_MARKER_COLOR,
            (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
        )
        pygame.draw.rect(
            screen,
            LANE_MARKER_COLOR,
            (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height),
        )

    # Draw the player's car
    player_group.draw(screen)

    # Add up to two vehicles
    if game_started and not game_over and not paused and len(vehicle_group) < 2:

        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / (-2))
            vehicle_group.add(vehicle)

    # Move vehicles and update score/speed
    if game_started and not game_over and not paused:
        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1
                Play_Music('point.mp3', 1)

                if score > 0 and score % 5 == 0:
                    speed += 1

            if score > high_score:
                high_score = score

    vehicle_group.draw(screen)

    # Collision check during normal gameplay
    if game_started and not game_over and not paused:
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            trigger_game_over((player.rect.center[0], player.rect.top))

    # Draw crash sprite where collision happened
    if game_over:
        screen.blit(crash, crash_rect)

    # HUD panel
    draw_hud(screen, score, high_score, speed, clock.get_fps())

    # Bottom hint row
    hint_y = height - 24
    draw_text(
        screen,
        'A/← left   D/→ right   Q/Esc quit',
        SMALL_FONT,
        TEXT_PRIMARY,
        width // 2,
        hint_y,
        align='midbottom',
    )

    if game_over:
        draw_text(
            screen,
            'SPACE to restart',
            SMALL_FONT,
            TEXT_ACCENT,
            width // 2,
            hint_y - 24,
            align='midbottom',
        )

    if paused and not game_over and game_started:
        draw_center_message(
            screen,
            'PAUSED',
            [
                'Press P to continue',
                'Press Q or ESC to quit',
            ],
        )

    if not game_started:
        draw_center_message(
            screen,
            'CAR GAME',
            [
                'Press SPACE to start',
                'A/← left   D/→ right',
                'Q or ESC to quit',
            ],
        )

    if game_over:
        draw_center_message(
            screen,
            'GAME OVER',
            [
                f'Score: {score}',
                f'High Score: {high_score}',
                'Press SPACE to play again',
                'Press Q or ESC to quit',
            ],
        )

    pygame.display.flip()

pygame.quit()
