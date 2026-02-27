id = 1  # 可根据碎片数量修改，
# 碎片目标坐标（X/Y，根据你的游戏界面调整）
target_x = 200  # 碎片要对齐的目标X坐标
target_y = 150  # 碎片要对齐的目标Y坐标
tolerance = 10
fragment_configs = [
    (id, "images/path.png", target_x, target_y, tolerance),
    # 需要替换为实际的碎片图片路径
]
fragment_configs = [
    (id, "images/path.png", target_x, target_y, tolerance),
    # 需要替换为实际的碎片图片路径
]
"""
《梨园戏梦》三大交互小游戏核心逻辑
包含：脸谱复原、伪造婚书、深夜潜行
"""

import math
import pygame
import time
################################################################################
## 小游戏 1：脸谱复原（拖拽拼图）
################################################################################

class PuzzleFragment:
    """脸谱碎片数据类"""
    def __init__(self, fragment_id, image_path, target_x, target_y, snap_tolerance=20):
        self.id = fragment_id
        self.image_path = image_path  # 如 "images/puzzle_fragment_1.png"
        self.target_x = target_x      # 目标吸附位置 X
        self.target_y = target_y      # 目标吸附位置 Y
        self.snap_tolerance = snap_tolerance  # 吸附容差（像素）
        
        # 当前位置（初始为随机值）
        self.current_x = None
        self.current_y = None
        
        # 状态标记
        self.is_snapped = False
        
    def check_snap(self, x, y):
        """检查是否应该吸附到目标位置"""
        distance = math.sqrt((x - self.target_x) ** 2 + (y - self.target_y) ** 2)
        if distance <= self.snap_tolerance:
            self.is_snapped = True
            return True
        return False
    
    def snap_to_target(self):
        """吸附到目标位置"""
        self.current_x = self.target_x
        self.current_y = self.target_y
        self.is_snapped = True


class PuzzleGame:
    """脸谱复原小游戏管理器"""
    def __init__(self, num_fragments=5):
        self.fragments = []
        self.num_fragments = num_fragments
        self.all_snapped = False
        
    def add_fragment(self, fragment):
        """添加一个碎片"""
        self.fragments.append(fragment)
    
    def check_completion(self):
        """检查是否所有碎片都已吸附"""
        if len(self.fragments) == 0:
            return False
        self.all_snapped = all(frag.is_snapped for frag in self.fragments)
        return self.all_snapped


################################################################################
## 小游戏 2：伪造婚书（汉字描红 / 轨迹追踪）
################################################################################

class StrokeCheckpoint:
    """笔画检查点"""
    def __init__(self, checkpoint_id, x, y, radius=15):
        self.id = checkpoint_id
        self.x = x
        self.y = y
        self.radius = radius
        self.is_triggered = False
    
    def check_proximity(self, mouse_x, mouse_y):
        """检查鼠标是否靠近此检查点"""
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius
    
    def trigger(self):
        """标记为已触发"""
        self.is_triggered = True


class StrokeTracker:
    """汉字描红笔画追踪系统（Creator-Defined Displayable）"""
    def __init__(self, checkpoints_data, time_limit=10.0, bg_image="images/hui_character.png"):
        """
        参数：
        - checkpoints_data: 列表，每个元素为 (id, x, y, radius) 或 (id, x, y)
        - time_limit: 限时秒数
        - bg_image: 背景字体图片路径（如 "images/hui_character.png"）
        """
        self.checkpoints = []
        for data in checkpoints_data:
            if len(data) == 3:
                cid, x, y = data
                checkpoint = StrokeCheckpoint(cid, x, y, radius=15)
            else:
                cid, x, y, radius = data
                checkpoint = StrokeCheckpoint(cid, x, y, radius)
            self.checkpoints.append(checkpoint)
        
        self.bg_image = bg_image
        self.time_limit = time_limit
        self.start_time = None
        
        # 绘制相关
        self.current_path = []  # 存储鼠标轨迹坐标 [(x1, y1), (x2, y2), ...]
        self.line_points = []   # 用于绘制的线条点集
        self.mouse_down = False
        
        # 触发状态
        self.last_ordered_checkpoint = -1  # 上一个按顺序触发的检查点 ID
        
    def update_mouse_position(self, mouse_x, mouse_y):
        """更新鼠标位置并检查检查点"""
        if not self.mouse_down:
            return
        
        self.current_path.append((mouse_x, mouse_y))
        
        # 检查是否触发下一个检查点
        next_checkpoint_id = self.last_ordered_checkpoint + 1
        if next_checkpoint_id < len(self.checkpoints):
            checkpoint = self.checkpoints[next_checkpoint_id]
            if checkpoint.check_proximity(mouse_x, mouse_y) and not checkpoint.is_triggered:
                checkpoint.trigger()
                self.last_ordered_checkpoint = next_checkpoint_id
    
    def is_completed(self):
        """检查是否完成（所有检查点都已触发）"""
        return self.last_ordered_checkpoint == len(self.checkpoints) - 1
    
    def is_timeout(self, current_time):
        """检查是否超时"""
        if self.start_time is None:
            self.start_time = current_time
            return False
        elapsed = current_time - self.start_time
        return elapsed >= self.time_limit
    
    def get_remaining_time(self, current_time):
        """获取剩余时间"""
        if self.start_time is None:
            return self.time_limit
        elapsed = current_time - self.start_time
        return max(0, self.time_limit - elapsed)


################################################################################
## 小游戏 3：深夜潜行（九宫格一笔画）
################################################################################

class NinePuzzleGame:
    """九宫格一笔画小游戏"""
    def __init__(self):
        """
        3x3 网格布局：
        0 1 2
        3 4 5
        6 7 8
        
        起点：0（左上）
        终点：8（右下）
        """
        # 定义节点邻接关系
        self.adjacency = {
            0: [1, 3],           # 节点 0 可连接到 1, 3
            1: [0, 2, 4],        # 节点 1 可连接到 0, 2, 4
            2: [1, 5],           # 节点 2 可连接到 1, 5
            3: [0, 4, 6],        # 节点 3 可连接到 0, 4, 6
            4: [1, 3, 5, 7],     # 节点 4 可连接到 1, 3, 5, 7（中心）
            5: [2, 4, 8],        # 节点 5 可连接到 2, 4, 8
            6: [3, 7],           # 节点 6 可连接到 3, 7
            7: [4, 6, 8],        # 节点 7 可连接到 4, 6, 8
            8: [5, 7]            # 节点 8 可连接到 5, 7
        }
        
        # 危险路线（红线）：禁止通过的边集合
        # 格式：(node_a, node_b) 或 (node_b, node_a) 都会被识别为危险
        self.dangerous_edges = set([
            (0, 2),  # 示例：左上到右上的对角线（可自定义）
            (6, 8),  # 示例：左下到右下的对角线（可自定义）
        ])
        
        # 当前游戏状态
        self.current_path = [0]  # 从节点 0 开始
        self.path_edges = set()  # 记录已走过的边（存储排序后的边）
        
    def _normalize_edge(self, node_a, node_b):
        """返回标准化的边表示（较小的节点在前）"""
        return (min(node_a, node_b), max(node_a, node_b))
    
    def is_dangerous_edge(self, node_a, node_b):
        """检查是否为危险路线"""
        edge = self._normalize_edge(node_a, node_b)
        return edge in self.dangerous_edges
    
    def can_move_to(self, to_node):
        """检查是否可以移动到指定节点"""
        current_node = self.current_path[-1]
        
        # 1. 检查相邻性
        if to_node not in self.adjacency[current_node]:
            return False, "非相邻节点"
        
        # 2. 检查危险路线
        if self.is_dangerous_edge(current_node, to_node):
            return False, "触发危险路线！"
        
        # 3. 检查边是否已走过（一笔画原则）
        edge = self._normalize_edge(current_node, to_node)
        if edge in self.path_edges:
            return False, "不能重复走过的边"
        
        return True, "可以移动"
    
    def move_to(self, to_node):
        """移动到下一个节点"""
        can_move, msg = self.can_move_to(to_node)
        if not can_move:
            return False, msg
        
        self.current_path.append(to_node)
        edge = self._normalize_edge(self.current_path[-2], to_node)
        self.path_edges.add(edge)
        
        # 检查是否到达终点
        if to_node == 8:
            return True, "到达终点！"
        
        return True, "继续移动"
    
    def get_drawable_path_edges(self):
        """返回可绘制的路径边（用于 screen 绘制）"""
        return list(self.path_edges)
    
    def reset(self):
        """重置游戏"""
        self.current_path = [0]
        self.path_edges = set()
