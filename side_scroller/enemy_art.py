"""enemy_art.py

敵キャラクターの「見た目」専用モジュール。

目的:
 - enemies.py / stage.py 側のロジックと分離し、描画差し替えを容易にする。
 - 画像素材が無い状態でも動くよう、まずは図形描画で成立させる。

前提:
 - enemy は少なくとも x, y を持つ（ワールド座標）。
 - 任意で w/h または radius、kind、direction 等を持てる。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pygame


@dataclass
class EnemyPalette:
    body: pygame.Color = pygame.Color(220, 60, 60)
    outline: pygame.Color = pygame.Color(40, 20, 20)
    eye_white: pygame.Color = pygame.Color(245, 245, 245)
    eye_black: pygame.Color = pygame.Color(10, 10, 10)


def _enemy_rect(enemy: Any) -> pygame.Rect:
    w = int(getattr(enemy, "w", 32))
    h = int(getattr(enemy, "h", 32))
    x = int(getattr(enemy, "x", 0))
    y = int(getattr(enemy, "y", 0))
    # y を「足元基準」で持っている実装に合わせ、rect は足元から上に伸ばす
    return pygame.Rect(x, y - h, w, h)


def draw_enemy(screen: pygame.Surface, enemy: Any, camera_x: int, palette: EnemyPalette | None = None) -> None:
    """敵を描画する。

    引数:
        screen: 描画対象
        enemy: 敵オブジェクト（enemies.py の Enemy インスタンス想定）
        camera_x: カメラのx（ワールド→スクリーン変換に使用）
        palette: 色設定（任意）
    """

    palette = palette or EnemyPalette()
    r = _enemy_rect(enemy)
    r_screen = r.move(-camera_x, 0)

    kind = getattr(enemy, "kind", "slime")
    direction = getattr(enemy, "direction", 1)  # 右=1, 左=-1 など想定

    if kind == "slime":
        # 丸っこいスライム
        body = r_screen.inflate(-4, -8)
        pygame.draw.ellipse(screen, palette.body, body)
        pygame.draw.ellipse(screen, palette.outline, body, 2)

        # 目（向きで位置をずらす）
        eye_y = body.centery - body.height * 0.1
        if direction >= 0:
            eye1_x = body.centerx - body.width * 0.1
            eye2_x = body.centerx + body.width * 0.18
        else:
            eye1_x = body.centerx - body.width * 0.18
            eye2_x = body.centerx + body.width * 0.1

        for ex in (eye1_x, eye2_x):
            pygame.draw.circle(screen, palette.eye_white, (int(ex), int(eye_y)), max(2, body.width // 10))
            pygame.draw.circle(screen, palette.eye_black, (int(ex), int(eye_y)), max(1, body.width // 20))

    else:
        # デフォルト: 四角い敵
        pygame.draw.rect(screen, palette.body, r_screen)
        pygame.draw.rect(screen, palette.outline, r_screen, 2)
