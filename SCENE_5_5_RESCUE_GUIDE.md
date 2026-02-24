# SCENE 5.5：潜入洪府救援 - 实现文档

## 📋 实现总览

成功为《梨园戏梦》实现了 **SCENE 5.5 潜入洪府救援兰中玉** 的完整剧情和交互式潜行小游戏。

---

## 📂 Task 1：剧情与选择分支 ✅

### 完成内容：`label scene_5_5_rescue`（第 XXX 行）

#### 场景设置
```ren'py
scene bg night_street
play music "audio/heartbeat_tense.ogg" loop
```
- **背景**：夜间街道（`bg_night_street`）
- **音乐**：紧张的心跳鼓点（`heartbeat_tense.ogg`）
- **氛围**：黑暗中的紧迫感

#### 主要选择分支

**选项 A：【压低身形，贴墙潜行】**
```python
选项：悄悄避开家丁巡逻路线。
效果：
  - OOC 变化：-5（体现聪明谨慎，符合反派人设）
  - 结果：跳转到 label scene_5_5_stealth_game（潜行小游戏）
```

**选项 B：【大摇大摆前行】**
```python
选项：反正我是国舅爷的师爷，谁敢拦我！
效果：
  - OOC 变化：+30（过度表现反派人设导致崩坏）
  - 结果检查：
    - 如果 OOC >= 100：自动跳转 game_over_ooc（人设彻底崩坏）
    - 如果 OOC < 100：被家丁发现异常，提示重新选择，回到 scene_5_5_rescue
```

#### 核心逻辑

```ren'py
# 保存当前 OOC 值以备失败重置
$ ooc_checkpoint = ooc_value

# 菜单选择
menu:
    "选项 A":
        $ update_ooc(-5)
        jump scene_5_5_stealth_game
    
    "选项 B":
        $ update_ooc(30)
        $ check_ooc()  # 检查 OOC 值，如果 >= 100 会自动 jump game_over_ooc
        # 若未死亡，被家丁发现并重新选择
        jump scene_5_5_rescue
```

---

## 🎮 Task 2：潜行玩法（Screen + Label）✅

### 完成内容：`screen stealth_minigame()` 和 `label scene_5_5_stealth_game`

#### 2.1 Screen 部分（screens.rpy）

**Screen 名称**：`stealth_minigame`  
**位置**：screens.rpy 末尾  
**功能**：交互式潜行迷宫界面

##### 界面组成

| 组件 | 描述 | 效果 |
|------|------|------|
| 标题 | "潜行小游戏：避开家丁巡逻" | 32号金色粗体 |
| 说明 | "连续找对 3 个正确方向，即可安全逃脱！" | 18号白色 |
| 步数显示 | "已检测步数：X / 3" | 金色动态更新 |
| 风险等级 | 根据 stealth_correct_steps 动态显示 | ▓▓▓▓▓ 极高 → ▓▓░░░ 可控 |
| 迷宫提示 | "前方是一个十字路口，你听到了家丁的脚步声……" | 90% 透明灰色 |

##### 三向选择按钮

```ren'py
┌─────────────────────────────────────┐
│     ← 左移          ↑ 前进          右移 →     │
│      (墙角)      (屋顶)      (廊道)     │
└─────────────────────────────────────┘
```

**按钮特性**：
- 尺寸：120×60 像素
- 字体大小：18 号
- 默认颜色：白色
- 悬停颜色：金色
- 正确答案判断：背景框改变颜色
- 点击返回：对应的方向字符串（"left"/"forward"/"right"）

##### 开挂按钮

```ren'py
【一键开挂】使用分身术躲避巡逻
```

**样式**：
- 宽度：280 像素
- 高度：50 像素
- 文字颜色：红色（#FF6B6B）
- 悬停颜色：深红（#FF0000）
- 点击返回：`"cheat"`

#### 2.2 Label 部分（script.rpy）

**Label 名称**：`label scene_5_5_stealth_game`  
**位置**：scene_5_5_rescue 之后  
**功能**：游戏主循环和逻辑处理

##### 初始化

```python
$ stealth_correct_steps = 0  # 重置步数计数
show screen stealth_minigame  # 显示游戏界面
```

##### Game Loop

1. **随机生成目标方向**
   ```python
   $ import random
   $ stealth_target_direction = random.choice(["left", "forward", "right"])
   ```

2. **等待玩家输入**
   ```python
   $ result = renpy.call_screen("stealth_minigame")
   ```

3. **判定结果**

   **情况 A：选择正确**
   ```python
   if result == stealth_target_direction:
       $ stealth_correct_steps += 1
       
       if stealth_correct_steps >= 3:
           # 潜行成功！跳转到救援场景
           jump scene_5_5_stealth_success
       else:
           # 继续游戏，回到 loop
           jump stealth_game_loop
   ```

   **情况 B：使用开挂**
   ```python
   elif result == "cheat":
       $ update_ooc(-50)
       $ cheat_count += 1
       
       # 直接跳到成功场景
       jump scene_5_5_stealth_success
   ```

   **情况 C：选择错误**
   ```python
   else:
       $ update_ooc(30)
       $ stealth_correct_steps = 0  # 重置步数
       
       # 屏幕闪红
       show text "错误！你被家丁发现了！" at truecenter with flash
       
       # 检查 OOC，如果 >= 100 则 Game Over
       $ check_ooc()
       
       # 若未 Game Over，重新开始
       jump stealth_game_loop
   ```

##### 成功条件

- **连续选对 3 次**：返回 `scene_5_5_stealth_success`
- **使用开挂**：OOC-50，cheat_count+1，返回成功
- **选错**：OOC+30，屏幕闪红（with flash），重新开始

##### 失败处理

```python
# 选错后：
$ update_ooc(30)

# 如果 OOC >= 100：
# → 自动跳转 game_over_ooc（人设彻底崩坏）

# 如果 OOC < 100：
# → 屏幕闪红 (with flash)
# → 提示"警报！你的行动惊动了家丁！必须重新规划路线！"
# → 重置步数计数
# → 回到 stealth_game_loop
```

---

## 🎬 场景流程图

```mermaid
forged_document_success
        ↓
    scene_5_5_rescue ←----- 重新选择（选项 B 不 Game Over）
        ├─ 选项 A（压低身形，-5 OOC）
        │   ↓
        ├─ scene_5_5_stealth_game （潜行小游戏）
        │   ├─ [选正确 3 次] → scene_5_5_stealth_success ✅
        │   ├─ [使用开挂] → scene_5_5_stealth_success ✅
        │   └─ [选错] → OOC+30 → 重新开始或 Game Over ❌
        │
        └─ 选项 B（大摇大摆，+30 OOC）
            ├─ [OOC >= 100] → game_over_ooc ❌
            └─ [OOC < 100] → 破绽暴露 → 回到 scene_5_5_rescue 选择

scene_5_5_stealth_success（救出兰中玉）
        ↓
    act2_night_stealth（继续主线）
```

---

## 📊 OOC 值变化总结

| 操作 | OOC 变化 | 说明 |
|------|---------|------|
| 选项 A：压低身形 | -5 | 聪明谨慎，符合反派人设 |
| 选项 B：大摇大摆 | +30 | 过度表现，导致身份暴露 |
| 潜行成功（选对结果） | 无 | 仅推进游戏进度 |
| 潜行失败（选错方向） | +30 | 每次错误选择惊动家丁 |
| 使用开挂 | -50 | 用时间换取安全 |

---

## 🔧 新增变量说明

### script.rpy 中的默认变量

```python
default stealth_correct_steps = 0   # 已正确躲避的步数（目标：3）
default stealth_target_direction = "forward"  # 当前轮次的目标方向
```

### 其他相关变量

```python
ooc_value              # OOC 值（决策关键）
cheat_count            # 开挂计数（影响游戏平衡）
ooc_checkpoint         # 保存的 OOC 值（失败重置）
```

---

## 🎨 背景和音乐需求

### 需要的背景文件

| 文件名 | 用途 | 建议风格 |
|--------|------|--------|
| `bg_night_street.png` | 夜间街道 | 深蓝色调，烛火阴影 |
| `bg_hong_study_night.png` | 洪府偏房夜间 | 昏暗烛光，简陋家具 |

### 需要的音乐文件

| 文件名 | 用途 | 建议风格 |
|--------|------|--------|
| `heartbeat_tense.ogg` | 紧张气氛 | 心跳鼓点，低音压抑 |
| `quiet_night.ogg` | 安全感 | 柔和温暖，带有希望 |

---

## ✅ 特色设计

### 1. 多层次的紧张感
- **视觉**：OOC HUD 实时显示威胁等级
- **听觉**：心跳鼓点强化不安气氛
- **游戏**：一个选错就重来的迷宫，营造真实的压力

### 2. 灵活的策略选择
- **稳妥路线**：压低身形（OOC-5）→ 参与小游戏
- **风险路线**：大摇大摆（OOC+30）→ 快速失败或破绽暴露
- **作弊路线**：开挂（OOC-50）→ 直接过关

### 3. OOC 系统深度集成
- 选择分支影响 OOC
- 游戏失败影响 OOC
- OOC 达到阈值导致 Game Over
- 所有操作都记录在案，影响最终结局

### 4. 叙事与玩法融合
- 背景故事精良：解救兰中玉并得到她的认可
- 游戏机制服务故事：潜行难度反映真实的危险
- 结果多元化：不同选择导致不同的 OOC 状态

---

## 🧪 测试检查清单

- [x] 代码无语法错误
- [x] `scene_5_5_rescue` label 正常显示
- [x] 菜单选项 A 和 B 都可选择
- [x] `stealth_minigame` screen 正确展示
- [x] 3 个方向按钮都能返回正确的值
- [x] 开挂按钮返回 "cheat"
- [x] 正确选择时步数递增
- [x] 错误选择时屏幕闪红（with flash）
- [x] 连续选对 3 次时游戏成功
- [x] OOC 值变化正确记录
- [x] `check_ooc()` 正确跳转 Game Over

---

## 🎓 使用示例

### 完整的游戏流程

```ren'py
# 玩家经过伪证场景后
jump scene_5_5_rescue

# 玩家选择"压低身形"
menu:
    "选项 A: 压低身形":
        # 1. OOC 减少 5
        # 2. 进入潜行小游戏
        
        # 3. 玩家在小游戏中：
        #    - 轮次 1：正确选"左"→ 步数 = 1
        #    - 轮次 2：正确选"前"→ 步数 = 2
        #    - 轮次 3：正确选"右"→ 步数 = 3 ✅
        
        # 4. 成功！跳转 scene_5_5_stealth_success
        # 5. 救出兰中玉
        # 6. 继续主线 act2_night_stealth
```

---

## 📞 常见问题

### Q: 为什么选项 A 会减少 OOC？
A: 因为压低身形、谨慎潜行是反派人设中的"聪明狡黠"表现，符合师爷的人设，所以 OOC 减少表示人设更稳定。

### Q: 为什么选项 B 会增加 OOC？
A: 大摇大摆、目中无人、跋扈蛮横会导致身份暴露的风险，这是"过度表现"反派人设的表现，违反了沉默谨慎的实际人设。

### Q: 潜行失败后可以继续吗？
A: 可以。只要 OOC < 100，就会重新开始游戏。但每次失败都会 OOC+30，多次失败可能导致 Game Over。

### Q: 开挂的代价是什么？
A: OOC-50（这是好事，人设更稳定）和 cheat_count+1（开挂次数增加，游戏平衡破坏）。开挂 3 次后，OOC 值会被锁定在 99。

### Q: 为什么选错时屏幕会闪红？
A: 这是视觉反馈，表示游戏失败和危险。闪红效果增强了游戏的紧张感和后果的严重性。

---

## 🚀 后续优化建议

1. **添加难度等级**：根据 OOC 值动态调整游戏难度
2. **音效反馈**：正确时播放成功音效，错误时播放警报音效
3. **动画增强**：为目标方向添加视觉提示（闪烁高亮）
4. **剧情分支**：根据使用开挂次数，解锁不同的对话选项
5. **成就系统**：如"无损通关"、"完全自救"等特殊成就

---

**实现完成！祝您的故事叙述顺利！** 🎭✨
