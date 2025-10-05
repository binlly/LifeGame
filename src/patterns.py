class Patterns:
  """预设图案类"""

  @staticmethod
  def create_glider(grid, center_x, center_y, width, height):
    """滑翔机 - 康威生命游戏经典图案"""
    pattern = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_pulsar(grid, center_x, center_y, width, height):
    """脉冲星 - 周期3振荡器"""
    pattern = [
      # 左上角
      (2, 0), (3, 0), (4, 0),
      (0, 2), (0, 3), (0, 4),
      (5, 2), (5, 3), (5, 4),
      (2, 5), (3, 5), (4, 5),
      # 右上角
      (8, 0), (9, 0), (10, 0),
      (7, 2), (7, 3), (7, 4),
      (12, 2), (12, 3), (12, 4),
      (8, 5), (9, 5), (10, 5),
      # 左下角
      (2, 7), (3, 7), (4, 7),
      (0, 8), (0, 9), (0, 10),
      (5, 8), (5, 9), (5, 10),
      (2, 12), (3, 12), (4, 12),
      # 右下角
      (8, 7), (9, 7), (10, 7),
      (7, 8), (7, 9), (7, 10),
      (12, 8), (12, 9), (12, 10),
      (8, 12), (9, 12), (10, 12)
    ]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_gosper_glider_gun(grid, center_x, center_y, width, height):
    """高斯帕滑翔机枪"""
    pattern = [
      (24, 0),
      (22, 1), (24, 1),
      (12, 2), (13, 2), (20, 2), (21, 2), (34, 2), (35, 2),
      (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), (35, 3),
      (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4),
      (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5), (24, 5),
      (10, 6), (16, 6), (24, 6),
      (11, 7), (15, 7),
      (12, 8), (13, 8)
    ]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_blinker(grid, center_x, center_y, width, height):
    """眨眼 - 周期2振荡器"""
    pattern = [(1, 0), (1, 1), (1, 2)]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_toad(grid, center_x, center_y, width, height):
    """吐司 - 周期2振荡器"""
    pattern = [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_beacon(grid, center_x, center_y, width, height):
    """信标 - 周期2振荡器"""
    pattern = [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_r_pentomino(grid, center_x, center_y, width, height):
    """R-五连方"""
    pattern = [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_acorn(grid, center_x, center_y, width, height):
    """橡果"""
    pattern = [(1, 0), (3, 1), (0, 2), (1, 2), (4, 2), (5, 2), (6, 2)]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_diehard(grid, center_x, center_y, width, height):
    """Diehard"""
    pattern = [
      (6, 0),
      (0, 1), (1, 1),
      (1, 2), (5, 2), (6, 2), (7, 2)
    ]
    for dx, dy in pattern:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_glider_collision(grid, center_x, center_y, width, height):
    """滑翔机对撞"""
    glider1 = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    glider2 = [(10, 1), (9, 2), (8, 0), (8, 1), (8, 2)]
    for dx, dy in glider1 + glider2:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1

  @staticmethod
  def create_glider_fleet(grid, center_x, center_y, width, height):
    """滑翔机舰队"""
    glider1 = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    glider2 = [(10, 1), (9, 2), (8, 0), (8, 1), (8, 2)]
    glider3 = [(5, 8), (4, 9), (4, 10), (5, 10), (6, 10)]
    for dx, dy in glider1 + glider2 + glider3:
      x, y = center_x + dx, center_y + dy
      if 0 <= x < width and 0 <= y < height:
        grid[y, x] = 1


# 预设图案映射
PRESET_PATTERNS = {
  "随机": None,
  "滑翔机": Patterns.create_glider,
  "滑翔机对撞": Patterns.create_glider_collision,
  "滑翔机舰队": Patterns.create_glider_fleet,
  "高斯帕滑翔机枪": Patterns.create_gosper_glider_gun,
  "眨眼": Patterns.create_blinker,
  "吐司": Patterns.create_toad,
  "信标": Patterns.create_beacon,
  "脉冲星": Patterns.create_pulsar,
  "R-五连方": Patterns.create_r_pentomino,
  "橡果": Patterns.create_acorn,
  "Diehard": Patterns.create_diehard,
}
