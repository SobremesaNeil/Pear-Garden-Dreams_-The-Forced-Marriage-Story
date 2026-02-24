# OOC 系统实现完成报告

## ✅ 任务完成状态

### Task 1：核心变量与判定逻辑 ✅ 完成

在 [game/script.rpy](game/script.rpy) 中实现：

#### 1. Init Python 块（第 1-57 行）
```python
init python:
    def check_ooc():
        """检查并处理 OOC 值的边界条件"""
        # - 限制范围在 0-100
        # - 达到 100 自动 jump 到 game_over_ooc
    
    def update_ooc(amount, auto_check=True):
        """更新 OOC 值的通用函数"""
        # - 支持正/负增量
        # - 开挂模式支持（cheat_count >= 3 时锁定在 99）
        # - 自动边界检查
```

#### 2. 默认变量定义（第 64-69 行）
```python
default ooc_value = 20          # 初始值：20%（相对安全）
default cheat_count = 0         # 开挂计数器
default qte_fail_count = 0      # QTE 失败计数
```

#### 3. Game Over 结局 Label（第 706-758 行）
```python
label game_over_ooc:
    """人设完全崩坏时自动触发"""
    # 显示结局动画和文本
    # 返回标题菜单
```

---

### Task 2：OOC 实时监控 UI ✅ 完成

在 [game/screens.rpy](game/screens.rpy) 中实现：

#### 1. 动画变换（第 37-61 行）
```python
# 安全区：微弱呼吸灯
transform ooc_safe_breathing:
    # α 在 0.4-0.7 循环脉动

# 警告区：警告脉动
transform ooc_warning_pulse:
    # α 在 0.6-1.0 循环脉动

# 危险区：震屏效果
transform ooc_danger_shake:
    # x 偏移 -3 到 +3 快速抖动
```

#### 2. OOC HUD Screen（第 1708-1804 行）
```python
screen ooc_hud():
    zorder 200
    
    # 显示区域：左上角（xpos=30, ypos=30）
    # 内容包括：
    # - OOC 数值（大号黄色显示）
    # - 状态标签（中文文本）
    # - 脾谱图片（根据状态动态选择）
    # - 动画效果（根据状态动态应用）
    # - 说明文本（底部）
    
    if ooc_value >= 71:
        # 危险区：face_danger.png + 震屏
    elif ooc_value >= 31:
        # 警告区：face_warning.png + 脉动
    else:
        # 安全区：face_safe.png + 呼吸灯
```

#### 3. 脸谱状态分段
| OOC 值 | 状态 | 图片 | 动画 | 颜色 |
|--------|------|------|------|------|
| 0-30% | 安全 | face_safe.png | 呼吸灯 | 绿色 |
| 31-70% | 警告 | face_warning.png | 脉动 | 黄色 |
| 71-99% | 危险 | face_danger.png | 震屏 | 红色 |
| 100% | 崩坏 | - | Game Over | - |

---

## 📊 代码统计

| 文件 | 新增/修改行数 | 主要内容 |
|------|--------------|---------|
| script.rpy | ~100 行 | Init Python + Functions + Game Over Label |
| screens.rpy | ~90 行 | ATL Transforms + ooc_hud Screen |
| **总计** | **~190 行** | **完整的 OOC 系统** |

---

## 🎯 系统功能一览

### 核心机制
- ✅ **OOC 值跟踪**：0-100% 范围，实时显示
- ✅ **自动 Game Over**：OOC >= 100 时自动跳转
- ✅ **开挂模式**：超过 3 次开挂后 OOC 锁定在 99
- ✅ **边界保护**：自动限制范围和防止越界

### UI 显示
- ✅ **HUD 实时显示**：左上角固定显示 OOC 监控ui
- ✅ **动态脸谱**：根据 OOC 值自动切换 3 种脸谱
- ✅ **动画效果**：3 种动画（呼吸灯/脉动/震屏）
- ✅ **状态标签**：中文实时显示威胁等级

### 集成友好
- ✅ **简单的 API**：`update_ooc()` 和 `check_ooc()`
- ✅ **自动检查**：默认自动检查边界并处理 Game Over
- ✅ **灵活配置**：支持手动检查、禁用自动跳转等
- ✅ **向后兼容**：现有的 `update_ooc()` 调用无需修改

---

## 🔧 使用示例

### 基础使用

```ren'py
# 显示 HUD
show screen ooc_hud

# 增加 OOC 值（正义行为）
$ update_ooc(15)

# 减少 OOC 值（反派行为）
$ update_ooc(-8)

# 隐藏 HUD
hide screen ooc_hud
```

### 菜单整合

```ren'py
menu:
    "选项 A（人设受损）":
        $ update_ooc(20)
    
    "选项 B（人设稳固）":
        $ update_ooc(-10)
```

---

## 📁 生成的文档

1. **OOC_SYSTEM_GUIDE.md**（详细使用指南）
   - 系统概述和规则
   - API 接口详解
   - 集成步骤
   - 使用示例
   - 最佳实践

2. **OOC_QUICK_REFERENCE.md**（快速参考卡）
   - 核心变量和函数速查
   - 常用代码片段
   - 调试命令

---

## ⚠️ 需要准备的资源

在 `game/gui/` 目录下准备以下图片文件：

```
game/gui/
├── face_safe.png        (100×120, 脸谱完整)
├── face_warning.png     (100×120, 脸谱有裂纹)
├── face_danger.png      (100×120, 脸谱大面积碎裂)
└── ooc_frame.png        (140×160, HUD 框架，可选)
```

如果图片文件暂时不存在，Ren'Py 会显示占位符（不影响功能测试）。

---

## ✨ 特色设计

### 1. 视觉反馈系统
- 3 层次的脸谱图片递进式提升压迫感
- 3 种不同的动画效果强化紧张气氛
- 颜色编码（绿/黄/红）符合直觉

### 2. 灵活的交互设计
- 自动和手动检查双模式
- 开挂系统制造额外的战略压力
- 可选的自动 Game Over 机制

### 3. Ren'Py 原生开发
- 遵循 Ren'Py 最佳实践
- 使用 init python 进行初始化
- 充分利用 ATL 动画系统

---

## 🎮 游戏集成清单

- [x] Init python 块定义
- [x] check_ooc() 函数
- [x] update_ooc() 函数
- [x] game_over_ooc label
- [x] 默认变量声明
- [x] ATL 动画变换
- [x] ooc_hud screen
- [x] 脸谱条件判断
- [x] 动画效果应用
- [x] 现有代码兼容性维护
- [x] 文档完整性

---

## 📞 问题排查

### Q: OOC 值不更新？
A: 确保在菜单选项中使用 `$ update_ooc(amount)`，不要忘记 `$` 前缀。

### Q: HUD 不显示？
A: 在游戏中执行 `show screen ooc_hud`，确保脚本中有此行。

### Q: 脸谱图片显示不出来？
A: 确保图片文件存在于 `game/gui/` 目录，文件名完全匹配。

### Q: update_ooc() 不工作？
A: 确保已经过初始化（游戏启动后）。如果是在 init 块中调用，需要使用直接赋值。

---

## 🎓 推荐的下一步

1. **美术资源**：制作 3 张脸谱图片（建议使用中国传统戏曲脸谱设计）
2. **剧情集成**：在关键选择点添加 `update_ooc()` 调用
3. **难度调整**：根据测试反馈调整各选项的 OOC 增减数值
4. **结局分支**：设计多条不同 OOC 值对应的游戏结局
5. **成就系统**：可以与 OOC 值系统结合设计特殊成就

---

**实现完成！祝您的游戏开发顺利！** 🎭✨
