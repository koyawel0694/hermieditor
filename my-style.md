# Video Editing Style: Educational & Explainer (Shorts & Reels)

- Format: Vertical 9:16 (1080x1920) optimized for YouTube Shorts and Instagram/Facebook Reels.
- Safe Zones: Keep all text and graphics within the upper 60% and middle zones; avoid the bottom 25% (reserved for platform UI, captions, usernames, and audio labels) and top 10% (header UI).
- Captions:
  - Dynamic word-by-word active tracking.
  - Large, readable sans-serif font (bold white with dark drop shadow/stroke).
  - High-contrast highlight color (vibrant yellow/gold #FFD700 or electric cyan) on key data points, numbers, and technical terms.
  - Position: Upper-middle third, directly below speaker's eye-line, never overlapping faces.
- Hook:
  - Big, bold question or curiosity hook in the first 3 seconds.
  - Strong kinetic text or punch-in framing to capture immediate retention before swipe.
- Pacing:
  - Tight and punchy: eliminate dead air, breath gaps, and pauses longer than 0.35s.
  - Remove all retakes, stutters, and throat clears immediately.
  - Fast-moving information density suited for science, finance, and educational explainers.
- Visual Graphics & B-Roll:
  - Explainer & Documentary animations: Strictly keep visual canvas clean. No pop-up windows or cards that block papercraft, dioramas, or 3D animations.
  - Affiliate & Vlogs: Use explainer-style pop-up windows, metric callouts, and clean data visualizations. Avoid static flat PNG cards with linear opacity fades. Use native HyperFrames + GSAP spring animations (`back.out(1.75)`) with macOS dark glassmorphic window chrome (traffic light controls, code/tab header, line-by-line staggered reveals). Reference template: `kit/style-templates/explainer-popup-window/`.
  - Subtle punch-in zoom cuts (5-8% scale) on topic shifts or punchy claims to reset visual attention every 3-5 seconds.
  - When a pop-up window appears on affiliate videos, the camera stage subtly scales down (scale: 0.95) and dims slightly so viewer focus immediately snaps to the card.
- Color:
  - Crisp, natural grading with punchy contrast and healthy skin tones; avoid heavy stylized color casts that obscure diagram clarity.
- Sound Design:
  - Voice audio front and center: compressed, leveled, clean, and normalized to -14 LUFS.
  - Curated sound library in `my-sounds/` (`mini-drama/`, `explainer/`, `us-niche/`). Catalog in `my-sounds/README.md`.
  - Tactical SFX synchronization:
    * Pop-up window entry: `my-sounds/explainer/pop-clean.mp3` (`volume=0.25`)
    * Detail/row reveals: `my-sounds/explainer/mouse-click-clean.mp3` (`volume=0.20`)
    * Major metric/stat reveals: `my-sounds/explainer/cinematic-thud-metric.mp3` (`volume=0.30`)
    * Window exit: `my-sounds/explainer/whoosh-transition-fast.mp3` (`volume=0.25`)
    * US Viral Hooks / Punchlines: `my-sounds/us-niche/vine-boom.mp3`, `bruh.mp3`, `taco-bell-bong.mp3` (`volume=0.25 to 0.35`)
  - Optional quiet background bed: ambient lo-fi or low-tempo pulse ducked deeply (-24 dB) beneath speech.
