"""
AeroVision AI - Tata Technologies InnoVent Presentation PDF Generator
Generates a professional 19-page PDF with White & Dark Blue theme.
Uses only ASCII-safe characters (no emojis) for Helvetica compatibility.
"""

from fpdf import FPDF
import os

# ─── Theme Colors (RGB tuples) ────────────────────────────────────────────────
DARK_BLUE    = (0, 31, 63)
NAVY_BLUE    = (0, 43, 92)
MEDIUM_BLUE  = (0, 116, 217)
LIGHT_BLUE   = (127, 219, 255)
ACCENT_BLUE  = (0, 158, 235)
SKY_BLUE     = (57, 204, 204)
WHITE        = (255, 255, 255)
OFF_WHITE    = (240, 244, 248)
LIGHT_GRAY   = (232, 236, 240)
DARK_GRAY    = (51, 51, 51)
GREEN        = (46, 204, 113)
ORANGE       = (255, 133, 27)
RED_ACCENT   = (231, 76, 60)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMGS_DIR = os.path.join(BASE_DIR, "imgs")
TRAIN_DIR = os.path.join(BASE_DIR, "runs", "train1")
RESULTS_DIR = os.path.join(BASE_DIR, "static", "results")


class AeroVisionPDF(FPDF):

    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.W = 297
        self.H = 210
        self.total_pages = 19

    def dark_bg(self):
        self.set_fill_color(*DARK_BLUE)
        self.rect(0, 0, self.W, self.H, 'F')

    def white_bg(self):
        self.set_fill_color(*WHITE)
        self.rect(0, 0, self.W, self.H, 'F')

    def top_bar(self, color=MEDIUM_BLUE):
        self.set_fill_color(*color)
        self.rect(0, 0, self.W, 2, 'F')

    def bottom_bar(self, color=MEDIUM_BLUE):
        self.set_fill_color(*color)
        self.rect(0, self.H - 5, self.W, 5, 'F')

    def left_accent(self, color=MEDIUM_BLUE):
        self.set_fill_color(*color)
        self.rect(0, 0, 3, self.H, 'F')

    def card(self, x, y, w, h, fill=NAVY_BLUE, border=None):
        self.set_fill_color(*fill)
        if border:
            self.set_draw_color(*border)
            self.set_line_width(0.5)
            self.rect(x, y, w, h, 'DF')
        else:
            self.rect(x, y, w, h, 'F')

    def accent_bar_v(self, x, y, w=2, h=12, color=MEDIUM_BLUE):
        self.set_fill_color(*color)
        self.rect(x, y, w, h, 'F')

    def hline(self, x, y, w, color=MEDIUM_BLUE, thickness=0.8):
        self.set_draw_color(*color)
        self.set_line_width(thickness)
        self.line(x, y, x + w, y)

    def slide_number(self, num):
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*MEDIUM_BLUE)
        self.text(self.W - 20, self.H - 7, f"{num} / {self.total_pages}")

    def section_header(self, title, subtitle=None, dark=True):
        tc = WHITE if dark else DARK_BLUE
        sc = LIGHT_BLUE if dark else MEDIUM_BLUE
        self.accent_bar_v(15, 10, 2, 12, MEDIUM_BLUE)
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(*tc)
        self.text(20, 20, title)
        if subtitle:
            self.set_font('Helvetica', '', 10)
            self.set_text_color(*sc)
            self.text(20, 27, subtitle)
        self.hline(15, 30, self.W - 30, MEDIUM_BLUE, 0.6)

    def txt(self, x, y, text, size=10, color=WHITE, bold=False, max_w=None):
        style = 'B' if bold else ''
        self.set_font('Helvetica', style, size)
        self.set_text_color(*color)
        if max_w:
            self.set_xy(x, y)
            self.multi_cell(max_w, size * 0.45, text, align='L')
        else:
            self.text(x, y, text)

    def bullet_list(self, x, y, items, size=9, color=WHITE, spacing=5.5, max_w=None):
        self.set_font('Helvetica', '', size)
        self.set_text_color(*color)
        cy = y
        for item in items:
            bullet = f"  >  {item}"
            if max_w:
                self.set_xy(x, cy)
                lines = self.multi_cell(max_w, size * 0.45, bullet, align='L', output='LINES')
                lc = len(lines) if lines else 1
                cy += spacing * max(1, lc * 0.7)
            else:
                self.text(x, cy, bullet)
                cy += spacing
        return cy

    def ctxt(self, y, text, size=10, color=WHITE, bold=False):
        style = 'B' if bold else ''
        self.set_font('Helvetica', style, size)
        self.set_text_color(*color)
        tw = self.get_string_width(text)
        self.text((self.W - tw) / 2, y, text)

    def ctxt_area(self, x, y, w, text, size=10, color=WHITE, bold=False):
        style = 'B' if bold else ''
        self.set_font('Helvetica', style, size)
        self.set_text_color(*color)
        tw = self.get_string_width(text)
        self.text(x + (w - tw) / 2, y, text)

    def safe_image(self, path, x, y, w=None, h=None):
        if os.path.exists(path):
            try:
                if w and h:
                    self.image(path, x, y, w, h)
                elif w:
                    self.image(path, x, y, w)
                elif h:
                    self.image(path, x, y, h=h)
                return True
            except Exception as e:
                print(f"  Warning: Could not load {path}: {e}")
                return False
        return False


def create_pdf():
    pdf = AeroVisionPDF()
    pdf.set_auto_page_break(auto=False)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 1: TITLE SLIDE
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.left_accent()

    pdf.set_font('Helvetica', 'B', 40)
    pdf.set_text_color(*WHITE)
    pdf.text(30, 40, "AEROVISION AI")

    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(*LIGHT_BLUE)
    pdf.text(30, 52, "AI-Powered Aircraft Surface Defect Detection")

    pdf.hline(30, 60, 80, MEDIUM_BLUE, 1)

    details = [
        ("TEAM", "Team Nexus Innovation"),
        ("TEAM LEAD", "Mugesh Kumar M"),
        ("MEMBERS", "Karthikeyan S  |  Gokulakrishnan S  |  Pradeep Kumar R"),
        ("COLLEGE", "K.S.Rangasamy College of Technology, Tiruchengode"),
        ("INDUSTRY", "Aerospace & Aviation"),
        ("CATEGORY", "AI-at-the-Edge / Real-Time Detection"),
    ]
    y = 70
    for label, value in details:
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_text_color(*MEDIUM_BLUE)
        pdf.text(30, y, label)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(*WHITE)
        pdf.text(75, y, value)
        y += 9

    pdf.card(200, 25, 80, 35, NAVY_BLUE, MEDIUM_BLUE)
    pdf.ctxt_area(200, 37, 80, "TATA TECHNOLOGIES", 9, MEDIUM_BLUE, True)
    pdf.ctxt_area(200, 50, 80, "InnoVent 2026", 18, WHITE, True)

    pdf.bottom_bar()
    pdf.slide_number(1)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 2: INTRODUCTION
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("TEAM INTRODUCTION", "Meet the Team Behind AeroVision AI")

    members = [
        ("Mugesh Kumar M", "Team Lead & AI/ML Developer",
         "Leads project architecture, designs and trains YOLOv8 models, manages ML pipeline."),
        ("Karthikeyan S", "Edge Computing & IoT Specialist",
         "Edge hardware setup, NVIDIA Jetson/RPi deployment, IoT integration."),
        ("Gokulakrishnan S", "Computer Vision Engineer",
         "Computer vision algorithms, image preprocessing, OpenCV pipelines."),
        ("Pradeep Kumar R", "Full-Stack & Data Engineer",
         "Flask web dashboard, REST APIs, database management, data pipelines."),
    ]

    for i, (name, role, desc) in enumerate(members):
        x = 15 + i * 68
        pdf.card(x, 38, 63, 90, NAVY_BLUE, MEDIUM_BLUE)
        # Circle avatar placeholder
        pdf.set_fill_color(*MEDIUM_BLUE)
        pdf.ellipse(x + 20, 43, 23, 23, 'F')
        pdf.ctxt_area(x, 57, 63, "[M]" if i == 0 else "[K]" if i == 1 else "[G]" if i == 2 else "[P]", 14, WHITE, True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(*WHITE)
        pdf.ctxt_area(x, 75, 63, name, 10, WHITE, True)
        pdf.set_font('Helvetica', '', 7)
        pdf.ctxt_area(x, 82, 63, role, 7, LIGHT_BLUE)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 4, 88)
        pdf.multi_cell(55, 3.5, desc, align='C')

    pdf.card(15, 135, 267, 20, NAVY_BLUE, MEDIUM_BLUE)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*OFF_WHITE)
    pdf.set_xy(20, 138)
    pdf.multi_cell(257, 4, "AeroVision AI is an AI-powered edge computing system for real-time aircraft surface defect detection, using a custom YOLOv8 model with ResCBAM attention and GhostConv for lightweight, high-accuracy inspection. Detects 6 defect types in <100ms, achieving 79.2% mAP@50.", align='C')

    pdf.bottom_bar()
    pdf.slide_number(2)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 3: PROBLEM STATEMENT
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("PROBLEM STATEMENT", "Why Aircraft Inspection Needs a Revolution", dark=False)

    problems = [
        ("SLOW PROCESS", "4+ hours per aircraft\nusing manual visual\ninspection methods"),
        ("LOW ACCURACY", "Only 85% detection\nrate due to human\nfatigue & error"),
        ("HIGH COST", "$200K+ annual facility\ncost, $100-300 per\nsingle inspection"),
        ("LOW OUTPUT", "Only 6 aircraft per\nday inspected,\ncreating bottlenecks"),
    ]

    for i, (title, desc) in enumerate(problems):
        x = 15 + i * 68
        pdf.card(x, 36, 63, 45, DARK_BLUE)
        pdf.ctxt_area(x, 50, 63, title, 12, LIGHT_BLUE, True)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 5, 55)
        pdf.multi_cell(53, 4, desc, align='C')

    pdf.card(15, 88, 267, 60, OFF_WHITE)
    pdf.txt(20, 96, "CURRENT LIMITATIONS OF EXISTING SOLUTIONS", 12, DARK_BLUE, True)

    left = [
        "Manual inspection inconsistent across inspectors",
        "Human fatigue leads to missed critical defects",
        "No real-time feedback during inspection process",
        "Training new inspectors takes 6-12 months",
    ]
    right = [
        "Existing AI solutions cost $200K-$250K per year",
        "Proprietary vendor lock-in with limited flexibility",
        "Slow inference speed (500ms-1s) not real-time",
        "Limited scalability to multiple production lines",
    ]
    pdf.bullet_list(20, 104, left, 8, DARK_GRAY, 6, 125)
    pdf.bullet_list(150, 104, right, 8, DARK_GRAY, 6, 125)

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(3)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 4: MARKET SIZE
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("MARKET SIZE & FUTURE POTENTIAL", "A Rapidly Growing Industry Opportunity")

    stats = [
        ("$15B", "Aircraft Maintenance\nInspection Market", MEDIUM_BLUE),
        ("8.5%", "CAGR Growth\nto 2030", ACCENT_BLUE),
        ("$26B", "Projected Market\nby 2030", SKY_BLUE),
        ("$500M", "Addressable Market\n(First 5 Years)", GREEN),
    ]
    for i, (val, label, clr) in enumerate(stats):
        x = 15 + i * 68
        pdf.card(x, 36, 63, 38, NAVY_BLUE, clr)
        pdf.ctxt_area(x, 50, 63, val, 22, clr, True)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 5, 56)
        pdf.multi_cell(53, 3.5, label, align='C')

    pdf.card(15, 80, 132, 70, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(20, 88, "MARKET SEGMENTS", 11, LIGHT_BLUE, True)
    segs = [
        "Global Aerospace NDT: $4.2B (2024) -> $7.8B (2030)",
        "AI-based Quality Inspection: $1.2B -> $4.5B by 2028",
        "Global Aerospace MRO Market: $90B+ annually",
        "Defense & Military Aviation: High growth sector",
        "Emerging Markets (India, Asia-Pacific): Fastest growth",
    ]
    pdf.bullet_list(20, 96, segs, 8, OFF_WHITE, 6, 120)

    pdf.card(152, 80, 130, 70, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(157, 88, "BUSINESS OPPORTUNITY", 11, LIGHT_BLUE, True)
    biz = [
        "TAM (Total Addressable): $4.5B",
        "SAM (Serviceable Available): $1.2B",
        "SOM (Serviceable Obtainable): $50M",
        "Break-even: 6-12 months",
        "5-Year ROI (500-Aircraft Fleet): $486K (548%)",
    ]
    pdf.bullet_list(157, 96, biz, 8, OFF_WHITE, 6, 120)

    pdf.bottom_bar()
    pdf.slide_number(4)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 5: PROJECT OBJECTIVE
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("PROJECT OBJECTIVE", "Defining Clear Goals for Impact", dark=False)

    pdf.card(15, 36, 267, 28, DARK_BLUE)
    pdf.txt(20, 42, "MAIN OBJECTIVE", 8, MEDIUM_BLUE, True)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 47)
    pdf.multi_cell(255, 5, "Develop an AI-powered edge computing system for real-time aircraft surface defect detection that achieves superior accuracy, speed, and cost-efficiency compared to manual inspection methods.", align='L')

    outcomes = [
        ("DETECTION ACCURACY", "Achieve >=94% mAP@50\ndefect detection accuracy\nacross all 6 categories"),
        ("REAL-TIME PROCESSING", "Process images in <100ms\nper frame enabling 30 FPS\nreal-time inspection"),
        ("COST REDUCTION", "Reduce inspection costs\nby 60% and inspection\ntime by 70%"),
    ]
    for i, (title, desc) in enumerate(outcomes):
        x = 15 + i * 90
        pdf.card(x, 70, 85, 50, OFF_WHITE)
        pdf.ctxt_area(x, 82, 85, title, 10, DARK_BLUE, True)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*DARK_GRAY)
        pdf.set_xy(x + 8, 87)
        pdf.multi_cell(69, 4, desc, align='C')

    pdf.txt(20, 130, "KEY GOALS", 11, DARK_BLUE, True)
    goals = ["Zero missed critical defects", "Edge-deployable model (<25MB)",
             "Web-based monitoring dashboard", "Scalable multi-camera support"]
    pdf.bullet_list(20, 137, goals, 8, DARK_GRAY, 6, 260)

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(5)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 6: PROPOSED SOLUTION
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("PROPOSED SOLUTION", "AeroVision AI -- How It Works")

    steps = [
        ("STEP 1", "IMAGE ACQUISITION", "High-resolution surface\nimages captured via UAV,\nhandheld camera or\nautomated system (640x640)"),
        ("STEP 2", "AI PROCESSING", "Custom YOLOv8 neural\nnetwork with ResCBAM\nattention processes image\nin 11-79ms on edge"),
        ("STEP 3", "INSTANT RESULTS", "Visual report with\nhighlighted defects,\nconfidence scores and\nautomatic alerts"),
    ]
    for i, (num, title, desc) in enumerate(steps):
        x = 15 + i * 90
        pdf.card(x, 36, 85, 68, NAVY_BLUE, MEDIUM_BLUE)
        pdf.set_fill_color(*MEDIUM_BLUE)
        pdf.ellipse(x + 28, 40, 28, 28, 'F')
        pdf.ctxt_area(x, 52, 85, num, 12, WHITE, True)
        pdf.ctxt_area(x, 74, 85, title, 10, LIGHT_BLUE, True)
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 8, 78)
        pdf.multi_cell(69, 4, desc, align='C')

    for i in range(2):
        x = 98 + i * 90
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(*MEDIUM_BLUE)
        pdf.text(x, 65, ">>>")

    pdf.card(15, 110, 267, 35, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(20, 118, "6 DEFECT TYPES DETECTED", 10, LIGHT_BLUE, True)

    defects = ["Crack", "Inclusion", "Corrosion", "Surface Wear", "Delamination", "Scratch"]
    dcolors = [RED_ACCENT, (180, 0, 180), ORANGE, SKY_BLUE, (128, 0, 128), (200, 200, 0)]
    for i, (name, clr) in enumerate(zip(defects, dcolors)):
        x = 20 + i * 44
        pdf.set_fill_color(*clr)
        pdf.rect(x, 124, 5, 5, 'F')
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*WHITE)
        pdf.text(x + 7, 128, name)

    pdf.bottom_bar()
    pdf.slide_number(6)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 7: INNOVATION AND NOVELTY
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("INNOVATION & NOVELTY", "What Makes AeroVision AI Unique", dark=False)

    innovations = [
        ("ResCBAM Attention",
         "Residual + CBAM (Channel + Spatial Attention) for superior feature extraction and reduced overfitting."),
        ("GhostConv Replacement",
         "Lightweight ghost convolutions in backbone achieve 40% parameter reduction for edge deployment."),
        ("WIOU Loss Function",
         "Improved Weighted IoU loss handles imbalanced data and prevents small target domination."),
    ]
    for i, (title, desc) in enumerate(innovations):
        x = 15 + i * 90
        pdf.card(x, 36, 85, 42, DARK_BLUE)
        pdf.ctxt_area(x, 48, 85, title, 11, LIGHT_BLUE, True)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 6, 54)
        pdf.multi_cell(73, 3.5, desc, align='C')

    pdf.card(15, 84, 132, 60, OFF_WHITE)
    pdf.txt(20, 92, "COMPETITIVE ADVANTAGES", 10, DARK_BLUE, True)
    adv = [
        "4.05M parameters -- 42% lighter than YOLOv5s",
        "79.2% mAP@50 -- best among all models",
        "Real-time edge inference, no cloud needed",
        "Multi-defect classification in single pass",
        "Open architecture -- no vendor lock-in",
    ]
    pdf.bullet_list(20, 99, adv, 8, DARK_GRAY, 6, 120)

    pdf.card(152, 84, 130, 60, OFF_WHITE)
    pdf.txt(157, 92, "AI-AT-THE-EDGE HIGHLIGHTS", 10, DARK_BLUE, True)
    edge = [
        "Runs on NVIDIA Jetson Nano / RPi 4",
        "Model: 25.4 MB (PT) / 12.7 MB (ONNX)",
        "No internet or cloud for inference",
        "TensorRT & ONNX optimized",
        "Factory floor ready -- 30 FPS",
    ]
    pdf.bullet_list(157, 99, edge, 8, DARK_GRAY, 6, 120)

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(7)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 8: SYSTEM ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("SYSTEM ARCHITECTURE", "End-to-End Pipeline Design")

    blocks = [
        ("Camera\nInput", 15, MEDIUM_BLUE),
        ("Image\nCapture", 60, NAVY_BLUE),
        ("Pre-\nprocess", 105, NAVY_BLUE),
        ("YOLOv8\nInference", 148, MEDIUM_BLUE),
        ("Post-\nprocess", 198, NAVY_BLUE),
        ("Defect\nClassify", 243, MEDIUM_BLUE),
    ]
    for label, x, clr in blocks:
        pdf.card(x, 36, 40, 20, clr, LIGHT_BLUE)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.set_text_color(*WHITE)
        pdf.set_xy(x + 2, 39)
        pdf.multi_cell(36, 4, label, align='C')

    for x in [55, 100, 145, 193, 238]:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(*LIGHT_BLUE)
        pdf.text(x, 48, ">")

    outputs = [("Alert System", 165, 62), ("Web Dashboard", 215, 62),
               ("Database", 165, 76), ("Report Gen.", 215, 76)]
    for label, x, y in outputs:
        pdf.card(x, y, 50, 10, NAVY_BLUE, ACCENT_BLUE)
        pdf.ctxt_area(x, y + 7, 50, label, 7, WHITE, True)

    # Model architecture image
    pdf.card(15, 60, 142, 82, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(20, 68, "MODEL: YOLOv8_ResBlock_CBAM_GhostConv", 9, LIGHT_BLUE, True)
    model_img = os.path.join(IMGS_DIR, "\u6a21\u578b\u7ed3\u6784.jpg")
    if not pdf.safe_image(model_img, 20, 72, w=130, h=65):
        specs = [
            "Backbone (GhostConv): Conv 3>16>32>64>128>256 | 2.1M params (51%)",
            "Neck (FPN): SPPF + Upsampling + ResCBAM | 1.5M params (37%)",
            "Head: 6-class detector + BBox regression | 0.46M params (11%)",
            "Total: 313 Layers | 4.05M Params | 10.2 GFLOPs | 25.4 MB",
        ]
        pdf.bullet_list(20, 75, specs, 8, OFF_WHITE, 7, 130)

    pdf.card(162, 84, 120, 58, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(167, 92, "ResCBAM ATTENTION MODULE", 9, LIGHT_BLUE, True)
    rescbam = os.path.join(IMGS_DIR, "ResCBAM.jpg")
    if not pdf.safe_image(rescbam, 167, 96, w=110, h=42):
        rdesc = [
            "Channel Attention: Global avg + max pooling",
            "Spatial Attention: 7x7 conv on pooled features",
            "Residual Connection: Skip for gradient flow",
        ]
        pdf.bullet_list(167, 100, rdesc, 8, OFF_WHITE, 6, 110)

    pdf.bottom_bar()
    pdf.slide_number(8)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 9: TECHNICAL IMPLEMENTATION
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("TECHNICAL IMPLEMENTATION", "Development Process & Methodology", dark=False)

    pdf.card(15, 36, 132, 110, OFF_WHITE)
    pdf.txt(20, 44, "DEVELOPMENT PROCESS", 11, DARK_BLUE, True)
    dev = [
        "1. Data Prep -- NEU-DET (1,800 images, 6 classes)",
        "2. Model Custom -- YOLOv8s + ResCBAM + GhostConv",
        "3. Transfer Learning -- COCO weights fine-tuned",
        "4. Training -- 100 epochs, batch 16, AdamW",
        "5. Validation -- mAP, precision, recall metrics",
        "6. Export -- ONNX (12.7 MB) for edge",
        "7. Web App -- Flask dashboard + REST APIs",
        "8. Edge Deploy -- Jetson Nano / RPi ready",
    ]
    pdf.bullet_list(20, 52, dev, 8, DARK_GRAY, 6.5, 120)

    pdf.card(152, 36, 130, 48, DARK_BLUE)
    pdf.txt(157, 44, "TRAINING CONFIGURATION", 10, LIGHT_BLUE, True)
    cfg = [
        "Epochs: 100 | Batch: 16 | Image: 640x640",
        "Optimizer: AdamW (lr=0.001, momentum=0.937)",
        "Warmup: 3 epochs | Early Stop: patience 20",
        "GPU: NVIDIA RTX 3050 (4GB, CUDA 11.8)",
    ]
    pdf.bullet_list(157, 52, cfg, 8, OFF_WHITE, 6, 120)

    pdf.card(152, 90, 130, 56, DARK_BLUE)
    pdf.txt(157, 98, "AI/ML APPROACH", 10, LIGHT_BLUE, True)
    ml = [
        "Detection: YOLOv8 (You Only Look Once v8)",
        "Attention: CBAM (Channel + Spatial)",
        "Augmentation: Mosaic, MixUp, HSV, Flip",
        "Loss: WIOU + Classification + Objectness",
        "Edge Opt: Quantization, ONNX, TensorRT",
    ]
    pdf.bullet_list(157, 106, ml, 8, OFF_WHITE, 6, 120)

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(9)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 10: TECHNOLOGIES
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("TECHNOLOGIES & FRAMEWORKS", "Our Complete Tech Stack")

    tech = [
        ("PROGRAMMING", ["Python 3.13", "HTML5 / CSS3", "JavaScript"]),
        ("AI FRAMEWORKS", ["Ultralytics YOLOv8", "PyTorch 2.7.1", "ONNX Runtime"]),
        ("COMPUTER VISION", ["OpenCV 4.8.0", "PIL / Pillow", "NumPy / SciPy"]),
        ("WEB & API", ["Flask 2.3.0", "REST APIs", "Gunicorn"]),
        ("EDGE HARDWARE", ["NVIDIA Jetson Nano", "Raspberry Pi 4", "RTX 3050"]),
        ("CLOUD / DEPLOY", ["AWS IoT Core", "Docker", "TensorRT"]),
        ("DATABASES", ["SQLite (Edge)", "PostgreSQL (Cloud)", "YAML Config"]),
        ("DEV TOOLS", ["VS Code", "Git / GitHub", "Jupyter Notebook"]),
    ]
    for i, (title, items) in enumerate(tech):
        row, col = i // 4, i % 4
        x = 15 + col * 68
        y = 36 + row * 58
        pdf.card(x, y, 63, 52, NAVY_BLUE, MEDIUM_BLUE)
        pdf.ctxt_area(x, y + 10, 63, title, 8, LIGHT_BLUE, True)
        pdf.bullet_list(x + 6, y + 17, items, 7, OFF_WHITE, 5.5, 50)

    pdf.bottom_bar()
    pdf.slide_number(10)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 11: CURRENT PROGRESS
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("CURRENT PROGRESS", "Development Milestones Achieved", dark=False)

    milestones = [
        ("Dataset Ready", "NEU-DET prepared\n1,800 images, 6 classes", True),
        ("Model Trained", "YOLOv8 custom model\n79.2% mAP@50", True),
        ("Web App Built", "Flask dashboard\nupload & detect", True),
        ("Model Exported", "ONNX (12.7MB)\nedge-ready", True),
        ("Edge Deploy", "Jetson Nano\nin progress", False),
    ]
    for i, (title, desc, done) in enumerate(milestones):
        x = 15 + i * 55
        clr = GREEN if done else ORANGE
        pdf.set_fill_color(*clr)
        pdf.rect(x + 8, 36, 35, 7, 'F')
        status = "DONE" if done else "IN PROGRESS"
        pdf.ctxt_area(x, 41, 52, status, 6, WHITE, True)
        pdf.card(x, 46, 52, 42, DARK_BLUE)
        pdf.ctxt_area(x, 56, 52, title, 9, LIGHT_BLUE, True)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 4, 60)
        pdf.multi_cell(44, 3.5, desc, align='C')

    # Add training result images
    pdf.card(15, 95, 267, 55, OFF_WHITE)
    pdf.txt(20, 102, "TRAINING RESULTS -- VALIDATION PREDICTIONS", 10, DARK_BLUE, True)

    vl = os.path.join(TRAIN_DIR, "val_batch0_labels.jpg")
    vp = os.path.join(TRAIN_DIR, "val_batch0_pred.jpg")
    if pdf.safe_image(vl, 22, 106, w=126, h=40):
        pdf.set_font('Helvetica', '', 6)
        pdf.set_text_color(*DARK_GRAY)
        pdf.text(65, 148, "Ground Truth Labels")
    if pdf.safe_image(vp, 155, 106, w=126, h=40):
        pdf.set_font('Helvetica', '', 6)
        pdf.set_text_color(*DARK_GRAY)
        pdf.text(195, 148, "Model Predictions")

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(11)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 12: CHALLENGES
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("CHALLENGES FACED", "Obstacles Encountered & Solutions Applied")

    challenges = [
        ("LIMITED DATASET", "Only 1,800 images for 6 classes",
         "Aggressive augmentation: mosaic, mixup, HSV, flip"),
        ("SMALL FEATURES", "Original 200x200 images too small",
         "Upscaled to 640x640 + CBAM attention module"),
        ("EDGE DEPLOYMENT", "Full model too heavy for edge",
         "GhostConv: 40% param reduction; ONNX: 12.7MB"),
        ("CLASS IMBALANCE", "Some defects harder to detect",
         "WIOU loss with adjusted class weights"),
        ("REAL-TIME SPEED", "Need <100ms with good accuracy",
         "YOLOv8s (small) + TensorRT = 35ms average"),
        ("HW INTEGRATION", "Camera + IoT + AI pipeline",
         "Modular Flask API with configurable inputs"),
    ]
    for i, (title, challenge, solution) in enumerate(challenges):
        row, col = i // 3, i % 3
        x = 15 + col * 90
        y = 36 + row * 58
        pdf.card(x, y, 85, 52, NAVY_BLUE, MEDIUM_BLUE)
        pdf.txt(x + 5, y + 8, title, 9, LIGHT_BLUE, True)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 5, y + 13)
        pdf.multi_cell(75, 3.5, f"Challenge: {challenge}", align='L')
        pdf.set_text_color(*GREEN)
        pdf.set_xy(x + 5, y + 28)
        pdf.multi_cell(75, 3.5, f"Solution: {solution}", align='L')

    pdf.bottom_bar()
    pdf.slide_number(12)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 13: RESULTS
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("RESULTS & ACHIEVEMENTS", "Performance Metrics & Benchmarks", dark=False)

    pdf.card(15, 36, 170, 70, DARK_BLUE)
    pdf.txt(20, 43, "MODEL COMPARISON ON NEU-DET DATASET", 9, LIGHT_BLUE, True)

    headers = ["Model", "Params", "FLOPs", "mAP50", "mAP50-95"]
    for j, h in enumerate(headers):
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_text_color(*MEDIUM_BLUE)
        pdf.text(22 + j * 30, 51, h)
    pdf.hline(20, 53, 155, MEDIUM_BLUE, 0.3)

    rows = [
        ("YOLOv5s", "7.04M", "15.9G", "70.87%", "35.02%"),
        ("YOLOv5m", "20.89M", "183.5G", "71.74%", "36.67%"),
        ("YOLOv7", "37.22M", "196.2G", "71.92%", "37.2%"),
        ("YOLOv8", "3.01M", "8.1G", "77.7%", "46.2%"),
        ("Ours *", "4.05M", "10.2G", "79.2%", "47.0%"),
    ]
    for i, rd in enumerate(rows):
        y = 58 + i * 7
        ours = i == 4
        fc = LIGHT_BLUE if ours else OFF_WHITE
        st = 'B' if ours else ''
        for j, v in enumerate(rd):
            pdf.set_font('Helvetica', st, 8)
            pdf.set_text_color(*fc)
            pdf.text(22 + j * 30, y, v)

    pdf.card(190, 36, 92, 70, DARK_BLUE)
    pdf.txt(195, 43, "VS MANUAL INSPECTION", 9, LIGHT_BLUE, True)
    perf = [
        ("Cost/Inspect", "$100-300 > $2-6", "98% Down"),
        ("Time/Aircraft", "4hrs > 15min", "94% Down"),
        ("Accuracy", "85% > 99%", "+14%"),
        ("Throughput", "6/day > 96/day", "1500% Up"),
        ("Annual Cost", "$200K > $50K", "75% Down"),
    ]
    for i, (m, c, imp) in enumerate(perf):
        y = 52 + i * 8
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(*OFF_WHITE)
        pdf.text(195, y, m)
        pdf.text(227, y, c)
        pdf.set_text_color(*GREEN)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.text(263, y, imp)

    # Charts
    pdf.card(15, 112, 132, 42, OFF_WHITE)
    pr = os.path.join(IMGS_DIR, "PR_curve.png")
    if not pdf.safe_image(pr, 17, 114, w=128, h=38):
        pdf.txt(50, 130, "[ PR Curve ]", 10, DARK_GRAY)

    pdf.card(152, 112, 130, 42, OFF_WHITE)
    cm = os.path.join(IMGS_DIR, "confusion_matrix_normalized.png")
    if not pdf.safe_image(cm, 154, 114, w=126, h=38):
        pdf.txt(185, 130, "[ Confusion Matrix ]", 10, DARK_GRAY)

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(13)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 14: DEMONSTRATION
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("DEMONSTRATION", "Working Prototype & Detection Results")

    pdf.card(15, 36, 132, 80, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(20, 43, "DETECTION HEATMAP", 9, LIGHT_BLUE, True)
    hm = os.path.join(IMGS_DIR, "heatmap.png")
    if not pdf.safe_image(hm, 20, 48, w=122, h=64):
        pdf.txt(55, 75, "[ Detection Heatmap ]", 10, OFF_WHITE)

    pdf.card(152, 36, 130, 80, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(157, 43, "MODEL PREDICTIONS", 9, LIGHT_BLUE, True)
    vp2 = os.path.join(IMGS_DIR, "val_pred.jpg")
    if not pdf.safe_image(vp2, 157, 48, w=120, h=64):
        pdf.txt(190, 75, "[ Predictions ]", 10, OFF_WHITE)

    pdf.card(15, 122, 132, 30, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(20, 129, "FLASK WEB APP -- RESULTS", 8, LIGHT_BLUE, True)
    r1 = os.path.join(RESULTS_DIR, "result_5aede7b55f7f4c328c4473197dee3464.jpg")
    r2 = os.path.join(RESULTS_DIR, "result_6a69dee4d2c34b01b44ac4d7352e08a6.jpg")
    pdf.safe_image(r1, 20, 133, w=58, h=16)
    pdf.safe_image(r2, 82, 133, w=58, h=16)

    pdf.card(152, 122, 130, 30, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(157, 129, "PROJECT LINKS", 8, LIGHT_BLUE, True)
    links = [
        "GitHub: github.com/MUGESH-KUMAR-M/AeroVision-AI",
        "API: /upload, /api/model-info, /health",
        "Demo: localhost:5000",
    ]
    pdf.bullet_list(157, 135, links, 7, OFF_WHITE, 5, 118)

    pdf.bottom_bar()
    pdf.slide_number(14)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 15: FUTURE ENHANCEMENTS
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("FUTURE ENHANCEMENTS", "Roadmap for Growth & Expansion", dark=False)

    cats = [
        ("ADDITIONAL FEATURES", [
            "Thermal/infrared for subsurface defects",
            "AR overlay for technician guidance",
            "Multi-camera 360-degree inspection",
            "Predictive maintenance integration",
        ]),
        ("SCALABILITY PLANS", [
            "Multi-production line deployment",
            "Cloud SaaS platform launch",
            "Federated learning across facilities",
            "Multi-aircraft type support",
        ]),
        ("COMMERCIAL DEPLOY", [
            "Industry certification (DO-254)",
            "Enterprise licensing model",
            "MRO facility partnerships",
            "Global deployment infrastructure",
        ]),
    ]
    for i, (title, items) in enumerate(cats):
        x = 15 + i * 90
        pdf.card(x, 36, 85, 80, DARK_BLUE)
        pdf.ctxt_area(x, 48, 85, title, 10, LIGHT_BLUE, True)
        pdf.bullet_list(x + 8, 56, items, 8, OFF_WHITE, 7, 70)

    pdf.card(15, 122, 267, 22, OFF_WHITE)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*DARK_BLUE)
    pdf.set_xy(20, 127)
    pdf.multi_cell(257, 4, "Future Vision: Autonomous drones with onboard AI | Mobile apps (Flutter/React Native) | IoT sensor fusion | Real-time video stream | Enterprise analytics", align='C')

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(15)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 16: PROTOTYPE PLAN
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("PROTOTYPE DEVELOPMENT PLAN", "3-Month Development Timeline")

    months = [
        ("MONTH 1", "Foundation & Data", [
            "Hardware procurement & setup",
            "Industrial camera integration",
            "NEU-DET dataset preparation",
            "Data augmentation pipeline",
            "Environment configuration",
        ], MEDIUM_BLUE),
        ("MONTH 2", "Model & Testing", [
            "YOLOv8 model customization",
            "ResCBAM + GhostConv integration",
            "100-epoch training cycle",
            "Validation & tuning",
            "Flask web app development",
        ], ACCENT_BLUE),
        ("MONTH 3", "Prototype & Validation", [
            "Physical prototype assembly",
            "Edge deploy (Jetson Nano)",
            "End-to-end system testing",
            "Performance benchmarking",
            "Documentation & demo prep",
        ], SKY_BLUE),
    ]
    for i, (month, title, tasks, clr) in enumerate(months):
        x = 15 + i * 90
        pdf.card(x, 36, 85, 12, clr)
        pdf.ctxt_area(x, 44, 85, f"{month}: {title}", 10, WHITE, True)
        pdf.card(x, 50, 85, 60, NAVY_BLUE, clr)
        pdf.bullet_list(x + 6, 58, tasks, 8, OFF_WHITE, 6, 72)

    pdf.card(15, 118, 267, 28, NAVY_BLUE, MEDIUM_BLUE)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*GREEN)
    pdf.set_xy(20, 123)
    pdf.multi_cell(257, 5, "STATUS: Month 2 Complete -- Model trained (79.2% mAP@50), Web app functional, ONNX export ready", align='C')
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*OFF_WHITE)
    pdf.set_xy(20, 134)
    pdf.multi_cell(257, 4, "Next: Physical prototype assembly & edge deployment with NVIDIA Jetson Nano", align='C')

    pdf.bottom_bar()
    pdf.slide_number(16)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 17: IMPACT
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.white_bg()
    pdf.top_bar(DARK_BLUE)
    pdf.section_header("IMPACT & SCALABILITY", "Creating Change Across Industries", dark=False)

    impacts = [
        ("SOCIAL IMPACT", [
            "Enhanced aviation safety for passengers",
            "Reduced human exposure to hazards",
            "Job upskilling: inspectors become AI operators",
            "Improved public confidence in air travel",
        ], MEDIUM_BLUE),
        ("INDUSTRY IMPACT", [
            "70% reduction in inspection time",
            "60% cost reduction per facility",
            "1500% throughput increase (6 to 96/day)",
            "Standardized quality across facilities",
        ], DARK_BLUE),
        ("ENVIRONMENTAL", [
            "Reduced material waste via early detection",
            "Lower energy vs cloud-based AI",
            "Extended aircraft lifecycle",
            "Minimized hazardous chemical usage",
        ], GREEN),
        ("REVENUE", [
            "SaaS: $50K-100K/year per facility",
            "Hardware + software bundle sales",
            "Per-inspection usage fees",
            "Consulting & customization",
        ], ACCENT_BLUE),
    ]
    for i, (title, items, clr) in enumerate(impacts):
        row, col = i // 2, i % 2
        x = 15 + col * 137
        y = 36 + row * 55
        pdf.card(x, y, 132, 48, DARK_BLUE)
        pdf.txt(x + 5, y + 8, title, 10, clr, True)
        pdf.bullet_list(x + 5, y + 16, items, 8, OFF_WHITE, 5.5, 120)

    pdf.card(15, 148, 267, 12, OFF_WHITE)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*DARK_BLUE)
    pdf.set_xy(20, 151)
    pdf.multi_cell(257, 4, "Scalability: Production lines > MRO > Airports > Defense > Industrial mfg > Automotive -- same AI, different domains.", align='C')

    pdf.set_fill_color(*DARK_BLUE)
    pdf.rect(0, pdf.H - 5, pdf.W, 5, 'F')
    pdf.slide_number(17)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 18: CONCLUSION
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.top_bar()
    pdf.section_header("CONCLUSION", "Summary of AeroVision AI")

    pdf.card(15, 36, 267, 30, NAVY_BLUE, MEDIUM_BLUE)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(20, 40)
    pdf.multi_cell(257, 4.5, "AeroVision AI transforms aircraft surface inspection from a slow, error-prone manual process into a fast, accurate, AI-powered system. Using custom YOLOv8 with ResCBAM attention and GhostConv on edge devices, we achieve real-time multi-defect detection -- setting a new benchmark for aerospace quality inspection.", align='C')

    metrics = [
        ("79.2%", "mAP@50\nAccuracy"),
        ("35ms", "Average\nInference"),
        ("4.05M", "Parameters\n(Lightweight)"),
        ("98%", "Cost\nReduction"),
        ("6", "Defect\nTypes"),
        ("$486K", "5-Year\nROI"),
    ]
    for i, (val, label) in enumerate(metrics):
        x = 15 + i * 45
        pdf.card(x, 72, 42, 32, NAVY_BLUE, MEDIUM_BLUE)
        pdf.ctxt_area(x, 83, 42, val, 16, MEDIUM_BLUE, True)
        pdf.set_font('Helvetica', '', 6)
        pdf.set_text_color(*OFF_WHITE)
        pdf.set_xy(x + 3, 88)
        pdf.multi_cell(36, 3, label, align='C')

    pdf.card(15, 110, 267, 38, NAVY_BLUE, MEDIUM_BLUE)
    pdf.txt(20, 118, "EXPECTED FUTURE OUTCOMES", 10, LIGHT_BLUE, True)
    future = [
        "Industry certification and commercial deployment within 12 months",
        "Expansion to automotive & industrial heavy machinery inspection",
        "Autonomous drone-based inspection integration",
        "SaaS platform serving 100+ aerospace facilities globally",
    ]
    pdf.bullet_list(20, 125, future, 8, OFF_WHITE, 6, 255)

    pdf.bottom_bar()
    pdf.slide_number(18)

    # ═══════════════════════════════════════════════════════════════════════
    # SLIDE 19: THANK YOU
    # ═══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.dark_bg()
    pdf.left_accent()
    pdf.top_bar()

    pdf.ctxt(60, "THANK YOU", 42, WHITE, True)
    pdf.ctxt(72, "AeroVision AI -- Redefining Aerospace Inspection with AI at the Edge", 12, LIGHT_BLUE)

    pdf.hline(90, 80, 117, MEDIUM_BLUE, 1)

    pdf.card(60, 88, 177, 60, NAVY_BLUE, MEDIUM_BLUE)
    contacts = [
        "Team Lead:   Mugesh Kumar M",
        "Team:        Karthikeyan S  |  Gokulakrishnan S  |  Pradeep Kumar R",
        "College:     K.S.Rangasamy College of Technology, Tiruchengode",
        "Email:       mugeshkumarm.22ai@ksr.ac.in",
        "GitHub:      github.com/MUGESH-KUMAR-M/AeroVision-AI",
    ]
    y = 98
    for item in contacts:
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(*OFF_WHITE)
        pdf.text(75, y, item)
        y += 9

    pdf.ctxt(158, "Tata Technologies InnoVent 2026  |  Aerospace & Aviation  |  AI-at-the-Edge", 8, MEDIUM_BLUE)

    pdf.bottom_bar()
    pdf.slide_number(19)

    # ═══════════════════════════════════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════════════════════════════════
    out = os.path.join(BASE_DIR, "Project_Presentation.pdf")
    pdf.output(out)
    print(f"\n{'='*60}")
    print(f"  PDF PRESENTATION GENERATED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"  File: {out}")
    print(f"  Pages: {pdf.total_pages}")
    print(f"  Format: A4 Landscape")
    print(f"  Theme: White & Dark Blue")
    print(f"{'='*60}")

    print(f"\n  Images included:")
    for d, dname in [(IMGS_DIR, "imgs"), (TRAIN_DIR, "runs/train1"), (RESULTS_DIR, "static/results")]:
        if os.path.exists(d):
            for f in os.listdir(d):
                fp = os.path.join(d, f)
                if os.path.isfile(fp) and f.endswith(('.jpg', '.png')):
                    print(f"    - {dname}/{f} ({os.path.getsize(fp)/1024:.0f} KB)")
    print(f"\n  Done!\n")


if __name__ == "__main__":
    create_pdf()
