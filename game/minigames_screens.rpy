"""
三大交互小游戏的 Ren'Py Screen 定义
集成脸谱复原、伪造婚书、深夜潜行
"""

################################################################################
## 小游戏 1：脸谱复原（拖拽拼图）
################################################################################

screen puzzle_restoration():
    """
    脸谱碎片拼图小游戏屏幕
    玩家通过拖拽碎片到中心目标区域来完成脸谱复原
    """
    zorder 100
    modal True
    
    # 背景暗化
    add Solid("#000000", xysize=(config.screen_width, config.screen_height)):
        alpha 0.6
    
    # 标题
    text "【脸谱复原】拖拽碎片拼凑完整的脸谱" size 28 color "#FFD700" xalign 0.5 ypos 50
    
    # 目标放置区域（中心）
    vbox:
        xalign 0.5
        yalign 0.5
        
        # 标记目标区域
        frame:
            background Solid("#1a1a1a")
            padding (20, 20)
            xysize (400, 400)
            
            # 目标区域背景或网格
            add Solid("#333333"):
                xysize (360, 360)
            
            # 【这里应该添加目标脸谱的轮廓或半透明背景】
            # add "images/puzzle_target_outline.png"  # 可选
    
    # 拖拽区域（DragGroup）
    # 注：DragGroup 需要在 init python 中创建拖拽对象
    if puzzle_game and puzzle_game.fragments:
        fixed:
            # 为每个碎片创建拖拽对象
            for fragment in puzzle_game.fragments:
                drag:
                    drag_name f"fragment_{fragment.id}"
                    draggable True
                    xoffset 0
                    yoffset 0
                    
                    # 如果已经吸附，显示在目标位置；否则显示在当前拖拽位置
                    if fragment.is_snapped:
                        xpos fragment.target_x - 50
                        ypos fragment.target_y - 50
                    else:
                        xpos 50 + fragment.id * 100
                        ypos 600
                    
                    # 碎片图像
                    add fragment.image_path xysize (100, 100)
    
    # 底部操作按钮
    vbox:
        xalign 0.5
        ypos 850
        spacing 20
        
        # 一键开挂按钮
        textbutton "【一键开挂】完美复原" xalign 0.5 xysize (300, 60) text_size 18:
            action Return("cheat")
        
        # 重置按钮（可选）
        textbutton "【重置】重新开始" xalign 0.5 xysize (300, 60) text_size 18:
            action Return("reset")
    
    # 计时器：检查碎片是否靠近目标位置
    timer 0.1 action Function(_check_puzzle_snapping) repeat True


init python:
    def _check_puzzle_snapping():
        """检查碎片是否应该吸附到目标位置"""
        if puzzle_game is None:
            return
        
        for fragment in puzzle_game.fragments:
            if not fragment.is_snapped:
                # 这里会在拖拽时检查距离
                # Ren'Py 的 drag 对象会自动更新位置
                # 需要在 event 处理中实现吸附逻辑
                pass
        
        # 检查是否全部完成
        if puzzle_game.check_completion():
            renpy.play("sound", "audio/success_chime.ogg")
            # 短暂显示完成提示后返回成功
            renpy.show_screen("_puzzle_success_popup")


screen _puzzle_success_popup():
    """完成提示"""
    zorder 200
    text "脸谱复原成功！" size 32 color "#00FF00" xalign 0.5 yalign 0.5
    timer 1.0 action Hide("_puzzle_success_popup")


################################################################################
## 小游戏 2：伪造婚书（汉字描红 / 轨迹追踪）
################################################################################

screen stroke_writing():
    """
    汉字描红笔画追踪小游戏屏幕
    玩家通过鼠标拖拽绘制笔画，系统检测笔画顺序和精准度
    """
    zorder 100
    modal True
    
    # 背景暗化
    add Solid("#000000", xysize=(config.screen_width, config.screen_height)):
        alpha 0.6
    
    # 标题和说明
    vbox:
        xalign 0.5
        ypos 30
        spacing 10
        
        text "【伪造婚书】在规定时间内按笔画顺序描红「婚」字" size 24 color "#FFD700" xalign 0.5
        text f"剩余时间：{stroke_tracker.get_remaining_time(renpy.get_time()):.1f} 秒 | 进度：{stroke_tracker.last_ordered_checkpoint + 1}/{len(stroke_tracker.checkpoints)}" size 14 color "#FFFFFF" xalign 0.5
    
    # 绘制区域
    vbox:
        xalign 0.5
        ypos 150
        
        # 背景字体（「婚」字）
        frame:
            background Solid("#1a1a1a")
            padding (10, 10)
            xysize (400, 400)
            
            # 【替换为实际的背景图片】
            # add stroke_tracker.bg_image
            
            # 使用 Custom 或纯色占位
            add Solid("#333333"):
                xysize (380, 380)
            
            # 【这里会动态绘制笔画轨迹】
            # 需要使用自定义 Displayable 或 Canvas
    
    # 检查点提示（显示已触发的检查点）
    hbox:
        xalign 0.5
        ypos 600
        spacing 10
        
        for i, checkpoint in enumerate(stroke_tracker.checkpoints):
            if checkpoint.is_triggered:
                text f"✓{i+1}" size 16 color "#00FF00"
            else:
                text f"○{i+1}" size 16 color "#FFFFFF"
    
    # 错误提示（如果笔画不连贯）
    if stroke_tracker.last_ordered_checkpoint >= 0:
        text "按照笔顺继续描红……" xpos 50 ypos 700 size 14 color "#FFD700"
    else:
        text "请从第一个检查点开始……" xpos 50 ypos 700 size 14 color "#FF6B6B"
    
    # 底部操作按钮
    vbox:
        xalign 0.5
        ypos 800
        spacing 20
        
        # 确认按钮
        textbutton "【确认提交】" xalign 0.5 xysize (300, 60) text_size 18:
            action Function(_submit_stroke_result)
        
        # 一键开挂
        textbutton "【一键开挂】神笔马良" xalign 0.5 xysize (300, 60) text_size 18:
            action Return("cheat")
        
        # 清除重来
        textbutton "【清除】重新开始" xalign 0.5 xysize (300, 60) text_size 18:
            action Function(_clear_stroke)
    
    # 实时更新计时器
    timer 0.01 action NullAction() repeat True


init python:
    def _submit_stroke_result():
        """提交笔画结果"""
        if stroke_tracker is None:
            return
        
        # 检查是否完成
        if stroke_tracker.is_completed():
            renpy.play("sound", "audio/success_chime.ogg")
            renpy.return_value("success")
        else:
            renpy.play("sound", "audio/error_buzzer.ogg")
            # 显示失败提示
            remaining = len(stroke_tracker.checkpoints) - (stroke_tracker.last_ordered_checkpoint + 1)
            renpy.show_screen("_stroke_fail_popup", remaining)
    
    def _clear_stroke():
        """清除笔画，重新开始"""
        if stroke_tracker is None:
            return
        stroke_tracker.current_path = []
        stroke_tracker.last_ordered_checkpoint = -1
        for cp in stroke_tracker.checkpoints:
            cp.is_triggered = False


screen _stroke_fail_popup(remaining):
    """失误提示"""
    zorder 200
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20
        
        text f"笔画不完整！还差 {remaining} 笔" size 24 color "#FF6B6B"
        text "请清除后重新描红" size 16 color "#FFFFFF"
    
    timer 2.0 action Hide("_stroke_fail_popup")


################################################################################
## 小游戏 3：深夜潜行（九宫格一笔画）
################################################################################

screen nine_puzzle_path():
    """
    九宫格一笔画小游戏屏幕
    玩家从左上角(0)出发，需要到达右下角(8)，路径中避开危险路线
    """
    zorder 100
    modal True
    
    # 背景暗化
    add Solid("#000000", xysize=(config.screen_width, config.screen_height)):
        alpha 0.6
    
    # 标题
    text "【深夜潜行】一笔画从左上角走到右下角，避开危险巡逻队" size 22 color "#FFD700" xalign 0.5 ypos 30
    
    # 网格显示区域
    vbox:
        xalign 0.5
        ypos 120
        spacing 40
        
        # 九宫格（3x3）
        default node_positions = {
            0: (200, 270),   3: (200, 420),   6: (200, 570),
            1: (400, 270),   4: (400, 420),   7: (400, 570),
            2: (600, 270),   5: (600, 420),   8: (600, 570),
        }
        
        # 绘制节点和连线
        fixed:
            xysize (800, 400)
            xalign 0.5
            
            # 首先绘制已经走过的路径（绿线）
            if nine_puzzle_game and nine_puzzle_game.path_edges:
                # 绘制路径边
                for edge in nine_puzzle_game.path_edges:
                    $ node_a, node_b = edge
                    $ x1, y1 = node_positions.get(node_a, (0, 0))
                    $ x2, y2 = node_positions.get(node_b, (0, 0))
                    
                    # 绘制线条（从 node_a 到 node_b）
                    add Line((x1, y1), (x2, y2), "#00FF00", 3)
            
            # 绘制危险路线（红虚线）
            if nine_puzzle_game:
                for danger_edge in nine_puzzle_game.dangerous_edges:
                    $ node_a, node_b = danger_edge
                    $ x1, y1 = node_positions.get(node_a, (0, 0))
                    $ x2, y2 = node_positions.get(node_b, (0, 0))
                    
                    # 绘制红色虚线
                    add Line((x1, y1), (x2, y2), "#FF0000", 2, dash_pattern=[5, 5])
            
            # 绘制节点
            for node_num in range(9):
                $ x, y = node_positions.get(node_num, (0, 0))
                
                # 判断节点的状态
                $ is_current = (nine_puzzle_game and node_num == nine_puzzle_game.current_path[-1])
                $ is_visited = (nine_puzzle_game and node_num in nine_puzzle_game.current_path)
                $ is_start = (node_num == 0)
                $ is_end = (node_num == 8)
                
                # 绘制节点圆圈
                if is_end:
                    # 终点（目标）：金色光环
                    add Circle(20, color="#FFD700"):
                        xpos x - 10
                        ypos y - 10
                    text "8\n(终)" xpos x - 25 ypos y + 25 size 12 color "#FFD700"
                elif is_start:
                    # 起点：蓝色
                    add Circle(20, color="#4169E1"):
                        xpos x - 10
                        ypos y - 10
                    text "0\n(起)" xpos x - 25 ypos y + 25 size 12 color="#4169E1"
                elif is_current:
                    # 当前节点：闪烁光芒
                    add Circle(18, color="#00FF00"):
                        xpos x - 9
                        ypos y - 9
                        at pulse_animation
                    text str(node_num) xpos x - 5 ypos y - 5 size 14 color "#000000"
                elif is_visited:
                    # 已访问：绿色
                    add Circle(15, color="#00AA00"):
                        xpos x - 7
                        ypos y - 7
                    text str(node_num) xpos x - 5 ypos y - 5 size 12 color "#FFFFFF"
                else:
                    # 未访问：灰色或白色
                    add Circle(12, color="#CCCCCC"):
                        xpos x - 6
                        ypos y - 6
                    text str(node_num) xpos x - 5 ypos y - 5 size 12 color "#000000"
                
                # 节点可点击区域
                imagebutton:
                    xpos x - 20
                    ypos y - 20
                    xysize (40, 40)
                    idle Solid("#00000000")  # 透明按钮
                    hover Solid("#FFFF0022")  # 悬停时显示淡黄色
                    action Function(_try_move_nine_puzzle, node_num)
    
    # 当前路径显示
    text f"当前路径: {nine_puzzle_game.current_path if nine_puzzle_game else []}" xpos 50 ypos 600 size 12 color "#AAAAAA"
    
    # 底部操作按钮
    vbox:
        xalign 0.5
        ypos 750
        spacing 20
        
        # 撤销按钮
        textbutton "【撤销】回退一步" xalign 0.5 xysize (300, 50) text_size 16:
            action Function(_undo_nine_puzzle_step)
        
        # 一键开挂
        textbutton "【一键开挂】分身之术" xalign 0.5 xysize (300, 50) text_size 16:
            action Return("cheat")
        
        # 重置
        textbutton "【重置】重新开始" xalign 0.5 xysize (300, 50) text_size 16:
            action Function(_reset_nine_puzzle)


# 动画定义
transform pulse_animation:
    alpha 0.6
    linear 0.3 alpha 1.0
    linear 0.3 alpha 0.6
    repeat


init python:
    def _try_move_nine_puzzle(node_num):
        """尝试在九宫格中移动到指定节点"""
        if nine_puzzle_game is None:
            return
        
        success, msg = nine_puzzle_game.move_to(node_num)
        
        if not success:
            # 触发危险路线
            if "危险" in msg:
                renpy.play("sound", "audio/alarm.ogg")
                renpy.show_screen("_danger_alert_popup", msg)
                renpy.return_value("fail")
            else:
                renpy.play("sound", "audio/error_buzzer.ogg")
                renpy.show_screen("_invalid_move_popup", msg)
        else:
            # 成功移动
            renpy.play("sound", "audio/click.ogg")
            
            # 检查是否到达终点
            if node_num == 8:
                renpy.play("sound", "audio/success_chime.ogg")
                renpy.show_screen("_nine_puzzle_success_popup")
                renpy.return_value("success")
    
    def _undo_nine_puzzle_step():
        """撤销上一步"""
        if nine_puzzle_game is None or len(nine_puzzle_game.current_path) <= 1:
            return
        
        # 移除最后一个节点和对应的边
        removed_node = nine_puzzle_game.current_path.pop()
        if len(nine_puzzle_game.current_path) > 0:
            last_edge = (nine_puzzle_game.current_path[-1], removed_node)
            nine_puzzle_game.path_edges.discard(last_edge)
            reversed_edge = (removed_node, nine_puzzle_game.current_path[-1])
            nine_puzzle_game.path_edges.discard(reversed_edge)
        
        renpy.play("sound", "audio/undo_sound.ogg")
    
    def _reset_nine_puzzle():
        """重置九宫格"""
        if nine_puzzle_game is None:
            return
        nine_puzzle_game.reset()
        renpy.play("sound", "audio/click.ogg")


screen _danger_alert_popup(msg):
    """触发危险提示"""
    zorder 200
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20
        
        text "⚠️ 触发巡逻队！" size 32 color "#FF0000"
        text msg size 18 color "#FF6B6B"
        text "你的行动暴露了！" size 16 color "#FFFFFF"
    
    timer 2.0 action Hide("_danger_alert_popup")


screen _invalid_move_popup(msg):
    """非法移动提示"""
    zorder 200
    text msg size 20 color "#FFD700" xalign 0.5 yalign 0.5
    timer 1.5 action Hide("_invalid_move_popup")


screen _nine_puzzle_success_popup():
    """成功到达终点"""
    zorder 200
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 20
        
        text "✓ 成功躲避！到达了目标地点" size 32 color "#00FF00"
        text "任务完成！" size 20 color "#FFD700"
    
    timer 1.5 action Hide("_nine_puzzle_success_popup")


################################################################################
## 工具内容（占位符 / Helper Displayables）
################################################################################

init python:
    """Ren'Py 原生 Canvas 绘图实现"""
    
    class Circle(renpy.Displayable):
        """
        圆形绘制 Displayable
        使用 Ren'Py 原生 canvas() API 绘制实心圆
        """
        def __init__(self, radius, color="#FFFFFF", **kwargs):
            super(Circle, self).__init__(**kwargs)
            self.radius = radius
            self.color = color
        
        def render(self, width, height, st, at):
            # 创建正方形 Canvas，边长为圆的直径
            canvas_size = self.radius * 2
            surf = renpy.Render(canvas_size, canvas_size)
            
            # 获取 Canvas 对象用于绘制
            canvas = surf.canvas()
            
            # 将色值字符串转换为 renpy.color.Color 对象
            try:
                color_obj = renpy.color.Color(self.color)
            except:
                color_obj = renpy.color.Color("#FFFFFF")
            
            # 绘制实心圆（圆心在 (radius, radius)，半径为 radius）
            canvas.circle(color_obj, (self.radius, self.radius), self.radius)
            
            return surf
    
    
    class Line(renpy.Displayable):
        """
        直线绘制 Displayable
        使用 Ren'Py 原生 canvas() API 绘制直线（支持虚线）
        """
        def __init__(self, start_pos, end_pos, color, width, dash_pattern=None, **kwargs):
            super(Line, self).__init__(**kwargs)
            self.start_pos = start_pos
            self.end_pos = end_pos
            self.color = color
            self.width = width
            self.dash_pattern = dash_pattern
        
        def render(self, width, height, st, at):
            # 创建一个覆盖足够大的 Canvas（包含两个端点）
            x1, y1 = self.start_pos
            x2, y2 = self.end_pos
            
            # 计算 Canvas 的尺寸和偏移量
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            
            # 添加一些边距（为了防止线条被裁剪）
            margin = self.width + 5
            canvas_width = int(max_x - min_x + margin * 2)
            canvas_height = int(max_y - min_y + margin * 2)
            
            # 防止 Canvas 尺寸过小
            if canvas_width < 1:
                canvas_width = 1
            if canvas_height < 1:
                canvas_height = 1
            
            surf = renpy.Render(canvas_width, canvas_height)
            canvas = surf.canvas()
            
            # 将色值字符串转换为 renpy.color.Color 对象
            try:
                color_obj = renpy.color.Color(self.color)
            except:
                color_obj = renpy.color.Color("#FFFFFF")
            
            # 调整坐标（相对于 Canvas 偏移）
            adjusted_start = (x1 - min_x + margin, y1 - min_y + margin)
            adjusted_end = (x2 - min_x + margin, y2 - min_y + margin)
            
            # 绘制线条
            if self.dash_pattern:
                # 虚线实现：使用多个短线段拼接
                self._draw_dashed_line(canvas, color_obj, adjusted_start, adjusted_end, 
                                      self.width, self.dash_pattern)
            else:
                # 实线绘制
                canvas.line(color_obj, adjusted_start, adjusted_end, self.width)
            
            return surf
        
        def _draw_dashed_line(self, canvas, color, start, end, width, dash_pattern):
            """
            绘制虚线
            dash_pattern: [dash_length, gap_length, ...]
            """
            import math
            
            x1, y1 = start
            x2, y2 = end
            
            # 计算线段总长度和方向
            total_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if total_len == 0:
                return
            
            # 单位方向向量
            dx = (x2 - x1) / total_len
            dy = (y2 - y1) / total_len
            
            # 交替绘制虚线段和空白段
            current_pos = 0.0
            pattern_idx = 0
            
            while current_pos < total_len:
                # 当前模式段长度
                segment_len = dash_pattern[pattern_idx % len(dash_pattern)]
                next_pos = min(current_pos + segment_len, total_len)
                
                # 计算端点坐标
                seg_start_x = x1 + dx * current_pos
                seg_start_y = y1 + dy * current_pos
                seg_end_x = x1 + dx * next_pos
                seg_end_y = y1 + dy * next_pos
                
                # 奇数索引是空白，偶数索引才绘制线段
                if pattern_idx % 2 == 0:
                    canvas.line(color, (seg_start_x, seg_start_y), 
                               (seg_end_x, seg_end_y), width)
                
                current_pos = next_pos
                pattern_idx += 1
