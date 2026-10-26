"""Gera as artes ORIGINAIS e padronizadas da loja Hydra (sem usar capas/logos oficiais).

Uso:  python tools/gerar_imagens.py      (requer: pip install pillow)
Formatos:
  - Jogos        -> poster vertical 3:4  (600x800)
  - Demais itens -> banner horizontal 16:10 (640x400)
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), "..", "static", "images")
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SS = 2  # supersampling para bordas suaves

def font(sz):
    try: return ImageFont.truetype(FB, sz)
    except Exception: return ImageFont.load_default()

def hexc(h): h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def gradient(w,h,c1,c2):
    a,b=hexc(c1),hexc(c2)
    img=Image.new("RGB",(w,h)); px=img.load()
    for y in range(h):
        for x in range(w):
            t=(x/w*0.35+y/h*0.65)
            px[x,y]=tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
    return img

def glow(img, draw_fn, color, blur=18, alpha=140):
    layer=Image.new("RGBA",img.size,(0,0,0,0))
    draw_fn(ImageDraw.Draw(layer), hexc(color)+(alpha,))
    layer=layer.filter(ImageFilter.GaussianBlur(blur*SS))
    img.paste(layer,(0,0),layer)

def bottom_fade(img, strength=210, start=0.45):
    w,h=img.size
    layer=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    y0=int(h*start)
    for y in range(y0,h):
        a=int(strength*((y-y0)/(h-y0))**1.4)
        d.line([(0,y),(w,y)],fill=(5,6,10,a))
    img.paste(layer,(0,0),layer)

def shards(img, color, seed, n=9):
    rnd=random.Random(seed); w,h=img.size
    layer=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    c=hexc(color)
    for _ in range(n):
        x,y=rnd.randint(0,w),rnd.randint(0,h); s=rnd.randint(w//6,w//2)
        ang=rnd.random()*math.tau
        pts=[(x+math.cos(ang+k*2.1)*s*rnd.uniform(.5,1),y+math.sin(ang+k*2.1)*s*rnd.uniform(.5,1)) for k in range(3)]
        d.polygon(pts,fill=c+(rnd.randint(8,22),))
    img.paste(layer,(0,0),layer)

def grid(img, step=40):
    w,h=img.size; layer=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    for x in range(0,w,step*SS): d.line([(x,0),(x,h)],fill=(255,255,255,10),width=SS)
    for y in range(0,h,step*SS): d.line([(0,y),(w,y)],fill=(255,255,255,10),width=SS)
    img.paste(layer,(0,0),layer)

def badge(d, w, text, color):
    f=font(13*SS); tw=d.textlength(text,font=f)
    d.rounded_rectangle([18*SS,18*SS,18*SS+tw+22*SS,18*SS+28*SS],radius=6*SS,fill=hexc(color)+(235,))
    d.text((29*SS,22*SS),text,font=f,fill=(255,255,255))

# ---------------- motivos ----------------
def m_mono(img, text, accent):
    w,h=img.size; f=font(int(w*(0.30 if len(text)<=3 else 0.2)))
    def g(d,c): d.text((w/2,h*0.42),text,font=f,fill=c,anchor="mm")
    glow(img,g,accent,blur=22,alpha=210)
    d=ImageDraw.Draw(img)
    d.text((w/2+3*SS,h*0.42+3*SS),text,font=f,fill=(0,0,0),anchor="mm")
    d.text((w/2,h*0.42),text,font=f,fill=(255,255,255),anchor="mm")
    # linha de destaque
    d.rectangle([w*0.30,h*0.58,w*0.70,h*0.58+3*SS],fill=hexc(accent))

def m_card(img, value, accent):
    w,h=img.size; d=ImageDraw.Draw(img)
    cw,ch=w*0.70,h*0.62; x0,y0=(w-cw)/2,(h-ch)/2-h*0.02
    glow(img,lambda dd,c: dd.rounded_rectangle([x0,y0,x0+cw,y0+ch],radius=26*SS,fill=c),accent,blur=26,alpha=170)
    d=ImageDraw.Draw(img)
    d.rounded_rectangle([x0,y0,x0+cw,y0+ch],radius=22*SS,fill=(14,16,24),outline=hexc(accent),width=3*SS)
    d.rounded_rectangle([x0+22*SS,y0+26*SS,x0+82*SS,y0+66*SS],radius=8*SS,fill=hexc(accent))  # chip
    for k in range(3): d.line([(x0+30*SS,y0+36*SS+k*9*SS),(x0+74*SS,y0+36*SS+k*9*SS)],fill=(14,16,24),width=2*SS)
    d.text((x0+cw-24*SS,y0+36*SS),"GIFT CARD",font=font(15*SS),fill=(190,195,208),anchor="rm")
    d.text((x0+24*SS,y0+ch-30*SS),value,font=font(44*SS),fill=(255,255,255),anchor="lm")
    for k in range(4): d.arc([x0+cw-110*SS+k*14*SS,y0+ch-80*SS,x0+cw-30*SS+k*14*SS,y0+ch-10*SS],200,340,fill=hexc(accent),width=3*SS)

def m_gauge(img, accent, level=0.78):
    w,h=img.size; cx,cy,r=w/2,h*0.62,h*0.36
    def g(d,c): d.arc([cx-r,cy-r,cx+r,cy+r],180,360,fill=c,width=22*SS)
    glow(img,g,accent,blur=14,alpha=200)
    d=ImageDraw.Draw(img)
    d.arc([cx-r,cy-r,cx+r,cy+r],180,360,fill=(40,44,58),width=20*SS)
    d.arc([cx-r,cy-r,cx+r,cy+r],180,180+180*level,fill=hexc(accent),width=20*SS)
    a=math.radians(180+180*level)
    d.line([(cx,cy),(cx+math.cos(a)*r*0.86,cy+math.sin(a)*r*0.86)],fill=(255,255,255),width=6*SS)
    d.ellipse([cx-12*SS,cy-12*SS,cx+12*SS,cy+12*SS],fill=(255,255,255))
    d.text((cx,cy+34*SS),"PERFORMANCE",font=font(14*SS),fill=(200,204,216),anchor="mm")

def m_gear(img, accent, teeth=8):
    w,h=img.size; cx,cy,R,r=w/2,h*0.48,h*0.30,h*0.22
    pts=[]
    for i in range(teeth*4):
        a=math.tau*i/(teeth*4); rr=R if (i%4) in (0,1) else r
        pts.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
    glow(img,lambda d,c: d.polygon(pts,fill=c),accent,blur=18,alpha=190)
    d=ImageDraw.Draw(img)
    d.polygon(pts,fill=hexc(accent)); d.ellipse([cx-r*.55,cy-r*.55,cx+r*.55,cy+r*.55],fill=(12,14,20))
    d.ellipse([cx-r*.25,cy-r*.25,cx+r*.25,cy+r*.25],fill=hexc(accent))

def m_chevrons(img, accent, n=3):
    w,h=img.size; cx=w/2; base=h*0.70; sz=h*0.20
    for k in range(n):
        y=base-k*sz*0.62; a=255-k*50
        def g(d,c,y=y): d.line([(cx-sz,y),(cx,y-sz*0.8),(cx+sz,y)],fill=c,width=22*SS,joint="curve")
        glow(img,g,accent,blur=12,alpha=200-k*40)
        d=ImageDraw.Draw(img)
        d.line([(cx-sz,y),(cx,y-sz*0.8),(cx+sz,y)],fill=hexc(accent)+(a,),width=18*SS,joint="curve")
    d=ImageDraw.Draw(img)
    d.rounded_rectangle([w*0.28,h*0.80,w*0.72,h*0.80+10*SS],radius=5*SS,fill=(40,44,58))
    d.rounded_rectangle([w*0.28,h*0.80,w*0.28+w*0.44*0.7,h*0.80+10*SS],radius=5*SS,fill=hexc(accent))

# ---------------- catálogo de artes ----------------
ARTS = [
 # arquivo, formato, cores, motivo, args, selo
 ("game-rdr","P","#2b0a05","#ff7a18","mono",("RDR","#ffb347"),"AVENTURA"),
 ("game-cyber","P","#0a0a1f","#e6d800","mono",("2077","#00f0ff"),"RPG"),
 ("game-elden","P","#0b1410","#c9a227","mono",("ER","#ffe08a"),"RPG"),
 ("game-minecraft","P","#0f2a12","#3fbf4f","mono",("MC","#9dff8a"),"SANDBOX"),
 ("game-forza","P","#06182e","#ff3b3b","mono",("FH5","#5ec8ff"),"CORRIDA"),
 ("game-gow","P","#1a0606","#8c1d1d","mono",("GoW","#ff6a5a"),"AÇÃO"),
 ("game-fc","P","#041a10","#14c26a","mono",("FC","#7dffb8"),"ESPORTE"),
 ("game-cod","P","#101214","#5a6b3a","mono",("CoD","#c3d97a"),"FPS"),
 ("gift-steam","L","#0a1a2e","#1b5a8f","card",("R$ 50","#4db3ff"),"STEAM"),
 ("gift-playstation","L","#08123a","#1a3fd0","card",("R$ 100","#6f9bff"),"PLAYSTATION"),
 ("gift-xbox","L","#06160a","#107c10","card",("R$ 100","#6bff6b"),"XBOX"),
 ("gift-google","L","#0b1f1a","#1f9d6a","card",("R$ 50","#5df2b0"),"GOOGLE PLAY"),
 ("gift-nintendo","L","#2a0508","#e60012","card",("R$ 100","#ff6b78"),"NINTENDO"),
 ("gift-roblox","L","#1a1a1f","#4a4f5c","card",("R$ 50","#c9ced9"),"ROBLOX"),
 ("opt-pc","L","#1a0610","#ff2038","gauge",(0.85,),"PC"),
 ("opt-fps","L","#14061f","#a62bff","gauge",(0.92,),"FPS"),
 ("opt-rede","L","#061a22","#12b5e5","gauge",(0.7,),"REDE"),
 ("opt-formatacao","L","#1f1306","#ff9a1f","gauge",(0.6,),"SISTEMA"),
 ("opt-limpeza","L","#06201a","#22d6a0","gauge",(0.75,),"LIMPEZA"),
 ("mod-minecraft","L","#0f2a12","#3fbf4f","gear",(8,),"MODS"),
 ("mod-texturas","L","#1c0f2e","#9b5cff","gear",(10,),"TEXTURAS"),
 ("mod-skyrim","L","#0e1a24","#6aa8d8","gear",(7,),"MODS"),
 ("mod-shaders","L","#2a1a05","#ffb020","gear",(12,),"SHADERS"),
 ("mod-instalacao","L","#2a0510","#ff2a55","gear",(9,),"SERVIÇO"),
 ("up-nivel","L","#1a0610","#ff2038","chev",(3,),"NÍVEL"),
 ("up-rank","L","#0e1630","#4d7cff","chev",(4,),"RANK"),
 ("up-farm","L","#1f1a05","#ffd02a","chev",(2,),"FARM"),
 ("up-missoes","L","#06201a","#22d6a0","chev",(3,),"MISSÕES"),
 ("up-pacote","L","#1f0620","#ff3bd4","chev",(5,),"COMBO"),
]

def make(name, fmt, c1, c2, motif, args, label):
    W,H=(600,800) if fmt=="P" else (640,400)
    a,b=hexc(c1),hexc(c2)
    mid="#%02x%02x%02x"%tuple(int(a[i]+(b[i]-a[i])*0.42) for i in range(3))
    img=gradient(W*SS,H*SS,c1,mid).convert("RGBA")
    shards(img,"#ffffff",hash(name)%1000)
    grid(img)
    accent=args[-1] if motif in ("mono","card") else c2
    if motif=="mono": m_mono(img,args[0],args[1])
    elif motif=="card": m_card(img,args[0],args[1])
    elif motif=="gauge": m_gauge(img,"#ffffff" if False else c2 if c2!="#000000" else "#ff2038",args[0])
    elif motif=="gear": m_gear(img,c2,args[0])
    elif motif=="chev": m_chevrons(img,c2,args[0])
    bottom_fade(img,200 if fmt=="P" else 120,0.55 if fmt=="P" else 0.7)
    d=ImageDraw.Draw(img); badge(d,W*SS,label,"#d50020")
    img=img.convert("RGB").resize((W,H),Image.LANCZOS)
    img.save(os.path.join(OUT,name+".jpg"),quality=88,optimize=True)

if __name__=="__main__":
    for a in ARTS: make(*a)
    print(len(ARTS),"imagens geradas em",os.path.abspath(OUT))


# ---------------- logo e banner ----------------
def make_brand():
    S=2
    # LOGO: hexágono vermelho com "H"
    L=Image.new("RGBA",(256*S,256*S),(0,0,0,0)); d=ImageDraw.Draw(L)
    cx=cy=128*S; R=118*S
    hexa=[(cx+math.cos(math.radians(60*i-30))*R, cy+math.sin(math.radians(60*i-30))*R) for i in range(6)]
    glow(L,lambda dd,c: dd.polygon(hexa,fill=c),"#ff2038",blur=10,alpha=200)
    d=ImageDraw.Draw(L); d.polygon(hexa,fill=(18,8,12),outline=hexc("#ff2038"),width=7*S)
    inner=[(cx+math.cos(math.radians(60*i-30))*R*0.78, cy+math.sin(math.radians(60*i-30))*R*0.78) for i in range(6)]
    d.polygon(inner,outline=(255,32,56,110),width=2*S)
    f=font(130*S); d.text((cx,cy+4*S),"H",font=f,fill=(255,255,255),anchor="mm")
    d.polygon([(cx-52*S,cy+46*S),(cx,cy+78*S),(cx+52*S,cy+46*S),(cx,cy+60*S)],fill=hexc("#ff2038"))
    L.resize((256,256),Image.LANCZOS).save(os.path.join(OUT,"hydra-logo.png"))
    # HERO 1400x520
    W,H=1400*S,520*S
    img=gradient(W,H,"#07070b","#3a0812").convert("RGBA")
    shards(img,"#ff2038",7,n=16); shards(img,"#ffffff",3,n=6)
    grid(img,50)
    cx,cy=W*0.78,H*0.5
    for k,r in enumerate((230,170,110)):
        rr=r*S; glow(img,lambda dd,c,rr=rr: dd.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=c,width=8*S),"#ff2038",blur=10,alpha=190-k*40)
    d=ImageDraw.Draw(img)
    for k,r in enumerate((230,170,110)):
        rr=r*S; d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=(255,32,56,200-k*50),width=3*S)
    d.text((cx,cy),"H",font=font(260*S),fill=(255,255,255,235),anchor="mm")
    img.convert("RGB").resize((1400,520),Image.LANCZOS).save(os.path.join(OUT,"hydra-hero.jpg"),quality=88,optimize=True)

if __name__=="__main__":
    make_brand(); print("logo e banner gerados")
