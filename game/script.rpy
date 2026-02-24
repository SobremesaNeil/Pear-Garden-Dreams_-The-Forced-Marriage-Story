# 游戏的脚本可置于此文件中。

################################################################################
## 初始化阶段：OOC 系统核心设置
################################################################################

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


# 游戏在此开始。

label start:
    
    # 第一场景：破败小屋 - 黄昏
    scene bg broken_cottage_dusk
    
    # 出现小莲，病态的样子
    show lian sick at center
    
    me "小莲，我给你带来了白面窝头。"
    
    me "虽然不多，但这是我能找到的最好的。"
    
    lian "咳咳……谢谢你……"
    
    lian "你为我做了这么多……我真是……"
    
    # 小莲剧烈咳嗽
    lian "咳咳咳！"
    
    # 在这里可以添加吐血的图片或效果
    lian "咳……"
    
    me "小莲！"
    
    # 主角内心独白
    me "只要能救小莲……做什么都行。"
    
    me "就算搭上我的命，我也在所不惜。"
    
    # 场景转换到戏班后台
    scene bg backstage
    
    # 主角手指被扎破，血滴在书上的特效
    me "啊……"
    
    # 显示刺痛和血滴的描述
    me "手指被扎破了……"
    
    me "血滴在了这本古籍上……"
    
    # 穿越时刻 - 显示 ooc_hud
    show screen ooc_hud
    
    # 穿越特效
    me "这是……什么……"
    
    me "眼前突然一黑……"
    
    # 场景切换到穿越后的世界（可自定义背景）
    scene bg ancient_world
    
    me "这里是……哪里？"
    
    # 进入虚空，复原脸谱的小游戏环节
    me "眼前是一片虚无的空间……"
    
    me "我需要复原被碎裂的脸谱……"
    
    menu:
        "　[手动拼合] 仔细将碎片拼合":
            $ update_ooc(-20)
            me "我深吸一口气，开始仔细地拼合每一个碎片……"
            me "一点一点地，脸谱在我手中慢慢复原了……"
        
        "　[一键开挂 (Skip)]":
            $ update_ooc(-20)
            $ cheat_count += 1
            me "算了，我直接跳过这个步骤……"
            me "以某种不可思议的力量，碎片在瞬间复原了。"
    
    # 系统提示
    me "[系统] 脸谱已复原。"
    me "[系统] 正式进入第一幕……"
    
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
        "　(A) [卑微叩首] 连忙跪地道歉":
            $ update_ooc(-10)
            me "对……对不起！我知道错了！"
            me "请您饶恕我这一次……"
            hong "哼。算你有眼力见。"
            jump act1_continuing_story
        
        "　(B) [挺直腰板，危险] 抬起头，与他对视":
            $ update_ooc(25)
            me "我……我没有做错什么！"
            hong "你说什么呢？你敢对我顶嘴？"
            
            # B的二次选择
            menu:
                "　(B1) [继续争辩] 毫不退缩地辩论":
                    $ update_ooc(75)
                    me "就是这样！我要说出来！"
                    me "你不能这样对……"
                    hong "你找死！"
                    jump game_over
                
                "　(B2) [紧急求饶] 意识到危险，立即低眉顺眼":
                    $ update_ooc(-10)
                    me "我……我说错了，对不起……"
                    hong "哼，这样才对。"
                    jump act1_continuing_story

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

# 继续正常剧情
label act1_continuing_story:

    scene bg hong_mansion
    show hong neutral at center
    hong "从现在开始，你就听我的安排。"
    me "是……"
    hong "那个兰中玉啊，打进府后就茶饭不思。"
    hong "好几天了，一粒米都不肯吃。"
    hong "再这样下去，她要反水就麻烦了。"
    me "大人，或许……我有个办法。"
    hong "什么办法？"
    me "既然她是自愿嫁给您的，那就让她看到婚书。"
    me "只要她看到了婚书，确认了身份，就不会再有心结。"
    hong "婚书？我这里还真没有……"
    me "不如就……由我来写一份？"
    hong "你会写这样的文书？"
    me "我曾在县衙做过文书。这点小事不在话下。"
    me "而且，我可以加入一些细节，让婚书更具说服力。"
    me "比如，三日前在庙会上，您就已经当众收了十两银子并按下了手印。"
    hong "妙啊！这样一来，就更显得名正言顺了。"
    hong "那就劳烦你了。"
    jump forged_document_minigame

# 玩法环节 2：伪证
label forged_document_minigame:
    $ ooc_checkpoint = ooc_value
    me "我拿起毛笔，墨已经磨好了。"
    me "笔尖在纸上，我开始描红……"
    me "首先，就是那最关键的'婚'字。"
    menu:
        "　[认真描红] 完美写下'婚'字":
            $ update_ooc(-20)
            me "我沉下心来，笔画一个一个地落下。"
            me "每一笔都是精心雕琢，笔锋有力但不失柔和。"
            me "最后一笔收笔，完美。"
            show hong happy at center
            hong "哈哈！好字！"
            hong "这笔迹，足以骗过任何人。"
            hong "你这小子，真有一手啊。"
            hong "给，这是赏赐你的。"
            me "感谢大人！"
            jump forged_document_success
        "　[描红失败] 字迹歪扭":
            $ update_ooc(10)
            me "我笔颤抖了一下……"
            me "最后一笔没有把握好，字看起来歪歪斜斜。"
            show hong frown at center
            hong "嗯？这笔迹……有点问题啊。"
            hong "太草率了。重写！"
            me "是……立刻重写……"
            jump forged_document_minigame
        "　[一键开挂 (Auto-Write)]":
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
    play music "audio/heartbeat_tense.ogg" loop
    
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
    潜行小游戏：连续选对 3 个方向避开家丁巡逻
    - 选对：stealth_correct_steps + 1，继续游戏
    - 选错：OOC + 30，屏幕闪红，重新开始
    - 开挂：OOC - 50，cheat_count + 1，直接获胜
    """
    
    # 重置潜行步数计数
    $ stealth_correct_steps = 0
    
    # 显示 HUD
    show screen stealth_minigame
    
    # 游戏循环
    label stealth_game_loop:
        
        # 随机生成目标方向
        $ import random
        $ stealth_target_direction = random.choice(["left", "forward", "right"])
        
        # 显示提示信息
        me "前方是十字路口，我听到了家丁的脚步声……"
        
        # 调用 stealth_minigame screen，等待玩家输入
        $ result = renpy.call_screen("stealth_minigame")
        
        # 处理玩家的选择
        if result == stealth_target_direction:
            # ========== 选择正确 ==========
            $ stealth_correct_steps += 1
            
            # 提示正确
            show text "正确！你成功躲过了家丁的视线。" at truecenter with vpunch
            pause 1.5
            hide text
            
            # 检查是否已经连续成功 3 次
            if stealth_correct_steps >= 3:
                # 潜行成功！
                hide screen stealth_minigame
                jump scene_5_5_stealth_success
            else:
                # 继续游戏
                pause 0.5
                jump stealth_game_loop
        
        elif result == "cheat":
            # ========== 使用一键开挂 ==========
            $ update_ooc(-50)
            $ cheat_count += 1
            
            hide screen stealth_minigame
            
            me "我仿佛分裂成了两个世界……"
            me "身体在一个次元行动，而家丁们的目光无法捕捉到我。"
            pause 1.0
            me "转眼间，我已经出现在了偏房外。"
            pause 0.5
            
            jump scene_5_5_stealth_success
        
        else:
            # ========== 选择错误 ==========
            $ update_ooc(30)
            $ stealth_correct_steps = 0  # 重置步数
            
            # 屏幕闪红效果
            show text "错误！你被家丁发现了！" at truecenter with flash
            pause 1.0
            hide text
            
            # 检查 OOC 值是否达到致命值
            $ check_ooc()
            
            # 如果还活着，重新提示
            show text "警报！你的行动惊动了家丁！必须重新规划路线！" at truecenter
            pause 2.0
            hide text
            
            me "不行！我得重新规划……"
            pause 0.5
            
            # 重置游戏，再试一次
            jump stealth_game_loop

################################################################################
## SCENE 5.5.2：潜行成功 - 救出兰中玉
################################################################################

label scene_5_5_stealth_success:
    """
    潜行成功，主角成功到达兰中玉的偏房。
    """
    
    # 停止背景音乐
    stop music
    
    # 场景：洪府偏房内（昏暗的烛光）
    scene bg hong_study_night
    
    # 播放柔和的背景音乐
    play music "audio/quiet_night.ogg" loop
    
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
        "　(A) [压低身形，贴墙潜行] 悄悄避开家丁":
            # OOC 不变，进入潜行小游戏
            jump stealth_minigame
        
        "　(B) [大摇大摆前行] 反正我是师爷":
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
        "　[路线正确] 成功避开巡逻到达县衙":
            $ update_ooc(-15)
            me "完美！我避开了所有的巡逻队。"
            me "前面就是县衙的后门了。"
            jump zhang_study_confession
        
        "　[走错断开] 惊动家丁":
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
        
        "　[一键开挂 (Skip)]":
            $ update_ooc(-50)
            $ cheat_count += 1
            me "我仿佛分裂成了两个世界……"
            me "身体在一个次元行动，而家丁们的目光无法捕捉到我。"
            me "转眼间，我已经出现在了县衙后门。"
            jump zhang_study_confession

# 主角在书房面见知县
label zhang_study_confession:
    
    scene bg zhang_study with fade
    
    show zhang neutral at center
    
    zhang "是谁在半夜潜入我的书房？"
    
    me "大人……是我。"
    
    me "我冒死来见您，是为了自首。"
    
    zhang "自首？你是何人，为何要自首？"
    
    me "我叫贾斯文，是洪彦龙的师爷。"
    
    me "我的身份是假的。我被强行卷入了一桩婚姻欺诈案。"
    
    me "兰中玉的婚书是我伪造的，整个事件的始末都是……"
    
    # 主角开始表演，飙演技自首
    me "我已经认清了自己的罪恶。我希望以诚恳的态度，"
    
    me "换取您的怜悯和法律的制裁。"
    
    zhang "好。你的勇气值得表扬。但具体的细节，"
    
    zhang "我们在公堂上再仔细审理。"
    
    jump act3_courtroom

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
    scene bg courtroom
    
    # 背景音乐：庄严的公堂主题
    play music "audio/courtroom_theme.ogg" loop
    
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
    
    zhang "【立此为证】是粗鲁的商人用语，充满铜臭味。"
    zhang "而一份郑重其事的婚书，应该用【谨立】、【特立】这样的文人雅言。"
    
    hide text
    
    zhang "你这样的伪造痕迹，实在太明显了！"
    
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
    play sound "audio/gavel_bang.ogg"
    show text "【惊堂木】" at truecenter with vpunch
    pause 0.3
    hide text
    
    zhang "荒唐！本官要审问的是……贾斯文！"
    
    me "……是！"
    
    # 场景镜头转向主角
    show me neutral at center
    hide hong
    hide zhang
    
    pause 1.0
    
    # ========================================
    # 关键选择菜单：配合知县的审判节奏
    # ========================================
    
    zhang "贾斯文！这份婚书，真的是你写的吗？还是……洪彦龙强迫你？"
    
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
            zhang "嗯？你这小子，倒是急于翻脸啊……"
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
            zhang "第一个问题：洪彦龙给了你多少好处？"
        elif dwrg_attempt_count == 2:
            zhang "那么，第二个问题：他是何时强迫你的？"
        else:
            zhang "证据呢？你有什么证据？"
        
        # 调用 dwrg_trial screen 等待玩家输入
        $ dwrg_result_raw = renpy.call_screen("dwrg_trial", round_num=dwrg_attempt_count)
        
        # ========== 处理玩家的选择 ==========
        
        if dwrg_result_raw == "attempt_hit":
            # 玩家点击了"拍案"，检查时机是否正确（指针在绿色区）
            if 0.3 <= dwrg_pointer_pos <= 0.7:
                # ========== 完美命中！==========
                $ update_ooc(-15)
                
                play sound "audio/gavel_bang.ogg"
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
                    zhang "从你们两人的言辞反差，本官已经看清楚了！"
                    
                    # 连续两个完美回答，可以直接宣判
                    jump act3_courtroom_success
                
                # 继续下一轮
                pause 1.0
                jump dwrg_round_begin
            
            else:
                # ========== 时机不对，击中了危险区 ==========
                $ update_ooc(10)
                
                show text "【节奏被破坏！】" at truecenter with flash
                pause 0.5
                hide text
                
                if dwrg_attempt_count == 1:
                    me "我……五十两……不是……"
                elif dwrg_attempt_count == 2:
                    me "我……我不清楚具体时间……"
                else:
                    me "证据？我……哪有什么证据……"
                
                show zhang frown at center
                zhang "吞吞吐吐！看来你在隐瞒什么！"
                
                hong "哈哈！你们瞧瞧，这小子都说不出个所以然来！"
                
                # 检查 OOC，如果达到致命值就 Game Over
                $ check_ooc()
                
                # 否则允许重新尝试
                me "不……不是这样的，大人……"
                pause 1.0
                jump dwrg_round_begin
        
        elif dwrg_result_raw == "miss":
            # ========== 超时，时间耗尽 ==========
            $ update_ooc(10)
            
            show text "【时间耗尽！】" at truecenter with flash
            pause 0.5
            hide text
            
            me "我……我的话还没说完……"
            
            show zhang angry at center
            zhang "大胆！你在本官面前还要支吾其辞？"
            
            # 检查 OOC 是否达到致命值
            $ check_ooc()
            
            # 否则允许重试
            me "大人，请再给我一次机会……"
            pause 1.0
            jump dwrg_round_begin
        
        elif dwrg_result_raw == "cheat":
            # ========== 使用一键开挂 ==========
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
            zhang "好了！本官已经听够了。证据确凿，毋庸置疑。"
            
            # 直接跳到成功
            jump act3_courtroom_success

# 公堂对峙成功
label act3_courtroom_success:
    scene bg courtroom
    show zhang satisfied at center
    
    zhang "洪彦龙！根据本官的审理，你犯有以下罪名："
    zhang "伪造婚书罪、人身威胁罪、婚约欺诈罪……"
    
    show hong desperate at left
    hong "大人……大人饶命啊！"
    
    zhang "来人！将洪彦龙打入死牢，等候处斩！"
    
    me "（……终于……结束了。）"
    
    pause 1.0
    
    jump act3_ending

# 第三幕结尾
    scene bg courtroom
    show zhang neutral at center
    me "经过这一次的磨难，我似乎更理解了这个世界……"
    me "脸谱在逐渐复原，人生的故事也在继续……"
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