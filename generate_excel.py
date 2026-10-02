import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Create workbook
wb = openpyxl.Workbook()

# Sheet 1: 20 QR Codes Directory
ws1 = wb.active
ws1.title = "20_TABLES_QR_DIRECTORY"
ws1.views.sheetView[0].showGridLines = True

# Colors (Royal Gold & Dark Luxury theme)
gold_fill = PatternFill(start_color="D4AF37", end_color="D4AF37", fill_type="solid")
gold_light_fill = PatternFill(start_color="F5E6BE", end_color="F5E6BE", fill_type="solid")
header_fill = PatternFill(start_color="1A120B", end_color="1A120B", fill_type="solid")
accent_fill = PatternFill(start_color="2C1810", end_color="2C1810", fill_type="solid")
alt_row_fill = PatternFill(start_color="FFFDF8", end_color="FFFDF8", fill_type="solid")
highlight_row = PatternFill(start_color="FFF8E7", end_color="FFF8E7", fill_type="solid")

font_title = Font(name="Arial", size=16, bold=True, color="D4AF37")
font_subtitle = Font(name="Arial", size=11, bold=True, color="FFFFFF")
font_header = Font(name="Arial", size=11, bold=True, color="D4AF37")
font_regular = Font(name="Arial", size=10, color="000000")
font_bold = Font(name="Arial", size=10, bold=True, color="000000")
font_link = Font(name="Arial", size=10, underline="single", color="1B5E20", bold=True)
font_vip = Font(name="Arial", size=10, bold=True, color="B8860B")

thin_border = Border(
    left=Side(style='thin', color='D4AF37'),
    right=Side(style='thin', color='D4AF37'),
    top=Side(style='thin', color='D4AF37'),
    bottom=Side(style='thin', color='D4AF37')
)

header_border = Border(
    left=Side(style='medium', color='D4AF37'),
    right=Side(style='medium', color='D4AF37'),
    top=Side(style='medium', color='D4AF37'),
    bottom=Side(style='medium', color='D4AF37')
)

# Title Block
ws1.merge_cells("A1:G1")
ws1["A1"] = "HOTEL THE SARA (गुना, मध्य प्रदेश) — SMART TABLE QR DIRECTORY"
ws1["A1"].font = font_title
ws1["A1"].fill = header_fill
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 35

ws1.merge_cells("A2:G2")
ws1["A2"] = "Stay in Style • Luxury Dining, Banquets & Executive Stays | AB Road, Guna (M.P.) | 20 Tables Master Hub"
ws1["A2"].font = font_subtitle
ws1["A2"].fill = accent_fill
ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[2].height = 24

# Headers
headers = [
    "टेबल नंबर (Table #)",
    "टेबल पहचान (Display Label)",
    "स्मार्ट QR कोड लिंक (Smart Web Link - Click to Open)",
    "गूगल रिव्यू शील्ड (Google Review Filter)",
    "मैनेजर टेलीग्राम अलर्ट (Telegram Alert)",
    "लाइसेंस सीरियल नंबर (Hardware Serial)",
    "स्टैंडी स्टेटस (Print Status)"
]

ws1.row_dimensions[4].height = 28
for col_idx, h in enumerate(headers, 1):
    cell = ws1.cell(row=4, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = header_fill
    cell.border = header_border
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# 20 Tables Data
base_url = "https://hospitalityqr.github.io/sara-hotel-guna/?table="

for i in range(1, 21):
    row_idx = 4 + i
    ws1.row_dimensions[row_idx].height = 24
    
    table_num = i
    display_label = "VIP TABLE #01" if i == 1 else f"TABLE #{i:02d}"
    url = f"{base_url}{i}"
    shield_status = "100% Active (4-5★ Direct Google / 1-3★ Block Google)"
    tg_status = "Active (Instant Bot Message + Call)"
    serial = f"HS-GUNA-VIP-{i:03d}" if i == 1 else f"HS-GUNA-TBL-{i:03d}"
    standee_status = "Ready to Print (Acrylic 4x6 / 6x8)"
    
    r_fill = highlight_row if (i % 2 == 0) else alt_row_fill
    if i == 1:
        r_fill = gold_light_fill

    c1 = ws1.cell(row=row_idx, column=1, value=f"#{table_num:02d}")
    c1.font = font_vip if i == 1 else font_bold
    c1.alignment = Alignment(horizontal="center", vertical="center")
    
    c2 = ws1.cell(row=row_idx, column=2, value=display_label)
    c2.font = font_vip if i == 1 else font_bold
    c2.alignment = Alignment(horizontal="center", vertical="center")
    
    c3 = ws1.cell(row=row_idx, column=3, value=url)
    c3.hyperlink = url
    c3.font = font_link
    c3.alignment = Alignment(horizontal="left", vertical="center")
    
    c4 = ws1.cell(row=row_idx, column=4, value=shield_status)
    c4.font = font_regular
    c4.alignment = Alignment(horizontal="center", vertical="center")
    
    c5 = ws1.cell(row=row_idx, column=5, value=tg_status)
    c5.font = font_regular
    c5.alignment = Alignment(horizontal="center", vertical="center")
    
    c6 = ws1.cell(row=row_idx, column=6, value=serial)
    c6.font = font_bold
    c6.alignment = Alignment(horizontal="center", vertical="center")
    
    c7 = ws1.cell(row=row_idx, column=7, value=standee_status)
    c7.font = font_regular
    c7.alignment = Alignment(horizontal="center", vertical="center")
    
    for c in [c1, c2, c3, c4, c5, c6, c7]:
        c.fill = r_fill
        c.border = thin_border

# Auto adjust column widths
ws1.column_dimensions['A'].width = 16
ws1.column_dimensions['B'].width = 18
ws1.column_dimensions['C'].width = 58
ws1.column_dimensions['D'].width = 44
ws1.column_dimensions['E'].width = 34
ws1.column_dimensions['F'].width = 22
ws1.column_dimensions['G'].width = 28

# Sheet 2: Guest Feedback Log Register (Pre-formatted for Manager)
ws2 = wb.create_sheet(title="GUEST_FEEDBACK_REGISTER")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:G1")
ws2["A1"] = "HOTEL THE SARA — 1, 2, 3 STAR GUEST FEEDBACK & SUGGESTION REGISTER"
ws2["A1"].font = font_title
ws2["A1"].fill = header_fill
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 35

ws2.merge_cells("A2:G2")
ws2["A2"] = "सभी 1, 2, 3 स्टार सुझावों का रिकॉर्ड रजिस्टर | मैनेजर एक्शन व समाधान स्टेटस"
ws2["A2"].font = font_subtitle
ws2["A2"].fill = accent_fill
ws2["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[2].height = 24

log_headers = [
    "क्र.सं. (S.No)",
    "तारीख (Date)",
    "समय (Time)",
    "टेबल नंबर (Table #)",
    "स्टार रेटिंग (Rating)",
    "ग्राहक का सुझाव / समस्या (Guest Written Remark)",
    "मैनेजर समाधान / स्टेटस (Manager Action Taken)"
]

ws2.row_dimensions[4].height = 28
for col_idx, h in enumerate(log_headers, 1):
    cell = ws2.cell(row=4, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = header_fill
    cell.border = header_border
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Sample entries to show the manager how it works
sample_rows = [
    (1, "03/10/2026", "02:25 AM", "VIP TABLE #01", "2 Stars", 'भोजन का स्वाद: "पनीर टिक्का में मसाला थोड़ा तेज था"', "मैनेजर ने टेबल पर जाकर कॉम्प्लिमेंट्री डेजर्ट ऑफर किया। कस्टमर 100% संतुष्ट।"),
    (2, "03/10/2026", "01:10 PM", "TABLE #04", "3 Stars", 'सर्विंग में समय: "सूप आने में 15 मिनट लगे"', "किचन शेफ को इन्फॉर्म किया गया और सर्विस स्पीड सुधारी गई।"),
    (3, "03/10/2026", "08:45 PM", "TABLE #07", "2 Stars", 'AC / वातावरण: "AC का फ्लो बहुत ज्यादा तेज था"', "टेबल का टेम्परेचर एडजस्ट किया गया।"),
]

for s in sample_rows:
    row_idx = 4 + s[0]
    ws2.row_dimensions[row_idx].height = 24
    for col_idx, val in enumerate(s, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=val)
        cell.font = font_regular
        cell.border = thin_border
        cell.fill = alt_row_fill
        cell.alignment = Alignment(horizontal="center" if col_idx <= 5 else "left", vertical="center")

# Pre-fill blank rows for future entries
for r in range(8, 50):
    ws2.row_dimensions[r].height = 22
    for c in range(1, 8):
        cell = ws2.cell(row=r, column=c, value=r-4 if c == 1 else "")
        cell.border = thin_border
        cell.fill = highlight_row if r % 2 == 0 else alt_row_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

ws2.column_dimensions['A'].width = 12
ws2.column_dimensions['B'].width = 15
ws2.column_dimensions['C'].width = 15
ws2.column_dimensions['D'].width = 18
ws2.column_dimensions['E'].width = 16
ws2.column_dimensions['F'].width = 45
ws2.column_dimensions['G'].width = 45

# Save workbook
file_path = "HOTEL_THE_SARA_20_TABLES_MASTER_DIRECTORY.xlsx"
wb.save(file_path)
print(f"Successfully generated: {file_path}")
