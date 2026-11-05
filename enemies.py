"""Enemy movement and player-contact behavior."""

import pygame


class Enemy:
    """A horizontally patrolling enemy that damages the player on contact."""

    def __init__(
        self,
        x: float,
        y: float,
        *,
        patrol_left: float,
        patrol_right: float,
        speed: float = 90.0,
        size: tuple[int, int] = (32, 32),
        hit_cooldown: float = 0.75,
    ) -> None:
        if patrol_left > patrol_right:
            raise ValueError("patrol_left must be less than or equal to patrol_right")
        if speed < 0 or hit_cooldown < 0:
            raise ValueError("speed and hit_cooldown must be non-negative")

        self.rect = pygame.Rect(round(x), round(y), *size)
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.speed = speed
        self.hit_cooldown = hit_cooldown
        self.alive = True
        self._x = float(x)
        self._direction = 1
        self._hit_timer = 0.0

    def update(self, dt: float, player: object) -> bool:
        """Move along the patrol path and report a newly registered hit."""
        if dt < 0:
            raise ValueError("dt must be non-negative")
        if not self.alive:
            return False

        self._hit_timer = max(0.0, self._hit_timer - dt)
        self._x += self._direction * self.speed * dt
        if self._x < self.patrol_left:
            self._x = self.patrol_left
            self._direction = 1
        elif self._x > self.patrol_right:
            self._x = self.patrol_right
            self._direction = -1
        self.rect.x = round(self._x)

        player_rect = getattr(player, "rect", None)
        if player_rect is None or not self.rect.colliderect(player_rect):
            return False
        if self._hit_timer > 0:
            return False

        self._hit_timer = self.hit_cooldown
        return True