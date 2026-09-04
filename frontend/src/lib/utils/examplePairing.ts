export function cleanString(text: string | undefined | null): string {
  if (!text) return "";
  return text
    .replace(/\r/g, "")
    .replace(/:\s*:\s*id=[^"'\s]*/gi, "")
    .replace(/id=[a-zA-Z0-9._&=-]+/gi, "")
    .replace(/\s*\b\d{3,}\b\s*$/, "")
    .trim();
}

export interface ExamplePair {
  en: string;
  vi: string;
}

export function formatExamplePairs(
  rawEn: string | undefined | null,
  rawVi: string | undefined | null
): ExamplePair[] {
  if (!rawEn && !rawVi) return [];

  const en = cleanString(rawEn);
  const rawEnParts = en.split(/\s*[/|]\s*|\n+/).map(s => s.trim()).filter(Boolean);
  let enSents: string[] = [];
  for (const p of rawEnParts) {
    const sents = p.match(/[^.!?]+[.!?]/g);
    if (sents && sents.length > 0) {
      for (const s of sents) {
        const sc = s.trim();
        if (sc.length > 5) enSents.push(sc);
      }
    } else if (p.length > 5) {
      enSents.push(p.replace(/[.!?]*$/, "") + ".");
    }
  }

  const vi = cleanString(rawVi || "");
  const viRawParts = vi.split(/\s*[/|]\s*|\n+/).map(s => s.trim()).filter(Boolean);
  let viSents: string[] = [];
  for (const p of viRawParts) {
    const sents = p.match(/[^.!?]+[.!?]/g);
    if (sents && sents.length > 0) {
      for (const s of sents) {
        const sc = s.trim();
        if (sc.length > 3) viSents.push(sc);
      }
    } else if (p.length > 3) {
      viSents.push(p.trim());
    }
  }

  const maxCount = Math.min(enSents.length, 2);
  const pairs: ExamplePair[] = [];
  for (let i = 0; i < maxCount; i++) {
    let viSent = viSents[i] || "";
    if (viSent.length > 250) {
      const first = viSent.match(/^[^.!?]+[.!?]/);
      if (first) viSent = first[0].trim();
    }
    pairs.push({
      en: enSents[i],
      vi: viSent
    });
  }

  if (pairs.length === 0 && en.length > 0) {
    pairs.push({ en, vi });
  }

  return pairs;
}
