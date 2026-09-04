export type ColorMode = 'dark' | 'light';
export type ThemePalette = 'editorial' | 'default' | 'nord' | 'everforest' | 'catppuccin' | 'tokyonight' | 'gruvbox' | 'dracula';

export interface ThemeState {
  palette: ThemePalette;
  colorMode: ColorMode;
}

export interface PaletteInfo {
  id: ThemePalette;
  name: string;
  colors: {
    bg: string;
    card: string;
    accent: string;
    text: string;
  };
  description: string;
}

export const THEME_PALETTES: PaletteInfo[] = [
  {
    id: 'editorial',
    name: 'Editorial Journal',
    colors: { bg: '#fcf9f4', card: '#ffffff', accent: '#386848', text: '#121814' },
    description: 'Classic journal parchment with deep pine accents'
  },
  {
    id: 'default',
    name: 'Midnight Slate',
    colors: { bg: '#090d16', card: '#0f172a', accent: '#38bdf8', text: '#f8fafc' },
    description: 'Modern Cyber Obsidian'
  },
  {
    id: 'nord',
    name: 'Nord',
    colors: { bg: '#242933', card: '#2e3440', accent: '#88c0d0', text: '#eceff4' },
    description: 'Arctic, north-bluish clean palette'
  },
  {
    id: 'everforest',
    name: 'Everforest',
    colors: { bg: '#272e33', card: '#2d353b', accent: '#a7c080', text: '#d3c6aa' },
    description: 'Comfortable, natural green aesthetic'
  },
  {
    id: 'catppuccin',
    name: 'Catppuccin',
    colors: { bg: '#181825', card: '#1e1e2e', accent: '#cba6f7', text: '#cdd6f4' },
    description: 'Soothing pastel mocha & latte tones'
  },
  {
    id: 'tokyonight',
    name: 'Tokyo Night',
    colors: { bg: '#16161e', card: '#1a1b26', accent: '#7aa2f7', text: '#c0caf5' },
    description: 'Vibrant neon Tokyo city night'
  },
  {
    id: 'gruvbox',
    name: 'Gruvbox',
    colors: { bg: '#1d2021', card: '#282828', accent: '#fabd2f', text: '#ebdbb2' },
    description: 'Warm retro groove palette'
  },
  {
    id: 'dracula',
    name: 'Dracula',
    colors: { bg: '#1e1f29', card: '#282a36', accent: '#ff79c6', text: '#f8f8f2' },
    description: 'Famous dark gothic vampire colors'
  }
];

export function getInitialThemeState(): ThemeState {
  const savedPalette = (localStorage.getItem('vaultlingo_palette') as ThemePalette) || 'editorial';
  const savedColor = (localStorage.getItem('vaultlingo_colormode') as ColorMode) || 'light';

  const validPalette = THEME_PALETTES.some(p => p.id === savedPalette) ? savedPalette : 'editorial';

  return {
    palette: validPalette,
    colorMode: savedColor === 'dark' ? 'dark' : 'light'
  };
}

export function applyThemeState(state: ThemeState): void {
  localStorage.setItem('vaultlingo_palette', state.palette);
  localStorage.setItem('vaultlingo_colormode', state.colorMode);

  const root = document.documentElement;

  // Remove existing palette classes
  THEME_PALETTES.forEach(p => {
    root.classList.remove(`palette-${p.id}`);
    document.body.classList.remove(`palette-${p.id}`);
  });

  root.classList.remove('dark', 'light', 'drawing');
  document.body.classList.remove('dark', 'light', 'drawing');

  // Add current palette and mode classes
  root.classList.add(`palette-${state.palette}`);
  document.body.classList.add(`palette-${state.palette}`);

  root.classList.add(state.colorMode);
  document.body.classList.add(state.colorMode);
}
