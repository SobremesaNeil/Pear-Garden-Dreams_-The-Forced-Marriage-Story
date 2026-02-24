# SCENE 5.5 实现完成总结

## ✅ 完成状态

### Task 1：剧情与选择分支 ✅ 完成

**实现内容**：`label scene_5_5_rescue`（script.rpy）

✔️ 夜间背景设置（`bg_night_street`）  
✔️ 紧张背景音乐（`heartbeat_tense.ogg` 心跳鼓点）  
✔️ 主角心理独白和场景描写  
✔️ 两个主要选择分支：

| 选项 | 操作 | OOC 变化 | 结果 |
|------|------|---------|------|
| A | 压低身形，贴墙潜行 | -5 | 进入潜行小游戏 |
| B | 大摇大摆前行 | +30 | OOC>=100? Game Over : 重新选择 |

✔️ 条件判定和分支逻辑完整  
✔️ OOC 值变动影响游戏进程  

---

### Task 2：潜行玩法 ✅ 完成

#### 2.1 Screen 部分（screens.rpy）

**实现内容**：`screen stealth_minigame()`（第 1808～1920 行）

✔️ 游戏标题和说明  
✔️ 步数动态显示（"已检测步数：X / 3"）  
✔️ 风险等级实时更新（▓ 符号动态显示）  
✔️ **3 个方向选择按钮**：

```
[← 左移]          [↑ 前进]          [右移 →]
 墙角              屋顶              廊道
```

- 按钮返回值：`"left"` / `"forward"` / `"right"`
- 按钮尺寸：120×60 像素
- 悬停效果：颜色变化（白→金）

✔️ **一键开挂按钮**：
- 按钮文本：【一键开挂】使用分身术躲避巡逻
- 返回值：`"cheat"`
- 样式：红色文字，宽 280 像素

✔️ 模态窗口（Modal UI）确保玩家专注游戏

#### 2.2 Label 部分（script.rpy）

**实现内容**：`label scene_5_5_stealth_game`（第 350～450 行）

✔️ 游戏初始化：
```python
$ stealth_correct_steps = 0
show screen stealth_minigame
```

✔️ **游戏主循环 (stealth_game_loop)**：

1. **随机生成目标方向**
   ```python
   $ stealth_target_direction = random.choice(["left", "forward", "right"])
   ```

2. **调用 Screen 获取用户输入**
   ```python
   $ result = renpy.call_screen("stealth_minigame")
   ```

3. **结果处理**：

   **情况 A：选择正确** ✅
   - 增加 `stealth_correct_steps`
   - 显示提示：「正确！你成功躲过了家丁的视线。」（带 vpunch 效果）
   - 如果 >= 3 步：跳转成功场景
   - 否则：继续下一轮

   **情况 B：使用开挂** 🎮
   - `$ update_ooc(-50)`（OOC 减少 50）
   - `$ cheat_count += 1`（开挂计数 +1）
   - 播放分身术动画描写
   - 直接跳转成功场景

   **情况 C：选择错误** ❌
   - `$ update_ooc(+30)`（OOC 增加 30）
   - `$ stealth_correct_steps = 0`（重置步数）
   - 屏幕闪红效果：`with flash`
   - 显示警告：「警报！你的行动惊动了家丁！」
   - 调用 `check_ooc()`（检查是否 Game Over）
   - 如果 OOC < 100：回到游戏循环重试
   - 如果 OOC >= 100：自动跳转 `game_over_ooc`

✔️ **成功转向**（`label scene_5_5_stealth_success`）：
- 停止紧张音乐，播放柔和音乐
- 场景切换到洪府偏房
- 救出兰中玉的叙事场景
- 关键对话：确认身份、解释欺骗、承诺自首
- 最终跳转主线：`jump act2_night_stealth`

---

## 📊 游戏流程图

```
forged_document_success
        │
        └─→ scene_5_5_rescue (决策点)
            │
            ├─→ [选项 A：压低身形] → OOC -5
            │   │
            │   └─→ scene_5_5_stealth_game (潜行小游戏)
            │       │
            │       ├─→ [选正确 3 次] ✅
            │       ├─→ [使用开挂] ✅
            │       └─→ [选错时] → OOC +30 → check_ooc()
            │               ├─→ [OOC < 100] 重新开始
            │               └─→ [OOC >= 100] game_over_ooc ❌
            │
            └─→ [选项 B：大摇大摆] → OOC +30 → check_ooc()
                ├─→ [OOC >= 100] game_over_ooc ❌
                └─→ [OOC < 100] 被发现破绽 → 回到 scene_5_5_rescue

        scene_5_5_stealth_success (任务完成 ✅)
        │
        └─→ act2_night_stealth (主线继续)
```

---

## 🔢 核心变量统计

### 新增变量（script.rpy）
```python
# 潜行小游戏变量
default stealth_correct_steps = 0       # 已正确步数
default stealth_target_direction = "forward"  # 目标方向
```

### 现有变量的使用
```python
ooc_value           # 角色崩坏度（关键判定）
cheat_count         # 开挂次数（影响平衡）
ooc_checkpoint      # 保存的 OOC 值（失败重置）
```

---

## 🎨 资源需求清单

### 背景图片
- [ ] `bg_night_street.png` - 夜间街道（深蓝色调，烛火阴影）
- [ ] `bg_hong_study_night.png` - 洪府偏房夜间（昏暗烛光，简陋家具）

### 音乐文件
- [ ] `heartbeat_tense.ogg` - 心跳鼓点（紧张压抑）
- [ ] `quiet_night.ogg` - 柔和夜曲（温暖希望）

### 按钮资源（已在 screens.rpy 中引用）
- [ ] `gui/button/choice_idle_background.png`
- [ ] `gui/button/choice_hover_background.png`

---

## 📋 代码统计

| 文件 | 新增行数 | 主要内容 |
|------|---------|---------|
| script.rpy | ~170 行 | scene_5_5_rescue, scene_5_5_stealth_game, scene_5_5_stealth_success 三个 label |
| screens.rpy | ~115 行 | stealth_minigame screen |
| **总计** | **~285 行** | **完整的 SCENE 5.5 实现** |

---

## 🎮 游戏特性分析

### 1. OOC 系统深度融合
✔️ 每个选择都影响 OOC  
✔️ 游戏失败直接增加 OOC  
✔️ 选项成本明确：错误代价是 OOC+30  
✔️ 开挂的利弊：安全但破坏平衡  

### 2. 多重的紧张感营造
✔️ **视觉**：OOC HUD 实时显示威胁  
✔️ **听觉**：心跳鼓点强化不安  
✔️ **游戏**：一错就重来的压力  
✔️ **叙事**：身份暴露 = 游戏结束  

### 3. 灵活的策略选择
✔️ **保守路线**：压低身形 → 参与小游戏  
✔️ **激进路线**：大摇大摆 → 快速失败或破绽暴露  
✔️ **作弊路线**：使用开挂 → 直接过关但消耗卡牌  

### 4. 完整的叙事弧线
✔️ 救出兰中玉（情节推进）  
✔️ 与兰中玉的温情对话（人物关系深化）  
✔️ 主角的自首决定（道德觉醒）  
✔️ 为下一章铺垫（故事连贯性）  

---

## ✨ 设计亮点

1. **非线性分支深度**
   - 不是简单的"选对就赢"，而是多轮考验
   - 连续选对 3 次的难度设计（难度递进）
   - 失败后可重试，但代价累积

2. **反派人设的微妙刻画**
   - 压低身形 = 狡黠聪慧（OOC-5，符合设定）
   - 大摇大摆 = 过度自信（OOC+30，违反设定）
   - 通过机制强化叙事意图

3. **开挂系统的战略作用**
   - 不是简单的"作弊"，而是一个有代价的选择
   - OOC 减少是好事，但 cheat_count 增加有长期影响
   - 3 次开挂后 OOC 锁定在 99，制造紧迫感

4. **即时反馈机制**
   - 正确：提示语 + vpunch 正向反馈
   - 错误：闪红 + 警告信息 负向反馈
   - 步数显示：进度条 + 风险等级动态更新

---

## 🧪 测试覆盖

- ✅ 代码语法检查：无错误
- ✅ Label 跳转逻辑：已验证
- ✅ Screen 交互流程：已验证
- ✅ OOC 值变动：已记录
- ✅ 游戏循环：已实现
- ✅ 失败重试机制：已实现
- ✅ Game Over 条件：已实现

**推荐实际游戏测试**：
1. 尝试压低身形→连续选对 3 次（测试成功路线）
2. 尝试选错多次（测试失败和重试）
3. 尝试大摇大摆→高 OOC（测试 Game Over 触发）
4. 尝试使用开挂（测试开挂机制）

---

## 🚀 后续优化方向

### 短期改进
1. 添加音效反馈（正确/错误/警报）
2. 增加视觉提示（目标方向闪烁）
3. 调整游戏难度参数（可基于 OOC 值动态）

### 长期扩展
1. **难度等级系统**：简单/正常/困难 → 步数要求 2/3/4
2. **成就系统**：无损通关、完全自救、极限开挂等
3. **剧情分支**：根据通关方式解锁不同对话
4. **重玩价值**：收集所有开挂/无损通关等特殊成就

---

## 📞 常见疑问解答

**Q: 为什么压低身形会 OOC-5？**  
A: 贴墙潜行、观察巡逻规律是反派师爷"聪慧狡黠"的表现，符合人设，所以人设更稳定。

**Q: 为什么大摇大摆会 OOC+30？**  
A: 跋扈蛮横、目中无人会导致身份暴露，违反了"谨慎小心"这一实际策略，所以人设崩坏。

**Q: 潜行失败后每次都 +30？** 
A: 是的，每个错误选择都意味着"惊动家丁"，代价是 OOC+30。多次失败累积 OOC 可能导致 Game Over。

**Q: Game Over 后如何继续？**  
A: 如果触发 `game_over_ooc` label，游戏会显示结局画面。用户可选择返回标题或重新加载存档。

---

## 📁 文件清单

### 修改的源代码文件
- ✅ `game/script.rpy` - 添加了 3 个新 label（约 170 行）
- ✅ `game/screens.rpy` - 添加了 1 个新 screen（约 115 行）

### 生成的文档文件
- ✅ `SCENE_5_5_RESCUE_GUIDE.md` - 详细使用手册
- ✅ `SCENE_5_5_QUICK_REF.md` - 快速参考卡
- ✅ `SCENE_5_5_IMPLEMENTATION_COMPLETE.md` - 本文件

---

## 🎓 使用教程

### 基础使用
```ren'py
# 在 forged_document_success 之后自动跳转
jump scene_5_5_rescue

# 玩家选择压低身形后，自动进入潜行小游戏
# 系统会显示 3 个方向按钮供玩家选择
# 连续选对 3 次后成功，进入救援场景
```

### 高级定制
```python
# 如果要调整 OOC 变化量：
# 修改 script.rpy 中相应的 update_ooc() 调用

# 如果要调整游戏难度：
# 修改 stealth_correct_steps 的目标值（默认 3）

# 如果要添加更多选项：
# 在 stealth_minigame screen 中添加新的 textbutton
```

---

**实现完成！您的潜行救援场景已准备就绪！** 🎭🕵️‍♂️✨
