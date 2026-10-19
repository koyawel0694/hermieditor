import os
import json
import numpy as np
import soundfile as sf
import scipy.signal

def load_resample_stereo(path, target_sr, target_len):
    """Loads an audio file, converts to stereo, resamples, and pads/truncates to target_len."""
    data, sr = sf.read(path)
    if len(data.shape) == 1:
        data = np.stack([data, data], axis=-1)
    elif data.shape[1] > 2:
        data = data[:, :2]
        
    if sr != target_sr:
        num_samples = int(len(data) * target_sr / sr)
        left = scipy.signal.resample(data[:, 0], num_samples)
        right = scipy.signal.resample(data[:, 1], num_samples)
        data = np.stack([left, right], axis=-1)
        
    out = np.zeros((target_len, 2), dtype=np.float32)
    copy_len = min(len(data), target_len)
    out[:copy_len] = data[:copy_len]
    return out

def main():
    target_sr = 44100
    total_sec = 600.12
    target_len = int(total_sec * target_sr)
    
    print("1. Loading English Dialogue Vocals...")
    vocals = load_resample_stereo('/home/john/.hermes/cache/scratch/true_dialogue_vocals.wav', target_sr, target_len)
    # Vocal level
    vocals_peak = np.max(np.abs(vocals))
    if vocals_peak > 0:
        vocals = vocals / vocals_peak * 0.95
        
    print("2. Loading Clean Original SFX (Chinese Voices Completely Muted)...")
    clean_sfx = load_resample_stereo('/home/john/.hermes/cache/scratch/clean_sfx_no_chinese.wav', target_sr, target_len)
    clean_sfx *= 0.55 # Balanced background SFX volume
    
    print("3. Building Continuous Seamless Cinematic BGM Bed...")
    bgm_raw, bgm_sr = sf.read('/home/john/.hermes/cache/scratch/probe_audio/Before_the_Silence_Falls.wav')
    if len(bgm_raw.shape) == 1:
        bgm_raw = np.stack([bgm_raw, bgm_raw], axis=-1)
    if bgm_sr != target_sr:
        num_samples = int(len(bgm_raw) * target_sr / bgm_sr)
        left = scipy.signal.resample(bgm_raw[:, 0], num_samples)
        right = scipy.signal.resample(bgm_raw[:, 1], num_samples)
        bgm_raw = np.stack([left, right], axis=-1)
        
    bgm_track = np.zeros((target_len, 2), dtype=np.float32)
    fade_len = int(2.0 * target_sr)
    bgm_len = len(bgm_raw)
    
    curr = 0
    while curr < target_len:
        chunk_len = min(bgm_len, target_len - curr)
        bgm_track[curr:curr+chunk_len] += bgm_raw[:chunk_len]
        curr += (bgm_len - fade_len)
        
    bgm_peak = np.max(np.abs(bgm_track))
    if bgm_peak > 0:
        bgm_track = (bgm_track / bgm_peak) * 0.12 # -18dB to -20dB background bed
        
    print("4. Overlaying Key Anime SFX Hits...")
    sfx_hits = [
        (8.5, '/home/john/Documents/hermieditor/my-sounds/mini-drama/thunder-crack.mp3', 0.8),
        (26.5, '/home/john/Documents/hermieditor/my-sounds/mini-drama/cinematic-sub-boom.mp3', 0.9),
        (60.0, '/home/john/Documents/hermieditor/my-sounds/explainer/whoosh-transition-cinematic.mp3', 0.6),
        (144.0, '/home/john/Documents/hermieditor/my-sounds/explainer/whoosh-transition-cinematic.mp3', 0.6),
        (224.0, '/home/john/Documents/hermieditor/my-sounds/explainer/whoosh-transition-cinematic.mp3', 0.7),
        (264.5, '/home/john/Documents/hermieditor/my-sounds/explainer/ding-correct-gameshow.mp3', 0.5),
        (296.0, '/home/john/Documents/hermieditor/my-sounds/explainer/ding-correct-gameshow.mp3', 0.6),
        (328.0, '/home/john/Documents/hermieditor/my-sounds/mini-drama/cinematic-boom-trailer.mp3', 0.95),
        (460.5, '/home/john/Documents/hermieditor/my-sounds/mini-drama/face-slap.mp3', 0.8),
        (587.2, '/home/john/Documents/hermieditor/my-sounds/explainer/cash-register-cha-ching.mp3', 0.7),
    ]
    
    extra_sfx = np.zeros((target_len, 2), dtype=np.float32)
    for timestamp, path, vol in sfx_hits:
        sdata, ssr = sf.read(path)
        if len(sdata.shape) == 1:
            sdata = np.stack([sdata, sdata], axis=-1)
        if ssr != target_sr:
            num = int(len(sdata) * target_sr / ssr)
            l = scipy.signal.resample(sdata[:, 0], num)
            r = scipy.signal.resample(sdata[:, 1], num)
            sdata = np.stack([l, r], axis=-1)
            
        start_idx = int(timestamp * target_sr)
        end_idx = min(start_idx + len(sdata), target_len)
        slen = end_idx - start_idx
        extra_sfx[start_idx:end_idx] += sdata[:slen] * vol

    print("5. Mastering & Summing Mix...")
    # Sum all elements
    final_mix = vocals + clean_sfx + bgm_track + extra_sfx
    
    # Soft Limiting to prevent any clipping
    max_val = np.max(np.abs(final_mix))
    if max_val > 0.95:
        final_mix = final_mix / max_val * 0.95
        
    out_master = '/home/john/.hermes/cache/scratch/clean_mastered_dub_v2.wav'
    sf.write(out_master, final_mix, target_sr)
    print(f"Master audio successfully saved to {out_master}!")

if __name__ == '__main__':
    main()
