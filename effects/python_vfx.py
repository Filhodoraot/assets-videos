"""Pequena biblioteca de VFX em Python/OpenCV.

Objetivo: reproduzir em código parte do tipo de efeito usado em DaVinci Resolve,
After Effects e CapCut: bloom, RGB split, grain, shake, zoom, motion blur,
glitch, vignette, scanlines e color grading.

Uso em imagens/frame a frame. Para vídeo completo, leia os frames com OpenCV e
preserve/remuxe o áudio com FFmpeg no final.
"""

import cv2
import numpy as np
import math


def clamp8(img):
    return np.clip(img, 0, 255).astype(np.uint8)


def bloom(frame, threshold=175, radius=22, intensity=0.9):
    src = frame.astype(np.float32)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = np.clip((gray.astype(np.float32)-threshold)/(255-threshold+1e-6), 0, 1)
    bright = src * mask[..., None]
    blur = cv2.GaussianBlur(bright, (0,0), radius)
    return clamp8(src + blur*intensity)


def rgb_split(frame, amount=8):
    b,g,r = cv2.split(frame)
    h,w = frame.shape[:2]
    M1 = np.float32([[1,0,amount],[0,1,0]])
    M2 = np.float32([[1,0,-amount],[0,1,0]])
    r = cv2.warpAffine(r,M1,(w,h),borderMode=cv2.BORDER_REFLECT)
    b = cv2.warpAffine(b,M2,(w,h),borderMode=cv2.BORDER_REFLECT)
    return cv2.merge([b,g,r])


def vignette(frame, strength=0.55):
    h,w = frame.shape[:2]
    y,x = np.ogrid[-1:1:h*1j, -1:1:w*1j]
    r = np.sqrt(x*x+y*y)
    mask = np.clip(1-strength*np.maximum(0,r-.15), 0, 1)
    return clamp8(frame.astype(np.float32)*mask[...,None])


def film_grain(frame, amount=10, seed=None):
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, amount, frame.shape).astype(np.float32)
    return clamp8(frame.astype(np.float32)+noise)


def scanlines(frame, strength=0.14, spacing=4):
    out = frame.astype(np.float32)
    out[::spacing] *= (1-strength)
    return clamp8(out)


def sharpen(frame, amount=0.8):
    blur = cv2.GaussianBlur(frame,(0,0),2)
    return clamp8(frame.astype(np.float32)*(1+amount)-blur.astype(np.float32)*amount)


def directional_motion_blur(frame, length=19, angle=0):
    length = max(3, int(length)|1)
    kernel = np.zeros((length,length),np.float32)
    kernel[length//2,:] = 1.0
    M = cv2.getRotationMatrix2D((length/2-0.5,length/2-0.5), angle, 1)
    kernel = cv2.warpAffine(kernel,M,(length,length))
    kernel /= kernel.sum() or 1
    return cv2.filter2D(frame,-1,kernel)


def camera_shake(frame, frame_index, strength=9, speed=0.85):
    h,w = frame.shape[:2]
    x = math.sin(frame_index*speed)*strength + math.sin(frame_index*1.91)*strength*.35
    y = math.cos(frame_index*speed*.83)*strength*.65
    angle = math.sin(frame_index*speed*.47)*strength*.08
    M = cv2.getRotationMatrix2D((w/2,h/2), angle, 1.015)
    M[0,2] += x; M[1,2] += y
    return cv2.warpAffine(frame,M,(w,h),borderMode=cv2.BORDER_REFLECT)


def punch_zoom(frame, progress, amount=0.16):
    h,w = frame.shape[:2]
    p = np.clip(progress,0,1)
    ease = 1-(1-p)**3
    scale = 1+amount*math.sin(math.pi*ease)
    nw,nh = int(w*scale),int(h*scale)
    z = cv2.resize(frame,(nw,nh),interpolation=cv2.INTER_CUBIC)
    x=(nw-w)//2; y=(nh-h)//2
    return z[y:y+h,x:x+w]


def zoom_blur(frame, strength=0.18, samples=12):
    h,w = frame.shape[:2]
    acc = np.zeros_like(frame,dtype=np.float32)
    for i in range(samples):
        s = 1 + strength*(i/(samples-1 if samples>1 else 1))
        nw,nh=int(w*s),int(h*s)
        z=cv2.resize(frame,(nw,nh),interpolation=cv2.INTER_LINEAR)
        x=(nw-w)//2; y=(nh-h)//2
        acc += z[y:y+h,x:x+w].astype(np.float32)
    return clamp8(acc/samples)


def glitch_blocks(frame, seed=0, intensity=0.6, blocks=12):
    rng=np.random.default_rng(seed)
    out=frame.copy(); h,w=out.shape[:2]
    for _ in range(blocks):
        y=int(rng.integers(0,h)); bh=int(rng.integers(2,max(3,h//15)))
        shift=int(rng.integers(-int(w*.12),int(w*.12)+1)*intensity)
        y2=min(h,y+bh)
        strip=out[y:y2].copy()
        out[y:y2]=np.roll(strip,shift,axis=1)
    if intensity>.35:
        out=rgb_split(out,int(3+12*intensity))
    return out


def halftone(frame, cell=8, strength=0.65):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    h,w=gray.shape
    canvas=np.zeros_like(frame)
    for y in range(0,h,cell):
        for x in range(0,w,cell):
            patch=gray[y:min(y+cell,h),x:min(x+cell,w)]
            lum=float(patch.mean())/255.0
            radius=max(1,int((1-lum)*cell*.48))
            cv2.circle(canvas,(x+cell//2,y+cell//2),radius,(255,255,255),-1)
    return clamp8(frame.astype(np.float32)*(1-strength)+canvas.astype(np.float32)*strength)


def teal_magenta_grade(frame, strength=0.35):
    x=frame.astype(np.float32)/255.0
    b,g,r=cv2.split(x)
    shadows=(1-(r+g+b)/3)[...,None]
    highlights=((r+g+b)/3)[...,None]
    tint=np.zeros_like(x)
    tint[...,0]=0.22*shadows[...,0]      # teal/blue nas sombras
    tint[...,1]=0.08*shadows[...,0]
    tint[...,2]=0.18*highlights[...,0]   # magenta/vermelho nas altas
    return clamp8((x+tint*strength)*255)


def example_stack(frame, frame_index=0):
    """Exemplo de stack estilo motion design."""
    x=bloom(frame,170,18,.7)
    x=teal_magenta_grade(x,.3)
    x=rgb_split(x,3)
    x=film_grain(x,5,frame_index)
    x=vignette(x,.45)
    return x
