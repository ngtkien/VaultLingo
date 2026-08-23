let currentAudio: HTMLAudioElement | null = null;
let currentPlayingId = '';

export function playTTS(text: string, speed = 1.0, id = ''): Promise<void> {
  return new Promise((resolve) => {
    stopAudio();
    if (!text) {
      resolve();
      return;
    }

    currentPlayingId = id;
    const url = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=${encodeURIComponent(text)}`;
    const audio = new Audio(url);
    audio.playbackRate = speed;
    currentAudio = audio;

    audio.onended = () => {
      currentPlayingId = '';
      currentAudio = null;
      resolve();
    };

    audio.onerror = () => {
      currentPlayingId = '';
      currentAudio = null;
      resolve();
    };

    audio.play().catch(() => {
      currentPlayingId = '';
      currentAudio = null;
      resolve();
    });
  });
}

export function playAudioUrl(url: string, speed = 1.0, id = ''): Promise<void> {
  return new Promise((resolve) => {
    stopAudio();
    if (!url) {
      resolve();
      return;
    }

    currentPlayingId = id;
    const audio = new Audio(url);
    audio.playbackRate = speed;
    currentAudio = audio;

    audio.onended = () => {
      currentPlayingId = '';
      currentAudio = null;
      resolve();
    };

    audio.onerror = () => {
      currentPlayingId = '';
      currentAudio = null;
      resolve();
    };

    audio.play().catch(() => {
      currentPlayingId = '';
      currentAudio = null;
      resolve();
    });
  });
}

export function stopAudio(): void {
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.currentTime = 0;
    currentAudio = null;
    currentPlayingId = '';
  }
}

export function isPlaying(id: string): boolean {
  return currentPlayingId === id && currentAudio !== null && !currentAudio.paused;
}
