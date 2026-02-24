# OOC 系统快速参考

## 核心变量

```python
# script.rpy - 默认值
default ooc_value = 20              # 角色崩坏度（0-100）
default cheat_count = 0             # 开挂次数
default qte_fail_count = 0          # QTE 失败次数
```

## 核心函数

```python
# 检查 OOC 值（自动 Game Over）
$ check_ooc()

# 更新 OOC 值（推荐方式）
$ update_ooc(10)        # 增加 10%
$ update_ooc(-5)        # 减少 5%
$ update_ooc(20, auto_check=False)  # 不自动检查
```

## HUD 控制

```python
# 显示 OOC 监控界面
show screen ooc_hud

# 隐藏 OOC 监控界面
hide screen ooc_hud
```

## 动画效果

```python
# ATL Transform（可用于其他元素）
at ooc_safe_breathing    # 安全区：微弱呼吸灯
at ooc_warning_pulse     # 警告区：警告脉动
at ooc_danger_shake      # 危险区：震屏效果
```

## 状态分界

```python
if ooc_value >= 100:
    # 已被 check_ooc() 自动处理，会 jump 到 game_over_ooc
    pass

elif ooc_value >= 71:
    # 危险区：face_danger.png + 震屏
    pass

elif ooc_value >= 31:
    # 警告区：face_warning.png + 脉动
    pass

else:
    # 安全区：face_safe.png + 呼吸灯
    pass
```

## Game Over Label

```python
label game_over_ooc:
    """自动触发，人设彻底崩坏"""
    scene bg black with fade
    # ... 结局演出 ...
    return
```

## 常用场景代码

### 道德选择菜单

```ren'py
menu:
    "正义选项（人设受损）":
        $ update_ooc(15)
        # ... 内容 ...
    
    "反派选项（人设稳固）":
        $ update_ooc(-10)
        # ... 内容 ...
```

### 暗地里做善事

```python
if ooc_value < 50:
    $ update_ooc(5)  # 轻微影响
    me "没人看到，应该没事……"
```

### 使用开挂

```python
$ cheat_count += 1
if cheat_count >= 3:
    me "开挂过度，游戏平衡被破坏……"
```

## 文件位置

| 文件 | 修改内容 |
|------|---------|
| `game/script.rpy` | init python + variables + game_over_ooc label |
| `game/screens.rpy` | Transforms + ooc_hud screen |
| `game/gui/` | face_safe.png, face_warning.png, face_danger.png |

## 调试命令

```python
$ ooc_value = 25   # 直接设置（调试用）
$ check_ooc()      # 手动检查
$ print(ooc_value)  # 控制台输出（Ren'Py 控制台）
```

---

**更详细的使用说明，请参考 `OOC_SYSTEM_GUIDE.md`**
