from typing import Dict

import numpy as np


class CellularAutomaton:
  """元胞自动机核心类"""

  def __init__(self, width=50, height=50):
    self.width = width
    self.height = height
    self.grid = np.zeros((height, width), dtype=int)
    self.next_grid = np.zeros((height, width), dtype=int)
    self.rules = {}
    self.default_rule = {
      'survive': [2, 3],
      'birth': [3],
      'states': 2,
      'neighborhood': 'moore'
    }
    self.set_rule(self.default_rule)

  def set_rule(self, rule: Dict):
    """设置规则"""
    self.rules = rule.copy()
    if 'neighborhood' not in self.rules:
      self.rules['neighborhood'] = 'moore'
    if 'states' not in self.rules:
      self.rules['states'] = 2

  def count_neighbors(self, x: int, y: int) -> int:
    """计算邻居数量 - 非循环边界"""
    count = 0
    if self.rules['neighborhood'] == 'moore':
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          if dx == 0 and dy == 0:
            continue
          nx, ny = x + dx, y + dy
          if 0 <= nx < self.width and 0 <= ny < self.height:
            if self.grid[ny, nx] > 0:
              count += 1
    else:
      for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
          if self.grid[ny, nx] > 0:
            count += 1
    return count

  def update_cell(self, x: int, y: int) -> int:
    """更新单个细胞状态"""
    current_state = self.grid[y, x]
    neighbors = self.count_neighbors(x, y)

    if current_state > 0:
      if neighbors in self.rules['survive']:
        return current_state
      else:
        return 0
    else:
      if neighbors in self.rules['birth']:
        return 1
      else:
        return 0

  def step(self):
    """执行一步演化"""
    for y in range(self.height):
      for x in range(self.width):
        self.next_grid[y, x] = self.update_cell(x, y)
    self.grid, self.next_grid = self.next_grid, self.grid

  def randomize(self, density=0.3):
    """随机初始化网格"""
    self.grid = np.random.choice(
      [0, 1],
      size=(self.height, self.width),
      p=[1 - density, density]
    )

  def clear(self):
    """清空网格"""
    self.grid.fill(0)

  def toggle_cell(self, x: int, y: int):
    """切换细胞状态"""
    if 0 <= x < self.width and 0 <= y < self.height:
      self.grid[y, x] = 1 - self.grid[y, x]
