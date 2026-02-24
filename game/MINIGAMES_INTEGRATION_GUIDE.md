# 《梨园戏梦》三大小游戏系统完整集成指南

## 📋 快速概览

本项目包含三个独立但相互配合的交互小游戏系统，用于增强《梨园戏梦》视觉小说的互动体验：

| 小游戏 | 场景 | 机制 | 核心类 | 返回值 |
|--------|------|------|--------|--------|
| **脸谱复原** | 序章 | 拖拽拼图 | `PuzzleGame` | success/cheat |
| **伪造婚书** | 第一幕 | 笔画追踪 | `StrokeTracker` | success/cheat |
| **深夜潜行** | 第二幕 | 路径规划 | `NinePuzzleGame` | success/cheat/fail |

---

## 🗂️ 文件结构

```
game/
├── minigames.py                  # 核心游戏逻辑类
├── minigames_screens.rpy         # Ren'Py 屏幕定义 
├── script.rpy                    # 主脚本（含初始化）
├── MINIGAMES_USAGE_GUIDE.txt     # 快速参考
└── MINIGAMES_INTEGRATION_GUIDE.md # 本文件
```

---

## 🚀 快速集成步骤

### 第1步：确保文件齐全

在 `game/` 目录下应有：
- ✅ `minigames.py` - 已创建，包含三大游戏逻辑
- ✅ `minigames_screens.rpy` - 已创建，包含屏幕定义
- ✅ `script.rpy` - 已包含初始化代码

### 第2步：在 label 中调用小游戏

```ren'py
label my_scene():
    # 初始化游戏
    $ init_puzzle_game()  # 或 init_stroke_tracker() 或 init_nine_puzzle()
    
    # 调用屏幕
    $ result = renpy.call_screen("puzzle_restoration")  # 屏幕名称
    
    # 处理结果
    if result == "success":
        $ update_ooc(-10)
        "成功完成！"
    elif result == "cheat":
        $ update_ooc(-40)
        $ cheat_count += 1
        "使用了开挂……"
    else:
        "失败或取消。"
```

### 第3步：配置资源路径

在 `script.rpy` 的初始化函数中，替换占位符图片路径：

```python
# 脸谱碎片图片
fragment_configs = [
    (0, "images/puzzle_fragment_1.png", 400, 250, 20),
    # 改为实际路径...
]

# 婚字背景图
stroke_tracker = StrokeTracker(
    checkpoints_data=checkpoints,
    time_limit=10.0,
    bg_image="images/hui_character.png"  # 改为实际的"婚"字图片
)
```

---

## 📖 各小游戏详细说明

### 1️⃣ 脸谱复原（Puzzle Restoration）

**场景**: 序章中，玩家发现破碎的京剧脸谱，需要拼凑完整。

**技术实现**: 
- 使用 Ren'Py 的 `Drag` & `Drop` 机制
- 自动吸附（20px 容差检测）
- 所有碎片吸附后自动返回 success

**核心类**: `PuzzleGame`, `PuzzleFragment`

**配置项**:
```python
fragment_configs = [
    (id, image_path, target_x, target_y, snap_tolerance),
    # target_x, target_y: 吸附目标位置
    # snap_tolerance: 吸附容差（像素）
]
```

**OOC值影响**:
- 正常完成: OOC -10
- 开挂完成: OOC -40 + cheat_count +1

---

### 2️⃣ 伪造婚书（Stroke Writing）

**场景**: 第一幕，帮助反派人物在婚书上描红"婚"字。

**技术实现**:
- 预设笔画检查点（Checkpoints）
- 鼠标轨迹追踪（CDD 实现）
- 顺序触发所有检查点即成功
- 10 秒限时

**核心类**: `StrokeTracker`, `StrokeCheckpoint`

**配置项**:
```python
checkpoints = [
    (checkpoint_id, x, y, radius),
    # 按笔顺排列检查点坐标
]

stroke_tracker = StrokeTracker(
    checkpoints_data=checkpoints,
    time_limit=10.0,  # 秒数
    bg_image="images/hui_character.png"
)
```

**工作流程**:
1. 玩家在"婚"字背景上拖拽鼠标
2. 系统绘制轨迹线，同时检测是否触发检查点
3. 按顺序触发所有检查点 → 返回 "success"
4. 超时或跳出顺序 → 清除状态，允许重试

**OOC值影响**:
- 正常完成: OOC -20
- 开挂完成: OOC -50 + cheat_count +1

---

### 3️⃣ 深夜潜行（Nine Puzzle Path）

**场景**: 第二幕，玩家需要规划从入口(0)到卧房(8)的安全路线，避开巡逻队。

**技术实现**:
- 3x3 网格图结构
- 节点邻接关系定义
- 危险路线（红线）检测
- 一笔画原则（边不可重复）

**核心类**: `NinePuzzleGame`

**网格布局**:
```
0 1 2
3 4 5
6 7 8

起点: 0 (左上)
终点: 8 (右下)
```

**配置项**:
```python
nine_puzzle_game.adjacency = {
    0: [1, 3],      # 节点 0 可连接到 1, 3
    1: [0, 2, 4],   # ...
    # ...
}

nine_puzzle_game.dangerous_edges = set([
    (0, 2),  # 禁止路线（示例）
    (6, 8),
])
```

**游戏规则**:
1. 玩家点击相邻节点，建立连线
2. 不能通过红线（危险路线）→ 触发警报 → 返回 "fail"
3. 不能重复走过的边 → 拒绝操作
4. 到达节点 8 → 返回 "success"

**OOC值影响**:
- 正常完成: OOC -15
- 开挂完成: OOC -45 + cheat_count +1
- 触发危险: OOC +20 + 返回 "fail"

---

## 🔧 自定义与扩展

### 修改碎片数量（脸谱）
```python
def init_puzzle_game():
    puzzle_game = PuzzleGame(num_fragments=6)  # 改为 6 个碎片
    # ... 添加 6 个 fragment_configs
```

### 修改检查点路径（描红）
编辑 `checkpoints` 列表，调整坐标以匹配"婚"字的实际笔画：
```python
checkpoints = [
    (0, 300, 200, 15),  # 起笔
    (1, 300, 250, 15),  # 第二笔
    # 用实际坐标替换...
]
```

### 修改网格邻接关系（九宫格）
```python
# 让节点 0 也能直接连到节点 8（不推荐，太简单）
nine_puzzle_game.adjacency[0].append(8)
nine_puzzle_game.adjacency[8].append(0)
```

### 添加更多危险路线
```python
nine_puzzle_game.dangerous_edges.add((1, 4))
nine_puzzle_game.dangerous_edges.add((5, 7))
```

---

## 🎮 测试与验证

### 快速测试 Label
```ren'py
label test_minigames:
    $ init_puzzle_game()
    $ result = renpy.call_screen("puzzle_restoration")
    $ renpy.notify(f"result: {result}")
```

### 完整测试流程
在 `script.rpy` 中有预设的 `label test_all_minigames()` 可用。

---

## 🐛 常见问题与排查

### Q1: 屏幕无响应或无法返回
A: 检查 `Return()` 语句是否正确，确保每个分支都有返回值。

### Q2: 图片路径错误导致 404
A: 验证 `images/` 目录中是否真的存在对应文件。路径为相对路径，从 `game/` 目录开始。

### Q3: OOC值没有正确增减
A: 确保在调用 `update_ooc()` 后，通过调用 `check_ooc()` 进行边界检查。

### Q4: DragGroup 拖拽没有反应
A: 检查碎片的初始坐标是否在屏幕范围内。位置超出屏幕外可能无法拖拽。

### Q5: 九宫格路线多次重复触发危险
A: 验证 `dangerous_edges` 集合中的边是否正确定义（使用标准化形式）。

---

## 📊 OOC 系统积分表

```
脸谱复原:
  ✓ 正常成功   → OOC -10
  🎫 开挂成功   → OOC -40

描红笔画:
  ✓ 正常成功   → OOC -20
  🎫 开挂成功   → OOC -50

九宫格路线:
  ✓ 正常成功   → OOC -15
  🎫 开挂成功   → OOC -45
  ✗ 触发危险   → OOC +20

通用:
  📍 开挂 3 次  → OOC 锁定在 99（不再增减）
```

---

## 💾 集成到现有项目的最小步骤

如果你只想快速集成而不做自定义：

1. **复制文件**
   ```bash
   cp minigames.py game/
   cp minigames_screens.rpy game/screens_minigames.rpy
   ```

2. **在 script.rpy 中导入并初始化**
   - ✅ 已在 init python 块中完成

3. **在需要的 label 中调用**
   ```ren'py
   $ init_puzzle_game()
   $ result = renpy.call_screen("puzzle_restoration")
   ```

4. **替换占位符图片路径**
   - 在 `script.rpy` 的初始化函数中修改

---

## 📞 技术支持

如有问题，检查以下文件：
- **游戏逻辑**: `minigames.py`
- **屏幕定义**: `minigames_screens.rpy`
- **初始化**: `script.rpy` 的 init python 块
- **API 参考**: `MINIGAMES_USAGE_GUIDE.txt`

---

**最后更新**: 2026-02-25  
**版本**: 1.0 - 完整实现三大小游戏系统
