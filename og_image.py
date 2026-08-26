from PIL import Image, ImageDraw, ImageFont, ImageFilter

S=3
W,H=1200*S,630*S
paper=(245,240,230); ink=(46,40,51); ink_soft=(124,114,134)
accent=(123,110,208); line=(224,214,196); bar=(248,243,234); cream=(255,254,251)
dots=[(232,154,192),(143,199,232),(185,166,224)]
inners={'sky':(191,227,245),'peri':(207,196,240),'mint':(205,236,207)}
sk={'pink':(232,154,192),'blue':(143,199,232),'purple':(185,166,224),
    'yellow':(236,217,138),'coral':(239,159,138),'mint':(168,217,176)}

img=Image.new('RGB',(W,H),paper)
blob=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(blob)
def ell(cx,cy,r,col,a): bd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=col+(a,))
ell(int(1.05*W),int(-0.15*H),int(0.55*W),accent,55)
ell(int(-0.1*W),int(1.15*H),int(0.4*W),(236,220,240),55)
blob=blob.filter(ImageFilter.GaussianBlur(140*S//3))
img=Image.alpha_composite(img.convert('RGBA'),blob).convert('RGB')
draw=ImageDraw.Draw(img)

def sparkle(cx,cy,size,color):
    half=size/2; s=(2/22)*size
    pts=[(10,10),(10,6),(10,2),(10,14),(10,18),(6,10),(2,10),(14,10),(18,10),
         (6,6),(14,14),(6,14),(14,6)]
    for x,y in pts:
        px=cx-half+(x/22)*size; py=cy-half+(y/22)*size
        draw.rectangle([px,py,px+s,py+s],fill=color)

wins=[(860,64,240,170,'sky','blue'),(880,290,220,160,'peri','purple')]
shadow=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(shadow)
for x,y,w,h,ic,stc in wins:
    x*=S;y*=S;w*=S;h*=S
    sd.rounded_rectangle([x+7*S,y+9*S,x+w+7*S,y+h+9*S],radius=14*S,fill=(46,40,51,55))
shadow=shadow.filter(ImageFilter.GaussianBlur(9*S))
img=Image.alpha_composite(img.convert('RGBA'),shadow).convert('RGB')
draw=ImageDraw.Draw(img)
for x,y,w,h,ic,stc in wins:
    x*=S;y*=S;w*=S;h*=S; th=int(h*0.24)
    draw.rounded_rectangle([x,y,x+w,y+h],radius=14*S,fill=cream,outline=line,width=S)
    draw.rounded_rectangle([x,y,x+w,y+th],radius=14*S,fill=bar)
    draw.rectangle([x,y+th-14*S,x+w,y+th],fill=bar)
    draw.line([x,y+th,x+w,y+th],fill=line,width=S)
    dr=6*S; dy=y+th//2
    for i,c in enumerate(dots):
        dx=x+18*S+i*18*S; draw.ellipse([dx-dr,dy-dr,dx+dr,dy+dr],fill=c)
    m=18*S; ib=[x+m,y+th+10*S,x+w-m,y+h-m]
    draw.rounded_rectangle(ib,radius=8*S,fill=inners[ic])
    scx=(ib[0]+ib[2])/2; scy=(ib[1]+ib[3])/2
    sparkle(scx,scy,min(ib[2]-ib[0],ib[3]-ib[1])*0.55,sk[stc])

for cx,cy,sz,c in [(760,120,22,'coral'),(792,420,26,'yellow'),(1080,250,20,'pink'),
                   (150,540,24,'mint'),(120,90,18,'purple'),(720,560,22,'blue')]:
    sparkle(cx*S,cy*S,sz*S,sk[c])

FS='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
FM='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
f_name=ImageFont.truetype(FS,72*S)
f_lab=ImageFont.truetype(FM,24*S)
f_sub=ImageFont.truetype(FM,21*S)
X0=88*S
def track(txt,font,x,y,fill,sp):
    for ch in txt:
        draw.text((x,y),ch,font=font,fill=fill); x+=draw.textlength(ch,font=font)+sp*S

draw.text((X0,230*S),"Christine Li",font=f_name,fill=ink)
track("DATA · AI PRODUCT · ML",f_lab,X0,330*S,accent,2)
draw.text((X0,372*S),"M. Analytics · UC Berkeley  ·  B.S. Statistics · UC Davis",font=f_sub,fill=ink_soft)

img.resize((1200,630),Image.LANCZOS).save('og-image.png')
print("saved")
