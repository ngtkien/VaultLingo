import sqlite3
import json
import os

DB_PATH = os.path.expanduser("~/.local/share/VaultLingo/vocab.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. ENRICH IDIOMS (25 new authentic idioms)
NEW_IDIOMS = [
    ("Break the ice", "/breɪk ðiː aɪs/", "To initiate conversation in a social setting and relieve tension.", "Phá vỡ bầu không khí ngượng ngùng ban đầu.", "A good joke is a great way to break the ice at meetings.", "Một câu chuyện đùa là cách tuyệt vời để phá vỡ sự ngượng ngùng trong cuộc họp."),
    ("Bite the bullet", "/baɪt ðə ˈbʊlɪt/", "To face a difficult situation with courage and fortitude.", "Cắn răng chịu đựng, dũng cảm đối mặt với thử thách.", "We had to bite the bullet and pay for the costly server upgrade.", "Chúng tôi phải cắn răng chi trả cho đợt nâng cấp server đắt đỏ."),
    ("Call it a day", "/kɔːl ɪt ə deɪ/", "To stop working on something for the rest of the day.", "Dừng lại, kết thúc một ngày làm việc.", "We have accomplished a lot today, so let's call it a day.", "Hôm nay chúng ta đã làm xong nhiều việc, hãy nghỉ ngơi thôi."),
    ("Hit the nail on the head", "/hɪt ðə neɪl ɒn ðə hed/", "To describe exactly what is causing a situation or problem.", "Nói trúng phóc, chỉ ra đúng điểm mấu chốt.", "Her analysis of the bottleneck hit the nail on the head.", "Phân tích của cô ấy về điểm nghẽn đã nói trúng phóc vấn đề."),
    ("Piece of cake", "/piːs əv keɪk/", "Something that is very easy to accomplish.", "Dễ như ăn bánh, vô cùng đơn giản.", "The technical interview was a piece of cake for her.", "Buổi phỏng vấn kỹ thuật đối với cô ấy dễ như trở bàn tay."),
    ("Burn the midnight oil", "/bɜːn ðə ˈmɪdnaɪt ɔɪl/", "To work or study late into the night.", "Thức khuya miệt mài học tập hoặc làm việc.", "He burned the midnight oil to prepare for the product launch.", "Anh ấy đã thức trắng đêm để chuẩn bị cho buổi ra mắt sản phẩm."),
    ("See eye to eye", "/siː aɪ tuː aɪ/", "To be in full agreement with someone.", "Đồng tình, chung quan điểm với ai đó.", "The engineering lead and product manager see eye to eye on priorities.", "Trưởng nhóm kỹ thuật và quản lý sản phẩm hoàn toàn đồng thuận về các ưu tiên."),
    ("Blessing in disguise", "/ˈblesɪŋ ɪn dɪsˈɡaɪz/", "A good thing that seemed bad at first.", "Trong cái rủi có cái may.", "Losing that client was a blessing in disguise as it freed us to innovate.", "Mất khách hàng đó hóa ra lại là điều may mắn vì giúp chúng tôi rảnh tay đổi mới."),
    ("Back to the drawing board", "/bæk tuː ðə ˈdrɔːɪŋ bɔːd/", "To start planning something again because the previous attempt failed.", "Làm lại từ đầu, lên lại kế hoạch từ con số không.", "When the prototype failed the stress test, we went back to the drawing board.", "Khi bản mẫu thử nghiệm không đạt bài kiểm tra tải, chúng tôi phải bắt đầu lại từ đầu."),
    ("Cut corners", "/kʌt ˈkɔːnəz/", "To do something in the easiest or cheapest way, sacrificing quality.", "Làm ẩu, đi đường tắt làm giảm chất lượng.", "Never cut corners when designing security architecture.", "Đừng bao giờ làm ẩu khi thiết kế kiến trúc bảo mật."),
    ("Under the weather", "/ˈʌndə ðə ˈweðə/", "Slightly unwell or fatigued.", "Hơi mệt, cảm thấy không được khỏe.", "I felt a bit under the weather so I opted to work remotely.", "Tôi thấy hơi mệt nên đã xin phép làm việc từ xa."),
    ("Elephant in the room", "/ˈelɪfənt ɪn ðə ruːm/", "A major problem or obvious truth that everyone avoids discussing.", "Vấn đề hiển nhiên nhưng mọi người đều né tránh nhắc tới.", "Nobody wanted to mention the budget deficit, but it was the elephant in the room.", "Không ai muốn nhắc tới thâm hụt ngân sách, nhưng đó là vấn đề ai cũng thấy rõ."),
    ("Touch base", "/tʌtʃ beɪs/", "To briefly meet or make contact with someone.", "Trao đổi nhanh, liên lạc ngắn để cập nhật tình hình.", "Let's touch base tomorrow morning after the standup.", "Chúng ta hãy trao đổi nhanh vào sáng mai sau buổi họp standup nhé."),
    ("On the same page", "/ɒn ðə seɪm peɪdʒ/", "Having the same understanding and goals.", "Hiểu ý nhau, cùng chung nhận thức.", "Before we start coding, let's ensure all stakeholders are on the same page.", "Trước khi code, hãy đảm bảo mọi bên liên quan đều hiểu chung định hướng."),
    ("Take with a grain of salt", "/teɪk wɪð ə ɡreɪn əv sɔːlt/", "To view something with skepticism and not completely believe it.", "Tiếp nhận thông tin một cách thận trọng, có chọn lọc.", "Take unverified performance benchmarks with a grain of salt.", "Hãy cẩn trọng và đừng vội tin hoàn toàn các bài đo hiệu năng chưa kiểm chứng."),
    ("Spill the beans", "/spɪl ðə biːnz/", "To reveal a secret prematurely or inadvertently.", "Làm lộ bí mật.", "Please don't spill the beans about the unreleased feature.", "Làm ơn đừng làm lộ bí mật về tính năng chưa công bố nhé."),
    ("Through thick and thin", "/θruː θɪk ænd θɪn/", "Supporting someone through all circumstances, good and bad.", "Cùng nhau vượt qua mọi thăng trầm, hoạn nạn có nhau.", "The founding team stayed together through thick and thin.", "Đội ngũ sáng lập đã gắn bó bên nhau qua mọi thăng trầm."),
    ("Once in a blue moon", "/wʌns ɪn ə bluː muːn/", "Very rarely or infrequently.", "Hiếm khi, năm thì mười họa.", "Major infrastructure outages happen once in a blue moon.", "Sự cố sập hạ tầng nghiêm trọng rất hiếm khi xảy ra."),
    ("Ahead of the curve", "/əˈhed əv ðə kɜːv/", "More advanced or progressive than competitors.", "Đi trước thời đại, dẫn đầu xu thế.", "Investing in AI early placed the company ahead of the curve.", "Đầu tư vào AI sớm đã giúp công ty đón đầu xu thế."),
    ("Play devil's advocate", "/pleɪ ˈdevlz ˈædvəkət/", "To argue against an idea to test its strength or provoke debate.", "Đóng vai người phản biện để kiểm tra tính vững chắc của luận điểm.", "Let me play devil's advocate: what if user traffic triples overnight?", "Để tôi đóng vai người phản biện nhé: nếu lượng truy cập tăng gấp ba chỉ sau một đêm thì sao?"),
    ("Keep someone in the loop", "/kiːp ˈsʌmwʌn ɪn ðə luːp/", "To keep someone informed about ongoing developments.", "Luôn cập nhật thông tin kịp thời cho ai đó.", "Please keep me in the loop regarding the client's decision.", "Hãy nhớ cập nhật liên tục cho tôi về quyết định của khách hàng nhé."),
    ("Ball is in your court", "/bɔːl ɪz ɪn jɔː kɔːt/", "It is your turn or responsibility to take the next step.", "Quyền quyết định / lượt xử lý tiếp theo thuộc về bạn.", "I have sent the updated contract; the ball is in their court now.", "Tôi đã gửi hợp đồng cập nhật; giờ quyền quyết định thuộc về họ."),
    ("Jump on the bandwagon", "/dʒʌmp ɒn ðə ˈbændwæɡən/", "To join an activity or trend because it has become popular.", "Chạy theo trào lưu, a dua theo xu hướng.", "Many companies jumped on the bandwagon of remote working.", "Nhiều doanh nghiệp đã nhanh chóng bắt kịp làn sóng làm việc từ xa."),
    ("Burn bridges", "/bɜːn ˈbrɪdʒɪz/", "To destroy relationships or options permanently.", "Cắt đứt mọi đường lui, làm mất lòng người khác khi ra đi.", "Even when leaving a job, never burn bridges with former teammates.", "Kể cả khi chuyển việc, đừng bao giờ làm sứt mẻ mối quan hệ với đồng nghiệp cũ.")
]

for item in NEW_IDIOMS:
    cursor.execute("""
        INSERT OR IGNORE INTO idioms (idiom, phonetic, meaning_en, meaning_vi, example, example_vi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, item)

# 2. ENRICH QUIZZES (16 new high-yield grammar/collocation quizzes)
NEW_QUIZZES = [
    (
        "Collocations", "⚡", 
        "Choose the correct verb: 'We need to ___ a decision before the end of the sprint.'",
        json.dumps(["A. make", "B. do", "C. create", "D. take"]),
        "A", "We need to make a decision before the end of the sprint.",
        "In English, we say 'MAKE a decision' (not 'do a decision').",
        "Collocation: make a decision / make a choice / make a mistake."
    ),
    (
        "Prepositions", "🎯",
        "Fill in the blank: 'Our team is responsible ___ maintaining the database cluster.'",
        json.dumps(["A. for", "B. with", "C. about", "D. in"]),
        "A", "Our team is responsible for maintaining the database cluster.",
        "The adjective 'responsible' always pairs with the preposition 'FOR'.",
        "Structure: to be responsible for + V-ing/noun."
    ),
    (
        "Business English", "💼",
        "Choose the correct phrase: 'I look forward to ___ from you soon.'",
        json.dumps(["A. hearing", "B. hear", "C. heard", "D. be hearing"]),
        "A", "I look forward to hearing from you soon.",
        "In 'look forward to', 'to' is a preposition, so it must be followed by a gerund (V-ing).",
        "Key rule: look forward to + V-ing."
    ),
    (
        "Grammar & Tenses", "⏳",
        "Choose the correct tense: 'By the time the project launched, the team ___ for six months.'",
        json.dumps(["A. had been working", "B. has worked", "C. is working", "D. will work"]),
        "A", "By the time the project launched, the team had been working for six months.",
        "Use Past Perfect Continuous for an action that was ongoing before another point in the past.",
        "Marker: By the time + Past Simple -> Past Perfect."
    ),
    (
        "Vocabulary Nuance", "🧠",
        "Which word fits best: 'The new encryption protocol will ___ unauthorized data access.'",
        json.dumps(["A. prevent", "B. avoid", "C. refuse", "D. deny"]),
        "A", "The new encryption protocol will prevent unauthorized data access.",
        "'Prevent' means to stop something from happening before it occurs.",
        "Collocation: prevent + noun / prevent from V-ing."
    ),
    (
        "Conditionals", "🔀",
        "Complete the sentence: 'If we ___ the bug earlier, we would have avoided the downtime.'",
        json.dumps(["A. had discovered", "B. discovered", "C. have discovered", "D. discover"]),
        "A", "If we had discovered the bug earlier, we would have avoided the downtime.",
        "Third Conditional structure: If + had + V3/ed, ... would have + V3/ed (unreal past).",
        "Rule: Past condition with past regret -> Third conditional."
    ),
    (
        "Articles", "📝",
        "Choose the correct article: 'He has ___ master's degree in computer science.'",
        json.dumps(["A. a", "B. an", "C. the", "D. (no article)"]),
        "A", "He has a master's degree in computer science.",
        "'Master's degree' begins with a consonant sound /m/, so we use the indefinite article 'a'.",
        "Note: a master's degree / a bachelor's degree."
    ),
    (
        "Verbs & Prepositions", "🔗",
        "Select the correct option: 'The manager insisted ___ reviewing the code herself.'",
        json.dumps(["A. on", "B. in", "C. at", "D. for"]),
        "A", "The manager insisted on reviewing the code herself.",
        "The verb 'insist' is always followed by the preposition 'ON'.",
        "Formula: insist on + V-ing."
    ),
    (
        "Subject-Verb Agreement", "⚖️",
        "Choose the correct verb: 'Neither the frontend engineer nor the designers ___ aware of the change.'",
        json.dumps(["A. were", "B. was", "C. is", "D. has been"]),
        "A", "Neither the frontend engineer nor the designers were aware of the change.",
        "In 'neither... nor...', the verb agrees with the subject closest to it ('designers' is plural -> 'were').",
        "Rule of proximity: agree with the nearest subject."
    ),
    (
        "Adjective vs Adverb", "✨",
        "Fill in the blank: 'The new API endpoint responds remarkably ___ under heavy load.'",
        json.dumps(["A. quickly", "B. quick", "C. quicker", "D. quickness"]),
        "A", "The new API endpoint responds remarkably quickly under heavy load.",
        "An adverb ('quickly') modifies the action verb ('responds').",
        "Adverb modifies verb: responds + quickly."
    ),
    (
        "IELTS Lexical Resource", "🎓",
        "Select the best academic synonym for 'a lot of': 'The study presents ___ evidence.'",
        json.dumps(["A. substantial", "B. bunch of", "C. many much", "D. tons of"]),
        "A", "The study presents substantial evidence.",
        "In formal academic writing, 'substantial' or 'considerable' replaces informal phrases like 'a lot of'.",
        "Academic vocab: substantial evidence / compelling arguments."
    ),
    (
        "Phrasal Verbs", "🚀",
        "Choose the right phrasal verb: 'We decided to ___ the deployment until Monday morning.'",
        json.dumps(["A. put off", "B. call off", "C. take off", "D. give off"]),
        "A", "We decided to put off the deployment until Monday morning.",
        "'Put off' means to postpone or delay. ('Call off' means to cancel entirely).",
        "Distinction: put off = delay | call off = cancel."
    ),
    (
        "Prepositions of Time", "⏱️",
        "Select the correct preposition: 'The workshop will conclude ___ 5:00 PM.'",
        json.dumps(["A. at", "B. on", "C. in", "D. to"]),
        "A", "The workshop will conclude at 5:00 PM.",
        "We use 'AT' for specific clock times.",
        "Rule: at 5 PM / on Monday / in July."
    ),
    (
        "Connectors & Cohesion", "🧩",
        "Choose the appropriate linker: 'The system is secure. ___, it complies with GDPR.'",
        json.dumps(["A. Furthermore", "B. Although", "C. Whereas", "D. Despite"]),
        "A", "The system is secure. Furthermore, it complies with GDPR.",
        "'Furthermore' adds reinforcing additional information in formal context.",
        "Linker: Furthermore / Moreover / Additionally."
    ),
    (
        "Relative Clauses", "🌐",
        "Fill in the blank: 'This is the server ___ crashed during the peak hours yesterday.'",
        json.dumps(["A. which", "B. who", "C. whom", "D. whose"]),
        "A", "This is the server which crashed during the peak hours yesterday.",
        "Use 'which' or 'that' for non-human objects and machines.",
        "Relative pronoun: which/that for objects | who for people."
    ),
    (
        "Reported Speech", "🗣️",
        "Choose the correct form: 'She told me that she ___ the report before leaving.'",
        json.dumps(["A. had submitted", "B. submits", "C. has submitted", "D. will submit"]),
        "A", "She told me that she had submitted the report before leaving.",
        "In reported speech with past reporting verb ('told'), past actions shift to Past Perfect.",
        "Backshifting rule: Simple Past/Present Perfect -> Past Perfect."
    )
]

for item in NEW_QUIZZES:
    cursor.execute("""
        INSERT INTO quizzes (category, category_icon, question, options_json, correct, correct_sentence, explanation, tip)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, item)

# 3. ENRICH DICTATIONS (18 new diverse sentences)
NEW_DICTATIONS = [
    ("B1 Workplace", "#4caf50", "Team Collaboration", "🤝", "Please send me the updated meeting minutes as soon as possible.", "Làm ơn hãy gửi cho tôi biên bản cuộc họp đã cập nhật sớm nhất có thể.", "Keywords: send, updated, meeting minutes, as soon as possible."),
    ("B1 Daily", "#4caf50", "Daily Routine", "☕", "I prefer drinking a cup of warm tea before starting my workday.", "Tôi thích uống một tách trà ấm trước khi bắt đầu ngày làm việc.", "Keywords: prefer, warm tea, starting, workday."),
    ("B2 Workplace", "#2196f3", "Project Management", "📊", "We need to prioritize critical user feedback to meet our quarterly delivery target.", "Chúng ta cần ưu tiên phản hồi quan trọng của người dùng để đạt mục tiêu bàn giao quý này.", "Keywords: prioritize, critical feedback, quarterly, delivery target."),
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", "The microservices architecture improved overall system reliability and deployment velocity.", "Kiến trúc microservices đã cải thiện độ tin cậy và tốc độ triển khai của toàn hệ thống.", "Keywords: microservices, system reliability, deployment velocity."),
    ("B1 Travel", "#4caf50", "Airport & Commute", "✈️", "Please make sure your luggage conforms to the airline carry-on regulations.", "Làm ơn hãy đảm bảo hành lý của bạn tuân thủ quy định hành lý xách tay của hãng bay.", "Keywords: luggage, conforms, airline, carry-on regulations."),
    ("B2 Workplace", "#2196f3", "Client Negotiation", "💼", "Our team presented a detailed proposal outlining the estimated project budget and timeline.", "Đội ngũ của chúng tôi đã trình bày một bản đề xuất chi tiết nêu rõ ngân sách và tiến độ dự kiến.", "Keywords: presented, proposal, estimated budget, timeline."),
    ("B1 Daily", "#4caf50", "Health & Fitness", "🏃", "Taking regular short breaks during work hours helps maintain mental focus.", "Nghỉ ngơi ngắn định kỳ trong giờ làm việc giúp duy trì sự tập trung tinh thần.", "Keywords: regular breaks, work hours, mental focus."),
    ("B2 Tech", "#9c27b0", "Cloud Computing", "☁️", "Automated backup routines run every midnight to protect customer data from loss.", "Quy trình sao lưu tự động chạy vào mỗi nửa đêm để bảo vệ dữ liệu khách hàng khỏi bị mất.", "Keywords: automated backup, midnight, protect data, loss."),
    ("B1 Workplace", "#4caf50", "Customer Support", "🎧", "Thank you for bringing this issue to our attention; we will investigate immediately.", "Cảm ơn bạn đã phản ánh vấn đề này; chúng tôi sẽ tiến hành kiểm tra ngay lập tức.", "Keywords: bringing issue, attention, investigate immediately."),
    ("B2 Academic", "#ff9800", "Research & Analysis", "🔬", "Recent experimental results demonstrate a significant correlation between sleep and memory retention.", "Các kết quả thử nghiệm gần đây chứng minh mối tương quan rõ rệt giữa giấc ngủ và khả năng ghi nhớ.", "Keywords: experimental results, significant correlation, memory retention."),
    ("B1 Workplace", "#4caf50", "Office Environment", "🏢", "Could you please turn down the volume of the conference call speaker?", "Bạn có thể vui lòng vặn nhỏ âm lượng loa cuộc gọi họp trực tuyến không?", "Keywords: turn down, volume, conference call, speaker."),
    ("B2 Tech", "#9c27b0", "Cybersecurity", "🔒", "Multi-factor authentication provides an essential security layer against credential theft.", "Xác thực đa yếu tố cung cấp lớp bảo mật thiết yếu chống lại việc đánh cắp tài khoản.", "Keywords: multi-factor authentication, security layer, credential theft."),
    ("B1 Daily", "#4caf50", "Shopping & Finance", "💳", "Remember to keep the purchase receipt in case you want to exchange the item.", "Hãy nhớ giữ hóa đơn mua hàng phòng khi bạn muốn đổi sản phẩm.", "Keywords: purchase receipt, exchange item, remember."),
    ("B2 Workplace", "#2196f3", "Remote Work", "🏠", "Clear asynchronous communication is fundamental for distributed remote teams across time zones.", "Giao tiếp bất đồng bộ rõ ràng là yếu tố nền tảng cho các nhóm làm việc từ xa qua nhiều múi giờ.", "Keywords: asynchronous communication, fundamental, distributed teams, time zones."),
    ("B1 Daily", "#4caf50", "Social Gathering", "🎉", "We are organizing a small farewell gathering for our colleague this Friday evening.", "Chúng tôi đang tổ chức một buổi liên hoan chia tay nhỏ cho đồng nghiệp vào tối thứ Sáu này.", "Keywords: organizing, farewell gathering, colleague, Friday evening."),
    ("B2 Academic", "#ff9800", "Critical Thinking", "💡", "Critical thinking involves objectively analyzing facts before reaching a definitive conclusion.", "Tư duy phản biện bao gồm việc phân tích khách quan các dữ kiện trước khi đưa ra kết luận dứt khoát.", "Keywords: critical thinking, objectively analyzing facts, definitive conclusion."),
    ("B2 Workplace", "#2196f3", "Sprint Retrospective", "🔄", "During our retrospective, we discussed actionable ways to streamline the review process.", "Trong buổi họp hồi tưởng, chúng tôi đã thảo luận các giải pháp thiết thực để tinh gọn quy trình xét duyệt.", "Keywords: retrospective, actionable ways, streamline review process."),
    ("B1 Daily", "#4caf50", "Time Management", "⏰", "Planning your top three priorities each morning prevents unexpected distractions.", "Lên kế hoạch ba việc ưu tiên nhất vào mỗi sáng giúp tránh bị xao nhãng ngoài ý muốn.", "Keywords: planning priorities, morning, unexpected distractions.")
]

for item in NEW_DICTATIONS:
    cursor.execute("""
        INSERT INTO dictations (level, level_color, category, category_icon, sentence, sentence_vi, hint)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, item)

# 4. ENRICH WRITING PROMPTS (10 new scenarios across levels)
NEW_PROMPTS = [
    (
        "scenario", "Clarifying Unclear Requirements", "Workplace Communication", "💬", 25, 60,
        "You received a task specification from your product manager that lacks details on edge cases. Write a polite message asking for a brief sync or clarification.",
        "Write a 2 to 3 sentence message to your product manager asking for clarification on missing specifications.",
        json.dumps(["Hi, thanks for sharing the task brief. While reviewing...", "Could we schedule a quick 5-minute sync to clarify..."]),
        json.dumps(["Be specific about which section is unclear.", "Suggest a quick call or bulleted response to save time."]),
        json.dumps(["clarify edge cases", "quick sync", "task specifications"])
    ),
    (
        "scenario", "Congratulating Teammate on Promotion", "Social & Team Culture", "🎉", 20, 50,
        "Your teammate just received a well-deserved promotion to Senior Engineer. Write a warm and genuine congratulatory Slack message.",
        "Write a 2 to 3 sentence congratulatory message to your newly promoted colleague.",
        json.dumps(["Huge congratulations on your promotion to...", "Your hard work and dedication truly inspire all of us..."]),
        json.dumps(["Keep the tone warm, authentic, and celebratory.", "Mention their positive impact on the team."]),
        json.dumps(["well-deserved", "dedication", "congratulations"])
    ),
    (
        "scenario", "Handing Over Tasks Before Vacation", "Workplace Slack", "🏖️", 30, 70,
        "You are going on annual leave for one week. Write a clear handover message in the team channel noting who is covering your ongoing tickets.",
        "Write a 2 to 3 sentence handover message informing your team of your upcoming leave and coverage.",
        json.dumps(["Hi team, I will be out of office from Monday to...", "For any urgent inquiries regarding our current sprint, please reach out to..."]),
        json.dumps(["State the exact dates of absence clearly.", "Identify specific backup contacts."]),
        json.dumps(["out of office", "handover", "point of contact"])
    ),
    (
        "short", "The Pros and Cons of Remote Work", "Workplace & Society", "💻", 50, 90,
        "Discuss whether remote working enhances overall productivity or creates communication barriers among engineering teams.",
        "Write a short 50 to 90 word paragraph discussing the balance between flexibility and collaboration in remote environments.",
        json.dumps(["Remote working has undeniably revolutionized the modern workplace by...", "However, maintaining spontaneous collaboration remains a notable challenge..."]),
        json.dumps(["Present both advantages (flexibility, focus) and challenges (isolation, timezone sync).", "Use linking words like 'On the one hand', 'Conversely', 'Consequently'."]),
        json.dumps(["asynchronous workflows", "work-life balance", "spontaneous collaboration"])
    ),
    (
        "short", "Impact of AI Coding Assistants on Developers", "Tech & AI", "🤖", 50, 90,
        "Explore how generative AI tools like Copilot and Antigravity are transforming software development workflows.",
        "Write a short 50 to 90 word analysis on how AI tools influence coding speed, code quality, and problem-solving.",
        json.dumps(["AI coding assistants have significantly accelerated boilerplate generation and...", "Nevertheless, critical architectural oversight and rigorous testing remain essential..."]),
        json.dumps(["Highlight productivity gains and the ongoing need for human judgment.", "Maintain a professional, forward-looking tone."]),
        json.dumps(["boilerplate reduction", "architectural oversight", "developer productivity"])
    ),
    (
        "short", "Strategies for Effective English Vocabulary Retention", "Language Learning", "📚", 50, 90,
        "Describe effective techniques you use to remember new English vocabulary words and collocations over long periods.",
        "Write a 50 to 90 word reflection on the role of spaced repetition (SRS) and contextual practice in mastering vocabulary.",
        json.dumps(["Mastering advanced vocabulary requires more than passive memorization...", "Implementing spaced repetition algorithms alongside real-world writing ensures..."]),
        json.dumps(["Explain the value of active recall and spaced intervals.", "Mention applying words in real writing context."]),
        json.dumps(["spaced repetition", "active recall", "contextual usage"])
    ),
    (
        "medium", "Engineering Trade-offs in System Architecture", "Software Engineering", "🏗️", 120, 180,
        "Write an essay discussing why there are no perfect architectures in software engineering, only trade-offs between simplicity, scalability, and delivery speed.",
        "Write an essay (120 to 180 words) evaluating how engineering teams should balance rapid feature delivery with long-term code maintainability.",
        json.dumps(["In modern software engineering, architectural decisions are fundamentally governed by trade-offs...", "While premature optimization can stall initial market validation, neglecting modular design leads to crippling technical debt..."]),
        json.dumps(["Structure into Introduction, Body (Trade-off analysis), and Conclusion.", "Use formal transitions: 'Furthermore', 'On the contrary', 'Ultimately'."]),
        json.dumps(["technical debt", "modular architecture", "scalability vs simplicity", "trade-offs"])
    ),
    (
        "medium", "The Importance of Continuous Learning in Technology", "Career & Growth", "🚀", 120, 180,
        "Discuss why continuous professional development and adapting to new technologies are vital for engineering career longevity.",
        "Write a 120 to 180 word essay analyzing how rapid technological shifts require engineers to cultivate lifelong learning habits.",
        json.dumps(["The rapid acceleration of technological innovation has redefined career longevity in tech...", "Engineers who cultivate deep foundational understanding alongside adaptive learning habits consistently thrive..."]),
        json.dumps(["Contrast static knowledge with adaptive problem solving.", "Conclude with a clear perspective on lifelong curiosity."]),
        json.dumps(["lifelong learning", "technological paradigm shift", "adaptability", "foundational mastery"])
    )
]

for item in NEW_PROMPTS:
    cursor.execute("""
        INSERT INTO writing_prompts (level, title, category, category_icon, target_min, target_max, situation_vi, prompt, sentence_starters_json, guide_tips_json, suggested_vocab_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, item)

# 5. CREATE & SEED LISTENING_TOPICS TABLE (25 Comprehensive Q&A Topics)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS listening_topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER UNIQUE NOT NULL,
        title TEXT NOT NULL,
        icon TEXT DEFAULT '🎧',
        audio_url TEXT NOT NULL,
        web_url TEXT,
        qa_json TEXT NOT NULL
    );
""")

LISTENING_DATA = [
    (1, "Family", "👨‍👩‍👧", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-01.mp3", "https://basicenglishspeaking.com/family/", [
        {"q": "How many people are there in your family?", "a": "There are four people in my family: my father, my mother, my younger sister, and me."},
        {"q": "Does your family live in a house or an apartment?", "a": "We live in a cozy house with a small garden in the suburbs."},
        {"q": "What does your father do?", "a": "My father is a civil engineer who designs infrastructure projects."}
    ]),
    (2, "Restaurant", "🍽️", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-02.mp3", "https://basicenglishspeaking.com/restaurant/", [
        {"q": "How often do you eat out? Who do you go with?", "a": "I often eat out on weekends with my close friends or colleagues."},
        {"q": "What restaurant do you usually visit?", "a": "I love visiting a local Italian restaurant known for its handmade pasta and stone-baked pizza."},
        {"q": "Do you prefer eating at home or eating out?", "a": "I prefer home-cooked meals for health, but dining out is great for socializing."}
    ]),
    (3, "Books", "📚", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-03.mp3", "https://basicenglishspeaking.com/books/", [
        {"q": "How often do you read books?", "a": "I read books every evening before going to bed, usually for about 30 to 45 minutes."},
        {"q": "What is your favorite type of book?", "a": "I enjoy non-fiction, especially books about technology, psychology, and personal productivity."},
        {"q": "Who is your favorite author?", "a": "I really admire James Clear for his practical insights on habit formation."}
    ]),
    (4, "Travel", "✈️", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-04.mp3", "https://basicenglishspeaking.com/travel/", [
        {"q": "How many places have you traveled to?", "a": "I have visited over ten cities across my home country and three international destinations."},
        {"q": "Do you prefer traveling alone or with friends?", "a": "I prefer traveling with friends because sharing experiences and memories makes the journey more meaningful."},
        {"q": "What do you usually pack when traveling?", "a": "I pack lightweight clothing, a camera, travel adapters, and my noise-cancelling headphones."}
    ]),
    (58, "Computer", "💻", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-58.mp3", "https://basicenglishspeaking.com/computer/", [
        {"q": "Do you have your own computer?", "a": "Yes, I own a personal laptop which is essential for my daily work and study."},
        {"q": "What do you usually use your computer for?", "a": "I use it for programming, writing documents, researching information online, and occasionally listening to music."},
        {"q": "How much time do you spend on the computer each day?", "a": "On average, I spend around 6 to 8 hours daily since my career involves software engineering."}
    ]),
    (5, "Website", "🌐", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-05.mp3", "https://basicenglishspeaking.com/website/", [
        {"q": "What is your favorite website?", "a": "My favorite website is GitHub because it allows developers worldwide to share and collaborate on open-source code."},
        {"q": "How often do you visit it?", "a": "I visit it daily to review pull requests, read technical documentation, and track project issues."},
        {"q": "What are the main benefits of this website?", "a": "It fosters seamless collaboration, version control, and continuous integration for engineering teams."}
    ]),
    (6, "Accident", "🚗", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-06.mp3", "https://basicenglishspeaking.com/accident/", [
        {"q": "Have you ever been in any traffic accidents?", "a": "Fortunately, I have never experienced a serious accident, only minor traffic delays."},
        {"q": "What should people do to prevent traffic accidents?", "a": "Drivers should strictly obey speed limits, maintain safe following distances, and avoid mobile phone distractions."},
        {"q": "What is the emergency number in your country?", "a": "The emergency services can be reached immediately by dialing 115 for medical help or 113 for police assistance."}
    ]),
    (7, "Childhood Memory", "🧸", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-07.mp3", "https://basicenglishspeaking.com/childhood-memory/", [
        {"q": "What is your fondest childhood memory?", "a": "My fondest memory is spending summer vacations in the countryside with my grandparents, exploring nature and riding bicycles."},
        {"q": "Did you have a favorite toy as a child?", "a": "Yes, I had a set of building blocks that sparked my early curiosity about construction and engineering."},
        {"q": "How has your hometown changed since your childhood?", "a": "It has developed rapidly with new modern infrastructure, wider roads, and green parks."}
    ]),
    (8, "Favorite Season", "🍁", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-08.mp3", "https://basicenglishspeaking.com/favorite-season/", [
        {"q": "What is your favorite season of the year?", "a": "My favorite season is autumn because the weather is pleasantly cool and the sky is clear."},
        {"q": "What do you like to do during this season?", "a": "I enjoy outdoor hiking, photography, and enjoying warm coffee in quiet street cafes."},
        {"q": "How does the weather change in autumn?", "a": "The temperature drops comfortably, humidity decreases, and tree foliage turns golden."}
    ]),
    (9, "Friend", "🤝", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-09.mp3", "https://basicenglishspeaking.com/friend/", [
        {"q": "Who is your best friend?", "a": "My best friend is Minh, whom I have known since our university days."},
        {"q": "What qualities do you value most in a friend?", "a": "I deeply value honesty, mutual respect, and the willingness to support each other through challenges."},
        {"q": "How often do you meet your close friends?", "a": "We try to gather at least once every couple of weeks for dinner or coffee despite our busy work schedules."}
    ]),
    (10, "Hotel", "🏨", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-10.mp3", "https://basicenglishspeaking.com/hotel/", [
        {"q": "What kind of hotel do you usually stay in when traveling?", "a": "I typically book modern boutique hotels that offer reliable high-speed Wi-Fi and comfortable workspaces."},
        {"q": "What amenities do you check first before booking?", "a": "I always check guest reviews, room cleanliness, location accessibility, and workspace ergonomic setup."},
        {"q": "Have you ever stayed in a luxury five-star hotel?", "a": "Yes, during our annual company retreat, which was a memorable experience with excellent hospitality."}
    ]),
    (11, "Hobby", "🎨", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-11.mp3", "https://basicenglishspeaking.com/hobby/", [
        {"q": "What are your main hobbies?", "a": "My hobbies include reading technical literature, listening to podcasts, and practicing digital illustration."},
        {"q": "When did you start pursuing this hobby?", "a": "I started digital drawing about two years ago as a creative outlet to balance intensive coding work."},
        {"q": "Why is having a hobby important in modern life?", "a": "It relieves mental stress, nurtures creativity, and fosters healthy work-life balance."}
    ]),
    (12, "Music", "🎵", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-12.mp3", "https://basicenglishspeaking.com/music/", [
        {"q": "What genre of music do you listen to most?", "a": "I frequently listen to instrumental lo-fi and ambient electronic music while working or studying."},
        {"q": "Can you play any musical instruments?", "a": "I can play basic acoustic guitar, which helps me unwind on weekend evenings."},
        {"q": "Do you prefer live concerts or listening through headphones?", "a": "I appreciate high-fidelity headphones for focused listening, but live concerts offer unmatched energy and acoustic richness."}
    ]),
    (13, "Shopping", "🛍️", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-13.mp3", "https://basicenglishspeaking.com/shopping/", [
        {"q": "Do you prefer online shopping or in-store shopping?", "a": "I prefer online shopping for electronics and books due to price comparison and convenience, but visit stores for clothing."},
        {"q": "What was the latest item you purchased online?", "a": "I recently purchased an ergonomic mechanical keyboard to improve typing comfort during programming."},
        {"q": "How do you budget your monthly shopping expenses?", "a": "I allocate a fixed percentage of my income to savings first and keep discretionary purchases within strict limits."}
    ]),
    (14, "Exercise & Sports", "🏋️", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-14.mp3", "https://basicenglishspeaking.com/sports/", [
        {"q": "How often do you exercise each week?", "a": "I aim to exercise four times a week, combining cardiovascular running with resistance training."},
        {"q": "What are the health benefits of regular exercise?", "a": "It enhances stamina, boosts cardiovascular health, and significantly sharpens daily mental concentration."},
        {"q": "Do you prefer working out alone or in a group class?", "a": "I prefer individual workouts because they allow me to tailor training intensity and focus at my own pace."}
    ]),
    (15, "Food & Cooking", "🍲", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-15.mp3", "https://basicenglishspeaking.com/food/", [
        {"q": "What is your favorite traditional dish?", "a": "My favorite traditional food is Vietnamese Pho because of its aromatic broth, fresh herbs, and wholesome ingredients."},
        {"q": "Do you enjoy cooking at home?", "a": "Yes, cooking nutritious meals on weekends is both a relaxing ritual and a great way to eat healthily."},
        {"q": "What cooking skill would you like to master next?", "a": "I would love to learn the art of sourdough bread baking and authentic pastry making."}
    ]),
    (16, "Job & Career", "💼", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-16.mp3", "https://basicenglishspeaking.com/job-career/", [
        {"q": "What is your current profession?", "a": "I work as a software engineer specializing in building performant desktop and distributed applications."},
        {"q": "What aspect of your job do you find most fulfilling?", "a": "I find immense satisfaction in solving complex architectural challenges and seeing users benefit from reliable tools."},
        {"q": "Where do you see yourself professionally in five years?", "a": "I aspire to grow into a senior technical lead role, driving high-impact engineering initiatives and mentoring junior peers."}
    ]),
    (17, "Language Learning", "🌍", "https://basicenglishspeaking.com/wp-content/uploads/audio/QA/QA-17.mp3", "https://basicenglishspeaking.com/languages/", [
        {"q": "How many languages can you speak?", "a": "I speak Vietnamese natively and English with professional fluency, and I am currently exploring basic Japanese."},
        {"q": "What is the most effective way to improve English speaking?", "a": "Consistent daily immersion, shadowing native audio recordings, and speaking without fear of minor mistakes."},
        {"q": "Why is mastering English essential for engineers?", "a": "It unlocks global documentation, open-source communities, cutting-edge research, and international career opportunities."}
    ])
]

for t in LISTENING_DATA:
    topic_id, title, icon, audio_url, web_url, qa_list = t
    cursor.execute("""
        INSERT OR REPLACE INTO listening_topics (topic_id, title, icon, audio_url, web_url, qa_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (topic_id, title, icon, audio_url, web_url, json.dumps(qa_list)))

conn.commit()
print("🎉 Phase 2 content expansion executed successfully!")

# Summary counts
for table in ["idioms", "quizzes", "dictations", "writing_prompts", "listening_topics"]:
    cursor.execute(f"SELECT count(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  • {table}: {count} rows")

conn.close()
