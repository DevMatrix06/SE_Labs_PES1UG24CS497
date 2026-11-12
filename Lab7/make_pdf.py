from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
W,H=A4
c=canvas.Canvas("Lab7_FuzzTesting_PES1UG24CS497.pdf",pagesize=A4)
def read(p): return open("logs/"+p,encoding="utf-8").read().replace("\t","    ").splitlines()
def page(title,note,lines,first=False):
    y=H-50
    c.setFont("Helvetica-Bold",15); c.drawString(40,y,title); y-=18
    c.setFont("Helvetica",9); c.drawString(40,y,"Tejas P  |  SRN: PES1UG24CS497  |  Lab 7: Fuzzing for Input Validation Bugs"); y-=16
    for n in note:
        c.drawString(40,y,n); y-=12
    y-=6
    # terminal box
    fs=6.2; lh=7.4; maxc=int((W-80-12)/(fs*0.6))
    out=[]
    for l in lines:
        while len(l)>maxc: out.append(l[:maxc]); l="    "+l[maxc:]
        out.append(l)
    h=len(out)*lh+14
    c.setFillColorRGB(.1,.1,.12); c.rect(34,y-h,W-68,h,fill=1,stroke=0)
    c.setFillColorRGB(.85,.9,.85); c.setFont("Courier",fs)
    yy=y-10
    for l in out: c.drawString(40,yy,l); yy-=lh
    c.setFillColorRGB(0,0,0); c.showPage()
def chunks(lines,n=95):
    return [lines[i:i+n] for i in range(0,len(lines),n)]
from reportlab.lib.utils import ImageReader
def shot(title,img,cap):
    c.setFont("Helvetica-Bold",14); c.drawString(40,H-50,title)
    c.setFont("Helvetica",9); c.drawString(40,H-66,"Tejas P  |  SRN: PES1UG24CS497"); c.drawString(40,H-79,cap)
    im=ImageReader("screenshots/"+img); iw,ih=im.getSize()
    w=W-80; h=w*ih/iw
    c.drawImage(im,40,H-95-h,w,h); c.showPage()
shot("Step 2: Run the buggy processor.py","step2_buggy_run.png","python processor.py on the original code. Valid input works, 'abc' crashes with a ValueError.")
shot("Step 4: pytest on the buggy code","step4_buggy_pytest.png","6 failed, 3 passed (bottom of the pytest output).")
shot("Step 5: Run the fixed processor.py","step5_fixed_run.png","Same inputs. Bad input now prints a message instead of a traceback.")
shot("Step 6: pytest on the fixed code","step6_fixed_pytest.png","All 9 tests pass.")
bugs=["Bugs Hypothesis found, and how each was fixed:","",
"verify_isbn10_format",
"  None or non-string input raised AttributeError on .replace. Now a type check returns None.",
"  Empty or short strings raised IndexError on cleaned[0] and cleaned[9]. Now a regex requires",
"  9 digits plus a digit or X.",
"  A non-digit first character (':' or 'a') raised ValueError in int(). The same regex rejects it.",
"",
"calculate_depreciation_factor",
"  None raised AttributeError on .split. Now a type check returns None.",
"  A missing or extra slash raised ValueError on unpacking. Now it needs exactly two parts.",
"  Empty or non-numeric parts raised ValueError in float(). Now wrapped in try/except.",
"  '3/0' raised ZeroDivisionError. A lifespan of zero or less is now rejected.",
"  'nan' and 'inf' parse as floats and produced inf/nan results. Now checked with math.isfinite.",
"  A negative age gave a factor above 1. Negative ages are now rejected.",
"",
"lookup_condition_multiplier",
"  None raised AttributeError on .strip. Now a type check returns None.",
"  An unknown grade raised KeyError. dict.get now returns None.",
"  'like new' and 'Like-New' now match LIKE_NEW as well.",
"",
"Invalid input returns None, and main() turns that into a readable message."]
c.setFont("Helvetica-Bold",15); c.drawString(40,H-50,"Summary of bugs and fixes"); c.setFont("Helvetica",9)
c.drawString(40,H-66,"Tejas P  |  SRN: PES1UG24CS497")
y=H-92
for l in bugs:
    c.setFont("Helvetica-Bold" if l and not l.startswith(" ") else "Helvetica",9.5); c.drawString(40,y,l); y-=14
c.showPage(); c.save()
