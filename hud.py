import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def _get_font(size=28):
    return pygame.font.SysFont("arial", size, bold=True)


def _format_time(time_left):
    return f"{max(0, int(time_left)):03}"


def _draw_text_with_shadow(screen, text, font, color, x, y):
    shadow_surface = font.render(text, True, BLACK)
    text_surface = font.render(text, True, color)

    screen.blit(shadow_surface, (x + 2, y + 2))
    screen.blit(text_surface, (x, y))


def draw_hud(screen, score, time_left, lives):
    """
    Draw score, remaining time, and lives at the top of the screen.

    Parameters
    ----------
    screen : pygame.Surface
        Destination surface.
    score : int
        Current score.
    time_left : float | int
        Remaining time in seconds.
    lives : int
        Current remaining lives.
    """
    width = screen.get_width()

    font_label = _get_font(22)
    font_value = _get_font(28)

    score = max(0, int(score))
    lives = max(0, int(lives))

    score_label = "SCORE"
    score_value = f"{score:06}"

    time_label = "TIME"
    time_value = _format_time(time_left)

    lives_label = "LIVES"
    lives_value = f"x {lives}"

    _draw_text_with_shadow(screen, score_label, font_label, WHITE, 30, 8)
    _draw_text_with_shadow(screen, score_value, font_value, WHITE, 30, 28)

    center_x = width // 2 - 35
    _draw_text_with_shadow(screen, time_label, font_label, WHITE, center_x, 8)
    _draw_text_with_shadow(screen, time_value, font_value, WHITE, center_x, 28)

    right_x = width - 140
    _draw_text_with_shadow(screen, lives_label, font_label, WHITE, right_x, 8)
    _draw_text_with_shadow(screen, lives_value, font_value, WHITE, right_x, 28)
