#!/usr/bin/env node
// HermiEditor One-Time Setup:
// 1. Checks system tools (Node.js 18+, Git, FFmpeg, FFprobe, Python 3)
// 2. Installs Herk Edit Kit engine into kit/ via sparse checkout
// 3. Verifies transcription (Groq API or local faster-whisper)
// 4. Installs/links the hermieditor skill into ~/.hermes/skills/media/hermieditor/
//
//   node setup.mjs

import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, symlinkSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const kit = join(root, 'kit');
const KIT_REPO = 'https://github.com/nateherkai/herk-edit-kit.git';
const KIT_COMMIT = '10511e5af86fc47756ea89803b397422e2d89284';
const SPARSE = ['/*', '!/examples/showcase/', '!/video-projects/**/*.mp4', '!/video-projects/**/*.mov',
  '!/video-projects/**/*.webm', '!/video-projects/**/*.mp3', '!/video-projects/**/*.wav'];

const win = process.platform === 'win32';
const step = (msg) => console.log(`\n== ${msg}`);
const run = (cmd, args, cwd = root, quiet = false) => {
  const opts = { cwd, stdio: quiet ? 'pipe' : 'inherit', encoding: 'utf8' };
  const r = win && (cmd === 'npm' || cmd === 'npx')
    ? spawnSync([cmd, ...args].join(' '), { ...opts, shell: true })
    : spawnSync(cmd, args, opts);
  return !r.error && r.status === 0;
};
const fail = (msg) => { console.error(`\nSETUP STOPPED: ${msg}`); process.exit(1); };

step('Checking system tools');
const missing = [];
for (const [tool, flag, label] of [
  ['git', '--version', 'Git'],
  ['ffmpeg', '-version', 'FFmpeg'],
  ['ffprobe', '-version', 'FFprobe'],
  ['python3', '--version', 'Python 3']
]) {
  if (!run(tool, [flag], root, true)) missing.push(label);
}
if (missing.length) {
  const hint = win
    ? 'winget install OpenJS.NodeJS.LTS Git.Git Gyan.FFmpeg Python.Python.3.11'
    : process.platform === 'darwin' ? 'brew install node git ffmpeg python' : 'Use your package manager (apt/dnf/pacman): node, git, ffmpeg, python3';
  fail(`Missing dependencies: ${[...new Set(missing)].join(', ')}.\nInstall with: ${hint}`);
}
console.log(`Node ${process.versions.node}, Git, FFmpeg, FFprobe, Python: OK`);

step('Scaffolding directories');
for (const dir of ['inbox', 'outbox', 'my-sounds', 'tools', 'templates']) {
  mkdirSync(join(root, dir), { recursive: true });
}

step('Installing the editing engine (Herk Edit Kit) into kit/');
if (!existsSync(join(kit, '.git'))) {
  if (!run('git', ['clone', '--quiet', '--no-checkout', '--depth', '1', '--filter=blob:limit=1m', KIT_REPO, kit])) {
    fail('Could not download Herk Edit Kit. Check internet connection and retry.');
  }
  run('git', ['-C', kit, 'fetch', '--quiet', '--depth', '1', '--filter=blob:limit=1m', 'origin', KIT_COMMIT]);
  run('git', ['-C', kit, 'sparse-checkout', 'set', '--no-cone', ...SPARSE]);
  if (!run('git', ['-C', kit, '-c', 'advice.detachedHead=false', 'checkout', '--quiet', KIT_COMMIT])) {
    fail(`Could not check out kit commit ${KIT_COMMIT}.`);
  }
} else {
  console.log('kit/ already installed.');
}

step('Installing kit packages (npm ci)');
if (!existsSync(join(kit, 'node_modules', 'hyperframes')) && !run('npm', ['ci', '--no-audit', '--no-fund'], kit)) {
  fail('npm ci failed in kit/.');
}
run('npm', ['run', 'setup', '--silent'], kit);

step('Checking Python dependencies (faster-whisper, numpy, scipy)');
const hasScipy = run('python3', ['-c', 'import numpy, scipy; print("OK")'], root, true);
const hasWhisper = run('python3', ['-c', 'import faster_whisper; print("OK")'], root, true);
console.log(`NumPy & SciPy: ${hasScipy ? 'Installed' : 'Missing (pip install numpy scipy)'}`);
console.log(`Local faster-whisper: ${hasWhisper ? 'Installed' : 'Optional (pip install faster-whisper or use Groq API)'}`);

step('Checking Hermes Skill registration');
const hermesSkillsDir = join(homedir(), '.hermes', 'skills', 'media', 'hermieditor');
const localSkillDir = join(root, 'skills', 'hermieditor');
if (existsSync(localSkillDir)) {
  try {
    mkdirSync(join(homedir(), '.hermes', 'skills', 'media'), { recursive: true });
    if (!existsSync(hermesSkillsDir)) {
      symlinkSync(localSkillDir, hermesSkillsDir, 'junction');
      console.log(`Linked skill into Hermes: ${hermesSkillsDir} -> ${localSkillDir}`);
    } else {
      console.log(`Skill already active in: ${hermesSkillsDir}`);
    }
  } catch (e) {
    console.log(`Note: could not auto-symlink skill (${e.message}). You can manually copy skills/hermieditor to ~/.hermes/skills/media/hermieditor/`);
  }
}

step('Checking .env configuration');
if (!existsSync(join(root, '.env')) && existsSync(join(root, '.env.example'))) {
  copyFileSync(join(root, '.env.example'), join(root, '.env'));
}
try { process.loadEnvFile(join(root, '.env')); } catch {}
const groq = Boolean(process.env.GROQ_API_KEY);
console.log(`Groq Whisper API key in .env: ${groq ? 'Configured' : 'Not set (optional, free from console.groq.com)'}`);

console.log('\n======================================================');
console.log(' HermiEditor setup is complete!');
console.log('======================================================');
console.log('How to use:');
console.log(`1. Drop raw video clips and voiceover audio in: ${resolve(root, 'inbox')}/<slug>`);
console.log('2. In your Hermes CLI/Agent session, simply say:');
console.log('   "edit this affiliate video in inbox/<slug>" or "edit this drama series"');
console.log('======================================================\n');
