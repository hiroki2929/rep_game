# side_scroller

担当 4（メイン処理・敵の見た目）を先行実装した最小構成です。

## 実行

```bash
cd side_scroller
python main.py
```

## 依存

- Python
- Pygame

```bash
python -m pip install pygame
```

## 他モジュールとの接続点（前提）

`main.py` は以下のAPIが存在する前提で呼び出します。

- `player.py`
  - `class Player` / `Player.update(dt, keys, stage)` / `Player.draw(screen, camera_x)`
  - `Player` は `x, y, vx, vy` を持つ想定
- `stage.py`
  - `class Stage` / `Stage.load(stage_id)` / `Stage.update(dt, player)` / `Stage.draw(screen, camera_x)`
  - `Stage` は `spawn_x, spawn_y, world_width, enemies` を持つ想定
  - 任意で `Stage.player_hit`, `Stage.cleared`（bool）
- `hud.py`
  - `draw_hud(screen, score, time_left, lives, font=None)`
- `enemies.py`
  - 敵クラスは `x, y`（ワールド座標。yは足元基準推奨）と `w, h`（任意）を持つ想定

`enemy_art.py` の `draw_enemy()` は敵の見た目のみ担当し、当たり判定や移動ロジックは持ちません。
