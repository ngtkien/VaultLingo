import { describe, it, expect } from "vitest";
import { formatExamplePairs } from "./examplePairing";

describe("formatExamplePairs", () => {
  it("should pair single sentence example correctly", () => {
    const en = "I bought a small model of the Eiffel Tower as a souvenir of my trip to Paris.";
    const vi = "Tôi đã mua một mô hình tháp Eiffel nhỏ làm quà lưu niệm cho chuyến đi đến Paris.";
    const pairs = formatExamplePairs(en, vi);
    expect(pairs).toHaveLength(1);
    expect(pairs[0].en).toBe(en);
    expect(pairs[0].vi).toBe(vi);
  });

  it("should prevent multi-sentence bloated Vietnamese text from dumping onto a single English sentence card", () => {
    const en = "I bought a small model of the Eiffel Tower as a souvenir of my trip to Paris.";
    const vi = "Tôi đã nhận được một lá thư từ người bạn của tôi đang đi du lịch ở Nhật Bản. Trường học đã nhận được một khoản quyên góp lớn. Tôi đã mua một mô hình tháp Eiffel.";
    const pairs = formatExamplePairs(en, vi);
    expect(pairs).toHaveLength(1);
    expect(pairs[0].en).toBe(en);
    // Must only take the first sentence and NOT dump all 3 concatenated sentences
    expect(pairs[0].vi).toBe("Tôi đã nhận được một lá thư từ người bạn của tôi đang đi du lịch ở Nhật Bản.");
  });

  it("should pair up to 2 sentences when multiple sentences exist in both en and vi", () => {
    const en = "First sentence here. Second sentence here. Third sentence here.";
    const vi = "Câu đầu tiên ở đây. Câu thứ hai ở đây. Câu thứ ba ở đây.";
    const pairs = formatExamplePairs(en, vi);
    expect(pairs).toHaveLength(2);
    expect(pairs[0].en).toBe("First sentence here.");
    expect(pairs[0].vi).toBe("Câu đầu tiên ở đây.");
    expect(pairs[1].en).toBe("Second sentence here.");
    expect(pairs[1].vi).toBe("Câu thứ hai ở đây.");
  });

  it("should handle empty inputs gracefully", () => {
    expect(formatExamplePairs("", "")).toEqual([]);
  });
});
