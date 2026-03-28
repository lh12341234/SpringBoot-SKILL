from PIL import Image, ImageDraw, ImageFont
import os
import math


def _mx_escape(text):
    text = str(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _write_drawio(filename, page_name, cells, page_width=1169, page_height=827):
    base, _ = os.path.splitext(filename)
    drawio_path = base + ".drawio"
    cells_xml = "\n".join(cells)
    xml = (
        f'<mxfile host="app.diagrams.net" modified="2026-03-12T00:00:00.000Z" agent="codex" version="22.1.0">\n'
        f'  <diagram id="d1" name="{_mx_escape(page_name)}">\n'
        f'    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{int(page_width)}" pageHeight="{int(page_height)}" math="0" shadow="0">\n'
        f'      <root>\n'
        f'        <mxCell id="0"/>\n'
        f'        <mxCell id="1" parent="0"/>\n'
        f'{cells_xml}\n'
        f'      </root>\n'
        f'    </mxGraphModel>\n'
        f'  </diagram>\n'
        f'</mxfile>\n'
    )
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml)


def create_usecase_drawio(filename, actor_name, use_cases):
    height = max(500, len(use_cases) * 100 + 100)
    actor_x, actor_y, actor_w, actor_h = 90, height // 2 - 28, 120, 56
    uc_x, uc_w, uc_h = 400, 180, 70
    start_y = (height - len(use_cases) * 100) // 2

    cells = []
    cells.append(
        f'<mxCell id="actor1" value="{_mx_escape(actor_name)}" style="rounded=0;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=20;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="1"><mxGeometry x="{actor_x}" y="{actor_y}" width="{actor_w}" height="{actor_h}" as="geometry"/></mxCell>'
    )

    for i, case in enumerate(use_cases):
        uc_id = f"uc{i+1}"
        y = start_y + i * 100
        cells.append(
            f'<mxCell id="{uc_id}" value="{_mx_escape(case)}" style="ellipse;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=20;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="1"><mxGeometry x="{uc_x}" y="{y}" width="{uc_w}" height="{uc_h}" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="e_uc_{i+1}" value="" style="endArrow=none;html=1;strokeWidth=2;strokeColor=#444444;" edge="1" parent="1" source="actor1" target="{uc_id}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    _write_drawio(filename, "UseCase", cells, page_width=1400, page_height=max(900, height + 120))


def create_system_architecture_drawio(filename, layers, width, height, fit=False):
    cells = []
    edge_idx = 1

    if fit:
        margin_x = 40
        layer_left = margin_x
        layer_right = width - margin_x
        layer_top = 35
        layer_h = 92
        gap_y = 24
        title_area_w = 170
        comp_box_h = 48
        comp_box_w_default = 136

        for i, (name, comps) in enumerate(layers):
            y1 = layer_top + i * (layer_h + gap_y)
            layer_id = f"layer_{i+1}"
            cells.append(
                f'<mxCell id="{layer_id}" value="" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{int(layer_left)}" y="{int(y1)}" width="{int(layer_right-layer_left)}" height="{int(layer_h)}" as="geometry"/></mxCell>'
            )
            title_id = f"title_{i+1}"
            cells.append(
                f'<mxCell id="{title_id}" value="{_mx_escape(name)}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=22;fontColor=#000000;" vertex="1" parent="1"><mxGeometry x="{int(layer_left + 8)}" y="{int(y1 + 12)}" width="{int(title_area_w - 16)}" height="{int(layer_h - 24)}" as="geometry"/></mxCell>'
            )

            divider_x = layer_left + title_area_w
            comp_area_left = divider_x + 18
            comp_area_right = layer_right - 28
            available = max(240, comp_area_right - comp_area_left)
            count = max(1, len(comps))
            max_gap = 26
            if count == 1:
                comp_w = min(comp_box_w_default + 10, available)
                gap = 0
            else:
                comp_w = min(comp_box_w_default, (available - max_gap * (count - 1)) / count)
                comp_w = max(116, comp_w)
                gap = (available - comp_w * count) / (count - 1)
                gap = max(14, min(max_gap, gap))

            used_width = comp_w if count == 1 else comp_w * count + gap * (count - 1)
            x = comp_area_left + max(0, (available - used_width) / 2)

            for j, comp in enumerate(comps):
                comp_id = f"comp_{i+1}_{j+1}"
                yb1 = y1 + (layer_h - comp_box_h) / 2
                cells.append(
                    f'<mxCell id="{comp_id}" value="{_mx_escape(comp)}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=18;fontColor=#000000;" vertex="1" parent="1"><mxGeometry x="{int(x)}" y="{int(yb1)}" width="{int(comp_w)}" height="{int(comp_box_h)}" as="geometry"/></mxCell>'
                )
                x = x + comp_w + gap

            if i < len(layers) - 1:
                cells.append(
                    f'<mxCell id="edge_{edge_idx}" value="" style="endArrow=none;html=1;strokeColor=#000000;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{int(width/2)}" y="{int(y1+layer_h)}" as="sourcePoint"/><mxPoint x="{int(width/2)}" y="{int(y1+layer_h+gap_y)}" as="targetPoint"/></mxGeometry></mxCell>'
                )
                edge_idx += 1
    else:
        start_y = 50
        for i, (name, comps) in enumerate(layers):
            y1 = start_y + i * 130
            layer_id = f"layer_{i+1}"
            cells.append(
                f'<mxCell id="{layer_id}" value="{_mx_escape(name)}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="100" y="{y1}" width="600" height="100" as="geometry"/></mxCell>'
            )
            cx = 300
            for j, comp in enumerate(comps):
                comp_id = f"comp_{i+1}_{j+1}"
                cells.append(
                    f'<mxCell id="{comp_id}" value="{_mx_escape(comp)}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{cx}" y="{y1+25}" width="120" height="50" as="geometry"/></mxCell>'
                )
                cx += 140
            if i < len(layers) - 1:
                cells.append(
                    f'<mxCell id="edge_{edge_idx}" value="" style="endArrow=none;html=1;strokeColor=#000000;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="400" y="{y1+100}" as="sourcePoint"/><mxPoint x="400" y="{y1+130}" as="targetPoint"/></mxGeometry></mxCell>'
                )
                edge_idx += 1

    _write_drawio(filename, "Architecture", cells, page_width=max(1000, width + 80), page_height=max(760, height + 80))


def create_function_structure_drawio(filename):
    modules = [
        ("用户模块", ["查看信息", "加入购物车", "下单购买", "维护个人信息", "评价", "退款"]),
        ("商家模块", ["管理信息", "处理订单", "分类管理"]),
        ("管理员模块", ["用户管理", "商家管理", "系统管理"]),
    ]

    cells = []
    cells.append('<mxCell id="root" value="系统功能结构" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;fillColor=#E6F0FF;" vertex="1" parent="1"><mxGeometry x="320" y="50" width="220" height="60" as="geometry"/></mxCell>')

    start_x = 80
    for i, (mod, subs) in enumerate(modules):
        mod_id = f"mod_{i+1}"
        mod_x = start_x + i * 240
        cells.append(
            f'<mxCell id="{mod_id}" value="{_mx_escape(mod)}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{mod_x}" y="180" width="160" height="50" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="edge_root_{i+1}" value="" style="endArrow=none;html=1;strokeColor=#000000;" edge="1" parent="1" source="root" target="{mod_id}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

        sy = 280
        for j, sub in enumerate(subs):
            sub_id = f"sub_{i+1}_{j+1}"
            cells.append(
                f'<mxCell id="{sub_id}" value="{_mx_escape(sub)}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{mod_x+20}" y="{sy}" width="120" height="40" as="geometry"/></mxCell>'
            )
            cells.append(
                f'<mxCell id="edge_sub_{i+1}_{j+1}" value="" style="endArrow=none;html=1;strokeColor=#000000;" edge="1" parent="1" source="{mod_id}" target="{sub_id}"><mxGeometry relative="1" as="geometry"/></mxCell>'
            )
            sy += 55

    _write_drawio(filename, "FunctionStructure", cells, page_width=1200, page_height=1100)


def create_flowchart_drawio(filename, steps, width=1200):
    if not steps:
        steps = ["开始", "接收订单", "订单是否已付款?", "确认订单信息", "安排发货", "完成订单", "结束"]

    normalized = []
    for step in steps:
        if isinstance(step, dict):
            text = str(step.get("text", "")).strip()
            step_type = str(step.get("type", "process"))
            no_action = str(step.get("no_action", "分支处理")).strip()
        else:
            text = str(step).strip()
            if text in ("开始", "结束"):
                step_type = "terminator"
            elif ("是否" in text) or ("?" in text) or ("？" in text):
                step_type = "decision"
            else:
                step_type = "process"
            no_action = "分支处理"
        normalized.append({"type": step_type, "text": text, "no_action": no_action})

    if not normalized or normalized[0]["text"] != "开始":
        normalized.insert(0, {"type": "terminator", "text": "开始", "no_action": ""})
    if normalized[-1]["text"] != "结束":
        normalized.append({"type": "terminator", "text": "结束", "no_action": ""})

    cells = []
    node_ids = []
    x_center = 420
    y = 60
    for i, n in enumerate(normalized):
        nid = f"n{i+1}"
        node_ids.append(nid)
        if n["type"] == "decision":
            w, h = 360, 110
            style = "rhombus;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;fillColor=#FFF2CC;"
        elif n["type"] == "terminator":
            w, h = 240, 66
            style = "rounded=1;arcSize=50;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;"
        else:
            w, h = 320, 76
            style = "rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;"
        x = x_center - w // 2
        cells.append(
            f'<mxCell id="{nid}" value="{_mx_escape(n["text"])}" style="{style}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        y += h + 38

    for i in range(len(node_ids) - 1):
        cells.append(
            f'<mxCell id="e_main_{i+1}" value="" style="endArrow=block;html=1;strokeColor=#000000;" edge="1" parent="1" source="{node_ids[i]}" target="{node_ids[i+1]}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    for i, n in enumerate(normalized):
        if n["type"] != "decision":
            continue
        bid = f"b{i+1}"
        bx = 760
        by = 60 + i * 120
        cells.append(
            f'<mxCell id="{bid}" value="{_mx_escape(n["no_action"])}" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{bx}" y="{by}" width="220" height="70" as="geometry"/></mxCell>'
        )
        target_id = node_ids[i+1] if (i + 1) < len(node_ids) else node_ids[-1]
        cells.append(
            f'<mxCell id="e_no_1_{i+1}" value="否" style="endArrow=block;html=1;strokeColor=#000000;" edge="1" parent="1" source="{node_ids[i]}" target="{bid}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="e_no_2_{i+1}" value="" style="endArrow=block;html=1;strokeColor=#000000;" edge="1" parent="1" source="{bid}" target="{target_id}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    _write_drawio(filename, "Flowchart", cells, page_width=max(1200, width), page_height=1900)
class ThesisDiagramPlotter:
    def __init__(self, width=800, height=600, scale=2):
        self.target_width = width
        self.target_height = height
        self.scale = scale
        self.width = width * scale
        self.height = height * scale
        self.colors = {
            'bg': '#FFFFFF',
            'line': '#444444',
            'fill_uc': '#FFFFFF',
            'fill_actor': '#FFFFFF',
            'text': '#111111',
            'fill_flow': '#FFFFFF',
        }
        self.img = Image.new('RGB', (self.width, self.height), self.colors['bg'])
        self.draw = ImageDraw.Draw(self.img)
        self.font = self._load_font(14 * scale)
        self._font_cache = {}

    def _load_font(self, size):
        font_names = ["msyh.ttc", "msyh.ttf", "simsun.ttc", "Arial Unicode.ttf"]
        system_font_dirs = [r"C:\Windows\Fonts", r"/usr/share/fonts", r"/System/Library/Fonts"]
        for font_name in font_names:
            for font_dir in system_font_dirs:
                path = os.path.join(font_dir, font_name)
                if os.path.exists(path):
                    try: return ImageFont.truetype(path, int(size))
                    except: continue
        try: return ImageFont.truetype("msyh.ttc", int(size))
        except: return ImageFont.load_default()

    def _get_font(self, size):
        size = max(8, int(size))
        if size not in self._font_cache:
            self._font_cache[size] = self._load_font(size)
        return self._font_cache[size]

    def _fit_text(self, text, max_w, max_h, preferred_size=None, min_size=None):
        text = str(text).strip()
        if preferred_size is None:
            preferred_size = 18 * self.scale
        if min_size is None:
            min_size = 10 * self.scale

        max_w = max(20, int(max_w))
        max_h = max(20, int(max_h))

        def wrap_lines(font_obj):
            lines = []
            for raw_line in text.splitlines() or [""]:
                raw_line = raw_line.strip()
                if not raw_line:
                    lines.append("")
                    continue
                current = ""
                for ch in raw_line:
                    candidate = current + ch
                    bbox = self.draw.textbbox((0, 0), candidate, font=font_obj)
                    if (bbox[2] - bbox[0]) <= max_w:
                        current = candidate
                    else:
                        if current:
                            lines.append(current)
                        current = ch
                if current:
                    lines.append(current)
            return lines or [text]

        for size in range(int(preferred_size), int(min_size) - 1, -1):
            font_obj = self._get_font(size)
            lines = wrap_lines(font_obj)
            sample = self.draw.textbbox((0, 0), "Ag", font=font_obj)
            line_h = sample[3] - sample[1]
            gap = max(2, int(size * 0.2))
            total_h = len(lines) * line_h + max(0, len(lines) - 1) * gap
            max_line_w = 0
            for line in lines:
                bbox = self.draw.textbbox((0, 0), line, font=font_obj)
                max_line_w = max(max_line_w, bbox[2] - bbox[0])
            if total_h <= max_h and max_line_w <= max_w:
                return font_obj, lines, line_h, gap

        font_obj = self._get_font(min_size)
        lines = wrap_lines(font_obj)
        sample = self.draw.textbbox((0, 0), "Ag", font=font_obj)
        line_h = sample[3] - sample[1]
        gap = max(2, int(min_size * 0.2))
        return font_obj, lines, line_h, gap

    def draw_text_in_box(self, x1, y1, x2, y2, text, preferred_size=None, min_size=None, fill=None):
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        if not str(text).strip():
            return

        font_obj, lines, line_h, gap = self._fit_text(
            text,
            max_w=(x2 - x1) - 12 * self.scale,
            max_h=(y2 - y1) - 12 * self.scale,
            preferred_size=preferred_size,
            min_size=min_size,
        )
        total_h = len(lines) * line_h + max(0, len(lines) - 1) * gap
        start_y = y1 + (y2 - y1 - total_h) / 2

        for idx, line in enumerate(lines):
            bbox = self.draw.textbbox((0, 0), line, font=font_obj)
            text_w = bbox[2] - bbox[0]
            tx = x1 + (x2 - x1 - text_w) / 2
            ty = start_y + idx * (line_h + gap)
            self.draw.text((tx, ty), line, fill=fill or self.colors['text'], font=font_obj)

    def draw_actor(self, x, y, name):
        x, y = x * self.scale, y * self.scale
        w, h = 110 * self.scale, 56 * self.scale
        self.draw.rectangle([x, y, x + w, y + h], fill=self.colors['fill_actor'], outline=self.colors['line'], width=2 * self.scale)
        self.draw_text_in_box(x, y, x + w, y + h, name, preferred_size=18 * self.scale, min_size=12 * self.scale)
        return (x + w, y + h//2)

    def draw_use_case(self, x, y, text):
        x, y = x * self.scale, y * self.scale
        w, h = 180 * self.scale, 70 * self.scale
        self.draw.ellipse([x, y, x+w, y+h], fill=self.colors['fill_uc'], outline=self.colors['line'], width=2*self.scale)
        self.draw_text_in_box(x, y, x + w, y + h, text, preferred_size=18 * self.scale, min_size=11 * self.scale)
        return (x, y + h//2)

    def draw_connection(self, start, end):
        self.draw.line([start, end], fill=self.colors['line'], width=2*self.scale)

    def draw_rect(self, x, y, w, h, text, fill='white'):
        x, y, w, h = x*self.scale, y*self.scale, w*self.scale, h*self.scale
        self.draw.rectangle([x, y, x+w, y+h], fill=fill, outline=self.colors['line'], width=2*self.scale)
        if text:
            self.draw_text_in_box(x, y, x + w, y + h, text, preferred_size=18 * self.scale, min_size=10 * self.scale, fill='black')
        return (x + w/2, y + h) # Return bottom center

    def draw_diamond(self, x, y, w, h, text):
        x, y, w, h = x*self.scale, y*self.scale, w*self.scale, h*self.scale
        # Draw diamond polygon
        pts = [(x+w/2, y), (x+w, y+h/2), (x+w/2, y+h), (x, y+h/2)]
        self.draw.polygon(pts, fill=self.colors['fill_flow'], outline=self.colors['line'], width=2*self.scale)
        if text:
            self.draw_text_in_box(
                x + 16 * self.scale,
                y + 12 * self.scale,
                x + w - 16 * self.scale,
                y + h - 12 * self.scale,
                text,
                preferred_size=18 * self.scale,
                min_size=10 * self.scale,
                fill='black',
            )
        return (x + w/2, y + h)

    def draw_arrow(self, start, end):
        self.draw.line([start, end], fill=self.colors['line'], width=2*self.scale)
        # Simple arrowhead logic could be added here
    def save(self, filename):
        final = self.img.resize((self.target_width, self.target_height), Image.Resampling.LANCZOS)
        final.save(filename, quality=95, dpi=(300, 300))
        print(f"Generated: {filename}")

def create_usecase_diagram(filename, actor_name, use_cases):
    height = max(500, len(use_cases) * 100 + 100)
    plotter = ThesisDiagramPlotter(width=800, height=height)
    actor_center = plotter.draw_actor(100, height//2 - 40, actor_name)
    start_y = (height - len(use_cases)*100) // 2
    for i, case in enumerate(use_cases):
        conn = plotter.draw_use_case(400, start_y + i*100, case)
        plotter.draw_connection(actor_center, conn)
    plotter.save(filename)
    create_usecase_drawio(filename, actor_name, use_cases)

def create_system_architecture_diagram(filename, layers=None):
    if layers is None:
        layers = [("前端展示层", ["Vue.js", "ElementUI"]), ("API网关层", ["Nginx", "鉴权"]), ("业务逻辑层", ["Spring Boot", "Service"]), ("数据持久层", ["MySQL", "MyBatis"])]
    plotter = ThesisDiagramPlotter(width=800, height=600)
    colors = ['#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF']
    start_y = 50
    for i, (name, comps) in enumerate(layers):
        plotter.draw.rectangle([100*plotter.scale, start_y*plotter.scale, 700*plotter.scale, (start_y+100)*plotter.scale], fill=colors[i], outline='black', width=2*plotter.scale)
        plotter.draw.text((120*plotter.scale, (start_y+40)*plotter.scale), name, fill='black', font=plotter._load_font(18*plotter.scale))
        cx = 300
        for comp in comps:
            plotter.draw.rectangle([cx*plotter.scale, (start_y+25)*plotter.scale, (cx+120)*plotter.scale, (start_y+75)*plotter.scale], fill='white', outline='black', width=1*plotter.scale)
            f = plotter._load_font(12*plotter.scale)
            tb = plotter.draw.textbbox((0,0), comp, font=f)
            plotter.draw.text(((cx+60)*plotter.scale - (tb[2]-tb[0])/2, (start_y+40)*plotter.scale), comp, fill='black', font=f)
            cx += 140
        if i < len(layers)-1:
            mx, my, ny = 400*plotter.scale, (start_y+100)*plotter.scale, (start_y+130)*plotter.scale
            plotter.draw.line([mx, my, mx, ny], fill='black', width=3*plotter.scale)
        start_y += 130
    plotter.save(filename)
    create_system_architecture_drawio(filename, layers, 800, 600, fit=False)

def create_function_structure_diagram(filename):
    """功能结构图 (树状图)"""
    plotter = ThesisDiagramPlotter(width=800, height=500)
    root = (400, 50)
    root_bottom = plotter.draw_rect(300, 50, 200, 60, "教室管理系统", '#E6F0FF')
    
    modules = ["学生模块", "教师模块", "管理员模块"]
    start_x = 100
    for mod in modules:
        mod_top = (start_x + 80, 200) # center of module rect
        plotter.draw_arrow(root_bottom, (root_bottom[0], 150*plotter.scale)) # vertical down
        # Simple lines logic omitted for brevity, just draw blocks
        plotter.draw_rect(start_x, 200, 160, 50, mod)
        
        # Sub-functions
        subs = []
        if "学生" in mod: 
            subs = ["登录注册", "教室查询", "预约申请", "我的预约", "论坛互动"]
        elif "教师" in mod: 
            subs = ["登录注册", "教室查询", "预约申请", "我的预约", "设备报修", "论坛互动"]
        else: 
            subs = ["基础管理", "预约审核", "数据统计", "报修处理"]
        sy = 300
        for sub in subs:
            plotter.draw_rect(start_x+30, sy, 100, 40, sub)
            sy += 60
        start_x += 220
    plotter.save(filename)
    create_function_structure_drawio(filename)

def create_flowchart(filename, steps):
    """简单流程图 (垂直)"""
    plotter = ThesisDiagramPlotter(width=400, height=600)
    cx = 100
    cy = 50
    for step in steps:
        if step.startswith("判断"):
            plotter.draw_diamond(cx, cy, 200, 80, step)
            cy += 120
        else:
            plotter.draw_rect(cx, cy, 200, 60, step)
            cy += 100
        # Draw arrow
        if step != steps[-1]:
            plotter.draw_arrow((200*plotter.scale, (cy-40)*plotter.scale), (200*plotter.scale, cy*plotter.scale))
    plotter.save(filename)
    create_flowchart_drawio(filename, steps, width=800)


def create_system_architecture_diagram_fit(filename, layers=None, width=920, height=500):
    """系统架构图(自适应版)

    目的：避免组件数量较多时画布宽度不够导致右侧内容被截断。

    - 会自动在固定画布内布局组件框。
    - 当组件数量较多时会缩小组件框宽度并调整间距。
    """
    if layers is None:
        layers = [
            ("前端展示层", ["Vue.js", "ElementUI"]),
            ("API网关层", ["Nginx", "鉴权"]),
            ("业务逻辑层", ["Spring Boot", "Service"]),
            ("数据持久层", ["MySQL", "MyBatis"]),
        ]

    plotter = ThesisDiagramPlotter(width=width, height=height)
    colors = ['#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF']

    margin_x = 40
    layer_left = margin_x
    layer_right = width - margin_x
    layer_top = 35
    layer_h = 92
    gap_y = 24
    title_area_w = 170

    title_font = plotter._load_font(24 * plotter.scale)
    comp_font = plotter._load_font(18 * plotter.scale)

    for i, (name, comps) in enumerate(layers):
        y1 = layer_top + i * (layer_h + gap_y)
        y2 = y1 + layer_h

        plotter.draw.rectangle(
            [layer_left * plotter.scale, y1 * plotter.scale, layer_right * plotter.scale, y2 * plotter.scale],
            fill=colors[i % len(colors)],
            outline='black',
            width=2 * plotter.scale,
        )
        divider_x = layer_left + title_area_w
        label_box = [layer_left + 8, y1 + 10, divider_x - 8, y2 - 10]
        label_text = plotter.draw.textbbox((0, 0), name, font=title_font)
        label_tw = label_text[2] - label_text[0]
        label_th = label_text[3] - label_text[1]
        label_x = (label_box[0] + label_box[2]) / 2 - label_tw / (2 * plotter.scale)
        label_y = (label_box[1] + label_box[3]) / 2 - label_th / (2 * plotter.scale)
        plotter.draw.text(
            (label_x * plotter.scale, label_y * plotter.scale),
            name,
            fill='black',
            font=title_font,
        )

        comp_box_h = 48
        comp_box_w_default = 136
        comp_area_left = divider_x + 18
        comp_area_right = layer_right - 28
        available = max(240, comp_area_right - comp_area_left)
        count = max(1, len(comps))

        if count == 1:
            comp_w = min(comp_box_w_default + 10, available)
            gap = 0
        else:
            max_gap = 26
            comp_w = min(comp_box_w_default, (available - max_gap * (count - 1)) / count)
            comp_w = max(116, comp_w)
            gap = (available - comp_w * count) / (count - 1)
            gap = max(14, min(max_gap, gap))

        used_width = comp_w if count == 1 else comp_w * count + gap * (count - 1)
        x = comp_area_left + max(0, (available - used_width) / 2)
        for comp in comps:
            x2 = x + comp_w
            yb1 = y1 + (layer_h - comp_box_h) / 2
            yb2 = yb1 + comp_box_h
            plotter.draw.rectangle(
                [x * plotter.scale, yb1 * plotter.scale, x2 * plotter.scale, yb2 * plotter.scale],
                fill='white',
                outline='black',
                width=1 * plotter.scale,
            )
            tb = plotter.draw.textbbox((0, 0), comp, font=comp_font)
            tw = tb[2] - tb[0]
            th = tb[3] - tb[1]
            plotter.draw.text(
                ((x + comp_w / 2) * plotter.scale - tw / 2, (yb1 + comp_box_h / 2) * plotter.scale - th / 2),
                comp,
                fill='black',
                font=comp_font,
            )
            x = x2 + gap

        if i < len(layers) - 1:
            mx = (width / 2) * plotter.scale
            plotter.draw.line(
                [mx, y2 * plotter.scale, mx, (y2 + gap_y) * plotter.scale],
                fill='black',
                width=3 * plotter.scale,
            )

    plotter.save(filename)
    create_system_architecture_drawio(filename, layers, width, height, fit=True)


def create_flowchart_fit(filename, steps=None, width=1400, min_height=1800, font_size=24):
    """流程图(固定模板 + 清晰文字高分辨率)

    样式强制：
    - 纵向主流程
    - 开始/结束使用圆角终止框
    - 处理步骤使用矩形
    - 条件判断使用菱形，带是/否分支
    - 否分支向右展开并回流主线
    """
    if not steps:
        steps = [
            "开始",
            "接收订单",
            "订单是否已付款？",
            "确认订单信息",
            "安排发货",
            "更新订单状态",
            "用户签收确认",
            "用户是否有售后需求？",
            "处理售后问题",
            "完成订单",
            "结束",
        ]

    def normalize_step(step):
        if isinstance(step, dict):
            step_type = str(step.get("type", "process"))
            text = str(step.get("text", "")).strip()
            no_action = str(step.get("no_action", "分支处理")).strip()
            return {"type": step_type, "text": text, "no_action": no_action}

        text = str(step).strip()
        if text.startswith("判断"):
            text = text.replace("判断", "", 1).lstrip(":： ")
        if text in ("开始", "结束"):
            step_type = "terminator"
        elif ("是否" in text) or ("?" in text) or ("？" in text):
            step_type = "decision"
        else:
            step_type = "process"

        no_action = "分支处理"
        if "付款" in text:
            no_action = "等待用户付款"
        elif ("售后" in text) or ("退款" in text):
            no_action = "直接完成订单"

        return {"type": step_type, "text": text, "no_action": no_action}

    normalized = [normalize_step(s) for s in steps]
    if not normalized or normalized[0]["text"] != "开始":
        normalized.insert(0, {"type": "terminator", "text": "开始", "no_action": ""})
    if normalized[-1]["text"] != "结束":
        normalized.append({"type": "terminator", "text": "结束", "no_action": ""})

    process_w, process_h = 320, 76
    decision_w, decision_h = 420, 112
    term_w, term_h = 240, 66
    top_margin, v_gap = 50, 34

    y = top_margin
    layout = []
    for node in normalized:
        node_type = node["type"]
        if node_type == "decision":
            h = decision_h
        elif node_type == "terminator":
            h = term_h
        else:
            h = process_h
        layout.append({"y": y, "h": h, "node": node})
        y += h + v_gap

    height = max(min_height, y + 80)
    plotter = ThesisDiagramPlotter(width=width, height=height, scale=2)
    scale = plotter.scale
    draw = plotter.draw
    line_color = "#222222"
    fill_color = "#FFFFFF"
    text_color = "#111111"
    font = plotter._load_font(font_size * scale)
    label_font = plotter._load_font(max(18, font_size - 2) * scale)

    def draw_text_centered_in_box(x1, y1, x2, y2, text, font_obj):
        text = str(text).strip()
        if not text:
            return
        max_width = max(60, int((x2 - x1) - 20 * scale))
        lines = []
        current = ""
        for ch in text:
            candidate = current + ch
            bbox = draw.textbbox((0, 0), candidate, font=font_obj)
            if (bbox[2] - bbox[0]) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)

        line_height = draw.textbbox((0, 0), "测", font=font_obj)[3]
        total_h = len(lines) * line_height + max(0, (len(lines) - 1) * int(6 * scale))
        start_y = y1 + (y2 - y1 - total_h) / 2

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_obj)
            tw = bbox[2] - bbox[0]
            tx = x1 + (x2 - x1 - tw) / 2
            ty = start_y + i * (line_height + int(6 * scale))
            draw.text((tx, ty), line, fill=text_color, font=font_obj)

    def draw_arrow_head(p0, p1):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        length = math.hypot(dx, dy)
        if length < 1:
            return
        ux, uy = dx / length, dy / length
        ah = 12 * scale
        aw = 7 * scale
        bx = p1[0] - ux * ah
        by = p1[1] - uy * ah
        px, py = -uy, ux
        left = (bx + px * aw, by + py * aw)
        right = (bx - px * aw, by - py * aw)
        draw.polygon([p1, left, right], fill=line_color)

    def draw_polyline(points, with_arrow=True, width_px=None):
        if width_px is None:
            width_px = 2 * scale
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=line_color, width=width_px)
        if with_arrow and len(points) >= 2:
            draw_arrow_head(points[-2], points[-1])

    x_center = width // 2
    rendered = []

    for item in layout:
        node = item["node"]
        y_top = item["y"]
        h = item["h"]

        if node["type"] == "decision":
            w = decision_w
            x1 = (x_center - w // 2) * scale
            y1 = y_top * scale
            x2 = (x_center + w // 2) * scale
            y2 = (y_top + h) * scale
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            pts = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
            draw.polygon(pts, fill=fill_color, outline=line_color, width=2 * scale)
            draw_text_centered_in_box(x1 + 20 * scale, y1 + 16 * scale, x2 - 20 * scale, y2 - 16 * scale, node["text"], font)
            anchors = {
                "top": (cx, y1),
                "bottom": (cx, y2),
                "left": (x1, cy),
                "right": (x2, cy),
                "center": (cx, cy),
                "bbox": (x1, y1, x2, y2),
            }
        elif node["type"] == "terminator":
            w = term_w
            x1 = (x_center - w // 2) * scale
            y1 = y_top * scale
            x2 = (x_center + w // 2) * scale
            y2 = (y_top + h) * scale
            radius = int(30 * scale)
            draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill_color, outline=line_color, width=2 * scale)
            draw_text_centered_in_box(x1 + 10 * scale, y1 + 8 * scale, x2 - 10 * scale, y2 - 8 * scale, node["text"], font)
            anchors = {
                "top": ((x1 + x2) / 2, y1),
                "bottom": ((x1 + x2) / 2, y2),
                "left": (x1, (y1 + y2) / 2),
                "right": (x2, (y1 + y2) / 2),
                "center": ((x1 + x2) / 2, (y1 + y2) / 2),
                "bbox": (x1, y1, x2, y2),
            }
        else:
            w = process_w
            x1 = (x_center - w // 2) * scale
            y1 = y_top * scale
            x2 = (x_center + w // 2) * scale
            y2 = (y_top + h) * scale
            draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline=line_color, width=2 * scale)
            draw_text_centered_in_box(x1 + 10 * scale, y1 + 8 * scale, x2 - 10 * scale, y2 - 8 * scale, node["text"], font)
            anchors = {
                "top": ((x1 + x2) / 2, y1),
                "bottom": ((x1 + x2) / 2, y2),
                "left": (x1, (y1 + y2) / 2),
                "right": (x2, (y1 + y2) / 2),
                "center": ((x1 + x2) / 2, (y1 + y2) / 2),
                "bbox": (x1, y1, x2, y2),
            }

        rendered.append({"type": node["type"], "text": node["text"], "no_action": node.get("no_action", "分支处理"), **anchors})

    for i in range(len(rendered) - 1):
        cur = rendered[i]
        nxt = rendered[i + 1]
        start = cur["bottom"]
        end = nxt["top"]
        draw_polyline([start, end], with_arrow=True)
        if cur["type"] == "decision":
            lx = start[0] - 26 * scale
            ly = (start[1] + end[1]) / 2 - 14 * scale
            draw.text((lx, ly), "是", fill=text_color, font=label_font)

    decision_indices = [i for i, n in enumerate(rendered) if n["type"] == "decision"]
    for order, idx in enumerate(decision_indices):
        dnode = rendered[idx]

        branch_box_w = 220 * scale
        branch_box_h = 72 * scale
        branch_x1 = dnode["right"][0] + 95 * scale
        branch_y1 = dnode["center"][1] - branch_box_h / 2
        branch_x2 = branch_x1 + branch_box_w
        branch_y2 = branch_y1 + branch_box_h

        draw.rectangle([branch_x1, branch_y1, branch_x2, branch_y2], fill=fill_color, outline=line_color, width=2 * scale)
        draw_text_centered_in_box(branch_x1 + 8 * scale, branch_y1 + 8 * scale, branch_x2 - 8 * scale, branch_y2 - 8 * scale, dnode["no_action"], font)

        entry = (branch_x1, dnode["center"][1])
        draw_polyline([dnode["right"], entry], with_arrow=True)
        draw.text((dnode["right"][0] + 22 * scale, dnode["center"][1] - 26 * scale), "否", fill=text_color, font=label_font)

        if order == 0 and idx > 0:
            target = rendered[idx - 1]["right"]
        elif idx + 1 < len(rendered):
            target = rendered[idx + 1]["right"]
        else:
            target = rendered[-2]["right"]

        route_x = branch_x2 + 52 * scale
        route = [
            (branch_x2, dnode["center"][1]),
            (route_x, dnode["center"][1]),
            (route_x, target[1]),
            target,
        ]
        draw_polyline(route, with_arrow=True)

    plotter.save(filename)
    create_flowchart_drawio(filename, normalized, width=width)

def create_er_diagram_fit(filename, width=1400, height=1000):
    """E-R图(固定版式)

    输出：PNG + SVG + draw.io(.drawio)
    """
    plotter = ThesisDiagramPlotter(width=width, height=height, scale=2)
    s = plotter.scale

    line_color = plotter.colors['line']
    text_color = plotter.colors['text']
    font = plotter._load_font(18 * s)
    card_font = plotter._load_font(16 * s)

    def rect(x, y, w, h, text):
        plotter.draw.rectangle([x*s, y*s, (x+w)*s, (y+h)*s], fill='white', outline=line_color, width=2*s)
        tb = plotter.draw.textbbox((0, 0), text, font=font)
        plotter.draw.text(((x + (w - (tb[2]-tb[0]))/2)*s, (y + (h - (tb[3]-tb[1]))/2)*s), text, fill=text_color, font=font)
        return {
            'cx': x + w / 2,
            'cy': y + h / 2,
            'left': (x, y + h / 2),
            'right': (x + w, y + h / 2),
            'top': (x + w / 2, y),
            'bottom': (x + w / 2, y + h),
        }

    def diamond(cx, cy, w, h, text):
        x = cx - w / 2
        y = cy - h / 2
        pts = [(cx*s, y*s), ((x+w)*s, cy*s), (cx*s, (y+h)*s), (x*s, cy*s)]
        plotter.draw.polygon(pts, fill=plotter.colors['fill_flow'], outline=line_color, width=2*s)
        tb = plotter.draw.textbbox((0, 0), text, font=font)
        plotter.draw.text(((cx - (tb[2]-tb[0]) / 2)*s, (cy - (tb[3]-tb[1]) / 2)*s), text, fill=text_color, font=font)
        return {
            'cx': cx,
            'cy': cy,
            'left': (x, cy),
            'right': (x + w, cy),
            'top': (cx, y),
            'bottom': (cx, y + h),
        }

    def line(p1, p2):
        plotter.draw.line([p1[0]*s, p1[1]*s, p2[0]*s, p2[1]*s], fill=line_color, width=2*s)

    def card(text, x, y):
        plotter.draw.text((x*s, y*s), text, fill=text_color, font=card_font)

    # Entities
    user_top = rect(100, 120, 220, 70, "用户")
    room = rect(560, 120, 220, 70, "直播间")
    interact = rect(560, 380, 220, 70, "互动")
    user_bottom = rect(100, 640, 220, 70, "用户")

    # Relationships
    rel_live = diamond(430, 155, 140, 90, "开播")
    rel_send = diamond(430, 415, 140, 90, "发送")
    rel_gen = diamond(850, 285, 140, 90, "产生")
    rel_follow = diamond(260, 415, 140, 90, "关注")

    # 用户 - 开播 - 直播间 (1:n)
    line(user_top['right'], rel_live['left'])
    line(rel_live['right'], room['left'])
    card("1", 330, 135)
    card("n", 530, 135)

    # 用户 - 发送 - 互动 (1:n)
    line((user_top['right'][0], user_top['right'][1] + 220), rel_send['left'])
    line(rel_send['right'], interact['left'])
    card("1", 330, 395)
    card("n", 530, 395)

    # 直播间 - 产生 - 互动 (1:n)
    line(room['right'], rel_gen['left'])
    line(rel_gen['bottom'], interact['right'])
    card("1", 790, 250)
    card("n", 790, 360)

    # 用户 - 关注 - 用户 (n:n)
    line(user_top['left'], rel_follow['left'])
    line(rel_follow['bottom'], user_bottom['top'])
    card("n", 120, 360)
    card("n", 230, 560)

    plotter.save(filename)

    create_er_diagram_drawio(filename)


def create_er_diagram_drawio(filename):
    """导出 draw.io 可编辑文件(.drawio)。"""
    base, _ = os.path.splitext(filename)
    drawio_path = base + ".drawio"

    xml = """<mxfile host=\"app.diagrams.net\" modified=\"2026-03-12T00:00:00.000Z\" agent=\"codex\" version=\"22.1.0\">\n  <diagram id=\"er\" name=\"Page-1\">\n    <mxGraphModel dx=\"1200\" dy=\"800\" grid=\"1\" gridSize=\"10\" guides=\"1\" tooltips=\"1\" connect=\"1\" arrows=\"1\" fold=\"1\" page=\"1\" pageScale=\"1\" pageWidth=\"1169\" pageHeight=\"827\" math=\"0\" shadow=\"0\">\n      <root>\n        <mxCell id=\"0\"/>\n        <mxCell id=\"1\" parent=\"0\"/>\n\n        <mxCell id=\"u1\" value=\"用户\" style=\"rounded=0;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"100\" y=\"120\" width=\"220\" height=\"70\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"room\" value=\"直播间\" style=\"rounded=0;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"560\" y=\"120\" width=\"220\" height=\"70\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"inter\" value=\"互动\" style=\"rounded=0;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"560\" y=\"380\" width=\"220\" height=\"70\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"u2\" value=\"用户\" style=\"rounded=0;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"100\" y=\"640\" width=\"220\" height=\"70\" as=\"geometry\"/>\n        </mxCell>\n\n        <mxCell id=\"r_live\" value=\"开播\" style=\"rhombus;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;fillColor=#FFF2CC;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"360\" y=\"110\" width=\"140\" height=\"90\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"r_send\" value=\"发送\" style=\"rhombus;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;fillColor=#FFF2CC;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"360\" y=\"370\" width=\"140\" height=\"90\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"r_gen\" value=\"产生\" style=\"rhombus;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;fillColor=#FFF2CC;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"780\" y=\"240\" width=\"140\" height=\"90\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"r_follow\" value=\"关注\" style=\"rhombus;whiteSpace=wrap;html=1;strokeColor=#2D4B7A;fillColor=#FFF2CC;\" vertex=\"1\" parent=\"1\">\n          <mxGeometry x=\"190\" y=\"370\" width=\"140\" height=\"90\" as=\"geometry\"/>\n        </mxCell>\n\n        <mxCell id=\"e1\" value=\"1\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"u1\" target=\"r_live\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"e2\" value=\"n\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"r_live\" target=\"room\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n\n        <mxCell id=\"e3\" value=\"1\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"u1\" target=\"r_send\">\n          <mxGeometry relative=\"1\" as=\"geometry\">\n            <Array as=\"points\">\n              <mxPoint x=\"320\" y=\"415\"/>\n            </Array>\n          </mxGeometry>\n        </mxCell>\n        <mxCell id=\"e4\" value=\"n\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"r_send\" target=\"inter\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n\n        <mxCell id=\"e5\" value=\"1\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"room\" target=\"r_gen\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"e6\" value=\"n\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"r_gen\" target=\"inter\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n\n        <mxCell id=\"e7\" value=\"n\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"u1\" target=\"r_follow\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n        <mxCell id=\"e8\" value=\"n\" style=\"endArrow=none;html=1;strokeColor=#2D4B7A;\" edge=\"1\" parent=\"1\" source=\"r_follow\" target=\"u2\">\n          <mxGeometry relative=\"1\" as=\"geometry\"/>\n        </mxCell>\n\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n"""

    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml)


def _wrap_text_lines(draw, text, font_obj, max_width):
    text = str(text or "").strip()
    if not text:
        return []
    max_width = max(20, int(max_width))
    lines = []
    for raw_line in text.splitlines() or [""]:
        raw_line = raw_line.strip()
        if not raw_line:
            lines.append("")
            continue
        current = ""
        for ch in raw_line:
            candidate = current + ch
            bbox = draw.textbbox((0, 0), candidate, font=font_obj)
            if (bbox[2] - bbox[0]) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def _line_metrics(draw, font_obj):
    bbox = draw.textbbox((0, 0), "Ag", font=font_obj)
    return bbox[3] - bbox[1]


def _fit_lines_in_box(draw, lines, load_font, max_w, max_h, preferred_size, min_size):
    lines = [str(line).strip() for line in (lines or [])]
    if not lines:
        return load_font(min_size), [], _line_metrics(draw, load_font(min_size)), max(2, int(min_size * 0.2))

    for size in range(int(preferred_size), int(min_size) - 1, -1):
        font_obj = load_font(size)
        wrapped = []
        for line in lines:
            wrapped.extend(_wrap_text_lines(draw, line, font_obj, max_w) or [""])
        line_h = _line_metrics(draw, font_obj)
        gap = max(2, int(size * 0.2))
        total_h = len(wrapped) * line_h + max(0, len(wrapped) - 1) * gap
        widest = 0
        for line in wrapped:
            bbox = draw.textbbox((0, 0), line, font=font_obj)
            widest = max(widest, bbox[2] - bbox[0])
        if widest <= max_w and total_h <= max_h:
            return font_obj, wrapped, line_h, gap

    font_obj = load_font(min_size)
    wrapped = []
    for line in lines:
        wrapped.extend(_wrap_text_lines(draw, line, font_obj, max_w) or [""])
    return font_obj, wrapped, _line_metrics(draw, font_obj), max(2, int(min_size * 0.2))


def create_class_diagram(filename, classes, relations=None, width=1600, height=1000):
    """生成黑白论文风格类图（PNG + .drawio）。"""
    relations = relations or []
    plotter = ThesisDiagramPlotter(width=width, height=height, scale=2)
    draw = plotter.draw
    s = plotter.scale
    line_color = "#444444"
    text_color = "#111111"

    normalized = []
    cols = 2 if len(classes) > 1 else 1
    box_w = 420
    box_h = 220
    margin_x = 70
    gap_x = 70
    gap_y = 90
    top_y = 20

    for idx, cls in enumerate(classes):
        item = dict(cls)
        if "x" not in item or "y" not in item:
            row = idx // cols
            col = idx % cols
            item["x"] = margin_x + col * (box_w + gap_x)
            item["y"] = top_y + row * (box_h + gap_y)
        item.setdefault("w", box_w)
        item.setdefault("h", box_h)
        item.setdefault("attributes", [])
        item.setdefault("methods", [])
        item.setdefault("id", f"class_{idx + 1}")
        normalized.append(item)

    def draw_class_box(item):
        x = item["x"] * s
        y = item["y"] * s
        w = item["w"] * s
        h = item["h"] * s
        title_h = max(42 * s, int(h * 0.18))
        body_h = h - title_h
        attr_h = body_h / 2
        method_h = body_h - attr_h

        draw.rounded_rectangle([x, y, x + w, y + h], radius=18 * s, fill="#FFFFFF", outline=line_color, width=2 * s)
        draw.line([x, y + title_h, x + w, y + title_h], fill=line_color, width=2 * s)
        draw.line([x, y + title_h + attr_h, x + w, y + title_h + attr_h], fill=line_color, width=2 * s)

        title_font, title_lines, title_line_h, title_gap = _fit_lines_in_box(
            draw, [item["name"]], plotter._get_font, w - 28 * s, title_h - 16 * s, 22 * s, 14 * s
        )
        title_total_h = len(title_lines) * title_line_h + max(0, len(title_lines) - 1) * title_gap
        title_start_y = y + (title_h - title_total_h) / 2
        for i, line in enumerate(title_lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            draw.text((x + (w - (bbox[2] - bbox[0])) / 2, title_start_y + i * (title_line_h + title_gap)), line, fill=text_color, font=title_font)

        for section_lines, sec_y, sec_h in (
            (item["attributes"], y + title_h, attr_h),
            (item["methods"], y + title_h + attr_h, method_h),
        ):
            font_obj, wrapped, line_h, gap = _fit_lines_in_box(
                draw, section_lines or [" "], plotter._get_font, w - 36 * s, sec_h - 20 * s, 18 * s, 10 * s
            )
            total_h = len(wrapped) * line_h + max(0, len(wrapped) - 1) * gap
            start_y = sec_y + (sec_h - total_h) / 2
            for i, line in enumerate(wrapped):
                bbox = draw.textbbox((0, 0), line, font=font_obj)
                draw.text((x + (w - (bbox[2] - bbox[0])) / 2, start_y + i * (line_h + gap)), line, fill=text_color, font=font_obj)

        return {
            "id": item["id"],
            "left": (item["x"], item["y"] + item["h"] / 2),
            "right": (item["x"] + item["w"], item["y"] + item["h"] / 2),
            "top": (item["x"] + item["w"] / 2, item["y"]),
            "bottom": (item["x"] + item["w"] / 2, item["y"] + item["h"]),
        }

    anchors = {}
    for item in normalized:
        anchors[item["id"]] = draw_class_box(item)

    for rel in relations:
        src = anchors.get(rel.get("source"))
        dst = anchors.get(rel.get("target"))
        if not src or not dst:
            continue

        if abs(src["right"][0] - dst["left"][0]) <= abs(src["bottom"][1] - dst["top"][1]):
            start = src["right"] if src["right"][0] <= dst["left"][0] else src["left"]
            end = dst["left"] if src["right"][0] <= dst["left"][0] else dst["right"]
        else:
            start = src["bottom"] if src["bottom"][1] <= dst["top"][1] else src["top"]
            end = dst["top"] if src["bottom"][1] <= dst["top"][1] else dst["bottom"]

        draw.line([start[0] * s, start[1] * s, end[0] * s, end[1] * s], fill=line_color, width=2 * s)

    plotter.save(filename)

    cells = []
    for item in normalized:
        x = item["x"]
        y = item["y"]
        w = item["w"]
        h = item["h"]
        title_h = max(42, int(h * 0.18))
        body_h = h - title_h
        attr_h = int(body_h / 2)
        method_h = h - title_h - attr_h
        cell_id = item["id"]
        cells.append(
            f'<mxCell id="{cell_id}" value="" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="{cell_id}_title" value="{_mx_escape(item["name"])}" style="text;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=20;fontStyle=1;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="{cell_id}"><mxGeometry x="0" y="0" width="{w}" height="{title_h}" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="{cell_id}_sep1" value="" style="endArrow=none;html=1;strokeWidth=2;strokeColor=#444444;" edge="1" parent="{cell_id}"><mxGeometry relative="1" as="geometry"><mxPoint x="0" y="{title_h}" as="sourcePoint"/><mxPoint x="{w}" y="{title_h}" as="targetPoint"/></mxGeometry></mxCell>'
        )
        cells.append(
            f'<mxCell id="{cell_id}_attr" value="{_mx_escape("<br/>".join(item["attributes"]))}" style="text;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=16;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="{cell_id}"><mxGeometry x="8" y="{title_h}" width="{w - 16}" height="{attr_h}" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="{cell_id}_sep2" value="" style="endArrow=none;html=1;strokeWidth=2;strokeColor=#444444;" edge="1" parent="{cell_id}"><mxGeometry relative="1" as="geometry"><mxPoint x="0" y="{title_h + attr_h}" as="sourcePoint"/><mxPoint x="{w}" y="{title_h + attr_h}" as="targetPoint"/></mxGeometry></mxCell>'
        )
        cells.append(
            f'<mxCell id="{cell_id}_method" value="{_mx_escape("<br/>".join(item["methods"]))}" style="text;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontSize=16;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="{cell_id}"><mxGeometry x="8" y="{title_h + attr_h}" width="{w - 16}" height="{method_h}" as="geometry"/></mxCell>'
        )

    for idx, rel in enumerate(relations, start=1):
        src = rel.get("source")
        dst = rel.get("target")
        if not src or not dst:
            continue
        cells.append(
            f'<mxCell id="rel_{idx}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#444444;endArrow=block;endFill=1;" edge="1" parent="1" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    _write_drawio(filename, "ClassDiagram", cells, page_width=max(1600, width), page_height=max(1000, height))


def create_entity_attribute_diagram(filename, entity_name, attributes, width=1600, height=1000):
    """生成黑白论文风格实体属性图（PNG + .drawio）。"""
    plotter = ThesisDiagramPlotter(width=width, height=height, scale=2)
    draw = plotter.draw
    s = plotter.scale
    line_color = "#444444"
    text_color = "#111111"

    cx = width / 2
    cy = max(220, height * 0.35)
    entity_w = 300
    entity_h = 90
    attr_w = 220
    attr_h = 70
    radius_x = min(width * 0.33, 520)
    radius_y = min(height * 0.27, 300)

    ex1 = (cx - entity_w / 2) * s
    ey1 = (cy - entity_h / 2) * s
    ex2 = (cx + entity_w / 2) * s
    ey2 = (cy + entity_h / 2) * s
    draw.rounded_rectangle([ex1, ey1, ex2, ey2], radius=18 * s, fill="#FFFFFF", outline=line_color, width=2 * s)
    plotter.draw_text_in_box(ex1, ey1, ex2, ey2, entity_name, preferred_size=24 * s, min_size=14 * s, fill=text_color)

    placed = []
    count = max(1, len(attributes))
    angle_offset = -math.pi / 2
    angles = [angle_offset + (2 * math.pi * i / count) for i in range(count)]

    for idx, attr in enumerate(attributes):
        angle = angles[idx]
        ax = cx + math.cos(angle) * radius_x
        ay = cy + math.sin(angle) * radius_y
        x1 = (ax - attr_w / 2) * s
        y1 = (ay - attr_h / 2) * s
        x2 = (ax + attr_w / 2) * s
        y2 = (ay + attr_h / 2) * s
        draw.ellipse([x1, y1, x2, y2], fill="#FFFFFF", outline=line_color, width=2 * s)
        plotter.draw_text_in_box(x1, y1, x2, y2, attr, preferred_size=22 * s, min_size=12 * s, fill=text_color)

        dx = ax - cx
        dy = ay - cy
        dist = math.hypot(dx, dy) or 1
        entity_edge = (cx + dx / dist * (entity_w / 2), cy + dy / dist * (entity_h / 2))
        attr_edge = (ax - dx / dist * (attr_w / 2), ay - dy / dist * (attr_h / 2))
        draw.line([entity_edge[0] * s, entity_edge[1] * s, attr_edge[0] * s, attr_edge[1] * s], fill=line_color, width=2 * s)
        placed.append({"id": f"attr_{idx + 1}", "text": attr, "x": ax - attr_w / 2, "y": ay - attr_h / 2, "w": attr_w, "h": attr_h})

    plotter.save(filename)

    cells = [
        f'<mxCell id="entity" value="{_mx_escape(entity_name)}" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=24;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="1"><mxGeometry x="{int(cx - entity_w / 2)}" y="{int(cy - entity_h / 2)}" width="{entity_w}" height="{entity_h}" as="geometry"/></mxCell>'
    ]

    for item in placed:
        cells.append(
            f'<mxCell id="{item["id"]}" value="{_mx_escape(item["text"])}" style="ellipse;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=22;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="1"><mxGeometry x="{int(item["x"])}" y="{int(item["y"])}" width="{item["w"]}" height="{item["h"]}" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="{item["id"]}_edge" value="" style="endArrow=none;html=1;strokeWidth=2;strokeColor=#444444;" edge="1" parent="1" source="entity" target="{item["id"]}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    _write_drawio(filename, "EntityAttribute", cells, page_width=max(1600, width), page_height=max(1000, height))


def create_sequence_diagram(filename, participants, messages, width=1600, height=900):
    """生成黑白论文风格时序图（PNG + .drawio）。"""
    plotter = ThesisDiagramPlotter(width=width, height=height, scale=2)
    draw = plotter.draw
    s = plotter.scale
    line_color = "#444444"
    text_color = "#111111"

    participants = [dict(p) if isinstance(p, dict) else {"name": str(p)} for p in participants]
    messages = [dict(m) for m in messages]

    count = max(1, len(participants))
    top_margin = 60
    header_w = 180
    header_h = 60
    bottom_margin = 70
    left_margin = 90
    right_margin = 90
    spacing = (width - left_margin - right_margin - header_w) / max(1, count - 1) if count > 1 else 0
    line_top = top_margin + header_h + 40
    line_bottom = max(line_top + 260, height - bottom_margin)

    participant_map = {}
    for idx, participant in enumerate(participants):
        px = left_margin + idx * spacing if count > 1 else width / 2 - header_w / 2
        participant.setdefault("id", f"p{idx + 1}")
        participant["x"] = px
        participant["center_x"] = px + header_w / 2
        participant_map[participant["id"]] = participant

        x1 = px * s
        y1 = top_margin * s
        x2 = (px + header_w) * s
        y2 = (top_margin + header_h) * s
        draw.rectangle([x1, y1, x2, y2], fill="#FFFFFF", outline=line_color, width=2 * s)
        plotter.draw_text_in_box(x1, y1, x2, y2, participant["name"], preferred_size=20 * s, min_size=12 * s, fill=text_color)
        draw.line([participant["center_x"] * s, line_top * s, participant["center_x"] * s, line_bottom * s], fill=line_color, width=2 * s)

    current_y = line_top + 20
    row_gap = 46
    activations = []
    rendered_messages = []

    for idx, message in enumerate(messages):
        frm = participant_map[message["from"]]
        to = participant_map[message["to"]]
        label = str(message.get("label", "")).strip()
        y = message.get("y", current_y)
        current_y = y + row_gap

        same_participant = frm["id"] == to["id"]
        msg_type = message.get("type", "call")
        label_font = plotter._get_font(16 * s)

        if same_participant:
            x = frm["center_x"]
            loop_w = 90
            loop_h = 42
            points = [
                (x * s, y * s),
                ((x + loop_w) * s, y * s),
                ((x + loop_w) * s, (y + loop_h) * s),
                (x * s, (y + loop_h) * s),
            ]
            for i in range(len(points) - 1):
                draw.line([points[i], points[i + 1]], fill=line_color, width=2 * s)
            draw.line([points[-1], ((x + 14) * s, (y + loop_h) * s)], fill=line_color, width=2 * s)
            draw.polygon(
                [((x + 2) * s, (y + loop_h) * s), ((x + 14) * s, (y + loop_h - 6) * s), ((x + 14) * s, (y + loop_h + 6) * s)],
                fill=line_color,
            )
            bbox = draw.textbbox((0, 0), label, font=label_font)
            draw.text((((x + loop_w / 2) * s) - (bbox[2] - bbox[0]) / 2, (y - 26) * s), label, fill=text_color, font=label_font)
            rendered_messages.append((frm["id"], y, y + loop_h, msg_type))
            continue

        start_x = frm["center_x"]
        end_x = to["center_x"]
        left_x = min(start_x, end_x)
        right_x = max(start_x, end_x)
        arrow_dir = 1 if end_x >= start_x else -1

        draw.line([start_x * s, y * s, end_x * s, y * s], fill=line_color, width=2 * s)
        ah = 12 * s
        aw = 7 * s
        arrow_tip = (end_x * s, y * s)
        arrow_base = ((end_x - arrow_dir * (ah / s)) * s, y * s)
        draw.polygon(
            [
                arrow_tip,
                (arrow_base[0], arrow_base[1] - aw),
                (arrow_base[0], arrow_base[1] + aw),
            ],
            fill=line_color,
        )

        if label:
            max_label_w = max(80, int((right_x - left_x) * s - 24 * s))
            lines = _wrap_text_lines(draw, label, label_font, max_label_w)
            line_h = _line_metrics(draw, label_font)
            total_h = len(lines) * line_h
            start_ty = (y - 12) * s - total_h
            for line_idx, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=label_font)
                tx = ((left_x + right_x) / 2) * s - (bbox[2] - bbox[0]) / 2
                ty = start_ty + line_idx * line_h
                draw.text((tx, ty), line, fill=text_color, font=label_font)

        rendered_messages.append((frm["id"], y - 4, y + 4, msg_type))
        if msg_type == "call":
            rendered_messages.append((to["id"], y + 4, y + 42, "activation"))
            activations.append({"participant": to["id"], "y": y + 4, "h": 38})

    activation_w = 16
    for item in activations:
        participant = participant_map[item["participant"]]
        x1 = (participant["center_x"] - activation_w / 2) * s
        x2 = (participant["center_x"] + activation_w / 2) * s
        y1 = item["y"] * s
        y2 = (item["y"] + item["h"]) * s
        draw.rectangle([x1, y1, x2, y2], fill="#FFFFFF", outline=line_color, width=2 * s)

    plotter.save(filename)

    cells = []
    for participant in participants:
        pid = participant["id"]
        px = participant["x"]
        cx = participant["center_x"]
        cells.append(
            f'<mxCell id="{pid}" value="{_mx_escape(participant["name"])}" style="rounded=0;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=20;fontColor=#111111;fontFamily=Microsoft YaHei;" vertex="1" parent="1"><mxGeometry x="{int(px)}" y="{top_margin}" width="{header_w}" height="{header_h}" as="geometry"/></mxCell>'
        )
        cells.append(
            f'<mxCell id="{pid}_life" value="" style="endArrow=none;dashed=1;html=1;strokeWidth=2;strokeColor=#444444;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{int(cx)}" y="{line_top}" as="sourcePoint"/><mxPoint x="{int(cx)}" y="{int(line_bottom)}" as="targetPoint"/></mxGeometry></mxCell>'
        )

    for idx, message in enumerate(messages, start=1):
        frm = participant_map[message["from"]]
        to = participant_map[message["to"]]
        label = str(message.get("label", "")).strip()
        y = int(message.get("y", line_top + 20 + (idx - 1) * row_gap))
        msg_type = message.get("type", "call")

        if frm["id"] == to["id"]:
            loop_x = int(frm["center_x"])
            cells.append(
                f'<mxCell id="msg_{idx}" value="{_mx_escape(label)}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;strokeColor=#444444;endArrow=block;endFill=1;fontSize=16;fontColor=#111111;fontFamily=Microsoft YaHei;loopDirection=0;" edge="1" parent="1" source="{frm["id"]}" target="{to["id"]}"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="{loop_x + 90}" y="{y}"/><mxPoint x="{loop_x + 90}" y="{y + 42}"/></Array></mxGeometry></mxCell>'
            )
            continue

        cells.append(
            f'<mxCell id="msg_{idx}" value="{_mx_escape(label)}" style="endArrow=block;endFill=1;html=1;strokeWidth=2;strokeColor=#444444;fontSize=16;fontColor=#111111;fontFamily=Microsoft YaHei;" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{int(frm["center_x"])}" y="{y}" as="sourcePoint"/><mxPoint x="{int(to["center_x"])}" y="{y}" as="targetPoint"/></mxGeometry></mxCell>'
        )
        if msg_type == "call":
            act_x = int(to["center_x"] - activation_w / 2)
            cells.append(
                f'<mxCell id="act_{idx}" value="" style="rounded=0;whiteSpace=wrap;html=1;strokeWidth=2;strokeColor=#444444;fillColor=#FFFFFF;" vertex="1" parent="1"><mxGeometry x="{act_x}" y="{y + 4}" width="{activation_w}" height="38" as="geometry"/></mxCell>'
            )

    _write_drawio(filename, "SequenceDiagram", cells, page_width=max(1600, width), page_height=max(900, height))
