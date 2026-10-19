import os
import json
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
import subprocess

SCRIPT_BLOCKS = [
    (0.0, 30.0, "Lu Ran, step onto the awakening altar and reveal your class! Suddenly, the sky tears open. An ominous purple vortex erupts with deafening thunder! The examiners freeze in disbelief. 'Is that... the mythical Underworld Sovereign?!' But moments later, the heavenly manifestation shatters."),
    (30.0, 67.0, "The headmaster sighs. 'The Underworld Sovereign only exists in ancient legends—the heavens could never allow it. He only awakened as... an ordinary Necromancer.' The crowd erupts in mocking laughter. 'What a joke! He was our academy's number one genius with an absurd 130 mental stat! And all he got was the most useless trash class in history?!' 'Silence! Next student: Qin Wuyao!'"),
    (67.0, 97.0, "The altar explodes into brilliant golden light! 'SSS-Rank Hidden Class: Void Walker!' Cheers roar across the stadium. The difference between heaven and earth in a single second. Next month, the Heavenly Alliance will recruit her directly... while the former prodigy won't even qualify to clean toilets. Lu Ran clenches his fist. 'A common class is still a combat class. As long as I grind, there's always a way.'"),
    (97.0, 129.0, "Lu Ran turns to his friend: 'Xiao Jiang, let's team up. You awakened Magic Archer—with our synergy we can clear dungeons fast!' Before she can reply, a haughty voice cuts in. 'Xiao Jiang, why waste your breath on a loser? My father already hired elite veterans to boost us. Leave him in the dirt.'"),
    (129.0, 160.0, "Xiao Jiang turns cold: 'Sorry Lu Ran, I can't gamble my future on you. Let's go, Young Master Liang.' Liang sneers: 'Have fun playing with your fragile little skeletons, Lu Ran! Just make sure you don't get lonely with them!' Lu Ran shakes his head. He thought he knew her, but in the end, it was just a bad joke. He turns toward the monster zones alone."),
    (160.0, 216.0, "A normal Necromancer's biggest fatal flaw is long skill cooldowns and paper-thin defense. But when Lu Ran checks his status window, his jaw drops. He unlocked a Divine Passive: Zero Skill Cooldown! 'Wait... Does this mean I can summon an infinite undead legion without waiting?! When I reach higher levels, I can flood the world with Death Knights, Bone Dragons, and Calamity Titans!' He steps into the wild forest."),
    (216.0, 256.0, "Any novice entering this territory gets immediately swarmed by wild boars. That's why no other beginners dare come here. Lu Ran raises his hand: 'Arise, Skeleton Warriors!' For an ordinary summoner, it takes four skeletons just to scratch one armored boar. But here, eight giant boars charge right at him!"),
    (256.0, 294.0, "'Five skeletons per boar—maximize efficiency! Strike!' In seconds, the wild beasts collapse into blood and bone. Ding! You have leveled up to Level 1! With each level up, his mana instantly refills to full! 'This system is tailor-made for me!' More beasts charge. Lu Ran's army steamrolls forward with ruthless precision."),
    (294.0, 326.0, "Ding! You have reached Level 5! Unlocked New Skill: Corpse Explosion! Any skeleton or corpse under his command can detonate, dealing 300% AoE magic damage within two meters! Lu Ran grins: 'Holy crap. With this skill, these aren't just skeleton grunts anymore... They're walking tactical nukes!'"),
    (326.0, 358.0, "He commands a skeleton to rush into a monster swarm and detonate! BOOM! The shockwave obliterates everything! And that's not all—his system unlocks another god-tier perk: Divine Damage Transfer! All damage directed at Lu Ran is 100% absorbed by his summoned undead!"),
    (358.0, 394.0, "A summoner's greatest weakness has always been fragile HP, easily one-shot by assassin ambushes. But with Damage Transfer, as long as a single skeleton breathes, Lu Ran is completely unkillable! He sweeps through the dungeon boss chamber, reaping EXP and mountains of loot."),
    (394.0, 425.0, "His inventory is overflowing with gold and rare drops. At this speed, when the Heavenly Alliance arrives next month, he will shock the entire nation. Realizing he hasn't eaten all day, he heads back to town. Just outside the gates, the crowd freezes: 'Wait, isn't that Lu Ran? He's already Level 5?!'"),
    (425.0, 464.0, "Young Master Liang struts over with Xiao Jiang, sneering: 'Well, well, look who crawled out. What happened to our top genius? Look at my full set of rare blue gear! Even Xiao Jiang's robe cost me a fortune. You probably can't afford a single potion, can you? In two hours, we already cleared the outskirts!'"),
    (464.0, 496.0, "Before Liang can finish his insult, a sudden kick sends him flying face-first into the dirt! 'Who the hell kicked me?!' He looks up, terrified: 'Q-Qin Wuyao?!' The academy's top goddess glares down at him: 'Lu Ran may be a Necromancer, but you are just an ordinary Berserker. What gives you the right to act arrogant?' Liang scrambles up in shame: 'Lu Ran, you better pray we don't catch you alone outside!'"),
    (496.0, 527.0, "Qin Wuyao turns to Lu Ran with a soft smile: 'You helped me back at the academy—consider us even. We're heading to the high-level wilderness to grind. Do you want to join our party?' Lu Ran politely declines. High-level parties cause massive EXP penalties. With his infinite army and zero cooldowns, solo leveling is ten times faster."),
    (527.0, 563.0, "He enters the Level 10 Dark Catacombs alone. 'Time to put everything I studied into practice. Skeletons, attack!' His skeleton legion moves like a disciplined death squad, slaughtering elite ghouls while Lu Ran casually collects gold and equipment. Twenty elite monsters fall in seconds. 'I'm done hiding my power!'"),
    (563.0, 595.0, "He advances deeper. With his expanded mana pool, he summons twenty more armored skeletal warriors! The boss appears—a massive corrupted beast. 'All units, full assault!' The skeletons surround the boss, detonating Corpse Explosions back to back! The boss roars and collapses in a flash of purple light. 'Wait... A purple drop?! The Twin Dragon Staff with a drop rate under 0.1%?!'"),
    (595.0, 600.0, "Holding the glowing legendary staff, Lu Ran smiles coldly. 'This is only the beginning.'")
]

def main():
    print("Loading Kokoro TTS model...")
    kokoro = Kokoro('/home/john/.cache/kokoro/kokoro-v1.0.onnx', '/home/john/.cache/kokoro/voices-v1.0.bin')
    sr = 24000
    total_samples = int(600.12 * sr)
    master_audio = np.zeros(total_samples, dtype=np.float32)
    
    print("Synthesizing narration for 18 blocks...")
    for idx, (start_sec, end_sec, text) in enumerate(SCRIPT_BLOCKS):
        print(f"[{idx+1}/18] Generating {start_sec}s - {end_sec}s...")
        samples, _ = kokoro.create(text, voice='am_adam', speed=1.08, lang='en-us')
        
        # calculate placement
        start_idx = int(start_sec * sr)
        # if samples exceed slot, clamp or speed up
        max_len = int((end_sec - start_sec) * sr)
        if len(samples) > max_len:
            samples = samples[:max_len]
        
        end_idx = min(start_idx + len(samples), total_samples)
        actual_len = end_idx - start_idx
        master_audio[start_idx:end_idx] = samples[:actual_len]
    
    # Normalize vocal to -1.0 dB peak
    peak = np.max(np.abs(master_audio))
    if peak > 0:
        master_audio = master_audio / peak * 0.90
        
    vocal_path = "/home/john/.hermes/cache/scratch/dubbed_vocals_10m.wav"
    sf.write(vocal_path, master_audio, sr)
    print(f"Vocals saved to {vocal_path}")

if __name__ == '__main__':
    main()
