export type Theme = 'dark' | 'light';

export function getInitialTheme(): Theme {
  const saved = localStorage.getItem('vaultlingo_theme');
  if (saved === 'light' || saved === 'dark') {
    return saved;
  }
  return 'dark'; // Default dark mode
}

export function applyTheme(theme: Theme): void {
  localStorage.setItem('vaultlingo_theme', theme);
  const root = document.documentElement;
  if (theme === 'light') {
    root.classList.remove('dark');
    root.classList.add('light');
    document.body.style.backgroundColor = '#f8fafc';
    document.body.style.color = '#0f172a';
  } else {
    root.classList.remove('light');
    root.classList.add('dark');
    document.body.style.backgroundColor = '#0b0f17';
    document.body.style.color = '#f1f5f9';
  }
}
