import { PlayTTS as wailsPlayTTS, PlayAudioUrl as wailsPlayAudioUrl, StopAudio as wailsStopAudio } from '../../../wailsjs/go/main/App.js';

let currentPlayingId = '';

export async function playTTS(text: string, speed = 1.0, id = ''): Promise<void> {
  if (!text) return;
  currentPlayingId = id;
  try {
    await wailsPlayTTS(text, speed);
  } catch (e) {
    console.error('TTS error:', e);
  }
}

export async function playAudioUrl(url: string, speed = 1.0, id = ''): Promise<void> {
  if (!url) return;
  currentPlayingId = id;
  try {
    await wailsPlayAudioUrl(url, speed);
  } catch (e) {
    console.error('Audio stream error:', e);
  }
}

export async function stopAudio(): Promise<void> {
  currentPlayingId = '';
  try {
    await wailsStopAudio();
  } catch (e) {
    console.error('Stop audio error:', e);
  }
}

export function isPlaying(id: string): boolean {
  return currentPlayingId === id;
}
