# 游戏的脚本可置于此文件中。

# 声明此游戏使用的角色。颜色参数可使角色姓名着色。

define me = Character("贾斯文", color="#808080")
define lian = Character("小莲", color="#FF69B4")
define hong = Character("洪彦龙", color="#8B0000")
define zhang = Character("张清", color="#228B22")

# 定义核心 Python 变量。
define ooc_value = 20
define cheat_count = 0

# 定义函数 update_ooc。
def update_ooc(amount):
    global ooc_value, cheat_count
    if cheat_count >= 3:
        ooc_value = 99
    else:
        ooc_value = max(0, min(100, ooc_value + amount))

# 定义 ooc_ui screen，用于显示脸谱状态。
screen ooc_ui():
    zorder 100
    
    if ooc_value >= 100:
        # 100%：显示特殊状态，准备跳转到 Death 标签
        add Solid("#FF0000", xysize=(config.screen_width, config.screen_height)) alpha 0.5
        text "脸谱已经完全碎裂..." xpos 0.5 ypos 0.5 xanchor 0.5 yanchor 0.5 size 30 color "#FFFFFF"
    elif ooc_value >= 71:
        # 71-99%：危险区，加红色暗角覆盖层
        add Solid("#FF0000", xysize=(config.screen_width, config.screen_height)) alpha 0.3
        text "[危险区] 脸谱大面积碎裂" xpos 20 ypos 20 size 20 color "#FF0000"
    elif ooc_value >= 31:
        # 31-70%：警告区
        text "[警告区] 脸谱出现裂纹" xpos 20 ypos 20 size 20 color "#FFFF00"
    else:
        # 0-30%：安全区
        text "[安全区] 脸谱完整" xpos 20 ypos 20 size 20 color "#FFFFFF"

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
    return

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
    
    # 显示 QTE 菜单
    zhang "机会只有一次！"
    
    me "我必须完美把握这一刻……"
    
    menu:
        "　[完美校准] (需要在 3 秒内点击)":
            $ update_ooc(-15)
            me "我清晰地陈述了所有的事实。"
            me "证据确凿，无可辩驳。"
            zhang "哼……你这条舌头确实厉害。"
            jump act3_courtroom_success
        
        "　[校准失败] (等待超时或点错)":
            $ update_ooc(10)
            me "我……我的话还没说完……"
            zhang "大胆！你在本官面前还敢言辞闪烁？"
            me "不……不是的……"
            jump act3_courtroom_failed
        
        "　[一键开挂 (Auto-Hit)]":
            $ cheat_count += 1
            
            if cheat_count >= 3:
                # 强制锁定 OOC 为 99
                $ ooc_value = 99
                zhang "这位看官，戏……可不是这么听的。"
                me "什……什么？"
                jump game_over
            else:
                $ update_ooc(-50)
                me "我仿佛有了某种超越凡人的力量……"
                me "字字珠玑，滴水不漏。"
                zhang "这……这怎么可能！"
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
