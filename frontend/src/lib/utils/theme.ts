export type Theme = 'dark' | 'light';

export function getInitialTheme(): Theme {
  const saved = localStorage.getItem('vaultlingo_theme') as Theme | null;
  if (saved === 'light' || saved === 'dark') {
    return saved;
  }
  return 'dark'; // Default dark theme
}

export function applyTheme(theme: Theme): void {
  localStorage.setItem('vaultlingo_theme', theme);
  const root = document.documentElement;
  if (theme === 'light') {
    root.classList.remove('dark');
    root.classList.add('light');
    document.body.classList.remove('dark');
    document.body.classList.add('light');
  } else {
    root.classList.remove('light');
    root.classList.add('dark');
    document.body.classList.remove('light');
    document.body.classList.add('dark');
  }
}
