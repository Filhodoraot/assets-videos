from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math, random, wave, urllib.request, shutil

ROOT = Path(__file__).resolve().parents[1]
BG = ROOT/'images'/'backgrounds'
PD = ROOT/'images'/'public-domain'
OV = ROOT/'graphics'/'overlays'
SFX = ROOT/'audio'/'sfx'
for p in (BG,PD,OV,SFX): p.mkdir(parents=True,exist_ok=True)

W,H=1920,1080
yy,xx=np.mgrid[0:H,0:W]
def radial(cx,cy,sx,sy): return np.exp(-(((xx-cx)/sx)**2+((yy-cy)/sy)**2))
def save_bg(name,a): Image.fromarray(np.clip(a,0,255).astype(np.uint8),'RGB').save(BG/name,quality=92,optimize=True)

# 12 fundos 1920x1080 criados do zero
specs=[
('neon_purple_dark_01.jpg',(3,2,14),[(450,760,650,500,(120,10,220)),(1450,300,540,420,(80,20,170))]),
('magenta_blue_gradient_01.jpg',(4,4,15),[(300,550,620,450,(245,20,175)),(1600,500,680,470,(20,90,245))]),
('cyan_dark_glow_01.jpg',(1,8,15),[(960,650,950,400,(5,170,220))]),
('cream_purple_corner_01.jpg',(4,2,14),[(80,930,430,320,(250,230,180)),(250,850,620,500,(110,5,230))]),
('gray_spotlight_01.jpg',(18,18,23),[(960,500,900,650,(95,95,105))]),
('red_black_glow_01.jpg',(5,1,2),[(960,580,900,520,(185,18,20))]),
('green_cyber_01.jpg',(1,7,5),[(1000,650,1100,500,(10,180,100))]),
('violet_pink_vertical_01.jpg',(9,2,22),[(960,300,650,530,(135,5,230)),(960,950,900,450,(100,12,210))]),
('orange_teal_cinematic_01.jpg',(3,8,10),[(300,680,600,460,(210,80,25)),(1600,420,700,520,(0,130,150))]),
('blue_horizon_01.jpg',(2,6,17),[(960,650,1200,250,(25,85,190))]),
]
for name,base,lights in specs:
    a=np.zeros((H,W,3),float); a[:]=base
    for cx,cy,sx,sy,c in lights: a+=radial(cx,cy,sx,sy)[...,None]*np.array(c)
    save_bg(name,a)
v=yy/(H-1); a=np.zeros((H,W,3),float); a[...,0]=255*(1-v)+40*v; a[...,1]=110*(1-v)+15*v; a[...,2]=170*(1-v)+75*v; save_bg('sunset_synthetic_01.jpg',a)
rng=np.random.default_rng(7); n=rng.normal(0,1,(H,W)); n=((n-n.min())/(n.max()-n.min())*255).astype(np.uint8); fog=np.asarray(Image.fromarray(n,'L').filter(ImageFilter.GaussianBlur(55)),float); fog=(fog-fog.min())/(fog.max()-fog.min()+1e-6); a=np.zeros((H,W,3),float); a[:]=[12,12,16]; a+=fog[...,None]*[55,55,65]; save_bg('fog_monochrome_01.jpg',a)

# overlays PNG transparentes
def save(name,im): im.save(OV/name,optimize=True,compress_level=9)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for x in range(0,W,80): d.line((x,0,x,H),fill=(135,90,255,80),width=2)
for y in range(0,H,80): d.line((0,y,W,y),fill=(135,90,255,80),width=2)
save('grid_neon_purple_01.png',im)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for y in range(0,H,4): d.line((0,y,W,y),fill=(255,255,255,24),width=1)
save('scanlines_soft_01.png',im)
a=np.zeros((H,W,4),np.uint8); rr=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); a[...,3]=np.clip((rr-.35)*170,0,180).astype(np.uint8); save('vignette_soft_01.png',Image.fromarray(a,'RGBA'))
im=Image.new('RGBA',(W,H),(0,0,0,0))
for cx,cy,c,alpha,r in [(-120,860,(124,0,255),180,520),(130,980,(255,0,190),120,360),(30,1020,(255,245,210),160,280)]:
    q=Image.new('RGBA',(W,H),(0,0,0,0)); qd=ImageDraw.Draw(q); qd.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(*c,alpha)); im=Image.alpha_composite(im,q.filter(ImageFilter.GaussianBlur(r//3)))
save('light_leak_purple_cream_01.png',im)
random.seed(2); im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for _ in range(320):
    x=random.randrange(W); y=random.randrange(H); r=random.choice([1,1,2,2,3]); d.ellipse((x-r,y-r,x+r,y+r),fill=(220,210,255,random.randrange(35,150)))
save('particles_soft_01.png',im)
random.seed(3); im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for _ in range(45):
    x=random.randrange(40,W-40); y=random.randrange(40,H-40); s=random.randrange(6,28); d.polygon([(x,y-s),(x+s//3,y-s//3),(x+s,y),(x+s//3,y+s//3),(x,y+s),(x-s//3,y+s//3),(x-s,y),(x-s//3,y-s//3)],fill=(255,100,240,random.randrange(80,220)))
save('sparkles_magenta_01.png',im)
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for y in range(0,H,20):
    for x in range(0,W,20):
        r=max(1,int(6*(1-min(1,math.hypot(x-W/2,y-H/2)/1100)))); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,65))
save('halftone_center_01.png',im)
random.seed(4); im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
for _ in range(100):
    ang=random.random()*math.tau; r1=random.randrange(250,650); r2=r1+random.randrange(80,420); x1=W/2+math.cos(ang)*r1; y1=H/2+math.sin(ang)*r1; x2=W/2+math.cos(ang)*r2; y2=H/2+math.sin(ang)*r2; d.line((x1,y1,x2,y2),fill=(255,255,255,random.randrange(25,100)),width=random.choice([1,2,3]))
save('speed_lines_radial_01.png',im)

# 10 SFX originais WAV
SR=44100
def wav(name,data):
    pcm=(np.clip(data,-1,1)*32767).astype(np.int16)
    with wave.open(str(SFX/name),'w') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
def lp(x,w): return np.convolve(x,np.ones(w)/w,mode='same')
n=int(.55*SR); x=np.linspace(0,1,n); z=lp(np.random.default_rng(1).normal(0,1,n),20); wav('whoosh_short_01.wav',.55*z/abs(z).max()*np.sin(np.pi*x)**1.8)
n=int(1.35*SR); x=np.linspace(0,1,n); z=lp(np.random.default_rng(2).normal(0,1,n),60); wav('whoosh_long_01.wav',.62*z/abs(z).max()*np.sin(np.pi*x)**1.4)
n=int(.7*SR); t=np.arange(n)/SR; wav('impact_bass_01.wav',.85*(np.sin(2*np.pi*(58-26*t)*t)*np.exp(-6*t)+.35*np.sin(2*np.pi*110*t)*np.exp(-9*t)))
n=int(.18*SR); t=np.arange(n)/SR; wav('ui_pop_01.wav',.45*(np.sin(2*np.pi*440*t)+.5*np.sin(2*np.pi*660*t))*np.exp(-20*t))
n=int(.08*SR); t=np.arange(n)/SR; wav('ui_click_01.wav',.6*np.sin(2*np.pi*1400*t)*np.exp(-55*t))
n=int(1.5*SR); t=np.arange(n)/SR; x=t/t[-1]; wav('riser_01.wav',.45*np.sin(2*np.pi*(100*t+650*t*x))*(x**2))
n=int(.9*SR); sig=np.zeros(n)
for f,delay,amp in [(1300,0,.45),(1800,.08,.35),(2400,.16,.25),(3100,.24,.18)]:
    i=int(delay*SR); tt=np.arange(n-i)/SR; sig[i:]+=amp*np.sin(2*np.pi*f*tt)*np.exp(-8*tt)
wav('sparkle_01.wav',sig)
n=int(.35*SR); sig=np.zeros(n); rng=np.random.default_rng(6)
for start in [0,.045,.11,.19,.27]:
    i=int(start*SR); L=min(int(.035*SR),n-i); sig[i:i+L]+=.5*rng.normal(0,1,L)*np.hanning(L)
wav('glitch_hit_01.wav',sig)
n=int(1*SR); t=np.arange(n)/SR; wav('transition_boom_01.wav',.8*np.sin(2*np.pi*45*t)*np.exp(-4*t)+.25*np.sin(2*np.pi*90*t)*np.exp(-7*t))
n=int(.65*SR); z=lp(np.random.default_rng(8).normal(0,1,n),45); wav('reverse_suck_01.wav',.55*z/abs(z).max()*np.linspace(0,1,n)**2)

# imagens externas somente quando a licença permite redistribuição
public={
'clouds_sky_pd.jpg':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Clouds_sky.jpg',
'beijing_skyline_night_pd.jpg':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Beijing_skyline_at_night.JPG',
'long_beach_skyline_night_pd.jpg':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Long_beach_skyline_night_city.jpg',
'football_stadium_berlin_cc0.jpg':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Football-stadium-berlin.jpg',
'stadium_crowd_pd.jpg':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Yankees_stadium_crowd.jpg',
'nya_ullevi_stadium_pd.jpg':'https://commons.wikimedia.org/wiki/Special:Redirect/file/Nya_Ullevi.jpg',
'earth_city_lights_nasa.jpg':'https://svs.gsfc.nasa.gov/vis/a030000/a030000/a030003/earth_lights_print.jpg'}
for name,url in public.items():
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'assets-videos-builder/1.0'})
        with urllib.request.urlopen(req,timeout=45) as r, open(PD/name,'wb') as f: shutil.copyfileobj(r,f)
        print('baixado:',name)
    except Exception as e: print('aviso:',name,e)
print('assets gerados')
