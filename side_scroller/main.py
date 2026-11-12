"""main.py

横スクロールアクション（学習用・最小構成）のエントリポイント。

このリポジトリでは担当分けとして
 - player.py: Player.update / Player.draw
 - hud.py: draw_hud
 - stage.py/enemies.py: Stage / Enemy
 - main.py/enemy_art.py: メイン処理/敵の見た目
を想定している。

この main.py は「4. メイン処理」の責務に集中し、
入力 → 更新 → 描画 のゲームループ、カメラ制御、ステージ遷移の枠組みを提供する。
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from enemy_art import draw_enemy
from hud import draw_hud
from player import Player
from stage import Stage


@dataclass
class GameConfig:
    title: str = "Side Scroller"
    width: int = 960
    height: int = 540
    fps: int = 60
    bg_color: tuple[int, int, int] = (135, 206, 235)  # skyblue


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def compute_camera_x(player_x: float, screen_w: int, world_w: int) -> int:
    """プレイヤー中心で追従する1軸カメラ（横のみ）。"""
    target = player_x - screen_w / 2
    return int(clamp(target, 0, max(0, world_w - screen_w)))


def main(stage_id: int = 1) -> int:
    pygame.init()
    pygame.display.set_caption(GameConfig.title)

    cfg = GameConfig()
    screen = pygame.display.set_mode((cfg.width, cfg.height))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # --- ゲーム状態 ---
    score = 0
    time_left = 300.0
    lives = 3

    stage = Stage()
    stage.load(stage_id)
    player = Player(stage.spawn_x, stage.spawn_y)

    paused = False
    camera_x = 0
    running = True

    while running:
        dt = clock.tick(cfg.fps) / 1000.0

        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused

        keys = pygame.key.get_pressed()

        # --- 更新処理 ---
        if not paused:
            time_left = max(0.0, time_left - dt)

            player.update(dt, keys, stage)
            stage.update(dt, player)

            # 敵との当たり判定などは stage/enemies 側に寄せたいが、
            # 「残機を減らす」などのゲーム全体状態更新は main が持つのが分担上自然。
            if getattr(stage, "player_hit", False):
                lives -= 1
                stage.player_hit = False
                # リスポーン（簡易）
                player.x = stage.spawn_x
                player.y = stage.spawn_y
                player.vx = 0
                player.vy = 0

            # ゴール到達
            if getattr(stage, "cleared", False):
                score += 1000
                stage_id += 1
                stage = Stage()
                stage.load(stage_id)
                player = Player(stage.spawn_x, stage.spawn_y)

            if lives <= 0 or time_left <= 0:
                paused = True

            camera_x = compute_camera_x(player.x, cfg.width, stage.world_width)

        # --- 描画処理 ---
        screen.fill(cfg.bg_color)
        stage.draw(screen, camera_x)

        # 敵描画（敵の見た目は enemy_art に委譲）
        for enemy in getattr(stage, "enemies", []):
            draw_enemy(screen, enemy, camera_x)

        player.draw(screen, camera_x)

        draw_hud(screen, score=score, time_left=time_left, lives=lives, font=font)

        if paused and (lives <= 0 or time_left <= 0):
            msg = "GAME OVER" if lives <= 0 else "TIME UP"
            surf = font.render(msg + "  (ESCで終了)", True, (0, 0, 0))
            rect = surf.get_rect(center=(cfg.width // 2, cfg.height // 2))
            screen.blit(surf, rect)

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
