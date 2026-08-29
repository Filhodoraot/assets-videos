# Catálogo de assets

A pasta é pensada para edição de vídeo e motion design. Os arquivos gerados pelo projeto são livres para usar nos nossos projetos.

## Atalho para assets externos

Antes de começar um vídeo, consulte também **`asset-roadmap.md`**. Ele tem tabelas com nomes, categorias, uso e links rápidos para Pixabay, Mixkit, Pexels, Freesound, Wikimedia Commons e NASA.

Esse arquivo funciona como nosso caminho rápido para achar áudio, GIF, footage, imagens, texturas e música sem começar a pesquisa do zero toda vez.

## Imagens / backgrounds

`images/backgrounds/`

- neon_purple_dark_01.jpg
- magenta_blue_gradient_01.jpg
- cyan_dark_glow_01.jpg
- cream_purple_corner_01.jpg
- gray_spotlight_01.jpg
- red_black_glow_01.jpg
- green_cyber_01.jpg
- violet_pink_vertical_01.jpg
- orange_teal_cinematic_01.jpg
- blue_horizon_01.jpg
- sunset_synthetic_01.jpg
- fog_monochrome_01.jpg

## Imagens públicas / CC0

`images/public-domain/`

- clouds_sky_pd.jpg
- beijing_skyline_night_pd.jpg
- long_beach_skyline_night_pd.jpg
- football_stadium_berlin_cc0.jpg
- stadium_crowd_pd.jpg
- nya_ullevi_stadium_pd.jpg
- earth_city_lights_nasa.jpg

Veja fonte e licença em `external-sources/public-domain-images.md`.

## Overlays transparentes

`graphics/overlays/`

- grid_neon_purple_01.png
- scanlines_soft_01.png
- vignette_soft_01.png
- light_leak_purple_cream_01.png
- particles_soft_01.png
- sparkles_magenta_01.png
- halftone_center_01.png
- speed_lines_radial_01.png

## Áudio / SFX

`audio/sfx/`

- whoosh_short_01.wav
- whoosh_long_01.wav
- impact_bass_01.wav
- ui_pop_01.wav
- ui_click_01.wav
- riser_01.wav
- sparkle_01.wav
- glitch_hit_01.wav
- transition_boom_01.wav
- reverse_suck_01.wav

Todos esses SFX são sintetizados pelo script do repositório, sem sample externo.

## Gerar tudo novamente

```bash
pip install pillow numpy
python scripts/generate_assets.py
```

A Action `build-assets.yml` também gera e salva os arquivos automaticamente no repositório.
