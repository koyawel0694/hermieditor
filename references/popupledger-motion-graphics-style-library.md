# PopUpLedger Motion-Graphics Style Library v3.0

Use this library when the user asks for motion graphics, gives reference videos, or chooses “Let me choose.” These are selectable visual languages and techniques, not mandatory items. Select by content, desired emotion, audience, source assets and available renderer.

## 1. Style families (overall visual language)

### MG-01 — Minimalist Editorial Motion
Clean backgrounds, precise alignment, restrained labels, thin rules, elegant callout lines, small graphic inserts, generous negative space and short deliberate animation. Best for: premium explainers, business/tech, educational reels, clean creator content. Risk: too sterile if every beat is a plain label.

### MG-02 — Kinetic Typography
Words/phrases act as visual subjects: masking, tracking, scale, stagger, word contrast, typography as shape and rhythm. Best for: hooks, key takeaways, emotional emphasis and short-form pacing. Risk: text replaces the explanation rather than supporting it.

### MG-03 — Diagram / Explainer Infographics
Flowcharts, cause-effect systems, sequence maps, parts-and-whole diagrams, feedback loops, hierarchy trees, node relationships, exploded views and process stages. Best for: explaining mechanisms, systems, strategies and abstract ideas. Use progressive builds rather than revealing the entire diagram at once.

### MG-04 — Data / Chart Motion
Bars, lines, slopes, distributions, counters, comparison ranks, labeled metrics and chart annotations. Best for: evidence, trends and quantitative explanations. Never invent values or distort scales; source and label context, units and dates.

### MG-05 — Product / UI / SaaS Motion
Real screenshots, browser/app windows, cursor paths, screen crops, masks, tracked highlights, animated UI states, feature callouts and guided walkthroughs. Best for: software demos, tutorials, product explainers and online services. Use genuine screenshots/captures where factual UI matters; don't hallucinate product screens.

### MG-06 — Minimal Graphic Pop-ups / Callout Inserts
A product, person, object, map pin, icon, quote, label, mini-illustration or key fact appears adjacent to the relevant footage or subject. Can use a label tab, connected callout, small panel, icon+text pair, or contextual diagram. Best for: vlogs, narration-led videos, product videos and occasional explainer support. Pop-ups must relate to the spoken idea; do not turn the frame into floating clutter.

### MG-07 — Mixed-Media Collage / Cut-out
Photographs, paper textures, scanned objects, isolated cut-outs, editorial clippings, hand-drawn marks, layered cards and graphic fragments move together in a controlled composition. Best for: culture, history, commentary, storytelling, expressive social video. Risk: visual chaos, cheap scrapbook look or unreadable layering.

### MG-08 — 2.5D Parallax / Depth Layers
Foreground, subject, midground and background move at different rates; camera pushes, pans, layered stills, depth reveals and restrained environmental motion. Best for: archival stills, posters, photographs, editorial scenes and atmospheric long-form. Keep warping mild; don't imply a fake camera movement was actual footage.

### MG-09 — 3D / Isometric / Object Motion
Rotating/exploded objects, isometric process models, simple 3D camera moves, object assembly and spatial diagrams. Best for: mechanisms, devices, architecture, products and complex systems. Only use when the toolchain can actually build/render it. Otherwise create a clean 2D/isometric illustration and disclose the fallback if relevant.

### MG-10 — Motion-Tracked Annotation / Compositing
Labels, shapes, tracking dots, outlines, arrows, spotlights, callout lines, object-following graphics, masking, rotoscoping and screen replacements. Best for: pointing at something in live footage, making a UI easier to follow, highlighting product parts, demonstrating cause and effect. Check tracker stability and occlusion frame-by-frame at critical points.

### MG-11 — Map / Timeline / Journey Graphics
Routes, location pins, milestone sequences, time markers, historical timelines, step progressions and location context. Best for: travel, biography, business histories and how-to content. Map position, borders, dates and route details must be grounded.

### MG-12 — Split Screen / Compare / Before-After
Two- or multi-panel comparisons, synchronized timelines, old/new states, pros/cons, contrast sliders and side-by-side process states. Best for: explaining differences, product demos, transformation and debunking. Keep corresponding scales and labels consistent; before/after claims must be genuine.

### MG-13 — Illustration / Icon Morph / Visual Metaphor
Purpose-made vector illustrations, expressive icons, objects that transform between concepts, metaphorical systems and simplified visual characters. Best for: abstract ideas that are hard to film. Avoid meaningless icon confetti; the metaphor should clarify the line.

### MG-14 — Shape Language / Graphic Transitions
Masks, wipes, shape morphs, typography-to-object transitions, graphic match-cuts, color blocks, line reveals, geometric transitions and frame-edge movement. Best for: connecting related visual ideas, opening chapters, or moving between live footage and designed scenes. Transition is not a substitute for story logic.

### MG-15 — Documentary / Evidence / Archive Graphics
Source cards, document excerpts, dates, archival labels, quote highlights, file tags, evidence boards, footnote/source inserts and editorial annotations. Best for: investigative explainers, history, finance, research and documentary. Show actual sources, don't invent document UI, and keep legibility/attribution.

### MG-16 — Whiteboard / Line-art / Draw-on
Lines draw, objects are sketched into view, labels write on, routes trace and components are progressively outlined. Best for: teaching, maps, processes and simple abstract explanations. Avoid faux handwriting for everything; keep line style consistent.

### MG-17 — Expressive Pop / Creator Energy
Elastic shapes, bold color blocks, playful stickers, comic emphasis, fast callouts, freeze frames and beat-synced graphic accents. Best for: short-form, humorous creator videos and high-energy hooks. Use sparingly in serious topics or long-form chapters.

### MG-18 — Cinematic Graphic / Atmospheric Motion
Slow graphic reveals, subtle grain, controlled glow, light sweeps, silhouettes, depth, parallax, sound-led transitions and restrained title animation. Best for: serious documentaries, dramatic reveals, mini-drama title/transition moments. Atmosphere should not compromise exact data/text.

### MG-19 — Futuristic Data / HUD Overlay
Instrument-like markers, tracking brackets, grids, scan sweeps, technical labels and interface overlays. Best for: actual technical contexts, sci-fi, interfaces or a consciously chosen futurist art direction. Avoid generic HUD decoration on unrelated subjects.

### MG-20 — Freeze-frame / Rotoscope / Subject Separation
Freeze an action/reaction, isolate a subject, move background independently, trace an outline, add editorial labels or create a controlled dimensional pop-out. Best for: short hooks, comedy, product demonstrations and emphasis. Respect hair/edge quality, subject contours and visual artifacts.

## 2. Technique library (mix into any family when supported)

- Animated masks and reveal mattes.
- Stroke/path drawing and line animation.
- Shape morphing and graphic match transitions.
- Object/subject tracking and stabilized callout lines.
- 2D layer animation and subtle parallax.
- Responsive layout changes and panel transitions.
- Camera push/pull and controlled virtual camera movement.
- Staggered entrances with shared rhythm; transform/position/opacity/scale combinations.
- Light sweeps, blur, distortion, grain, glow, particles and lens effects—only where visually motivated.
- Image cut-outs, background removal, roto, compositing and screen replacement.
- Beat-synchronized edit points and sound-led transitions.
- Animated charts, numbers, diagrams, timelines, maps and process steps.
- Frame-within-frame, picture-in-picture, split screen and tracked labels.
- Loops and seamless graphic handoffs where the sequence benefits.

## 3. How to combine styles

1. Choose **one primary family** that defines the overall graphic language.
2. Choose up to **two support families** for specific needs (e.g., Minimalist Editorial + Diagram/Infographics + Tracked Annotation).
3. Add a technique only when it helps explain, emphasize, orient, transition, create emotion, or maintain momentum.
4. Define shared colors, type, shape language, line weights, corner radius, shadows, animation curves and sound palette.
5. Vary individual scene compositions so the video doesn't feel templated; keep system consistency through design rules rather than repeating the exact same pop-up every scene.
6. For a one-minute minimalist-style short, start with a few standout graphic moments (often around 3–5) and let footage breathe between them; do not treat that as a quota.
7. For long-form, build more meaningful hero graphics across chapters, and use simpler support visuals between them. Let the required reading time drive the hold.

## 4. Reference video analysis protocol

For each reference that can be inspected, note:
- Primary style family and supporting techniques.
- Canvas/aspect ratio and visual density.
- Typography: font character, size, hierarchy, line breaks, placement and animation.
- Composition: subject position, negative space, grid, layering and focus.
- Graphic elements: callouts, shape language, diagrams, UI, texture, objects, labels or illustrations.
- Motion: direction, duration, easing, stagger, weight, hold time and exit.
- Transitions: cut, match, mask, push, wipe, whip, glitch, speed ramp or other observable behavior.
- Color, contrast, material/texture and lighting.
- Sound cues: impacts, clicks, whooshes, Foley, ambience, music accents and silence.
- Pacing: how often a graphic moment appears and how long it stays readable.
- Which techniques are actually relevant to the user's script and which are only stylistic decoration.

If direct playback is blocked, list what is confirmed from metadata and mark shot-level observations as unverified. Ask for a screenshot, screen recording or accessible local reference only if the exact style is a blocker. Use references as inspiration; do not copy complete scenes, unique assets, logos, or exact timing frame-for-frame.

## 5. Fast style picker

- **Clean / premium / minimal:** MG-01 + MG-06, optional MG-14.
- **Explaining a mechanism:** MG-03 + MG-16, optional MG-13.
- **Numbers / finance / business:** MG-01 + MG-04 + MG-15, optional MG-12.
- **Apps / AI / software:** MG-05 + MG-01 + MG-10.
- **History / documentary:** MG-15 + MG-08 + MG-11, optional MG-18.
- **Creative / playful short-form:** MG-02 + MG-07 or MG-17, optional MG-20.
- **Product highlight:** MG-06 + MG-10 + MG-12, optional MG-09 if the actual build is possible.
- **Travel vlog:** MG-06 + MG-11 + natural footage, optional MG-08.
- **Cinematic/emotional story:** MG-18 with story-relevant MG-14, limited text/overlays.
- **Tech/sci-fi by explicit request:** MG-19 with MG-05 or MG-09; avoid HUD clutter.
