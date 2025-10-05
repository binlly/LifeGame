# macOS 输入法兼容性修复
import os
import sys

if sys.platform == "darwin":
  os.environ['TK_SILENCE_DEPRECATION'] = '1'

import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
      'survive': [2, 3],  # 存活条件（邻居数量）
      'birth': [3],  # 诞生条件（邻居数量）
      'states': 2,  # 状态数量
      'neighborhood': 'moore'  # 邻域类型：'moore' 或 'von_neumann'
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
    """计算邻居数量"""
    count = 0
    if self.rules['neighborhood'] == 'moore':
      # Moore邻域（8个方向）
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          if dx == 0 and dy == 0:
            continue
          nx, ny = (x + dx) % self.width, (y + dy) % self.height
          if self.grid[ny, nx] > 0:
            count += 1
    else:
      # Von Neumann邻域（4个方向）
      for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = (x + dx) % self.width, (y + dy) % self.height
        if self.grid[ny, nx] > 0:
          count += 1
    return count

  def update_cell(self, x: int, y: int) -> int:
    """更新单个细胞状态"""
    current_state = self.grid[y, x]
    neighbors = self.count_neighbors(x, y)

    if current_state > 0:  # 细胞存活
      if neighbors in self.rules['survive']:
        return current_state
      else:
        return 0
    else:  # 细胞死亡
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


class CellularAutomatonGUI:
  """元胞自动机图形界面"""

  def __init__(self, root):
    self.root = root
    self.root.title("元胞自动机模拟器")
    self.root.geometry("900x750")

    # 初始化元胞自动机
    self.ca = CellularAutomaton(50, 50)
    self.running = False
    self.fps = 10  # 迭代速度 (1-50)
    self.show_grid_lines = True  # 是否显示网格线

    # 预设规则
    self.preset_rules = {
      "康威生命游戏": {
        'survive': [2, 3],
        'birth': [3],
        'states': 2,
        'neighborhood': 'moore'
      },
      "高生命": {
        'survive': [2, 3],
        'birth': [3, 6],
        'states': 2,
        'neighborhood': 'moore'
      },
      "Day & Night": {
        'survive': [3, 4, 6, 7, 8],
        'birth': [3, 6, 7, 8],
        'states': 2,
        'neighborhood': 'moore'
      },
      "Von Neumann Life": {
        'survive': [2, 3],
        'birth': [3],
        'states': 2,
        'neighborhood': 'von_neumann'
      }
    }

    self.setup_ui()
    self.bind_window_events()
    self.draw_grid()

  def setup_ui(self):
    """设置用户界面"""
    # 主框架
    self.main_frame = ttk.Frame(self.root)
    self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 第一行控制面板
    control_frame1 = ttk.Frame(self.main_frame)
    control_frame1.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

    # 基本操作按钮
    ttk.Button(control_frame1, text="开始/暂停", command=self.toggle_run).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame1, text="单步", command=self.step).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame1, text="清空", command=self.clear).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame1, text="随机", command=self.randomize).pack(side=tk.LEFT, padx=5)

    # 网格显示选项
    grid_check_var = tk.BooleanVar(value=True)
    self.grid_check_var = grid_check_var
    ttk.Checkbutton(
      control_frame1,
      text="显示网格线",
      variable=grid_check_var,
      command=self.toggle_grid_lines
    ).pack(side=tk.LEFT, padx=(20, 5))

    # 网格大小设置
    size_frame = ttk.Frame(control_frame1)
    size_frame.pack(side=tk.LEFT, padx=(20, 0))
    ttk.Label(size_frame, text="网格大小:").pack(side=tk.LEFT, padx=(0, 5))
    self.size_var = tk.StringVar(value="50")
    size_entry = ttk.Entry(size_frame, textvariable=self.size_var, width=5)
    size_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(size_frame, text="应用", command=self.apply_grid_size).pack(side=tk.LEFT, padx=5)

    # 第二行控制面板 - 自定义规则按钮
    control_frame2 = ttk.Frame(self.main_frame)
    control_frame2.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

    # 规则选择
    rule_frame = ttk.Frame(control_frame2)
    rule_frame.pack(side=tk.LEFT)
    ttk.Label(rule_frame, text="规则:").pack(side=tk.LEFT, padx=(0, 5))
    self.rule_var = tk.StringVar(value="康威生命游戏")
    rule_combo = ttk.Combobox(
      rule_frame,
      textvariable=self.rule_var,
      values=list(self.preset_rules.keys()),
      state="readonly",
      width=15
    )
    rule_combo.pack(side=tk.LEFT, padx=5)
    rule_combo.bind('<<ComboboxSelected>>', self.on_rule_change)

    # 自定义规则按钮移到第二行
    custom_frame = ttk.Frame(control_frame2)
    custom_frame.pack(side=tk.RIGHT)
    ttk.Button(custom_frame, text="自定义规则", command=self.custom_rule_dialog).pack(side=tk.LEFT, padx=5)
    ttk.Button(custom_frame, text="保存规则", command=self.save_rule).pack(side=tk.LEFT, padx=5)
    ttk.Button(custom_frame, text="加载规则", command=self.load_rule).pack(side=tk.LEFT, padx=5)

    # 迭代速度控制（替换原来的速度控制）
    fps_frame = ttk.Frame(control_frame2)
    fps_frame.pack(side=tk.LEFT, padx=(20, 0))
    ttk.Label(fps_frame, text="迭代速度:").pack(side=tk.LEFT, padx=(0, 5))

    # 迭代速度显示
    self.fps_display_var = tk.StringVar(value="10 步")
    ttk.Label(fps_frame, textvariable=self.fps_display_var, width=8).pack(side=tk.LEFT, padx=(0, 5))

    self.fps_var = tk.IntVar(value=10)
    fps_scale = ttk.Scale(
      fps_frame,
      from_=1,
      to=50,
      variable=self.fps_var,
      orient=tk.HORIZONTAL,
      length=120,
      command=self.on_fps_change
    )
    fps_scale.pack(side=tk.LEFT, padx=5)

    # 网格显示区域 - 使用Frame作为容器，Canvas会填充它
    self.canvas_frame = ttk.Frame(self.main_frame)
    self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    # 创建画布（初始大小稍后会调整）
    self.canvas = tk.Canvas(
      self.canvas_frame,
      bg='white',
      highlightthickness=1,
      highlightbackground='black'
    )
    self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 绑定鼠标事件
    self.canvas.bind('<Button-1>', self.on_canvas_click)
    self.canvas.bind('<B1-Motion>', self.on_canvas_drag)

    # 绑定键盘事件
    self.root.bind('<space>', self.toggle_run)
    self.root.focus_set()  # 确保窗口获得焦点

    # 状态栏
    self.status_var = tk.StringVar(value="就绪 | 迭代速度: 10 步")
    status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

  def bind_window_events(self):
    """绑定窗口事件"""
    self.root.bind('<Configure>', self.on_window_resize)
    # 防止重复调用的标志
    self.resize_pending = False

  def on_window_resize(self, event):
    """窗口大小改变时的处理"""
    # 只处理主窗口的Configure事件，避免子组件触发
    if event.widget == self.root and not self.resize_pending:
      self.resize_pending = True
      # 使用after来延迟处理，避免频繁重绘
      self.root.after(50, self.handle_resize)

  def handle_resize(self):
    """处理窗口调整大小"""
    self.resize_pending = False
    self.calculate_cell_size()
    self.draw_grid()

  def calculate_cell_size(self):
    """根据当前窗口大小计算单元格大小"""
    # 获取可用空间
    frame_width = self.canvas_frame.winfo_width()
    frame_height = self.canvas_frame.winfo_height()

    # 减去边距
    available_width = max(100, frame_width - 20)  # 最小100像素
    available_height = max(100, frame_height - 20)  # 最小100像素

    # 计算单元格大小，确保网格能完整显示
    cell_size_x = available_width // self.ca.width
    cell_size_y = available_height // self.ca.height
    self.cell_size = min(cell_size_x, cell_size_y, 30)  # 最大30像素

    # 确保至少为4像素
    self.cell_size = max(4, self.cell_size)

  def draw_grid(self):
    """绘制网格"""
    # 如果窗口还没有正确初始化，跳过绘制
    if self.canvas.winfo_width() <= 1 or self.canvas.winfo_height() <= 1:
      return

    self.calculate_cell_size()
    self.canvas.delete("all")

    # 计算实际绘制区域
    total_width = self.ca.width * self.cell_size
    total_height = self.ca.height * self.cell_size

    # 居中绘制
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()
    offset_x = (canvas_width - total_width) // 2
    offset_y = (canvas_height - total_height) // 2

    for y in range(self.ca.height):
      for x in range(self.ca.width):
        x1 = offset_x + x * self.cell_size
        y1 = offset_y + y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if self.ca.grid[y, x]:
          self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='black',
            outline='black' if self.show_grid_lines else 'black'
          )
        else:
          if self.show_grid_lines:
            self.canvas.create_rectangle(
              x1, y1, x2, y2,
              fill='white',
              outline='lightgray'
            )
          else:
            self.canvas.create_rectangle(
              x1, y1, x2, y2,
              fill='white',
              outline=''
            )

  def toggle_run(self, event=None):
    """切换运行/暂停状态"""
    self.running = not self.running
    if self.running:
      self.run_step()
    else:
      # 取消现有的after调用
      if self.after_id:
        self.root.after_cancel(self.after_id)
        self.after_id = None
    self.update_status()

  def run_step(self):
    """运行步骤（递归调用实现动画）"""
    if self.running:
      self.step()
      # 计算延迟时间（毫秒）= 1000 / FPS
      delay = max(20, int(1000 / self.fps))  # 最小20ms避免过于频繁
      # 存储after调用的ID，以便后续取消
      self.after_id = self.root.after(delay, self.run_step)

  def step(self):
    """执行单步"""
    self.ca.step()
    self.draw_grid()
    if hasattr(self, 'step_count'):
      self.step_count += 1
    else:
      self.step_count = 1
    self.update_status()

  def clear(self):
    """清空网格 - 自动暂停"""
    # 自动暂停
    if self.running:
      self.running = False
      if self.after_id:
        self.root.after_cancel(self.after_id)
        self.after_id = None

    self.ca.clear()
    self.draw_grid()
    self.step_count = 0
    self.update_status()
    self.status_var.set(f"已清空 | 迭代速度: {self.fps} 步")

  def randomize(self):
    """随机初始化"""
    self.ca.randomize()
    self.draw_grid()
    self.step_count = 0
    self.update_status()

  def on_fps_change(self, value):
    """迭代速度改变时的处理"""
    new_fps = int(float(value))
    self.fps = new_fps
    self.fps_display_var.set(f"{new_fps} 步")

    # 如果正在运行，重新启动以应用新迭代速度
    if self.running:
      # 先取消当前的定时器
      if self.after_id:
        self.root.after_cancel(self.after_id)
        self.after_id = None
      # 重新启动
      delay = max(20, int(1000 / self.fps))
      self.after_id = self.root.after(delay, self.run_step)

    self.update_status()

  def on_rule_change(self, event=None):
    """规则改变时的处理"""
    rule_name = self.rule_var.get()
    if rule_name in self.preset_rules:
      self.ca.set_rule(self.preset_rules[rule_name])
      self.clear()
      self.status_var.set(f"已切换到规则: {rule_name} | 迭代速度: {self.fps} 步")

  def apply_grid_size(self):
    """应用新的网格大小"""
    try:
      size = int(self.size_var.get())
      if size < 10 or size > 150:  # 扩大范围到150
        messagebox.showerror("错误", "网格大小必须在10-150之间")
        return

      # 保存当前运行状态
      was_running = self.running
      if was_running:
        self.running = False
        if self.after_id:
          self.root.after_cancel(self.after_id)
          self.after_id = None

      # 创建新的元胞自动机
      self.ca = CellularAutomaton(size, size)
      self.ca.set_rule(self.preset_rules[self.rule_var.get()])

      # 重置步骤计数
      self.step_count = 0

      # 重新绘制
      self.draw_grid()

      # 恢复运行状态（如果之前在运行）
      if was_running:
        self.running = True
        self.run_step()

      self.status_var.set(f"网格大小已设置为 {size}x{size} | 迭代速度: {self.fps} 步")

    except ValueError:
      messagebox.showerror("错误", "请输入有效的数字")

  def toggle_grid_lines(self):
    """切换网格线显示"""
    self.show_grid_lines = self.grid_check_var.get()
    self.draw_grid()
    self.status_var.set(f"网格线: {'显示' if self.show_grid_lines else '隐藏'} | 迭代速度: {self.fps} 步")

  def custom_rule_dialog(self):
    """自定义规则对话框"""
    dialog = tk.Toplevel(self.root)
    dialog.title("自定义规则")
    dialog.geometry("400x300")
    dialog.transient(self.root)
    dialog.grab_set()

    # 获取当前规则
    current_rule = self.ca.rules.copy()

    # 生存条件
    ttk.Label(dialog, text="生存条件 (邻居数量):").pack(pady=(10, 5))
    survive_var = tk.StringVar(value=','.join(map(str, current_rule.get('survive', []))))
    survive_entry = ttk.Entry(dialog, textvariable=survive_var)
    survive_entry.pack(pady=5)

    # 诞生条件
    ttk.Label(dialog, text="诞生条件 (邻居数量):").pack(pady=(10, 5))
    birth_var = tk.StringVar(value=','.join(map(str, current_rule.get('birth', []))))
    birth_entry = ttk.Entry(dialog, textvariable=birth_var)
    birth_entry.pack(pady=5)

    # 邻域类型
    ttk.Label(dialog, text="邻域类型:").pack(pady=(10, 5))
    neighborhood_var = tk.StringVar(value=current_rule.get('neighborhood', 'moore'))
    neighborhood_combo = ttk.Combobox(
      dialog,
      textvariable=neighborhood_var,
      values=['moore', 'von_neumann'],
      state="readonly"
    )
    neighborhood_combo.pack(pady=5)

    def apply_rule():
      try:
        # 解析输入
        survive_input = survive_var.get().strip()
        birth_input = birth_var.get().strip()

        if not survive_input and not birth_input:
          messagebox.showerror("错误", "生存条件和诞生条件不能同时为空")
          return

        survive = [int(x.strip()) for x in survive_input.split(',') if x.strip()] if survive_input else []
        birth = [int(x.strip()) for x in birth_input.split(',') if x.strip()] if birth_input else []
        neighborhood = neighborhood_var.get()

        # 验证输入范围
        for val in survive + birth:
          if val < 0 or val > 8:
            messagebox.showerror("错误", "邻居数量必须在0-8之间")
            return

        # 创建新规则
        new_rule = {
          'survive': survive,
          'birth': birth,
          'states': 2,
          'neighborhood': neighborhood
        }

        self.ca.set_rule(new_rule)
        self.clear()
        self.status_var.set(f"已应用自定义规则 | 迭代速度: {self.fps} 步")
        dialog.destroy()

      except ValueError:
        messagebox.showerror("错误", "请输入有效的数字，用逗号分隔")

    button_frame = ttk.Frame(dialog)
    button_frame.pack(pady=20)
    ttk.Button(button_frame, text="应用", command=apply_rule).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

  def save_rule(self):
    """保存规则到文件"""
    filename = filedialog.asksaveasfilename(
      defaultextension=".json",
      filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if filename:
      try:
        with open(filename, 'w', encoding='utf-8') as f:
          json.dump(self.ca.rules, f, indent=2, ensure_ascii=False)
        self.status_var.set(f"规则已保存到: {os.path.basename(filename)} | 迭代速度: {self.fps} 步")
      except Exception as e:
        messagebox.showerror("错误", f"保存失败: {str(e)}")

  def load_rule(self):
    """从文件加载规则"""
    filename = filedialog.askopenfilename(
      filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if filename:
      try:
        with open(filename, 'r', encoding='utf-8') as f:
          rule = json.load(f)
        self.ca.set_rule(rule)
        self.clear()
        self.status_var.set(f"已加载规则: {os.path.basename(filename)} | 迭代速度: {self.fps} 步")
      except Exception as e:
        messagebox.showerror("错误", f"加载失败: {str(e)}")

  def on_canvas_click(self, event):
    """处理鼠标点击"""
    if self.running:
      return

    # 获取可用绘制区域的偏移量
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()
    total_width = self.ca.width * self.cell_size
    total_height = self.ca.height * self.cell_size
    offset_x = (canvas_width - total_width) // 2
    offset_y = (canvas_height - total_height) // 2

    # 转换鼠标坐标到网格坐标
    grid_x = (event.x - offset_x) // self.cell_size
    grid_y = (event.y - offset_y) // self.cell_size

    # 检查是否在有效范围内
    if 0 <= grid_x < self.ca.width and 0 <= grid_y < self.ca.height:
      self.ca.toggle_cell(grid_x, grid_y)
      self.draw_grid()
      self.status_var.set(f"切换细胞 ({grid_x}, {grid_y}) | 迭代速度: {self.fps} 步")

  def on_canvas_drag(self, event):
    """处理鼠标拖拽"""
    if self.running:
      return

    # 获取可用绘制区域的偏移量
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()
    total_width = self.ca.width * self.cell_size
    total_height = self.ca.height * self.cell_size
    offset_x = (canvas_width - total_width) // 2
    offset_y = (canvas_height - total_height) // 2

    # 转换鼠标坐标到网格坐标
    grid_x = (event.x - offset_x) // self.cell_size
    grid_y = (event.y - offset_y) // self.cell_size

    # 检查是否在有效范围内
    if 0 <= grid_x < self.ca.width and 0 <= grid_y < self.ca.height:
      self.ca.toggle_cell(grid_x, grid_y)
      self.draw_grid()

  def update_status(self):
    """更新状态栏"""
    if hasattr(self, 'step_count'):
      status_text = f"步骤: {self.step_count} | 运行中: {'是' if self.running else '否'} | 迭代速度: {self.fps} 步 | 网格: {self.ca.width}x{self.ca.height}"
    else:
      status_text = f"就绪 | 运行中: {'是' if self.running else '否'} | 迭代速度: {self.fps} 步 | 网格: {self.ca.width}x{self.ca.height}"
    self.status_var.set(status_text)


def main():
  root = tk.Tk()
  app = CellularAutomatonGUI(root)
  root.mainloop()


if __name__ == "__main__":
  main()
