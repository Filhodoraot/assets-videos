# Efeitos em Python

`python_vfx.py` prova que dá para reproduzir bastante coisa de editores como DaVinci Resolve/After Effects usando código.

## Já incluído

- bloom / glow
- RGB split / chromatic aberration
- vignette
- film grain
- scanlines
- sharpen
- directional motion blur
- camera shake
- punch zoom
- zoom blur
- glitch blocks
- halftone
- color grading teal/magenta

## Dependências

```bash
pip install opencv-python numpy
```

## Onde Python funciona muito bem

Python + OpenCV + FFmpeg é ótimo para efeitos 2D, motion graphics procedurais, transições, partículas, composição, automação em massa e tratamento de vídeo.

## Onde DaVinci/Fusion ainda é melhor

Para tracking complexo, rotoscopia manual, máscaras desenhadas quadro a quadro, 3D pesado, composição com dezenas de nodes e feedback em tempo real, Fusion/After Effects é mais confortável e normalmente usa melhor a GPU.

A ideia deste repositório é misturar os dois mundos: assets bons + efeitos programáveis + editor quando necessário.
