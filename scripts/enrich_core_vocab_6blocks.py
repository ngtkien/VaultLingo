import sqlite3
import json
import os

DB_PATH = os.path.expanduser("~/.local/share/VaultLingo/vocab.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

ENRICHED_WORDS = [
    {
        "word": "collaborate",
        "pos": "Verb",
        "phonetic": "/kəˈlæbəreɪt/",
        "definition_en": "To work jointly with others on an activity or project, especially in an intellectual or creative endeavor.",
        "definition_vi": "Hợp tác, cộng tác cùng người khác để thực hiện một dự án hoặc mục tiêu chung.",
        "word_family": [
            {"pos": "Noun", "word": "collaboration"},
            {"pos": "Adjective", "word": "collaborative"},
            {"pos": "Adverb", "word": "collaboratively"},
            {"pos": "Noun", "word": "collaborator"}
        ],
        "etymology": "From Latin 'collaborare', from 'com-' (together) + 'laborare' (to work).",
        "examples": [
            {"en": "Our engineering and design teams collaborate closely to deliver intuitive software.", "vi": "Đội ngũ kỹ thuật và thiết kế của chúng tôi hợp tác chặt chẽ để mang lại phần mềm trực quan."},
            {"en": "Researchers across continents collaborated to map the entire human genome.", "vi": "Các nhà nghiên cứu xuyên lục địa đã cộng tác cùng nhau để lập bản đồ toàn bộ bộ gen người."}
        ],
        "synonyms": ["cooperate", "partner", "team up", "concur", "join forces"],
        "antonyms": ["compete", "oppose", "resist", "work in isolation"],
        "collocations": ["collaborate closely", "collaborate with stakeholders", "collaborative effort", "cross-functional collaboration"],
        "mnemonic_hook": "COM (cùng nhau) + LABOR (lao động) -> Cùng nhau làm việc, tức là 'cộng tác'.",
        "nuance_tips": "In IELTS Speaking and Writing Task 2, 'collaborate' is significantly more academic and precise than 'work together'. Always pair with 'collaborate WITH someone ON a project'."
    },
    {
        "word": "innovate",
        "pos": "Verb",
        "phonetic": "/ˈɪnəveɪt/",
        "definition_en": "To make changes in something established, especially by introducing new methods, ideas, or products.",
        "definition_vi": "Đổi mới, sáng tạo, đưa ra các phương pháp, ý tưởng hoặc sản phẩm mới.",
        "word_family": [
            {"pos": "Noun", "word": "innovation"},
            {"pos": "Adjective", "word": "innovative"},
            {"pos": "Noun", "word": "innovator"},
            {"pos": "Adverb", "word": "innovatively"}
        ],
        "etymology": "From Latin 'innovare', from 'in-' (into) + 'novus' (new).",
        "examples": [
            {"en": "Tech companies must continuously innovate to maintain their competitive advantage.", "vi": "Các công ty công nghệ phải liên tục đổi mới để duy trì lợi thế cạnh tranh."},
            {"en": "The startup innovated a zero-waste packaging solution for consumer goods.", "vi": "Công ty khởi nghiệp đã sáng tạo ra giải pháp đóng gói không rác thải cho hàng tiêu dùng."}
        ],
        "synonyms": ["revolutionize", "pioneer", "modernize", "transform", "invent"],
        "antonyms": ["stagnate", "preserve", "follow tradition", "regress"],
        "collocations": ["continuously innovate", "technological innovation", "innovative approach", "foster innovation"],
        "mnemonic_hook": "Chứa gốc 'NOVA' (mới, ngôi sao mới) -> Làm cho mọi thứ mới mẻ, hiện đại hơn -> 'đổi mới'.",
        "nuance_tips": "Avoid using 'innovate' passively. Use active phrasing like 'foster/drive innovation' in IELTS essays discussing technology, business, or education."
    },
    {
        "word": "opportunity",
        "pos": "Noun",
        "phonetic": "/ˌɒpəˈtjuːnəti/",
        "definition_en": "A set of circumstances that makes it possible to do something advantageous or desirable.",
        "definition_vi": "Cơ hội, thời cơ thuận lợi để thực hiện hoặc đạt được điều gì đó.",
        "word_family": [
            {"pos": "Adjective", "word": "opportunistic"},
            {"pos": "Adverb", "word": "opportunely"},
            {"pos": "Noun", "word": "opportunism"}
        ],
        "etymology": "From Latin 'opportunitas', from 'opportunus' (favorable, coming at the right time).",
        "examples": [
            {"en": "Studying abroad provides a unique opportunity to experience diverse cultures.", "vi": "Du học mang lại cơ hội độc đáo để trải nghiệm các nền văn hóa đa dạng."},
            {"en": "He seized the opportunity to pitch his startup to venture capitalists.", "vi": "Anh ấy đã nắm bắt cơ hội để trình bày ý tưởng khởi nghiệp trước các nhà đầu tư mạo hiểm."}
        ],
        "synonyms": ["chance", "opening", "occasion", "prospect", "favorable time"],
        "antonyms": ["misfortune", "disadvantage", "obstacle", "setback"],
        "collocations": ["seize an opportunity", "miss an opportunity", "golden opportunity", "equal opportunities", "ample opportunity"],
        "mnemonic_hook": "'OP-PORT-unity': Tàu vừa cập CẢNG (port) đúng lúc thuận gió -> 'Thời cơ/Cơ hội thuận lợi'.",
        "nuance_tips": "Do not confuse 'opportunity' with 'possibility'. 'Opportunity' implies a beneficial, advantageous situation (e.g., career opportunity), whereas 'possibility' simply means something might happen."
    },
    {
        "word": "challenge",
        "pos": "Noun",
        "phonetic": "/ˈtʃælɪndʒ/",
        "definition_en": "A call to take part in a contest or fight; a task or situation that tests someone's abilities.",
        "definition_vi": "Thử thách, thách thức; nhiệm vụ đòi hỏi nhiều nỗ lực và năng lực để vượt qua.",
        "word_family": [
            {"pos": "Verb", "word": "challenge"},
            {"pos": "Adjective", "word": "challenging"},
            {"pos": "Noun", "word": "challenger"}
        ],
        "etymology": "From Old French 'chalenge' (false accusation), from Latin 'calumnia' (trickery, calumny).",
        "examples": [
            {"en": "Transitioning to renewable energy represents the greatest global challenge of our century.", "vi": "Chuyển dịch sang năng lượng tái tạo là thách thức toàn cầu lớn nhất của thế kỷ chúng ta."},
            {"en": "The complex algorithm posed a formidable challenge for the engineering team.", "vi": "Thuật toán phức tạp đã đặt ra một thử thách ghê gớm cho đội ngũ kỹ sư."}
        ],
        "synonyms": ["obstacle", "hurdle", "difficulty", "trial", "test"],
        "antonyms": ["ease", "simplicity", "advantage", "walkover"],
        "collocations": ["pose a challenge", "face a challenge", "overcome a challenge", "formidable challenge", "tackle challenges"],
        "mnemonic_hook": "CHAL-LENGE: Khi đối mặt với thử thách, hãy coi đó là bài tập rèn luyện (challenge -> rèn luyện bản lĩnh).",
        "nuance_tips": "Use 'pose a challenge' instead of 'create a problem' in IELTS Writing Task 2 for elevated academic register."
    },
    {
        "word": "develop",
        "pos": "Verb",
        "phonetic": "/dɪˈveləp/",
        "definition_en": "To grow or cause to grow and become more mature, advanced, or elaborate.",
        "definition_vi": "Phát triển, mở rộng, hoàn thiện hoặc làm cho tiến bộ, phức tạp hơn.",
        "word_family": [
            {"pos": "Noun", "word": "development"},
            {"pos": "Adjective", "word": "developing"},
            {"pos": "Adjective", "word": "developed"},
            {"pos": "Noun", "word": "developer"}
        ],
        "etymology": "From Old French 'desvoloper' (to unwrap, unfurl), opposite of 'envelopper' (to envelop).",
        "examples": [
            {"en": "Reading extensively helps students develop critical thinking skills.", "vi": "Đọc sách sâu rộng giúp học sinh phát triển kỹ năng tư duy phản biện."},
            {"en": "The software engineer developed an automated script to streamline data backups.", "vi": "Kỹ sư phần mềm đã phát triển một script tự động để tinh gọn quy trình sao lưu dữ liệu."}
        ],
        "synonyms": ["advance", "evolve", "cultivate", "expand", "enhance", "formulate"],
        "antonyms": ["regress", "deteriorate", "decline", "stagnate"],
        "collocations": ["develop skills", "develop a strategy", "rapidly develop", "sustainable development"],
        "mnemonic_hook": "Gốc 'de-velop' = Mở gói (unwrap) những tiềm năng ẩn giấu ra bên ngoài -> 'phát triển'.",
        "nuance_tips": "'Develop' can mean both natural growth ('children develop') and intentional creation ('develop a software app')."
    },
    {
        "word": "improve",
        "pos": "Verb",
        "phonetic": "/ɪmˈpruːv/",
        "definition_en": "To make or become better in quality, condition, or performance.",
        "definition_vi": "Cải thiện, nâng cao chất lượng, năng lực hoặc tình trạng.",
        "word_family": [
            {"pos": "Noun", "word": "improvement"},
            {"pos": "Adjective", "word": "improvable"},
            {"pos": "Adjective", "word": "improved"}
        ],
        "etymology": "From Anglo-Norman French 'emprower' (to turn to profit), from 'prou' (profit, advantage).",
        "examples": [
            {"en": "Consistent daily practice is the fastest way to improve your English pronunciation.", "vi": "Luyện tập đều đặn mỗi ngày là cách nhanh nhất để cải thiện phát âm tiếng Anh của bạn."},
            {"en": "Refactoring legacy code significantly improved application loading times.", "vi": "Tái cấu trúc mã nguồn cũ đã cải thiện đáng kể thời gian tải của ứng dụng."}
        ],
        "synonyms": ["enhance", "upgrade", "refine", "boost", "ameliorate"],
        "antonyms": ["worsen", "deteriorate", "degrade", "impair"],
        "collocations": ["drastically improve", "improve efficiency", "continuous improvement", "room for improvement"],
        "mnemonic_hook": "IM-PROVE: Chứng minh (prove) bản thân tiến bộ hơn mỗi ngày -> 'cải thiện'.",
        "nuance_tips": "In academic writing, 'enhance' or 'ameliorate' can be used as sophisticated synonyms for 'improve' depending on whether you are augmenting quality or fixing a problem."
    },
    {
        "word": "achieve",
        "pos": "Verb",
        "phonetic": "/əˈtʃiːv/",
        "definition_en": "To successfully bring about or reach a desired objective, result, or level through effort.",
        "definition_vi": "Đạt được, hoàn thành xuất sắc một mục tiêu hay kết quả mong muốn qua nỗ lực.",
        "word_family": [
            {"pos": "Noun", "word": "achievement"},
            {"pos": "Adjective", "word": "achievable"},
            {"pos": "Noun", "word": "achiever"}
        ],
        "etymology": "From Old French 'achever' (to finish), from 'a chief' (to a head/end).",
        "examples": [
            {"en": "With discipline and persistence, you can achieve your long-term career milestones.", "vi": "Với kỷ luật và sự kiên trì, bạn có thể đạt được các cột mốc sự nghiệp dài hạn của mình."},
            {"en": "The engineering team achieved a 99.99% system uptime over the past year.", "vi": "Đội ngũ kỹ thuật đã đạt tỷ lệ uptime hệ thống 99.99% trong suốt năm qua."}
        ],
        "synonyms": ["accomplish", "attain", "realize", "fulfill", "secure"],
        "antonyms": ["fail", "abandon", "fall short", "surrender"],
        "collocations": ["achieve a goal", "achieve success", "remarkable achievement", "achieve balance"],
        "mnemonic_hook": "CHIEF (đứng đầu) -> Nỗ lực leo lên vị trí đứng đầu để 'đạt được' mục tiêu.",
        "nuance_tips": "Pair with abstract goals: 'achieve success', 'achieve an objective', 'achieve mastery'."
    },
    {
        "word": "maintain",
        "pos": "Verb",
        "phonetic": "/meɪnˈteɪn/",
        "definition_en": "To cause or enable a condition or state of affairs to continue; to keep something in good condition.",
        "definition_vi": "Duy trì, giữ gìn trạng thái ổn định hoặc bảo dưỡng đồ vật, hệ thống.",
        "word_family": [
            {"pos": "Noun", "word": "maintenance"},
            {"pos": "Adjective", "word": "maintainable"},
            {"pos": "Noun", "word": "maintainer"}
        ],
        "etymology": "From Latin 'manu tenere' (to hold in the hand), from 'manus' (hand) + 'tenere' (to hold).",
        "examples": [
            {"en": "Engineers write unit tests to ensure software remains easy to maintain.", "vi": "Kỹ sư viết unit tests để đảm bảo phần mềm luôn dễ duy trì và bảo trì."},
            {"en": "It is essential to maintain regular physical activity for cardiovascular health.", "vi": "Duy trì hoạt động thể chất đều đặn là điều thiết yếu cho sức khỏe tim mạch."}
        ],
        "synonyms": ["preserve", "sustain", "uphold", "retain", "conserve"],
        "antonyms": ["neglect", "abandon", "discontinue", "destroy"],
        "collocations": ["maintain stability", "maintain focus", "high maintenance", "maintain standards"],
        "mnemonic_hook": "MAIN (chính) + TAIN (giữ): Giữ vững phần cốt lõi chính yếu -> 'duy trì'.",
        "nuance_tips": "'Maintain' also means to assert or declare firmly ('He maintained his innocence throughout the trial')."
    }
]

for w in ENRICHED_WORDS:
    cursor.execute("""
        INSERT INTO words (
            word, pos, phonetic, definition_en, definition_vi,
            level, topic, source,
            synonyms_json, antonyms_json, collocations_json, word_family_json,
            etymology, mnemonic_hook, nuance_tips, examples_json
        )
        VALUES (?, ?, ?, ?, ?, 'B2', 'general', 'enriched_seed', ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(word) DO UPDATE SET
            pos = excluded.pos,
            phonetic = excluded.phonetic,
            definition_en = excluded.definition_en,
            definition_vi = excluded.definition_vi,
            synonyms_json = excluded.synonyms_json,
            antonyms_json = excluded.antonyms_json,
            collocations_json = excluded.collocations_json,
            word_family_json = excluded.word_family_json,
            etymology = excluded.etymology,
            mnemonic_hook = excluded.mnemonic_hook,
            nuance_tips = excluded.nuance_tips,
            examples_json = excluded.examples_json
    """, (
        w["word"], w["pos"], w["phonetic"], w["definition_en"], w["definition_vi"],
        json.dumps(w["synonyms"]), json.dumps(w["antonyms"]), json.dumps(w["collocations"]),
        json.dumps(w["word_family"]), w["etymology"], w["mnemonic_hook"], w["nuance_tips"],
        json.dumps(w["examples"])
    ))

conn.commit()
print("🎉 Enriched core vocabulary entries!")

# Sync to data/vocab.db & backend/data/vocab.db
conn.close()
