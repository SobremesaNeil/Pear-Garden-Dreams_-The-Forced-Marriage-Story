# OOC 系统（角色崩坏度）使用指南

## 📋 系统概述

**OOC（Out of Character，角色崩坏度）** 是《梨园戏梦：逼婚记篇》的核心机制。主角必须在舞台上维持"卑躬屈膝、阴险狡诈"的反派师爷人设，否则人设会逐渐崩坏，最终导致 Game Over。

### 核心规则
- **初始值**：20%（相对安全）
- **危险值**：100%（人设彻底崩坏 → 游戏结束）
- **范围限制**：0 - 100

---

## 🎮 四个状态区间

| OOC 值 | 状态 | 脸谱图片 | 动画效果 | 说明 |
|--------|------|---------|--------|------|
| 0-30% | **安全区** | `face_safe.png` | 微弱呼吸灯（白光） | 反派人设稳定，最安全 |
| 31-70% | **警告区** | `face_warning.png` | 警告脉动（黄色） | 人设开始出现裂纹，维持平衡中 |
| 71-99% | **危险区** | `face_danger.png` | 紧急震屏（红色） | 人设即将崩坏，紧急状态 |
| 100% | **崩坏** | N/A | Game Over | 人设完全崩坏，游戏结束 |

---

## 🔧 API 接口

### 1. `check_ooc()` - 检查 OOC 值

**功能**：检查并处理 OOC 值的边界条件

```python
$ check_ooc()
```

**行为**：
- 限制 `ooc_value` 在 0-100 范围内
- 如果 `ooc_value >= 100`，自动跳转到 `game_over_ooc` label
- 返回当前的 `ooc_value`

**使用场景**：每次直接修改 `ooc_value` 后调用

### 2. `update_ooc(amount, auto_check=True)` - 更新 OOC 值

**功能**：根据玩家的行为和选择，增减 OOC 值

```python
$ update_ooc(10)      # 增加 10%
$ update_ooc(-5)      # 减少 5%
$ update_ooc(20, auto_check=False)  # 更新 20%，不自动检查
```

**参数**：
- `amount` (int)：增减量（正数增加，负数减少）
- `auto_check` (bool)：是否自动调用 `check_ooc()` 进行检查（默认 True）

**返回值**：更新后的 `ooc_value`

**开挂模式**：如果 `cheat_count >= 3`，`ooc_value` 强制锁定在 99

### 3. `ooc_value` - 当前 OOC 值

```python
if ooc_value >= 70:
    # 执行危险区逻辑
    pass
```

### 4. `cheat_count` - 开挂次数

```python
$ cheat_count += 1  # 每次使用"一键开挂"时递增
```

当 `cheat_count >= 3` 时，OOC 值锁定在 99（游戏平衡被破坏）

---

## 📺 UI 显示：`ooc_hud` Screen

### 显示 HUD

```ren'py
show screen ooc_hud
```

### 隐藏 HUD

```ren'py
hide screen ooc_hud
```

### 屏幕位置

- **位置**：屏幕左上角（xpos=30, ypos=30）
- **大小**：约 290×320 像素
- **图层**：zorder = 200（在大多数 UI 元素上方）

### HUD 显示内容

1. **OOC 数值**：大号显示当前百分比（例如 "45%"）
2. **脸谱图片**：根据状态显示不同的脸谱（100×120）
3. **动画效果**：根据状态自动播放相应动画
4. **状态文字**：中文状态标签（安全/警告/紧急）
5. **说明文本**："维持反派人设 | OOC 越低越安全"

---

## 🛠️ 集成步骤

### 第 1 步：初始化
在游戏开始前，OOC 系统已自动初始化：
- `ooc_value = 20`（默认值）
- `cheat_count = 0`
- `check_ooc()` 和 `update_ooc()` 已注册

### 第 2 步：显示 HUD
在合适的位置显示 OOC 监控界面：

```ren'py
label start:
    scene bg broken_cottage_dusk
    show screen ooc_hud
    # ... 游戏内容 ...
```

### 第 3 步：响应玩家选择
根据玩家的选择更新 OOC 值：

```ren'py
menu:
    "选项 A（正义行为，人设崩坏）":
        $ update_ooc(25)
        me "这是正确的事情！"
    
    "选项 B（反派行为，人设稳定）":
        $ update_ooc(-10)
        me "这才是我的风格……"
```

### 第 4 步：关键时刻检查
在故事分支点进行显式检查（可选）：

```ren'py
$ check_ooc()
```

---

## 📝 实现示例

### 示例 1：基础菜单选择

```ren'py
label act1_moral_choice:
    hong "贾师爷，这个贫民应该如何处置？"
    
    menu:
        "　【正义】给他一些银两救济":
            $ update_ooc(15)  # +15%（人设受损）
            me "他是个可怜人，应该帮助他。"
            hong "你这是什么鬼主意？！"
        
        "　【反派】驱赶他出城":
            $ update_ooc(-8)  # -8%（人设稳固）
            me "一个废物，不必浪费我们的时间。"
            hong "哈哈，你还是那个贾师爷！"
```

### 示例 2：隐性行为检查

```ren'py
label secret_action:
    # 暗地里做善事（不被发现）
    if ooc_value < 50:
        me "我秘密救济了一个穷人……"
        $ update_ooc(5)  # 轻微人设毛病，但风险小
    else:
        me "现在太危险了，不能冒险……"
```

### 示例 3：一键开挂

```ren'py
label use_cheat:
    $ cheat_count += 1
    $ update_ooc(0)  # 开挂不改变 OOC 值
    
    if cheat_count >= 3:
        me "我已经使用了太多次开挂……游戏平衡被破坏了。"
        me "[系统] 开挂过度使用警告：OOC 值锁定在 99"
```

---

## ⚠️ Game Over 结局

当 `ooc_value >= 100` 时，游戏自动跳转到 `game_over_ooc` label：

```ren'py
label game_over_ooc:
    """
    当玩家的 OOC（角色崩坏度）值达到 100% 时触发此标签
    人设彻底崩坏，游戏结束
    """
    scene bg black with fade
    show text "脸谱已经完全碎裂了……" at center
    show text "你维持不下反派的人设了。" at center
    show text "剧本彻底坏了。" at center
    show text "【崩坏结局】人设尽毁" at truecenter
    return
```

---

## 🎨 所需资源文件

确保游戏的 `game/gui/` 目录下有以下文件：

- `face_safe.png`（0-30%，脸谱完整）
- `face_warning.png`（31-70%，脸谱有裂纹）
- `face_danger.png`（71-99%，脸谱大面积碎裂）
- `ooc_frame.png`（HUD 框架；可选，如不需要可注释掉）

**尺寸建议**：
- 脸谱图片：100×120 像素
- 框架：140×160 像素

---

## 🐛 调试技巧

### 查看当前 OOC 值
```ren'py
me "[ooc_value]%"
```

### 快速测试各状态
```ren'py
$ ooc_value = 20   # 安全区
$ ooc_value = 50   # 警告区
$ ooc_value = 80   # 危险区
$ ooc_value = 100  # Game Over（会自动跳转）
```

### 禁用自动检查
```ren'py
$ update_ooc(50, auto_check=False)  # 更新，但不检查边界
```

---

## 📌 最佳实践

1. **在关键场景显示 HUD**：在重要的道德选择点前显示，让玩家意识到风险
2. **渐进式增加难度**：早期的选择影响小，后期的选择影响大
3. **隐藏式选择**：某些暗地里的善事可以有较低的 OOC 增加
4. **提示玩家**：在 OOC 值接近危险区时，通过 NPC 对话给出警告
5. **多周目鼓励**：将不同的 OOC 结局设为隐藏内容，鼓励多周目游玩

---

## 📚 文件清单

### 修改文件
- **`game/script.rpy`**：
  - ✅ Init Python 块（定义 `check_ooc()` 和 `update_ooc()`）
  - ✅ Default 变量（`ooc_value`, `cheat_count`, `qte_fail_count`）
  - ✅ `game_over_ooc` label

- **`game/screens.rpy`**：
  - ✅ ATL Transform（`ooc_safe_breathing`, `ooc_warning_pulse`, `ooc_danger_shake`）
  - ✅ `ooc_hud()` Screen Definition

#### 文档
- 📄 `OOC_SYSTEM_GUIDE.md`（本文件）

---

**祝您游戏开发顺利！** 🎭✨
