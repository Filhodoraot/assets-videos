from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math, random, wave, urllib.request, time

ROOT = Path(__file__).resolve().parents[1]
SFX = ROOT / 'audio' / 'sfx'
PUBLIC_AUDIO = ROOT / 'audio' / 'public-domain'
PUBLIC_VIDEO = ROOT / 'video' / 'public-domain'
GIFS = ROOT / 'gifs' / 'overlays'
for p in (SFX, PUBLIC_AUDIO, PUBLIC_VIDEO, GIFS):
    p.mkdir(parents=True, exist_ok=True)

SR = 44100

def save_wav(name, data, sr=SR):
    data = np.asarray(data, dtype=float)
    peak = np.max(np.abs(data)) or 1.0
    pcm = (np.clip(data / max(1.0, peak), -1, 1) * 32767).astype(np.int16)
    with wave.open(str(SFX / name), 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(pcm.tobytes())


def lowpass(x, n):
    return np.convolve(x, np.ones(n) / n, mode='same')

rng = np.random.default_rng(42)

# SFX originais: equivalentes de efeitos populares, sem copiar arquivos protegidos.
# 1) impacto grave pesado
n = int(0.95 * SR); t = np.arange(n) / SR
sig = 0.9*np.sin(2*np.pi*(52-20*t)*t)*np.exp(-4.6*t)
sig += 0.28*np.sin(2*np.pi*105*t)*np.exp(-8*t)
sig += 0.18*lowpass(rng.normal(0,1,n), 25)*np.exp(-10*t)
save_wav('impact_heavy_02.wav', sig)

# 2) bass drop
n = int(1.2 * SR); t = np.arange(n) / SR
f = 105 - 72*(t/t[-1])
phase = 2*np.pi*np.cumsum(f)/SR
save_wav('bass_drop_01.wav', 0.82*np.sin(phase)*np.exp(-1.9*t))

# 3) whoosh rápido
n = int(.42 * SR); x = np.linspace(0,1,n)
z = lowpass(rng.normal(0,1,n), 12); z /= np.max(np.abs(z))
save_wav('whoosh_fast_02.wav', .68*z*np.sin(np.pi*x)**1.6)

# 4) whoosh grave
n = int(.85 * SR); x = np.linspace(0,1,n)
z = lowpass(rng.normal(0,1,n), 50); z /= np.max(np.abs(z))
save_wav('whoosh_deep_01.wav', .72*z*np.sin(np.pi*x)**1.35)

# 5) reverse riser
n = int(1.4 * SR); t = np.arange(n)/SR; x=t/t[-1]
z = lowpass(rng.normal(0,1,n), 45); z /= np.max(np.abs(z))
save_wav('reverse_riser_01.wav', .48*z*(x**2.4))

# 6) notification ding
n = int(.62*SR); t=np.arange(n)/SR
sig=.42*np.sin(2*np.pi*880*t)*np.exp(-7*t)+.25*np.sin(2*np.pi*1320*t)*np.exp(-9*t)
save_wav('notification_ding_01.wav',sig)

# 7) camera shutter sintético
n=int(.19*SR); sig=np.zeros(n)
for delay,amp in [(0,.75),(.035,.55),(.073,.38)]:
    i=int(delay*SR); L=min(int(.025*SR),n-i)
    noise=rng.normal(0,1,L)*np.hanning(L)
    sig[i:i+L]+=amp*noise
save_wav('camera_shutter_01.wav',sig)

# 8) heartbeat
n=int(1.25*SR); sig=np.zeros(n)
for delay,amp,freq in [(0.08,.9,58),(0.24,.52,64),(.72,.78,56),(.87,.42,62)]:
    i=int(delay*SR); tt=np.arange(n-i)/SR
    sig[i:]+=amp*np.sin(2*np.pi*freq*tt)*np.exp(-15*tt)
save_wav('heartbeat_01.wav',sig)

# 9) glitch stutter
n=int(.44*SR); sig=np.zeros(n)
for start in [0,.042,.09,.17,.24,.31,.37]:
    i=int(start*SR); L=min(int(.03*SR),n-i)
    tone=np.sin(2*np.pi*rng.choice([210,320,510,820,1300])*np.arange(L)/SR)
    sig[i:i+L]+=.45*tone*np.hanning(L)
save_wav('glitch_stutter_02.wav',sig)

# 10) phone ring moderno
n=int(1.8*SR); t=np.arange(n)/SR
carrier=.35*np.sin(2*np.pi*720*t)+.18*np.sin(2*np.pi*960*t)
env=((np.sin(2*np.pi*2.15*t)>0).astype(float))*np.exp(-.18*t)
save_wav('phone_ring_modern_01.wav',carrier*env)

# 11) record stop / tape stop
n=int(.85*SR); t=np.arange(n)/SR; x=t/t[-1]
f=620*(1-x)**2+55
phase=2*np.pi*np.cumsum(f)/SR
save_wav('tape_stop_01.wav',.5*np.sin(phase)*(1-x)**.6)

# 12) sparkle chime
n=int(1.15*SR); sig=np.zeros(n)
for delay,freq,amp in [(0,1300,.34),(.08,1820,.28),(.17,2480,.22),(.28,3310,.16),(.42,4100,.10)]:
    i=int(delay*SR); tt=np.arange(n-i)/SR
    sig[i:]+=amp*np.sin(2*np.pi*freq*tt)*np.exp(-6.5*tt)
save_wav('sparkle_chime_02.wav',sig)

# 13) whistle short sintético
n=int(.48*SR); t=np.arange(n)/SR; f=1900+180*np.sin(2*np.pi*5*t)
phase=2*np.pi*np.cumsum(f)/SR
env=np.sin(np.pi*np.clip(t/.48,0,1))**.7
save_wav('whistle_short_synth_01.wav',.35*np.sin(phase)*env)

# 14) typing burst
n=int(1.15*SR); sig=np.zeros(n)
for start in np.arange(.03,1.1,.09):
    i=int(start*SR); L=min(int(.018*SR),n-i)
    burst=rng.normal(0,1,L)*np.hanning(L)
    sig[i:i+L]+=.34*burst
save_wav('typing_burst_01.wav',sig)

# GIF loops criados do zero
GW, GH, FRAMES = 480, 270, 30

def save_gif(name, frames, duration=50):
    pal = [f.convert('P', palette=Image.Palette.ADAPTIVE, colors=128) for f in frames]
    pal[0].save(GIFS/name, save_all=True, append_images=pal[1:], duration=duration, loop=0, optimize=True, disposal=2)

random.seed(11)
pts=[(random.random()*GW,random.random()*GH,random.uniform(.5,1.8),random.random()*math.tau) for _ in range(80)]
frames=[]
for k in range(FRAMES):
    im=Image.new('RGBA',(GW,GH),(0,0,0,255)); d=ImageDraw.Draw(im); tt=k/FRAMES*math.tau
    for x,y,s,p in pts:
        xx=(x+18*math.sin(tt+p))%GW; yy=(y-24*(k/FRAMES)*s)%GH
        a=int(75+120*(.5+.5*math.sin(tt*2+p))); r=1 if s<1.25 else 2
        d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(220,205,255,a))
    frames.append(im.convert('RGB'))
save_gif('particles_purple_loop_01.gif',frames,50)

frames=[]
for k in range(FRAMES):
    im=Image.new('RGBA',(GW,GH),(8,3,18,255))
    tt=k/FRAMES*math.tau
    for cx,cy,col,rad,alpha in [(80+55*math.sin(tt),230,(120,0,255),170,140),(30+35*math.cos(tt),260,(255,245,210),125,145),(165+50*math.sin(tt+.8),250,(255,0,205),115,90)]:
        q=Image.new('RGBA',(GW,GH),(0,0,0,0)); qd=ImageDraw.Draw(q)
        qd.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),fill=(*col,alpha)); q=q.filter(ImageFilter.GaussianBlur(rad//3)); im=Image.alpha_composite(im,q)
    frames.append(im.convert('RGB'))
save_gif('light_leak_purple_cream_loop_01.gif',frames,50)

frames=[]
for k in range(FRAMES):
    im=Image.new('RGB',(GW,GH),(4,3,12)); d=ImageDraw.Draw(im); tt=k/FRAMES*math.tau
    for i in range(16):
        a=tt+i*.65; x=GW/2+math.cos(a)*random.Random(i).uniform(60,220); y=GH/2+math.sin(a*1.2)*random.Random(i+20).uniform(30,120)
        s=4+9*(.5+.5*math.sin(tt*2+i)); d.polygon([(x,y-s),(x+s*.35,y),(x,y+s),(x-s*.35,y)],fill=(255,90,235))
    frames.append(im)
save_gif('sparkles_magenta_loop_01.gif',frames,55)

frames=[]
for k in range(FRAMES):
    im=Image.new('RGB',(GW,GH),(5,4,12)); d=ImageDraw.Draw(im)
    rr=random.Random(k*31)
    for _ in range(14):
        y=rr.randrange(GH); h=rr.randrange(2,10); shift=rr.randrange(-70,70); col=rr.choice([(255,0,205),(75,30,255),(230,230,255)])
        d.rectangle((max(0,shift),y,min(GW,GW+shift),y+h),fill=col)
    frames.append(im)
save_gif('glitch_bars_loop_01.gif',frames,45)

# Arquivos externos realmente redistribuíveis (CC0/Public Domain).
# Pixabay/Pexels/Mixkit NÃO são reupados em forma standalone: ver external-sources/stock-media.md.
DOWNLOADS = {
    PUBLIC_AUDIO: {
        'soft_whistle_public_domain.ogg': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Soft_whistle.ogg',
        'applause_auditorium_public_domain.ogg': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Applause_ii.ogg',
        'festival_crowd_public_domain.ogg': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Festival_concert_people_crowd.ogg',
        'applause_concert_cc0.ogg': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Sound_Effects_-_Applause_after_a_concert.ogg',
    },
    PUBLIC_VIDEO: {
        'football_spectators_cc0.webm': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Spectators_during_a_football_match.webm',
        'flight_over_clouds_cc0.webm': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Flight_over_clouds.webm',
        'eureka_stadium_panorama_cc0.webm': 'https://commons.wikimedia.org/wiki/Special:Redirect/file/Eureka_Stadium_21st_August_2026.webm',
    }
}

def download(url, dest):
    if dest.exists() and dest.stat().st_size > 1024:
        return
    for attempt in range(4):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'assets-videos-media-pack/1.0'})
            with urllib.request.urlopen(req,timeout=75) as r, open(dest,'wb') as f:
                while True:
                    chunk=r.read(1024*1024)
                    if not chunk: break
                    f.write(chunk)
            print('baixado:',dest.name, dest.stat().st_size)
            time.sleep(2.5)
            return
        except Exception as e:
            print('tentativa',attempt+1,'falhou:',dest.name,e)
            time.sleep(4*(attempt+1))
    if dest.exists() and dest.stat().st_size < 1024:
        dest.unlink(missing_ok=True)

for folder, items in DOWNLOADS.items():
    for name,url in items.items():
        download(url, folder/name)

print('media pack finalizado')
