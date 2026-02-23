# OOC UI 脸谱状态显示屏幕，带有动画效果
screen ooc_ui():
    zorder 100
    
    if ooc_value >= 100:
        # 100%：显示特殊状态，准备跳转到 Death 标签
        add Solid("#FF0000", xysize=(config.screen_width, config.screen_height)) at heartbeat_red
        text "脸谱已经完全碎裂..." xpos 0.5 ypos 0.5 xanchor 0.5 yanchor 0.5 size 30 color "#FFFFFF" at ooc_fadein
    elif ooc_value >= 71:
        # 71-99%：危险区，加红色暗角覆盖层，使用心跳动画
        add Solid("#FF0000", xysize=(config.screen_width, config.screen_height)) at heartbeat_red
        text "[危险区] 脸谱大面积碎裂" xpos 20 ypos 20 size 20 color "#FF0000" at ooc_fadein
    elif ooc_value >= 31:
        # 31-70%：警告区
        text "[警告区] 脸谱出现裂纹" xpos 20 ypos 20 size 20 color "#FFFF00" at ooc_fadein
    else:
        # 0-30%：安全区
        text "[安全区] 脸谱完整" xpos 20 ypos 20 size 20 color "#FFFFFF" at ooc_fadein        hbox:
            spacing 50
            xalign 0.5
            background Solid("#000000AA")
            padding (20, 10)
            
            # 按钮1：点击校准
            textbutton "[点击校准]":
                xsize 150
                text_idle_color "#FFFFFF"
                text_hover_color "#FFD700"
                action Return("success")
            
            # 按钮2：一键开挂
            textbutton "[一键开挂]":
                xsize 150
                text_idle_color "#FFFFFF"
                text_hover_color "#FFD700"
                action Return("cheat")# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define me = Character("贾斯文", color="#808080")
define lian = Character("小莲", color="#FF69B4")
define hong = Character("洪彦龙", color="#8B0000")
define zhang = Character("张清", color="#228B22")
define lan = Character("兰中玉", color="#4682B4")

# 定义核心 Python 变量。
define ooc_value = 20
define cheat_count = 0
define qte_fail_count = 0

# 定义函数 update_ooc。
# 这个函数用于增减 ooc_value，并确保其值始终在 0 到 100 之间。
# 当 cheat_count >= 3 时，ooc_value 被强制锁定在 99（游戏平衡被破坏的状态）。
def update_ooc(amount):
    global ooc_value, cheat_count
    if cheat_count >= 3:
        # 如果使用开挂次数达到 3 次，强制锁定 ooc_value 为 99
        ooc_value = 99
    else:
        # 正常情况下，按照 amount 修改 ooc_value，并确保在 0-100 之间
        ooc_value = max(0, min(100, ooc_value + amount))

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
    
    # 穿越时刻 - 显示 ooc_ui
    show screen ooc_ui
    
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
    hide screen ooc_ui
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
    hide screen ooc_ui
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
    hide screen ooc_ui
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
    
    # 保存当前 ooc_value，以备 game_over 重置
    $ ooc_checkpoint = ooc_value
    
    # 场景：衙门公堂
    scene bg courtroom
    
    show zhang angry at center
    
    # 知县发难
    zhang "贾斯文！你敢欺瞒本官？"
    
    zhang "在堂下认罪，还是继续狡辩！"
    
    me "我……"
    
    me "我有话要说。"
    
    # 进入 QTE 小游戏
    jump qte_minigame

# QTE 小游戏标签
label qte_minigame:
    
    # 初始化本次 QTE 的失败次数计数器
    $ qte_fail_count = 0
    
    # 显示 QTE 场景
    zhang "机会只有一次！"
    
    me "我必须完美把握这一刻……"
    
    # 进入 QTE 判定条 screen
    label qte_attempt:
        
        $ qte_result = renpy.call_screen("qte_bar", time_limit=3.0)
        
        if qte_result == "success":
            # 成功校准
            $ update_ooc(-15)
            # play sound "audio/gavel.ogg"  # 惊堂木音效
            # 播放惊堂木音效（注释可启用）
            show text "【校准成功！】" at truecenter with flash
            pause 1.0
            hide text
            
            show hong shocked at center
            hong "你……你这小子！"
            hong "竟然敢在本官面前如此大胆！"
            
            me "大人！请听我分辩！"
            
            jump act3_courtroom_success
        
        elif qte_result == "fail":
            # 失败（超时或点错）
            $ update_ooc(10)
            $ qte_fail_count += 1
            
            show text "【校准失败！】" at truecenter with flash
            pause 1.0
            hide text
            
            me "我……我的话还没说完……"
            zhang "大胆！你在本官面前还敢言辞闪烁？"
            
            # 检查是否已失败 3 次且 OOC >= 90
            if qte_fail_count >= 3 and ooc_value >= 90:
                # 达到死亡条件
                me "不……不是的……"
                zhang "你这种人，死不足惜！"
                jump game_over
            else:
                # 允许重试
                me "大人，请再给我一次机会……"
                zhang "好吧。最后一次。"
                jump qte_attempt
        
        elif qte_result == "cheat":
            # 一键开挂
            $ cheat_count += 1
            
            if cheat_count >= 3:
                # 强制锁定 OOC 为 99
                $ ooc_value = 99
                zhang "这位看官，戏……可不是这么听的。"
                me "什……什么？"
                jump game_over
            else:
                # 正常开挂效果
                $ update_ooc(-50)
                show text "【一键开挂激活！】" at truecenter with flash
                pause 1.0
                hide text
                
                me "我仿佛有了某种超越凡人的力量……"
                me "字字珠玑，滴水不漏。"
                
                show hong amazed at center
                hong "这……这怎么可能！"
                
                jump act3_courtroom_success

# 公堂对峙成功
label act3_courtroom_success:
    scene bg courtroom
    show zhang neutral at center
    zhang "既然如此，本官就饶你一命。"
    zhang "但你欠本官一个人情。"
    me "多谢大人开恩。"
    jump act3_ending

# 公堂对峙失败（但未触发 Game Over）
label act3_courtroom_failed:
    scene bg courtroom
    show zhang angry at center
    zhang "来人！将贾斯文打入大牢！"
    me "大人，请再听我一言……"
    # 这里可以添加返回菜单或继续故事的逻辑
    jump qte_minigame

# 第三幕结尾
label act3_ending:
    scene bg courtroom
    show zhang neutral at center
    me "经过这一次的磨难，我似乎更理解了这个世界……"
    me "脸谱在逐渐复原，人生的故事也在继续……"
    jump epilogue

# 尾声：根据 OOC 值选择结局
label epilogue:
    
    # 场景：戏班后台，主角醒来
    hide screen ooc_ui
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
