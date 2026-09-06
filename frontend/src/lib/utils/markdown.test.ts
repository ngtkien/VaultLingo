import { describe, it, expect } from "vitest";
import { renderMarkdown } from "./markdown";

describe("renderMarkdown", () => {
  it("renders headings properly", () => {
    const md = "# Bố cục ảnh firmware gốc — mô hình phân tích đã hiệu chỉnh";
    const html = renderMarkdown(md);
    expect(html).toContain("<h1");
    expect(html).toContain("Bố cục ảnh firmware gốc — mô hình phân tích đã hiệu chỉnh");
  });

  it("renders markdown tables with headers and rows", () => {
    const md = `| Phân vùng | Địa chỉ phân tích | Kích thước / phạm vi |
|---|---|---|
| Ảnh mã thực thi (Code image) | \`0x84000000\` | 101.804 byte |
| Dữ liệu khởi tạo (Initialized data) | \`0x3E900000\` | 3.044 byte |`;

    const html = renderMarkdown(md);
    expect(html).toContain("<table");
    expect(html).toContain("<thead");
    expect(html).toContain("<th");
    expect(html).toContain("Phân vùng");
    expect(html).toContain("<tbody");
    expect(html).toContain("Ảnh mã thực thi");
    expect(html).toContain("<code");
    expect(html).toContain("0x84000000");
  });

  it("renders links and inline formatting", () => {
    const md = "Tham khảo [bản kiểm tra IDA](18_ida_rv32_live_audit.md) và **quan trọng**.";
    const html = renderMarkdown(md);
    expect(html).toContain('<a href="18_ida_rv32_live_audit.md"');
    expect(html).toContain("bản kiểm tra IDA</a>");
    expect(html).toContain('<strong class="font-bold text-[var(--text-main)]">quan trọng</strong>');
  });

  it("prevents XSS injection", () => {
    const md = `<script>alert('xss')</script>`;
    const html = renderMarkdown(md);
    expect(html).not.toContain("<script>");
    expect(html).toContain("&lt;script&gt;");
  });

  it("handles lists and code blocks", () => {
    const md = `- Item 1\n- Item 2\n\n\`\`\`go\nfmt.Println("hi")\n\`\`\``;
    const html = renderMarkdown(md);
    expect(html).toContain("<ul");
    expect(html).toContain("Item 1");
    expect(html).toContain("<pre");
    expect(html).toContain("fmt.Println");
  });

  it("handles complete firmware translation markdown from user report", () => {
    const md = `# Bố cục ảnh firmware gốc — mô hình phân tích đã hiệu chỉnh

Tham khảo [bản kiểm tra IDA trực tiếp](18_ida_rv32_live_audit.md) và [dự án được lưu giữ](../../reverse/ida/projects/stock_rv32_mailbox/README.md).

| Phân vùng | Địa chỉ phân tích | Kích thước / phạm vi |
|---|---|---|
| Ảnh mã thực thi (Code image) | \`0x84000000\` | 101.804 byte; bao gồm các hằng số nhúng |
| Dữ liệu khởi tạo (Initialized data) | \`0x3E900000\` | 3.044 byte |
| Vùng khởi tạo 0 khi khởi động (Startup zero range) | \`[0x3E900BE8, 0x3E903AEC)\` | Suy dẫn từ tập lệnh khởi động gốc |

Đây là mô hình địa chỉ liên kết/phân tích được chứng thực bởi các con trỏ dữ liệu và tập lệnh gốc của hệ thống.`;

    const html = renderMarkdown(md);
    expect(html).toContain("<h1");
    expect(html).toContain("<table");
    expect(html).toContain("Ảnh mã thực thi");
    expect(html).toContain("<code>0x84000000</code>");
    expect(html).toContain("<code>[0x3E900BE8, 0x3E903AEC)</code>");
    expect(html).toContain('<a href="18_ida_rv32_live_audit.md"');
    expect(html).toContain("Đây là mô hình");
  });
});
