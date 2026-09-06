function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderInline(text: string): string {
  const codeTokens: string[] = [];
  const linkTokens: string[] = [];

  // 1. Protect inline code `code`
  let result = text.replace(/`([^`]+)`/g, (_, code) => {
    const idx = codeTokens.length;
    codeTokens.push(`<code class="px-1.5 py-0.5 rounded bg-[var(--bg-inner)] border border-[var(--border-main)] font-mono text-xs text-[var(--accent-primary)] font-medium">${code}</code>`);
    return `___CODE_TOKEN_${idx}___`;
  });

  // 2. Protect links [text](url)
  result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, linkText, url) => {
    const idx = linkTokens.length;
    linkTokens.push(`<a href="${url}" class="text-[var(--accent-primary)] hover:underline underline-offset-2" target="_blank" rel="noopener noreferrer">${linkText}</a>`);
    return `___LINK_TOKEN_${idx}___`;
  });

  // 3. Bold: **text** or __text__
  result = result.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-bold text-[var(--text-main)]">$1</strong>');
  result = result.replace(/(^|[^\w])__([^_]+)__([^\w]|$)/g, '$1<strong class="font-bold text-[var(--text-main)]">$2</strong>$3');

  // 4. Italic: *text* or _text_ (only match _ when at word boundaries, not snake_case)
  result = result.replace(/(^|[^\*])\*([^*]+)\*([^\*]|$)/g, '$1<em class="italic">$2</em>$3');
  result = result.replace(/(^|[^\w])_([^_]+)_([^\w]|$)/g, '$1<em class="italic">$2</em>$3');

  // 5. Restore tokens
  result = result.replace(/___LINK_TOKEN_(\d+)___/g, (_, idx) => linkTokens[Number(idx)] || "");
  result = result.replace(/___CODE_TOKEN_(\d+)___/g, (_, idx) => codeTokens[Number(idx)] || "");

  return result;
}

export function renderMarkdown(markdown: string): string {
  if (!markdown) return "";

  // Normalize line endings
  const rawLines = markdown.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n");
  const htmlParts: string[] = [];

  let i = 0;
  while (i < rawLines.length) {
    const line = rawLines[i];

    // Fenced code block
    if (line.trim().startsWith("```")) {
      const lang = line.trim().replace(/^```/, "").trim();
      const codeLines: string[] = [];
      i++;
      while (i < rawLines.length && !rawLines[i].trim().startsWith("```")) {
        codeLines.push(escapeHtml(rawLines[i]));
        i++;
      }
      i++; // skip closing ```
      htmlParts.push(
        `<pre class="my-3 p-3.5 rounded-lg bg-[var(--bg-inner)] border border-[var(--border-main)] overflow-x-auto font-mono text-xs leading-relaxed text-[var(--text-main)]"><code>${codeLines.join("\n")}</code></pre>`
      );
      continue;
    }

    // Markdown Table: detects | col | col |
    if (line.trim().startsWith("|") && line.trim().endsWith("|")) {
      const tableLines: string[] = [];
      while (i < rawLines.length && rawLines[i].trim().startsWith("|") && rawLines[i].trim().endsWith("|")) {
        tableLines.push(rawLines[i].trim());
        i++;
      }

      if (tableLines.length >= 2) {
        const headerRow = tableLines[0];
        const isDivider = (str: string) => /^\|(\s*:?-+:?\s*\|)+$/.test(str.replace(/\s/g, ""));
        let hasDivider = false;
        let dataStartIndex = 1;

        if (tableLines.length > 1 && isDivider(tableLines[1])) {
          hasDivider = true;
          dataStartIndex = 2;
        }

        const parseRow = (rowStr: string) => {
          // Remove leading and trailing pipe
          const trimmed = rowStr.replace(/^\|/, "").replace(/\|$/, "");
          return trimmed.split("|").map(c => c.trim());
        };

        const headerCols = parseRow(headerRow);
        let tableHtml = '<div class="my-3.5 overflow-x-auto rounded-lg border border-[var(--border-main)]"><table class="w-full text-xs text-left border-collapse">';

        tableHtml += '<thead class="bg-[var(--bg-inner)] border-b border-[var(--border-main)]"><tr>';
        for (const col of headerCols) {
          tableHtml += `<th class="px-3.5 py-2.5 font-semibold text-[var(--text-main)] font-mono uppercase text-[11px] tracking-wider">${renderInline(escapeHtml(col))}</th>`;
        }
        tableHtml += '</tr></thead>';

        tableHtml += '<tbody class="divide-y divide-[var(--border-main)]">';
        for (let r = dataStartIndex; r < tableLines.length; r++) {
          const cells = parseRow(tableLines[r]);
          tableHtml += '<tr class="hover:bg-[var(--bg-inner)]/50 transition-colors">';
          for (let c = 0; c < headerCols.length; c++) {
            const cellVal = cells[c] !== undefined ? cells[c] : "";
            tableHtml += `<td class="px-3.5 py-2.5 text-[var(--text-main)] font-sans leading-relaxed">${renderInline(escapeHtml(cellVal))}</td>`;
          }
          tableHtml += '</tr>';
        }
        tableHtml += '</tbody></table></div>';

        htmlParts.push(tableHtml);
        continue;
      }
    }

    // Blank line
    if (!line.trim()) {
      i++;
      continue;
    }

    // Headings
    const headingMatch = line.match(/^(#{1,6})\s+(.*)$/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      const text = renderInline(escapeHtml(headingMatch[2]));
      const classes: Record<number, string> = {
        1: "text-lg font-bold font-serif text-[var(--text-main)] mt-4 mb-2 pb-1 border-b border-[var(--border-main)]",
        2: "text-base font-bold font-serif text-[var(--text-main)] mt-3 mb-1.5",
        3: "text-sm font-semibold font-serif text-[var(--text-main)] mt-2.5 mb-1",
        4: "text-xs font-semibold uppercase tracking-wider font-mono text-[var(--text-muted)] mt-2 mb-1",
        5: "text-xs font-semibold text-[var(--text-muted)] mt-1.5 mb-0.5",
        6: "text-xs italic text-[var(--text-subtle)] mt-1 mb-0.5",
      };
      htmlParts.push(`<h${level} class="${classes[level] || ""}">${text}</h${level}>`);
      i++;
      continue;
    }

    // Blockquote
    if (line.trim().startsWith(">")) {
      const quoteLines: string[] = [];
      while (i < rawLines.length && rawLines[i].trim().startsWith(">")) {
        quoteLines.push(rawLines[i].replace(/^\s*>\s?/, ""));
        i++;
      }
      const quoteText = quoteLines.map(l => renderInline(escapeHtml(l))).join("<br/>");
      htmlParts.push(
        `<blockquote class="my-2.5 pl-3.5 border-l-2 border-[var(--accent-primary)] italic text-xs text-[var(--text-muted)]">${quoteText}</blockquote>`
      );
      continue;
    }

    // Unordered List (- or *)
    if (/^\s*[-*]\s+/.test(line)) {
      const listItems: string[] = [];
      while (i < rawLines.length && /^\s*[-*]\s+/.test(rawLines[i])) {
        const itemText = rawLines[i].replace(/^\s*[-*]\s+/, "");
        listItems.push(renderInline(escapeHtml(itemText)));
        i++;
      }
      htmlParts.push(
        `<ul class="my-2 space-y-1 text-xs text-[var(--text-main)] list-disc pl-5">${listItems.map(item => `<li>${item}</li>`).join("")}</ul>`
      );
      continue;
    }

    // Ordered List (1. 2.)
    if (/^\s*\d+\.\s+/.test(line)) {
      const listItems: string[] = [];
      while (i < rawLines.length && /^\s*\d+\.\s+/.test(rawLines[i])) {
        const itemText = rawLines[i].replace(/^\s*\d+\.\s+/, "");
        listItems.push(renderInline(escapeHtml(itemText)));
        i++;
      }
      htmlParts.push(
        `<ol class="my-2 space-y-1 text-xs text-[var(--text-main)] list-decimal pl-5">${listItems.map(item => `<li>${item}</li>`).join("")}</ol>`
      );
      continue;
    }

    // Regular paragraph: accumulate lines until empty line or special element
    const pLines: string[] = [];
    while (
      i < rawLines.length &&
      rawLines[i].trim() &&
      !rawLines[i].trim().startsWith("```") &&
      !(rawLines[i].trim().startsWith("|") && rawLines[i].trim().endsWith("|")) &&
      !/^#{1,6}\s+/.test(rawLines[i]) &&
      !rawLines[i].trim().startsWith(">") &&
      !/^\s*[-*]\s+/.test(rawLines[i]) &&
      !/^\s*\d+\.\s+/.test(rawLines[i])
    ) {
      pLines.push(renderInline(escapeHtml(rawLines[i])));
      i++;
    }

    if (pLines.length > 0) {
      htmlParts.push(`<p class="my-1.5 leading-relaxed text-xs text-[var(--text-main)]">${pLines.join("<br/>")}</p>`);
    }
  }

  return htmlParts.join("\n");
}
