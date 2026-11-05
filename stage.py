"""Stage geometry, enemy updates, and stage drawing."""

from dataclasses import dataclass

import pygame

from enemies import Enemy


@dataclass(frozen=True)
class StageEvent:
    """An event the game loop can use to update score, lives, or state."""

    kind: str
    enemy: Enemy


class Stage:
    TILE_SIZE = 48
    HEIGHT = 576

    _LEVELS = {
        1: {
            "width": 1920,
            "platforms": (
                (0, 528, 1920, 48),
                (288, 432, 192, 24),
                (624, 360, 192, 24),
                (1008, 432, 240, 24),
                (1440, 360, 192, 24),
            ),
            "enemies": (
                (400, 496, 336, 528),
                (1104, 400, 1008, 1248),
                (1536, 328, 1440, 1632),
            ),
        },
    }

    def __init__(
        self,
        stage_id: int,
        width: int,
        platforms: list[pygame.Rect],
        enemies: list[Enemy],
    ) -> None:
        self.stage_id = stage_id
        self.width = width
        self.platforms = platforms
        self.enemies = enemies
        self.exit_rect = pygame.Rect(width - self.TILE_SIZE, 0, self.TILE_SIZE, self.HEIGHT)

    @classmethod
    def load(cls, stage_id: int) -> "Stage":
        """Create a stage from its built-in level definition."""
        try:
            definition = cls._LEVELS[stage_id]
        except KeyError as error:
            raise ValueError(f"Unknown stage_id: {stage_id}") from error

        platforms = [pygame.Rect(*values) for values in definition["platforms"]]
        enemies = [
            Enemy(
                x,
                y,
                patrol_left=patrol_left,
                patrol_right=patrol_right,
            )
            for x, y, patrol_left, patrol_right in definition["enemies"]
        ]
        return cls(stage_id, definition["width"], platforms, enemies)

    def update(self, dt: float, player: object) -> list[StageEvent]:
        """Update enemies and return player-hit events for the main loop."""
        events = []
        for enemy in self.enemies:
            if enemy.update(dt, player):
                events.append(StageEvent("player_hit", enemy))
        return events

    def draw(self, screen: pygame.Surface, camera_x: float) -> None:
        """Draw stage terrain in screen coordinates; enemy art is drawn separately."""
        screen.fill((134, 203, 235))
        viewport = screen.get_rect()
        for platform in self.platforms:
            screen_rect = platform.move(-round(camera_x), 0)
            if viewport.colliderect(screen_rect):
                pygame.draw.rect(screen, (73, 132, 82), screen_rect)