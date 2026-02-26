# 游戏的脚本可置于此文件中。

################################################################################
## 初始化阶段：OOC 系统核心设置
################################################################################
define me = Character("我", image="me")
init python:
    """
    OOC（Out of Character，角色崩坏度）系统
    量化系统用于监控主角在"反派人设"中的表现
    - 低 OOC：维持反派人设，安全状态
    - 高 OOC（>=100）：人设彻底崩坏，Game Over
    """
    
    def check_ooc():
        """
        检查并处理 OOC 值的边界条件
        在每次 OOC 值变动后调用此函数
        """
        global ooc_value
        
        # 限制 ooc_value 在 0-100 范围内
        ooc_value = max(0, min(100, ooc_value))
        
        # 如果 OOC 值达到 100%，触发 Game Over
        if ooc_value >= 100:
            renpy.jump("game_over_ooc")
        
        return ooc_value
    
    def update_ooc(amount, auto_check=True):
        """
        更新 OOC 值
        
        Args:
            amount: 增减量（正数增加，负数减少）
            auto_check: 是否自动调用 check_ooc 进行检查
        
        Returns:
            更新后的 ooc_value
        """
        global ooc_value, cheat_count
        
        # 强制开挂模式：使用开挂 3 次后，OOC 值锁定在 99
        if cheat_count >= 3:
            ooc_value = 99
            return ooc_value
        
        # 正常模式：按照 amount 更新
        ooc_value = ooc_value + amount
        
        # 自动检查并限制范围
        if auto_check:
            check_ooc()
        else:
            ooc_value = max(0, min(100, ooc_value))
        
        return ooc_value

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define me = Character("贾斯文", color="#808080")
define lian = Character("小莲", color="#FF69B4")
define hong = Character("洪彦龙", color="#8B0000")
define zhang = Character("张清", color="#228B22")
define lan = Character("兰中玉", color="#4682B4")
define servant_a = Character("家丁甲", color="#696969")
define servant_b = Character("家丁乙", color="#696969")
define servant_c = Character("家丁丙", color="#696969")
define servant_d = Character("家丁丁", color="#696969")

# 特效定义：闪白转场（用于精神暴击时刻）
define flash = Fade(0.1, 0.0, 0.5, color="#fff")

# 音效定义：值不帜打击感
define sfx_gavel = "audio/gavel.mp3"
define sfx_gong = "audio/gong.mp3"

################################################################################
## 核心游戏变量
################################################################################

# OOC 系统变量
default ooc_value = 20              # 角色崩坏度，初始值 20%（相对安全）
default cheat_count = 0             # 使用"一键开挂"的次数
default qte_fail_count = 0          # QTE（快速反应时间）失败次数

# 潜行小游戏变量
default stealth_correct_steps = 0   # 已正确躲避的步数（目标：连续 3 步）
default stealth_target_direction = "forward"  # 当前轮次的正确方向

# DWRG 节奏审判变量
default dwrg_time_remaining = 5.0   # 剩余时间
default dwrg_pointer_pos = 0.0      # 指针位置（0.0-1.0，左到右）
default dwrg_success_threshold = (0.3, 0.7)  # 绿色安全区范围（30%-70%）
default dwrg_attempt_count = 0      # QTE 尝试次数
default dwrg_auto_hit_uses = 0      # DWRG 一键开挂的使用次数（限额 3 次）

################################################################################
## 初始化三大小游戏系统
################################################################################

init python:
    from minigames import (
        PuzzleGame, PuzzleFragment,
        StrokeTracker, StrokeCheckpoint,
        NinePuzzleGame
    )
    
    # 全局小游戏实例（根据需要创建）
    puzzle_game = None
    stroke_tracker = None
    nine_puzzle_game = None
    
    def init_puzzle_game():
        """初始化脸谱复原小游戏"""
        global puzzle_game
        puzzle_game = PuzzleGame(num_fragments=5)
        
        # 添加碎片
        # 【需要替换为实际的图片路径】
        fragment_configs = [
            (0, "images/puzzle_fragment_1.png", 400, 250, 20),  # id, 路径, 目标X, 目标Y, 容差
            (1, "images/puzzle_fragment_2.png", 420, 240, 20),
            (2, "images/puzzle_fragment_3.png", 410, 270, 20),
            (3, "images/puzzle_fragment_4.png", 390, 260, 20),
            (4, "images/puzzle_fragment_5.png", 410, 250, 20),
        ]
        
        for frag_id, path, target_x, target_y, tolerance in fragment_configs:
            frag = PuzzleFragment(frag_id, path, target_x, target_y, tolerance)
            puzzle_game.add_fragment(frag)
        
        return puzzle_game
    
    def init_stroke_tracker():
        """初始化描红笔画追踪系统"""
        global stroke_tracker
        
        # 定义"婚"字的笔画检查点（需要根据实际调整坐标）
        # 格式：(检查点ID, X坐标, Y坐标, 触发半径)
        checkpoints = [
            (0, 300, 200, 15),  # 第一笔起点
            (1, 300, 250, 15),  # 第二笔
            (2, 350, 250, 15),  # 第三笔
            (3, 350, 200, 15),  # 第四笔
            (4, 400, 225, 15),  # 第五笔
        ]
        
        stroke_tracker = StrokeTracker(
            checkpoints_data=checkpoints,
            time_limit=10.0,
            bg_image="images/hui_character.png"  # 【需要替换为"婚"字背景图】
        )
        
        return stroke_tracker
    
    def init_nine_puzzle():
        """初始化九宫格一笔画小游戏"""
        global nine_puzzle_game
        nine_puzzle_game = NinePuzzleGame()
        # 可选：自定义危险路线
        # nine_puzzle_game.dangerous_edges = set([(0, 2), (6, 8)])
        return nine_puzzle_game


# 游戏在此开始。

label start:
    
    # ========================================
    # 全局背景音乐：主题曲
    # ========================================
    # 在游戏起点播放主题音乐，并持续循环至游戏结束
    play music "audio/main_theme.mp3" fadein 2.0
    
    # ========================================
    # 序章：破败小屋的光影演出
    # ========================================
    # 场景设置：初始背景为普通光线的破败小屋
    scene bg broken_cottage with dissolve
    
    # 出现小莲，病态的样子
    show lian sick at center
    
    me "小莲，我给你带来了白面窝头。"
    
    # ========================================
    # 道具特写 1：温情与辛酸（白面窝头）
    # ========================================
    # 在阳光下悬浮展示的窝头，象征主角对妹妹的关切
    show prop_bun at truecenter with dissolve
    
    pause 1.5
    
    me "虽然不多，但这是我能找到的最好的。"
    
    lian "咳咳……谢谢你……"
    
    lian "你为我做了这么多……我真是……"
    
    # 窝头的任务已完成，收起特写
    hide prop_bun with dissolve
    
    # ========================================
    # 光影转折点：戏剧高潮
    # ========================================
    # 小莲剧烈咳嗽 - 此刻阳光通过窗户倾泻而入
    lian "咳咳咳！"
    
    # 【光影转折】
    # 切换背景：普通小屋 → 阳光照亮的小屋
    scene bg broken_cottage_sun with dissolve
    
    # ========================================
    # 道具特写 2：惊瞳与刺痛（带血手帕）
    # ========================================
    # 极其短促的过渡（0.2秒）模拟主角视觉上的冲击与心头一震
    show prop_handkerchief at truecenter with Dissolve(0.2)
    with hpunch  # 配合左右剧烈晃动，强化惊骇感
    
    pause 0.5
    
    # 时光流逝的旁白，强化光线与现实苦难的对比
    me "刺眼的阳光忽然透过窗户倾泻进来，照在她苍白的脸庞上。"
    
    me "那光线本该温暖，却只映照出她病态的虚弱和眼中的绝望。"
    
    # 血色细节：强化视觉冲击
    lian "咳……"
    
    # 血手帕被阳光照亮，产生刺目的视觉对比
    me "她用手绢捂住嘴，手绢上的血迹在阳光下闪闪发光……"
    
    # 收起手帕特写，回到标准画面
    hide prop_handkerchief with dissolve
    
    me "那是一种讽刺的美：希望之光洒在绝望之上。"
    
    me "小莲！"
    
    # 主角内心独白 - 配合阳光的意象
    me "只要能救小莲……做什么都行。"
    
    me "即使这残酷的阳光也见证了我的决心：无论如何，都要拯救她。"
    
    # 内心最深的承诺
    me "就算搭上我的命，我也在所不惜。"
    
    # ========================================
    # 【戏班后台】定格动画演出
    # 8张背景图 + 8句台词的完美咬合
    # ========================================
    
    # 镜头 1：主角睁眼的瞬间
    scene bg backstage_1 with dissolve
    
    me "啊……"
    
    # 镜头 2：手指刺痛的感受
    scene bg backstage_2 with Dissolve(0.2)
    
    me "手指被扎破了……"
    
    # 镜头 3：血滴在古籍上
    scene bg backstage_3 with Dissolve(0.2)
    
    me "血滴在了这本古籍上……"
    
    # ========================================
    # 道具特写 3：命运转折（线状血书）
    # ========================================
    # 这是穿越前的终极悬念，使用深邃缓慢的过渡（1.5秒）
    show prop_book at truecenter with Dissolve(1.5)
    
    # 定格在书上 1.5-2 秒，让玩家感受到命运转折的沉重感
    pause 2.0
    
    # 镜头 4：主角环顾四周，逐渐清醒
    scene bg backstage_4 with Dissolve(0.2)
    
    # 血书随着背景切换而隐没，过渡到穿越后的陌生世界
    hide prop_book with dissolve
    
    me "等等……这里是……？"
    
    # 显示 ooc_hud 系统界面
    show screen ooc_hud
    
    # 镜头 5：主角意识到周围的异样
    scene bg backstage_5 with Dissolve(0.2)
    
    me "这是……什么地方……"
    
    # 镜头 6：主角看向舞台方向，感到陌生
    scene bg backstage_6 with Dissolve(0.2)
    
    me "为什么我会在这里？"
    
    # 镜头 7：时空扭曲的感觉开始侵袭
    scene bg backstage_7 with Dissolve(0.2)
    
    me "这一切……太奇怪了……"
    
    # 镜头 8：最后的意识消散
    scene bg backstage_8 with Dissolve(0.2)
    
    me "眼前突然一黑……"
    
    # 场景切换到穿越后的世界（可自定义背景）
    scene bg ancient_world
    
    me "这里是……哪里？"
    
    # 进入虚空，复原脸谱的小游戏环节
    me "眼前是一片虚无的空间……"
    
    me "我需要复原被碎裂的脸谱……"
    
    # ========================================
    # 小游戏状态锁定 (脸谱复原)
    # ========================================
    # 防止玩家在小游戏中使用 Skip(快进)、Rollback(回滚)、Menu(菜单)
    $ renpy.block_rollback()      # 阻止滚轮强制回退
    $ _skipping = False           # 禁用快进功能
    $ _rollback = False           # 禁用回滚功能
    $ _game_menu_screen = None    # 禁用右键/ESC菜单
    
    # 初始化并调用脸谱复原小游戏
    $ init_puzzle_game()
    $ puzzle_result = renpy.call_screen("puzzle_restoration")
    
    if puzzle_result == "success":
        # ========== 成功完成 ==========
        $ update_ooc(-20)
        me "我深吸一口气，开始仔细地拼合每一个碎片……"
        me "一点一点地，脸谱在我手中慢慢复原了……"
        
        # ========================================
        # 高光时刻：入戏与灵魂夺舍
        # ========================================
        # 死寂与悬念：最后一笔油彩的铺垫
        pause 1.0
        me "我拿起画笔，勾勒下眼角最后一抹油彩……"
        
        pause 1.5
        
        # 铜镜骤现：化完妆的贾斯文极其缓慢、深邃地浮现
        # 模拟镜子里倒影的诡异感
        show jia_siwen at truecenter with Dissolve(1.5)
        with vpunch  # 灵魂被角色吞噬的战栗感
        
        pause 1.0
        
        # 文本咬合：极其有力量的定场台词
        me "镜子里的人，不再是懦弱的沈怀瑾。"
        me "而是相府里满腹坏水、只手遮天的丑角师爷——贾斯文。"
        
        pause 1.5
        
        # 转场离去：制造极其压抑的对视后，切黑
        scene black with Dissolve(1.0)
    
    elif puzzle_result == "cheat":
        # ========== 一键开挂 ==========
        $ update_ooc(-20)
        $ cheat_count += 1
        me "算了，我直接跳过这个步骤……"
        me "以某种不可思议的力量，碎片在瞬间复原了。"
        
        # 开挂分支也加入化身时刻，但更显突兀
        pause 0.8
        me "我拿起镜子……"
        
        pause 1.0
        show jia_siwen at truecenter with flash  # 用flash制造闪电式入戏
        
        pause 0.8
        me "镜子里的人已经不是我。那是贾斯文。"
        
        pause 1.0
        scene black with Dissolve(1.0)
    
    # ========================================
    # 小游戏状态解锁 (脸谱复原完成)
    # ========================================
    $ _skipping = True                # 恢复快进功能
    $ _rollback = True                # 恢复回滚功能
    $ _game_menu_screen = "save"      # 恢复菜单功能
    
    # 系统提示
    me "「系统」脸谱已复原。"
    me "「系统」正式进入第一幕……"
    
    # 此处为序章结尾
    return

# 第一幕：洪家大宅
label act1_hong_mansion:
    
    # 保存当前 ooc_value，用于 game_over 重置
    $ ooc_checkpoint = ooc_value
    
    # 场景：洪家大宅，洪彦龙面前
    scene bg hong_mansion
    
    show hong angry at center
    
    # 洪彦龙咆哮
    hong "你这个下等人！竟敢……"
    
    hong "你知道你在做什么吗？"
    
    me "……"
    
    # 主角的选择
    menu:
        "　(A) 「卑微叩首」连忙跪地道歉":
            $ update_ooc(-10)
            me "对……对不起！我知道错了！"
            me "请您饶恕我这一次……"
            hong "哼。算你有眼力见。"
            jump scene_2_messenger_montage
        
        "　(B) 「挺直腰板，危险」抬起头，与他对视":
            $ update_ooc(25)
            me "我……我没有做错什么！"
            hong "你说什么呢？你敢对我顶嘴？"
            
            # B的二次选择
            menu:
                "　(B1) 「继续争辩」毫不退缩地辩论":
                    $ update_ooc(75)
                    me "就是这样！我要说出来！"
                    me "你不能这样对……"
                    hong "你找死！"
                    jump game_over
                
                "　(B2) 「紧急求饶」意识到危险，立即低眉顺眼":
                    $ update_ooc(-10)
                    me "我……我说错了，对不起……"
                    hong "哼，这样才对。"
                    jump scene_2_messenger_montage

# 游戏结束标签
label game_over:
    
    # 隐藏所有画面和 UI
    hide screen ooc_hud
    hide eileen
    hide lian
    hide hong
    hide zhang
    
    # 黑屏
    scene bg black
    
    # 播放碎锣音效
    # play sound "audio/crash_gong.ogg"
    
    # 显示 Game Over 文本
    show text "Game Over：戏碎人亡" at truecenter with dissolve
    
    # 停留 3 秒
    pause 3.0
    
    # 隐藏文本
    hide text
    
    # 重置 ooc_value 为保存的状态
    $ ooc_value = ooc_checkpoint
    
    # 返回到洪彦龙咆哮前的场景
    jump act1_hong_mansion

################################################################################
## SCENE 2：洪府书房 - 连环急报蒙太奇
################################################################################

label scene_2_messenger_montage:
    """
    电影级演出：连环急报蒙太奇
    利用 5 张背景图（bg_hong_study_1 到 bg_hong_study_5）展现洪彦龙的怒火层层叠加。
    每张图里都有不同衣着的仆人在跪地禀报。
    节奏越来越快，最后以主角（贾斯文）的登场献计收尾。
    """
    
    # ========================================
    # 镜头 1：家丁甲 - 第一个坏消息（慌张）
    # ========================================
    scene bg hong_study_1 with dissolve
    
    # 画外音：快速脚步声
    # play sound "audio/footsteps_rushed.ogg"
    
    servant_a "大……大人！不好了！"
    servant_a "那个女人……那个兰中玉……她……她反抗了！"
    servant_a "我们按照您的吩咐，去让她吃饭，她……她直接把饭碗摔了！"
    servant_a "还骂我们是'下等奴才'，说要……要告官！"
    
    # 短暂停顿，等待反应
    pause 1.0
    
    # ========================================
    # 镜头 2：家丁乙 - 升级的坏消息（快速切换）
    # ========================================
    scene bg hong_study_2 with Dissolve(0.2)
    
    # 快速的脚步声和门撞击音
    # play sound "audio/footsteps_faster.ogg"
    
    servant_b "大人！情况更糟了！"
    servant_b "那女人跑到后花园去了！我们想控制住她，她……她挠伤了我三个人！"
    servant_b "她还大喊大叫，说什么'这是强占民女'、'洪彦龙是恶棍'……"
    servant_b "邻居都听到了！这必然要传出去啊！"
    
    # 快速积累压力
    pause 0.8
    
    # ========================================
    # 镜头 3：家丁丙 - 彻底的失控（配合 hpunch 横向冲击）
    # ========================================
    scene bg hong_study_3 with hpunch
    
    # 狂乱的脚步和喘息
    # play sound "audio/panic_breathing.ogg"
    
    servant_c "大……大人！她……她逃出府了！！！"
    servant_c "就在刚才，她趁我们不注意，从侧门冲了出去！"
    servant_c "现在她在大街上！衣衫褴褛，边走边骂……"
    servant_c "在喊什么'洪彦龙强暴民女'、'大家来看啊'……"
    servant_c "围观的人越来越多！眼看要成为众矢之的了！"
    
    pause 0.8
    
    # ========================================
    # 镜头 4：洪彦龙的暴怒时刻（垂直冲击 vpunch + 音效）
    # ========================================
    scene bg hong_study_4 with vpunch
    
    # 拍案惊堂木的音效
    # play sound "audio/table_flip.ogg"
    
    # 显示暴怒的洪彦龙
    show hong furious at center
    
    hong "【一群废物！！！】"
    hong "养你们这些东西有什么用？！连一个女人都看不住？！"
    hong "你们简直就是一帮蠢猪！！！"
    
    # 舞台暴力：掀翻桌子的画面效果
    show text "【整个书房陷入混乱……】" at truecenter with vpunch
    pause 0.5
    hide text
    
    hong "现在她在大街上胡言乱语，这是要毁了我的名声！！"
    hong "我需要一个解决方案，而且要立刻！！！"
    
    # 洪彦龙离场（或转身）
    hide hong
    
    pause 1.0
    
    # ========================================
    # 镜头 5：废墟中的最后仆人 + 主角登场（淡入，转折）
    # ========================================
    scene bg hong_study_5 with dissolve
    
    # 剧院般的沉寂，只有拉风箱的声音
    # play sound "audio/deep_breath.ogg"
    
    # 最后一个仆人的瑟瑟发抖
    servant_d "大……大人……我们……我们该怎么办啊……"
    
    pause 1.0
    
    # 显示主角 - 从暗处走进书房，镇定自若
    show me confident at center
    
    # 淡入背景音乐：沉着、智慧的主题
    # play music "audio/strategist_theme.ogg" loop
    
    # 舞台中心：主角献计的关键时刻
    me "大人的遭遇，我已经听明白了。"
    me "诸位家丁做得已经很尽力了，但这件事……不是武力能解决的。"
    
    # 主角走向中心，表现出睿智的气质
    me "现在关键是，要用一个合法、体面的说法，把这个局面扭转过来。"
    
    # 洪彦龙冲出，期待答案
    show hong intense at right
    
    hong "你有办法？"
    
    me "有。我建议，我们不如……主动出击。"
    
    # 镜头定格在这一刻，暗示即将进入关键的对话
    pause 1.0
    
    me "既然她已经逃出去、闹出这么大的动静，我们就索性……给她一个'名分'。"
    
    hong "名分？"
    
    me "没错。一份婚书。"
    
    me "只要她签署了婚书、承认自己是您的妻子，那之前的所有反抗……"
    
    me "就变成了'新娘的任性'，而非'强占民女的证据'。"
    
    # 镜头缓缓拉远，展现这一刻的格局转变
    scene bg hong_study_5 with dissolve
    
    show hong satisfied at right
    show me confident at left
    
    hong "妙计！你这小子，果然有两把刷子。"
    
    hong "好，那就照你说的办。婚书呢？"
    
    me "大人，您给我一点时间……"
    
    me "我从前在县衙做过文书，写一份婚书……"
    
    # 过渡到正式对话场景
    jump act1_continuing_story

# 继续正常剧情
label act1_continuing_story:

    scene bg hong_mansion
    show hong neutral at center
    
    hong "那就劳烦你了。立刻给我写一份婚书，必须无懈可击。"
    hong "如果能让兰中玉心甘情愿地接受这个身份，你的赏赐少不了。"
    
    me "是，大人。我这就去准备。"
    
    jump forged_document_minigame

# 玩法环节 2：伪证
label forged_document_minigame:
    # ========================================
    # 小游戏状态锁定 (伪造婚书)
    # ========================================
    # 防止玩家在小游戏中使用 Skip(快进)、Rollback(回滚)、Menu(菜单)
    $ renpy.block_rollback()      # 阻止滚轮强制回退
    $ _skipping = False           # 禁用快进功能
    $ _rollback = False           # 禁用回滚功能
    $ _game_menu_screen = None    # 禁用右键/ESC菜单
    
    $ ooc_checkpoint = ooc_value
    me "我拿起毛笔，墨已经磨好了。"
    me "这是最关键的一刻……我深吸一口气。"
    me "三秒钟内必须落笔完美，否则一切都会露陷。"
    me "笔尖悬在纸上方，我等待着准备的时刻……"
    
    # 初始化并调用笔画描红小游戏
    $ init_stroke_tracker()
    $ qte_result = renpy.call_screen("stroke_writing")
    
    if qte_result == "success":
        # ========== 完美成功 ==========
        $ update_ooc(-20)
        me "我沉下心来，笔画一个一个地落下。"
        me "每一笔都是精心雕琢，笔锋有力但不失柔和。"
        me "最后一笔收笔……完美！"
        show hong happy at center
        hong "哈哈！好字！"
        hong "这笔迹，足以骗过任何人。"
        hong "你这小子，真有一手啊。"
        hong "给，这是赏赐你的。"
        me "感谢大人！"
        jump forged_document_success
        
    elif qte_result == "fail":
        # ========== 失误重试 ==========
        $ update_ooc(10)
        me "我笔……颤抖了一下……"
        me "最后一笔没有把握好，字看起来歪歪斜斜。"
        show hong frown at center
        hong "嗯？这笔迹……有点问题啊。"
        hong "太草率了。重写！"
        me "是……立刻重写……"
        pause 0.5
        me "（手心冒汗……为什么这一次这么难？）"
        me "（每次重新开始，压力就更大一分……）"
        me "（必须集中精力，不能再失误了……）"
        
        # ========================================
        # 小游戏状态解锁 (伪造婚书失败重试前)
        # ========================================
        $ _skipping = True                # 恢复快进功能
        $ _rollback = True                # 恢复回滚功能
        $ _game_menu_screen = "save"      # 恢复菜单功能
        
        jump forged_document_minigame
        
    elif qte_result == "cheat":
        # ========== 一键开挂 ==========
        $ update_ooc(-50)
        $ cheat_count += 1
        me "我的手仿佛获得了某种力量……"
        me "笔尖飞快地舞动，字迹工整得不可思议。"
        me "几秒钟内，一个完美的'婚'字就跃然纸上。"
        show hong amazed at center
        hong "这……这笔迹，简直是鬼斧神工！"
        hong "你这小子，不简单啊！"
        hong "给，这是赏赐你的。"
        me "感谢大人！"
        jump forged_document_success

# 伪证成功
label forged_document_success:
    # ========================================
    # 小游戏状态解锁 (伪造婚书完成)
    # ========================================
    $ _skipping = True                # 恢复快进功能
    $ _rollback = True                # 恢复回滚功能
    $ _game_menu_screen = "save"      # 恢复菜单功能
    
    scene bg hong_mansion
    show hong neutral at center
    hong "婚书写完了？"
    me "已经完成，大人。"
    hong "很好。现在去见兰中玉，给她看看这份婚书。"
    hong "告诉她，一切都是真的。"
    me "遵命。"
    jump scene_5_5_rescue

################################################################################
## SCENE 5.5：潜入洪府救援兰中玉
################################################################################

label scene_5_5_rescue:
    """
    深夜行动：主角沈怀瑾需要避开家丁巡逻，潜入洪府偏房救出兰中玉。
    这是一个关键的 OOC 判定节点，暴露身份将导致任务失败和 Game Over。
    """
    
    # 保存当前 ooc_value，以备失败时重置
    $ ooc_checkpoint = ooc_value
    
    # 场景：深夜的洪府外院
    scene bg night_street
    
    # 播放紧张的背景音乐（心跳鼓点）
    # play music "audio/heartbeat_tense.ogg" loop
    
    # 主角内心独白
    me "夜色已深。洪府的灯火都已熄灭，但四处都有家丁在巡逻。"
    
    me "我必须找到机会，潜入兰中玉被关押的偏房。"
    
    me "但身份暴露的代价是……Game Over。"
    
    # 主角来到一个关键的决策点
    pause 1.0
    
    # 创建潜行路线选择菜单
    menu:
        "　【压低身形，贴墙潜行】悄悄避开家丁巡逻路线。":
            # 选项 A：符合反派人设的狡黠行为
            # OOC 不变（或略微减少，体现聪明谨慎）
            $ update_ooc(-5)
            me "我压低身形，尽量贴着墙壁移动。"
            me "观察了家丁的巡逻规律……他们大约每三分钟会经过这里一次。"
            me "这正好给了我足够的窗口期。"
            pause 0.5
            
            # 进入潜行小游戏
            jump scene_5_5_stealth_game
        
        "　【大摇大摆前行】反正我是国舅爷的师爷，谁敢拦我！":
            # 选项 B：过度表现反派人设导致崩坏
            # OOC 增加 30
            $ update_ooc(30)
            
            me "我站直身体，大步流星地往前走。"
            me "反正我是洪彦龙的师爷，有什么好怕的？"
            me "谁敢拦我！"
            pause 1.0
            
            # 检查 OOC 值是否达到致命值
            $ check_ooc()
            
            # 如果还活着，会被家丁发现异常
            show text "咦？这个人……走路的姿态有点奇怪……" at truecenter
            pause 2.0
            hide text
            
            # 被发现破绽
            me "不好！被家丁看出破绽了！"
            me "我得赶紧改变策略，否则身份会彻底暴露！"
            pause 0.5
            
            # 重新进行选择（给玩家改正的机会）
            jump scene_5_5_rescue

################################################################################
## SCENE 5.5.1：潜行小游戏
################################################################################

label scene_5_5_stealth_game:
    """
    潜行小游戏：使用九宫格一笔画避开巡逻队
    - 成功：避开危险路线，到达终点（节点8）
    - 失败：踩到红线（危险路线），被发现
    - 开挂：使用分身术直接成功
    """
    
    # ========================================
    # 小游戏状态锁定 (潜行避敌)
    # ========================================
    # 防止玩家在小游戏中使用 Skip(快进)、Rollback(回滚)、Menu(菜单)
    $ renpy.block_rollback()      # 阻止滚轮强制回退
    $ _skipping = False           # 禁用快进功能
    $ _rollback = False           # 禁用回滚功能
    $ _game_menu_screen = None    # 禁用右键/ESC菜单
    
    # 重置潜行步数计数
    $ stealth_correct_steps = 0
    
    # 主角内心独白
    me "我必须小心翼翼地规划路线，避开家丁的巡逻红线……"
    pause 0.5
    
    # 初始化并调用九宫格一笔画小游戏
    $ init_nine_puzzle()
    $ stealth_result = renpy.call_screen("nine_puzzle_path")
    
    if stealth_result == "success":
        # ========== 成功规划路线 ==========
        $ update_ooc(-15)
        me "终于……躲过了所有巡逻队。我已经到达了目标区域。"
        jump scene_5_5_stealth_success
    
    elif stealth_result == "cheat":
        # ========== 使用分身术（一键开挂）==========
        $ update_ooc(-50)
        $ cheat_count += 1
        
        me "我仿佛分裂成了两个世界……"
        me "身体在一个次元行动，而家丁们的目光无法捕捉到我。"
        pause 1.0
        me "转眼间，我已经出现在了偏房外。"
        pause 0.5
        
        jump scene_5_5_stealth_success
    
    else:
        # ========== 触发危险（踩到红线）==========
        $ update_ooc(30)
        
        # 屏幕闪红效果
        show text "触发警报！你踩到了巡逻队的路线！" at truecenter with flash
        pause 1.0
        hide text
        
        # 检查 OOC 值是否达到致命值
        $ check_ooc()
        
        # 如果还活着，重新提示
        show text "不行！我得重新规划……" at truecenter
        pause 2.0
        hide text
        
        me "这条路走不通……我必须重新找个安全的路线。"
        pause 0.5
        
        # ========================================
        # 小游戏状态解锁 (潜行避敌失败重试前)
        # ========================================
        $ _skipping = True                # 恢复快进功能
        $ _rollback = True                # 恢复回滚功能
        $ _game_menu_screen = "save"      # 恢复菜单功能
        
        # 重新开始潜行小游戏
        jump scene_5_5_stealth_game

################################################################################
## SCENE 5.5.2：潜行成功 - 救出兰中玉
################################################################################

label scene_5_5_stealth_success:
    """
    潜行成功，主角成功到达兰中玉的偏房。
    """
    
    # ========================================
    # 小游戏状态解锁 (潜行完成)
    # ========================================
    $ _skipping = True                # 恢复快进功能
    $ _rollback = True                # 恢复回滚功能
    $ _game_menu_screen = "save"      # 恢复菜单功能
    
    # 停止背景音乐
    stop music
    
    # 场景：洪府偏房内（昏暗的烛光）
    scene bg hong_study_night
    
    # 播放柔和的背景音乐
    # play music "audio/quiet_night.ogg" loop
    
    # 出现兰中玉，穿着粗布衣服，神情黯淡
    show lan sad at center
    
    me "兰中玉……"
    
    # 兰中玉惊讶地抬起头
    show lan shocked at center
    
    lan "你……你怎么来了？"
    lan "这里很危险，如果被……"
    
    me "没有时间了。我来救你。"
    
    lan "救我？……可你是洪家的人啊……"
    
    me "我不是你想的那种人。相信我。"
    
    me "我编造了一个谎言，但我正在尽力弥补。"
    
    me "无论如何，我不能让你继续被困在这里。"
    
    lan "……你是认真的？"
    
    me "完全认真。现在，跟我一起离开。"
    
    # 场景切换：众人一起逃离洪府
    pause 1.0
    
    scene bg night_street with fade
    
    show lan neutral at right
    show me at left
    
    me "路就在前面了。出城之后就安全了。"
    
    lan "我……我会永远记得你的。"
    
    me "不要说这些话。我们的事还没完。"
    
    me "接下来，我还要去县衙自首。"
    me "这样的话，你的名字才能彻底洗白。"
    
    lan "你要……自首？"
    
    me "是的。因为欺骗了你，我必须为此负责。"
    
    # 兰中玉的反应
    show lan sad at right
    
    lan "如果你自首了，那你……"
    
    me "我知道会发生什么。但这是必须的。"
    
    # 场景淡出
    pause 2.0
    scene bg black with fade
    
    # 继续跳转主线剧情
    jump act2_night_stealth

# 第二幕：夜间行动
label act2_night_stealth:
    
    # 保存当前 ooc_value，以备 game_over 重置
    $ ooc_checkpoint = ooc_value
    
    # 场景：深夜的历城街道
    scene bg night_street
    
    # 播放紧张的低音鼓点
    # play sound "audio/tense_bass_drum.ogg"
    
    me "夜色降临了。历城的灯火渐渐熄灭。"
    me "我下定决心，必须去县衙找知县张清自首。"
    me "只有这样，才能彻底摆脱这个困局。"
    me "但这条路上，守卫森严。到处都是洪家的家丁在巡逻。"
    me "我必须小心谨慎……"
    
    # 主角的选择
    menu:
        "　(A) 「压低身形，贴墙潜行」悄悄避开家丁":
            # OOC 不变，进入潜行小游戏
            jump stealth_minigame
        
        "　(B) 「大摇大摆前行」反正我是师爷":
            $ update_ooc(30)
            if ooc_value >= 70:
                # OOC 过高，直接暴露
                me "我站直身体，大步流星地往前走。"
                me "反正我是洪家的师爷，有什么好怕的？"
                # 家丁很快发现异常
                jump game_over_exposed
            else:
                # OOC 未达到致命值，但被警告
                me "我站直身体，大步流星地往前走。"
                me "反正我是洪家的师爷，有什么好怕的？"
                show text "咦？这个人……不太对劲……" at truecenter
                pause 2.0
                hide text
                me "不好，被家丁看出破绽了！"
                me "我得赶紧改变策略。"
                jump stealth_minigame

# 玩法环节 3：潜行模拟
label stealth_minigame:
    
    me "一步一步，我仔细观察着家丁的巡逻路线。"
    me "找到一条空隙……精确地绘制出这条逃脱的路线……"
    
    menu:
        "　「路线正确」成功避开巡逻到达县衙":
            $ update_ooc(-15)
            me "完美！我避开了所有的巡逻队。"
            me "前面就是县衙的后门了。"
            jump zhang_study_confession
        
        "　「走错断开」惊动家丁":
            $ update_ooc(30)
            if ooc_value >= 100:
                # OOC 达到 100，直接失败
                show text "「惊！」" at truecenter with flash
                me "糟糕！被发现了！"
                jump game_over_exposed
            else:
                # OOC 未达 100，画面闪红重试
                show text "【警报】你的行动惊动了家丁！" at truecenter with flash
                pause 2.0
                hide text
                me "不行，我得重新计划路线……"
                jump stealth_minigame
        
        "　「一键开挂 (Skip)」":
            $ update_ooc(-50)
            $ cheat_count += 1
            me "我仿佛分裂成了两个世界……"
            me "身体在一个次元行动，而家丁们的目光无法捕捉到我。"
            me "转眼间，我已经出现在了县衙后门。"
            jump zhang_study_confession

# 主角在书房面见知县
label zhang_study_confession:
    
    # ========================
    # 1. 破冰定场（全景1）
    # ========================
    # 主角刚潜入书房，知县呵斥或询问身份
    scene bg zhang_study_1 with dissolve
    
    show zhang neutral at center
    
    zhang "是谁在半夜潜入我的书房？"
    
    me "大人……是我。"
    
    me "我冒死来见您，不是为了投案……"
    
    zhang "那你是为了什么？"
    
    me "我是来送您一条破局之法的。"
    
    zhang "破局？"
    
    zhang "贾斯文……你有胆子背叛洪彦龙？"
    
    me "我本不想的，大人。但我已经看清了洪彦龙的真面目。"
    
    me "他将兰中玉囚禁在府中，意图私吞彩礼与聘金。"
    
    me "当年那份婚书，正是他强迫我伪造的。"
    
    # ========================
    # 2. 交锋与态度松动（全景2）
    # ========================
    # 知县开始认真倾听，心理距离拉近
    scene bg zhang_study_2 with Dissolve(0.5)
    
    show zhang thoughtful at center
    
    zhang "……继续说。"
    
    zhang "你这样背叛他，就不怕死吗？"
    
    me "大人，死有很多种。"
    
    me "有的死法是被刀剑斩杀，有的死法是良心每日谴责。"
    
    me "我已经决定，用一种有意义的死法——"
    
    me "揭露真相，还兰中玉自由，还大人您一个清廉的名声。"
    
    zhang "有趣。说说你的计划。"
    
    me "明天，洪彦龙会拿出一份假的婚书，谎称兰中玉已同意这段婚姻。"
    
    me "他以为这份伪造的文书能骗过您的法眼。"
    
    me "但……如果大人您能识破这份文书的破绽，"
    
    me "在公堂上着他个措手不及……"
    
    # ========================
    # 3. 终极密谋（案卷特写）
    # ========================
    # 主角抛出底牌，两人定下公堂连环计
    scene bg zhang_study_closeup with Dissolve(1.5)
    
    show zhang contemptuous at center
    
    zhang "你是说……"
    
    me "是的，大人。那份婚书，是用【立此为证】这样的粗俗商人用语。"
    
    me "一个懂文化的知县，只需一眼就能看出破绽。"
    
    me "而我，可以在公堂上指认这份书是出自我的笔迹——"
    
    me "再加上兰中玉本人的证词，三层铁证，无懈可击。"
    
    zhang "……聪慧的小子。"
    
    zhang "你已经把所有的赌注都押在我的诚廉之上了。"
    
    zhang "如果我也是贪官，现在就该杀人灭口。"
    
    me "是的，大人。我甘愿冒这个险。"
    
    zhang "很好。那明天公堂上，就按你的计划来。"
    
    zhang "兰中玉会被释放，洪彦龙会受到应有的惩罚。"
    
    # ========================
    # 4. 大局已定（全景3）
    # ========================
    # 镜头拉回全景，谈判结束，契约已成
    scene bg zhang_study_3 with dissolve
    
    show zhang satisfied at center
    
    zhang "现在，你可以离开了。"
    
    zhang "去做你要做的事。解救那位女子。"
    
    me "是，大人。我这就启程。"
    
    zhang "等等。"
    
    me "……是？"
    
    zhang "后会有期，贾斯文。"
    
    zhang "无论你的结局是生还是死，我都会信守今晚的承诺。"
    
    me "谢大人。"
    
    jump scene_5_5_rescue

# 游戏结束：身份暴露
label game_over_exposed:
    
    # 隐藏所有画面和 UI
    hide screen ooc_hud
    hide eileen
    hide lian
    hide hong
    hide zhang
    hide lan
    
    # 黑屏
    scene bg black
    
    # 显示失败文本
    show text "Game Over：身份暴露" at truecenter with dissolve
    
    # 停留 3 秒
    pause 3.0
    
    # 隐藏文本
    hide text
    
    # 重置 ooc_value 为保存的状态
    $ ooc_value = ooc_checkpoint
    
    # 返回到夜间行动前的场景
    jump act2_night_stealth

# 游戏结束：露馅被斩
label game_over_court:
    
    # 隐藏所有画面和 UI
    hide screen ooc_hud
    hide eileen
    hide lian
    hide hong
    hide zhang
    hide lan
    
    # 黑屏
    scene bg black
    
    # 显示失败文本
    show text "Game Over：露馅被斩" at truecenter with dissolve
    
    # 停留 3 秒
    pause 3.0
    
    # 隐藏文本
    hide text
    
    # 重置 ooc_value 为保存的状态
    $ ooc_value = ooc_checkpoint
    
    # 返回到公堂对峙前的场景
    jump act3_courtroom

# 第三幕：公堂对峙
label act3_courtroom:
    """
    SCENE 6：公堂对质 - 高潮对峙
    知县张清通过文化论证戳穿洪彦龙伪造文书的阴谋
    主角需要把握时机，配合知县击溃洪彦龙
    """
    
    # 保存当前 ooc_value，以备失败时重置
    $ ooc_checkpoint = ooc_value
    
    # 场景：衙门公堂（庄严肃穆）
    scene bg courtroom with dissolve
    
    # 背景音乐：庄严的公堂主题
    # play music "audio/courtroom_theme.ogg" loop
    
    # 三人登场：洪彦龙（紧张）、张清（沉着）、贾斯文（主角，准备应战）
    show hong nervous at left
    show zhang calm at right
    
    # ========================================
    # 知县质证：文化阶级的差异
    # ========================================
    
    zhang "洪彦龙！你提交的婚书上写着：'立此为证，兹定……'"
    
    zhang "但我读了二十年的公牍，却发现了问题。"
    
    # 知县冷笑，走向公堂中央
    show zhang contemptuous at center
    
    # 显示高亮对比：两个关键词句
    show text "{color=#FF6B6B}立此为证{/color}（粗俗商贾用语）\nvs\n{color=#6BCB77}谨立此据{/color}（文人雅言）" at truecenter
    
    zhang "【立此为证】是粗鲁的商人用语，充满铜臭味。" with vpunch
    zhang "而一份郑重其事的婚书，应该用【谨立】、【特立】这样的文人雅言。" with vpunch
    
    hide text
    
    zhang "你这样的伪造痕迹，实在太明显了！" with vpunch
    
    # 洪彦龙惊慌失措
    show hong shocked at left
    
    hong "我……这……"
    
    hong "这婚书是……是贾斯文写的！"
    
    # 知县大喝一声，拍惊堂木
    show zhang angry at center
    
    # ========================================
    # 戏剧高潮：知县的威势
    # ========================================
    
    # 拍惊堂木音效和震屏效果
    play sound sfx_gavel
    show text "【惊堂木】" at truecenter with vpunch
    pause 0.3
    hide text
    
    zhang "荒唐！本官要审问的是……贾斯文！" with vpunch
    
    me "……是！"
    
    # 场景镜头转向主角
    show me neutral at center
    hide hong
    hide zhang
    
    pause 1.0
    
    # ========================================
    # 关键选择菜单：配合知县的审判节奏
    # ========================================
    
    zhang "贾斯文！这份婚书，真的是你写的吗？还是……洪彦龙强迫你？" with vpunch

    menu:
        "　【声泪俱下，甩锅】我……我本不想的！都是洪大人强迫我！":
            # ========== 选项 A：推卸责任，符合反派人设 ==========
            $ update_ooc(-10)
            
            me "我……我本是个良善的人啊！"
            me "都是洪彦龙这个恶棍！强行指使我，不从就要打死我！"
            me "我也是被逼无奈啊，大人！"
            
            # 这个选项激发洪彦龙的愤怒
            show hong furious at left
            hong "你……你这个忘恩负义的……"
            
            # 跳转到 QTE 小游戏
            jump scene_6_dwrg_trial
        
        "　【语气强硬】这份婚书确实是我写的，请立即定洪彦龙有罪！":
            # ========== 选项 B：强硬要求定罪，可能引起反感 ==========
            $ update_ooc(20)
            
            me "大人，这份婚书确实是我写的。"
            me "但这一切都是在洪彦龙的授意和威胁下进行的！"
            me "我建议您遵循法律，立即定他有罪！"
            
            # 知县可能认为他过于积极，引起怀疑
            show zhang suspicious at center
            zhang "嗯？你这小子，倒是急于翻脸啊……" with hpunch
            zhang "让我想想，你的动机是什么？"
            
            me "我……我只是想见证正义！"
            
            # 检查 OOC 值
            $ check_ooc()
            
            # 如果还活着，跳转到 QTE
            jump scene_6_dwrg_trial

################################################################################
## SCENE 6.1：DWRG 节奏审判小游戏（QTE）
################################################################################

label scene_6_dwrg_trial:
    """
    DWRG（Dynamic Weighted Rhythm Game）节奏审判小游戏
    玩家需要在知县的提问节奏中（通过 QTE），
    在适当的时刻"拍案"，配合张清压制洪彦龙。
    
    - Perfect：完美时机点击"拍案" → OOC-15，获得知县支持
    - Miss：时机不对或超时 → OOC+10，画面闪红，知县怀疑
    - Cheat：使用一键开挂 → OOC-50，cheat_count+1
    """
    
    # ========================================
    # 小游戏状态锁定 (DWRG公堂审判)
    # ========================================
    # 防止玩家在小游戏中使用 Skip(快进)、Rollback(回滚)、Menu(菜单)
    $ renpy.block_rollback()      # 阻止滚轮强制回退
    $ _skipping = False           # 禁用快进功能
    $ _rollback = False           # 禁用回滚功能
    $ _game_menu_screen = None    # 禁用右键/ESC菜单
    
    # 显示 HUD
    show screen ooc_hud
    
    # 知县的催促
    zhang "现在，让我逐一质证你的说词！"
    
    # ========================================
    # 重置 QTE 计数
    # ========================================
    $ dwrg_attempt_count = 0
    
    # ========================================
    # QTE 循环：轮流进行多轮审问
    # ========================================

label dwrg_round_begin:
    $ dwrg_attempt_count += 1
    
    if dwrg_attempt_count == 1:
        zhang "第一个问题：洪彦龙给了你多少好处？" with vpunch
    elif dwrg_attempt_count == 2:
        zhang "那么，第二个问题：他是何时强迫你的？" with vpunch
    else:
        zhang "证据呢？你有什么证据？" with vpunch
    
    # 调用 dwrg_trial screen 等待玩家输入
    $ dwrg_result_raw = renpy.call_screen("dwrg_trial", round_num=dwrg_attempt_count)
    
    # ========== 处理玩家的选择 ==========
    
    if dwrg_result_raw == "attempt_hit":
        # 玩家点击了"拍案"，检查时机是否正确（指针在绿色区）
        if 0.3 <= dwrg_pointer_pos <= 0.7:
                # ========== 完美命中！==========
                $ update_ooc(-15)
                
                play sound sfx_gavel
                scene bg courtroom with flash
                play sound sfx_gong  # 绝杀时刻：京剧鼓声
                show text "【精确压制！】" at truecenter with vpunch
                pause 0.5
                hide text
                
                # 根据轮数播放特定对话
                if dwrg_attempt_count == 1:
                    me "大人！他答应了我五十两银子，还说会送我一个媾美妾……"
                    
                    show hong panicked at left
                    hong "你说什么呢！这是……这是胡说八道！"
                    
                    zhang "闭嘴！"
                
                elif dwrg_attempt_count == 2:
                    me "就在……就在那个私会的晚上！他忽然闯进书房，"
                    me "拔剑对着我，说如果不照办，就杀我全家！"
                    
                    show hong angry at left
                    hong "这……这是血口喷人！"
                    
                    # 知县给予严厉制止
                    show zhang confident at center
                    zhang "从你们两人的言辞反差，本官已经看清楚了！" with vpunch
                    
                    # 连续两个完美回答，可以直接宣判
                    jump act3_courtroom_success
                
                # 继续下一轮
                pause 1.0
                jump dwrg_round_begin
            
                # else:
                # ========== 时机不对，击中了危险区 ==========
                $ update_ooc(10)
                
                show text "【节奏被破坏！】" at truecenter with hpunch
                pause 0.5
                hide text
                
                if dwrg_attempt_count == 1:
                    me "我……五十两……不是……"
                elif dwrg_attempt_count == 2:
                    me "我……我不清楚具体时间……"
                else:
                    me "证据？我……哪有什么证据……"
                
                show zhang frown at center
                zhang "吞吞吐吐！看来你在隐瞒什么！" with vpunch
                
                hong "哈哈！你们瞧瞧，这小子都说不出个所以然来！"
                
                # 检查 OOC，如果达到致命值就 Game Over
                $ check_ooc()
                
                # 否则允许重新尝试
                me "不……不是这样的，大人……"
                pause 1.0
                
                # ========================================
                # 小游戏状态解锁 (DWRG失败重试前)
                # ========================================
                $ _skipping = True                # 恢复快进功能
                $ _rollback = True                # 恢复回滚功能
                $ _game_menu_screen = "save"      # 恢复菜单功能
                
                jump dwrg_round_begin
        
        elif dwrg_result_raw == "miss":
            # ========== 超时，时间耗尽 ==========
            $ update_ooc(10)
            
            show text "【时间耗尽！】" at truecenter with hpunch
            pause 0.5
            hide text
            
            me "我……我的话还没说完……"
            
            show zhang angry at center
            play sound sfx_gavel
            zhang "大胆！你在本官面前还要支吾其辞？" with vpunch
            
            # 检查 OOC 是否达到致命值
            $ check_ooc()
            
            # 否则允许重试
            me "大人，请再给我一次机会……"
            pause 1.0
            
            # ========================================
            # 小游戏状态解锁 (DWRG超时重试前)
            # ========================================
            $ _skipping = True                # 恢复快进功能
            $ _rollback = True                # 恢复回滚功能
            $ _game_menu_screen = "save"      # 恢复菜单功能
            
            jump dwrg_round_begin
        
        elif dwrg_result_raw == "cheat_auto_hit":
            # ========== 使用一键开挂（前 3 次，合法） ==========
            $ update_ooc(-50)
            $ cheat_count += 1
            
            show text "【系统骇入：完美反杀！】" at truecenter with flash
            play sound sfx_gong  # 绝杀时刻音效
            pause 0.5
            hide text
            
            show hong shocked at left
            
            if dwrg_attempt_count == 1:
                me "（我……仿佛获得了超凡的说辞能力！）"
                me "大人！他给了我五十两银子，还威胁要杀我全家！"
            else:
                me "（真是……天赐的智慧与口才……）"
                me "大人，他那天拔剑对我，还当众发誓要杀我全家！"
                me "这是有目共睹的罪行！"
            
            hong "我……我……"
            
            show zhang satisfied at center
            zhang "好了！本官已经听够了。证据确凿，毋庸置疑。" with flash
            
            # 直接跳到成功
            jump act3_courtroom_success
        
        elif dwrg_result_raw == "cheat_exceed":
            # ========== 开挂超限（第 4 次及以上，触发惩罚） ==========
            # OOC 强制锁定为 99（极度危险）
            $ ooc_value = 99
            
            show text "【禁止骇入！系统反制！】" at truecenter with hpunch
            pause 0.5
            hide text
            
            me "我……我突然感到一阵虚弱……仿佛所有的力量都被夺走了……"
            
            show zhang contemptuous at center
            zhang "你这小子，竟敢在本官面前玩花样？！" with vpunch
            
            # OOC 达到 99，触发即将 Game Over 的恐怖感
            show text "【警告】您的人设即将崩坏！下一次失误将导致 Game Over！" at truecenter with flash
            pause 1.0
            hide text
            
            # 允许继续但处于极端危险状态
            me "不……不是……我真的……"
            pause 1.0
            jump dwrg_round_begin
        
        elif dwrg_result_raw == "cheat":
            # ========== 保留原有逻辑作为后备 ==========
            $ update_ooc(-50)
            $ cheat_count += 1
            
            show text "【一键开挂激活！】" at truecenter with flash
            pause 0.5
            hide text
            
            show hong shocked at left
            
            if dwrg_attempt_count == 1:
                me "（我……仿佛获得了超凡的说辞能力！）"
                me "大人！他给了我五十两银子，还威胁要杀我全家！"
            else:
                me "（真是……天赐的智慧与口才……）"
                me "大人，他那天拔剑对我，还当众发誓要杀我全家！"
                me "这是有目共睹的罪行！"
            
            hong "我……我……"
            
            show zhang satisfied at center
            zhang "好了！本官已经听够了。证据确凿，毋庸置疑。" with flash
            
            # 直接跳到成功
            jump act3_courtroom_success

# 公堂对峙成功
label act3_courtroom_success:
    # ========================================
    # 小游戏状态解锁 (DWRG公堂完成)
    # ========================================
    $ _skipping = True                # 恢复快进功能
    $ _rollback = True                # 恢复回滚功能
    $ _game_menu_screen = "save"      # 恢复菜单功能
    
    scene bg courtroom
    show zhang satisfied at center
    
    zhang "洪彦龙！根据本官的审理，你犯有以下罪名："
    zhang "伪造婚书罪、人身威胁罪、婚约欺诈罪……"
    
    show hong desperate at left
    hong "大人……大人饶命啊！"
    
    zhang "来人！将洪彦龙打入死牢，等候处斩！"
    
    me "（……终于……结束了。）"
    
    pause 1.0
    
    jump epilogue

# 尾声：根据 OOC 值选择结局
label epilogue:
    
    # 场景：戏班后台，主角醒来
    hide screen ooc_hud
    scene bg backstage
    
    me "……"
    
    me "我醒了。"
    
    me "刚才的一切……真的发生过吗？"
    
    me "我的手指上还有血迹，那本古籍……也真实存在。"
    
    # 根据 OOC 值选择结局
    if ooc_value <= 30:
        jump ending_perfect
    elif ooc_value <= 70:
        jump ending_normal
    else:
        jump ending_bittersweet

# 完美结局：戏悟人生
label ending_perfect:
    
    me "也许……我终于理解了什么叫'戏悟人生'。"
    
    me "我用最清纯的心去领悟那个世界，所以我在那里找到了救赎。"
    
    show lian healthy at center with dissolve
    
    lian "你终于回来了。"
    
    me "小莲？你……你好了！"
    
    lian "是的。就在你进去的那一刻，我感到了一种力量……"
    
    lian "它温暖而坚定，就像你一样。"
    
    me "小莲……"
    
    # 渐黑效果
    scene bg black with fade
    
    me "也许这就是代价和救赎的关系。我用我的脸谱，换来了她的生命。"
    
    me "而我在那个舞台上，真正地活了一次。"
    
    # 显示完美结局标题
    show text "【完美结局】戏悟人生" at truecenter with dissolve:
        pause 3.0
    hide text
    
    return

# 普通结局：大梦初醒
label ending_normal:
    
    me "也许…… 这一切不过是一场大梦。"
    
    me "我在梦中扮演过别人，体验过别人的人生。"
    
    me "但现在，我回到了现实。"
    
    me "小莲还在咳嗽，这个世界还是一样的残酷。"
    
    me "但我不一样了。我知道了什么叫坚持，什么叫妥协。"
    
    me "就这样慢慢走下去吧。"
    
    # 渐黑效果
    scene bg black with fade
    pause 1.0
    
    # 显示普通结局标题
    show text "【标准结局】大梦初醒" at truecenter with dissolve:
        pause 3.0
    hide text
    
    return

# 遗憾结局：半生彷徨
label ending_bittersweet:
    
    me "我活了那么久，却从没像现在这样感到迷茫。"
    
    me "我在那个舞台上几乎失手，那种恐惧还缠绕着我。"
    
    me "也许我根本不配去救小莲。"
    
    me "也许我只配在这个世界里……半生彷徨。"
    
    me "看着她慢慢陷入深渊，却无能为力。"
    
    me "如果能重来就好了……"
    
    # 渐黑效果
    scene bg black with fade
    pause 1.0
    
    # 显示遗憾结局标题
    show text "【遗憾结局】半生彷徨" at truecenter with dissolve:
        pause 3.0
    hide text
    
    return
################################################################################
## Game Over 标签：OOC 值崩坏结局
################################################################################

label game_over_ooc:
    """
    当玩家的 OOC（角色崩坏度）值达到 100% 时触发此标签
    人设彻底崩坏，游戏结束
    """
    
    # 场景效果：脸谱完全碎裂
    scene bg black with fade
    pause 0.5
    
    # 显示游戏结束画面
    scene bg black
    show text "脸谱已经完全碎裂了……" at center with dissolve:
        pause 2.0
    hide text
    
    pause 0.5
    
    show text "你维持不下反派的人设了。" at center with dissolve:
        pause 2.0
    hide text
    
    pause 0.5
    
    show text "剧本彻底坏了。" at center with dissolve:
        pause 2.0
    hide text
    
    pause 0.5
    
    show text "游戏结束。" at center with dissolve:
        pause 2.0
    hide text
    
    pause 1.0
    
    # 显示结局标题
    show text "【崩坏结局】人设尽毁" at truecenter with dissolve:
        pause 3.0
    hide text
    
    # 返回标题菜单
    return

################################################################################
## Game Over 结局：露馅被斩（法庭败露）
################################################################################

label game_over_exposed_final:
    """
    OOC 达到 100 时触发的死亡结局
    极其震撼的法庭崩溃与斩首场景
    """
    
    # 隐藏所有角色和屏幕元素
    hide screen ooc_hud
    hide lian
    hide hong
    hide zhang
    hide me
    hide jia_siwen
    
    # 停止背景音乐，1 秒淡出
    stop music fadeout 1.0
    
    # ========================================
    # 1. 画面瞬间切红 + 极度震屏
    # ========================================
    scene solid "#8B0000" with vpunch
    
    pause 0.5
    
    # 播放惊堂木音效（追加多次以强化绝望感）
    play sound sfx_gavel
    pause 0.2
    play sound sfx_gavel
    pause 0.2
    play sound sfx_gavel
    
    pause 0.5
    
    # ========================================
    # 2. 知县的震怒台词（大字赤红）
    # ========================================
    # 使用 show text 显示知县的绝对威权台词
    show text "{size=48}{color=#FFFFFF}大胆狂徒！{/color}{/size}" at truecenter:
        pause 1.5
    hide text
    
    pause 0.3
    
    show text "{size=40}{color=#FF6B6B}满口胡言，竟敢咆哮公堂！{/color}{/size}" at truecenter:
        pause 2.0
    hide text
    
    pause 0.3
    
    show text "{size=40}{color=#FF0000}左右，给我拉下去斩了！{/color}{/size}" at truecenter:
        pause 2.0
    hide text
    
    pause 0.8
    
    # ========================================
    # 3. 主角的绝望内心独白
    # ========================================
    scene black with Fade(0.5, 0.2, 0.5)
    
    pause 0.5
    
    me "我……终究没能演好这场戏……"
    
    pause 1.0
    
    me "这个角色吞没了我。"
    
    me "而我，也逃脱不了宿命的绞刑架。"
    
    pause 1.5
    
    # ========================================
    # 4. 画面切黑+结局文字
    # ========================================
    scene black with fade
    
    pause 1.0
    
    show text "{size=52}{color=#FFFFFF}Game Over{/color}{/size}\n{size=36}{color=#FF6B6B}露馅被斬{/color}{/size}" at truecenter with dissolve:
        pause 4.0
    hide text
    
    pause 1.0
    
    # 返回主菜单
    return