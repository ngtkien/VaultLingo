#!/usr/bin/env python3
"""
Seed 60+ high quality Grammar & Question Drills for VaultLingo:
- Question Formations (QUASM standard)
- 12 Verb Tenses (Present, Past, Future, Perfect, Continuous)
- Modal Questions, Polite Indirect Questions, and Tag Questions
- Interactive word scramble tokens and in-depth grammar tips
"""

import sqlite3
import os
import json

DB_PATHS = [
    os.path.expanduser("~/.local/share/VaultLingo/vocab.db"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend/data/vocab.db")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/vocab.db")),
]

GRAMMAR_DRILLS = [
    # 🌟 1. Present Simple (6 drills)
    (
        "question_form", "Present Simple", "⚡", "A2",
        "She studies English grammar for thirty minutes every morning.",
        "Cô ấy học ngữ pháp tiếng Anh ba mươi phút mỗi sáng.",
        "Đặt câu hỏi với 'How often...?' để hỏi về tần suất.",
        "How often does she study English grammar?",
        "Cô ấy học ngữ pháp tiếng Anh thường xuyên như thế nào?",
        "Qu: How often | Aux: does | Subj: she | Verb: study",
        "Thì Hiện Tại Đơn (Hỏi tần suất): How often + do/does + S + V-inf? (Lưu ý: Chủ ngữ 'she' dùng trợ động từ 'does', động từ 'study' về nguyên thể).",
        json.dumps(["How", "often", "does", "she", "study", "English", "grammar", "?"])
    ),
    (
        "question_form", "Present Simple", "⚡", "A2",
        "Software engineers use version control systems like Git daily.",
        "Các kỹ sư phần mềm sử dụng hệ thống quản lý phiên bản như Git hàng ngày.",
        "Đặt câu hỏi với 'What...?' để hỏi về công cụ kỹ sư sử dụng.",
        "What do software engineers use daily?",
        "Các kỹ sư phần mềm sử dụng cái gì hàng ngày?",
        "Qu: What | Aux: do | Subj: software engineers | Verb: use",
        "Thì Hiện Tại Đơn: Wh- + do/does + S + V-inf? (Chủ ngữ số nhiều 'software engineers' đi với trợ động từ 'do').",
        json.dumps(["What", "do", "software", "engineers", "use", "daily", "?"])
    ),
    (
        "question_form", "Present Simple", "⚡", "B1",
        "This modern coffee machine costs two hundred dollars.",
        "Chiếc máy pha cà phê hiện đại này có giá hai trăm đô la.",
        "Đặt câu hỏi với 'How much...?' để hỏi về giá tiền.",
        "How much does this coffee machine cost?",
        "Chiếc máy pha cà phê này có giá bao nhiêu?",
        "Qu: How much | Aux: does | Subj: this coffee machine | Verb: cost",
        "Hỏi giá tiền: How much + do/does + S + cost? (Chủ ngữ 'this coffee machine' số ít -> dùng 'does').",
        json.dumps(["How", "much", "does", "this", "coffee", "machine", "cost", "?"])
    ),
    (
        "question_form", "Present Simple", "⚡", "A2",
        "The express train to the capital leaves at eight sharp.",
        "Chuyến tàu nhanh đến thủ đô khởi hành lúc tám giờ đúng.",
        "Đặt câu hỏi với 'What time...?' để hỏi về giờ tàu chạy theo lịch trình.",
        "What time does the express train leave?",
        "Chuyến tàu nhanh khởi hành lúc mấy giờ?",
        "Qu: What time | Aux: does | Subj: the express train | Verb: leave",
        "Hiện tại đơn diễn tả lịch trình cố định (Timetable): What time + does + S + leave?",
        json.dumps(["What", "time", "does", "the", "express", "train", "leave", "?"])
    ),
    (
        "question_form", "Present Simple", "⚡", "B1",
        "You usually prefer working remotely from home on Fridays.",
        "Bạn thường thích làm việc từ xa tại nhà vào các ngày thứ Sáu.",
        "Đặt câu hỏi Yes/No với 'Do you...?'",
        "Do you usually prefer working remotely on Fridays?",
        "Bạn có thường thích làm việc từ xa vào thứ Sáu không?",
        "Aux: Do | Subj: you | Adv: usually | Verb: prefer",
        "Câu hỏi Yes/No Hiện tại đơn: Do/Does + S + (Trạng từ tần suất) + V-inf?",
        json.dumps(["Do", "you", "usually", "prefer", "working", "remotely", "on", "Fridays", "?"])
    ),
    (
        "question_form", "Present Simple", "⚡", "B1",
        "He lives in downtown Melbourne near the university campus.",
        "Anh ấy sống ở trung tâm thành phố Melbourne gần khuôn viên trường đại học.",
        "Đặt câu hỏi với 'Where...?'",
        "Where does he live in Melbourne?",
        "Anh ấy sống ở đâu tại Melbourne?",
        "Qu: Where | Aux: does | Subj: he | Verb: live",
        "Công thức QUASM: Where (Qu) + does (Aux) + he (Subj) + live (Verb)?",
        json.dumps(["Where", "does", "he", "live", "in", "Melbourne", "?"])
    ),

    # ⏳ 2. Present Continuous (5 drills)
    (
        "question_form", "Present Continuous", "🔄", "A2",
        "The development team is preparing the new feature release right now.",
        "Đội ngũ phát triển đang chuẩn bị bản phát hành tính năng mới ngay lúc này.",
        "Đặt câu hỏi với 'What...?' về hành động đang diễn ra.",
        "What is the development team preparing right now?",
        "Đội ngũ phát triển đang chuẩn bị điều gì ngay lúc này?",
        "Qu: What | Aux: is | Subj: the development team | Verb: preparing",
        "Hiện tại tiếp diễn: Wh- + am/is/are + S + V-ing? (Dùng diễn tả hành động đang diễn ra tại thời điểm nói).",
        json.dumps(["What", "is", "the", "development", "team", "preparing", "right", "now", "?"])
    ),
    (
        "question_form", "Present Continuous", "🔄", "B1",
        "We are meeting with our international partners tomorrow afternoon.",
        "Chúng tôi sẽ họp với các đối tác quốc tế vào chiều mai.",
        "Đặt câu hỏi với 'When...?' về kế hoạch tương lai đã sắp xếp sẵn.",
        "When are you meeting with your international partners?",
        "Khi nào bạn sẽ họp với các đối tác quốc tế?",
        "Qu: When | Aux: are | Subj: you | Verb: meeting",
        "Hiện tại tiếp diễn chỉ kế hoạch tương lai chắc chắn (Fixed arrangement): When + are + you + V-ing?",
        json.dumps(["When", "are", "you", "meeting", "with", "your", "international", "partners", "?"])
    ),
    (
        "question_form", "Present Continuous", "🔄", "A2",
        "She is currently taking an intensive IELTS preparation course.",
        "Cô ấy hiện đang tham gia một khóa học luyện thi IELTS cấp tốc.",
        "Đặt câu hỏi với 'What kind of course...?'",
        "What kind of course is she currently taking?",
        "Cô ấy hiện đang theo học loại khóa học nào?",
        "Qu: What kind of course | Aux: is | Subj: she | Verb: taking",
        "Từ để hỏi ghép cụm danh từ: [What kind of + Noun] + is/are + S + V-ing?",
        json.dumps(["What", "kind", "of", "course", "is", "she", "currently", "taking", "?"])
    ),
    (
        "question_form", "Present Continuous", "🔄", "B1",
        "The company's server CPU usage is increasing rapidly.",
        "Mức sử dụng CPU máy chủ của công ty đang tăng lên nhanh chóng.",
        "Đặt câu hỏi với 'Why...?'",
        "Why is the server CPU usage increasing rapidly?",
        "Tại sao mức sử dụng CPU của máy chủ lại đang tăng nhanh chóng?",
        "Qu: Why | Aux: is | Subj: the server CPU usage | Verb: increasing",
        "Hiện tại tiếp diễn diễn tả xu hướng đang thay đổi: Why + is + S + increasing?",
        json.dumps(["Why", "is", "the", "server", "CPU", "usage", "increasing", "rapidly", "?"])
    ),
    (
        "question_form", "Present Continuous", "🔄", "A2",
        "They are testing the mobile application on multiple devices.",
        "Họ đang thử nghiệm ứng dụng di động trên nhiều thiết bị.",
        "Đặt câu hỏi Yes/No với 'Are they...?'",
        "Are they testing the mobile application on multiple devices?",
        "Họ có đang thử nghiệm ứng dụng di động trên nhiều thiết bị không?",
        "Aux: Are | Subj: they | Verb: testing",
        "Câu hỏi Yes/No Tiếp diễn: Am/Is/Are + S + V-ing?",
        json.dumps(["Are", "they", "testing", "the", "mobile", "application", "on", "multiple", "devices", "?"])
    ),

    # 📜 3. Past Simple (6 drills)
    (
        "question_form", "Past Simple", "📜", "A2",
        "I graduated from university three years ago.",
        "Tôi đã tốt nghiệp đại học ba năm trước.",
        "Đặt câu hỏi với 'When...?' để hỏi mốc thời gian trong quá khứ.",
        "When did you graduate from university?",
        "Bạn đã tốt nghiệp đại học khi nào?",
        "Qu: When | Aux: did | Subj: you | Verb: graduate",
        "Quá khứ đơn: When + did + S + V-inf? (Lưu ý: Đã có trợ động từ 'did' thì động từ chính 'graduate' trở về nguyên mẫu, không thêm -ed).",
        json.dumps(["When", "did", "you", "graduate", "from", "university", "?"])
    ),
    (
        "question_form", "Past Simple", "📜", "B1",
        "Our team solved the critical production outage by restarting the database replica.",
        "Nhóm chúng tôi đã xử lý sự cố ngừng hoạt động bằng cách khởi động lại bản sao cơ sở dữ liệu.",
        "Đặt câu hỏi với 'How...?' về cách thức giải quyết.",
        "How did your team solve the production outage?",
        "Nhóm của bạn đã giải quyết sự cố như thế nào?",
        "Qu: How | Aux: did | Subj: your team | Verb: solve",
        "Công thức QUASM: How (Qu) + did (Aux) + your team (Subj) + solve (Verb)?",
        json.dumps(["How", "did", "your", "team", "solve", "the", "production", "outage", "?"])
    ),
    (
        "question_form", "Past Simple", "📜", "A2",
        "The conference keynote was delayed due to technical difficulties.",
        "Bài phát biểu chính của hội nghị đã bị hoãn do sự cố kỹ thuật.",
        "Đặt câu hỏi với 'Why was...?'",
        "Why was the conference keynote delayed?",
        "Tại sao bài phát biểu chính của hội nghị lại bị hoãn?",
        "Qu: Why | Aux: was | Subj: the conference keynote | Verb: delayed",
        "Quá khứ đơn với Động từ To Be / Thể bị động: Why + was/were + S + V3/ed?",
        json.dumps(["Why", "was", "the", "conference", "keynote", "delayed", "?"])
    ),
    (
        "question_form", "Past Simple", "📜", "B1",
        "She spent two weeks in Tokyo attending an international tech summit.",
        "Cô ấy đã dành hai tuần ở Tokyo để tham dự một hội nghị thượng đỉnh công nghệ quốc tế.",
        "Đặt câu hỏi với 'How long...?'",
        "How long did she spend in Tokyo?",
        "Cô ấy đã ở Tokyo trong bao lâu?",
        "Qu: How long | Aux: did | Subj: she | Verb: spend",
        "Hỏi về khoảng thời gian trong quá khứ đã kết thúc hoàn toàn: How long + did + S + spend?",
        json.dumps(["How", "long", "did", "she", "spend", "in", "Tokyo", "?"])
    ),
    (
        "question_form", "Past Simple", "📜", "A2",
        "You received the contract signed by both executives yesterday.",
        "Bạn đã nhận được hợp đồng có chữ ký của cả hai giám đốc điều hành vào hôm qua.",
        "Đặt câu hỏi Yes/No với 'Did you...?'",
        "Did you receive the signed contract yesterday?",
        "Bạn đã nhận được hợp đồng đã ký vào hôm qua chưa?",
        "Aux: Did | Subj: you | Verb: receive",
        "Câu hỏi Yes/No Quá khứ đơn: Did + S + V-inf? (Động từ 'receive' ở dạng nguyên mẫu).",
        json.dumps(["Did", "you", "receive", "the", "signed", "contract", "yesterday", "?"])
    ),
    (
        "question_form", "Past Simple", "📜", "B1",
        "They decided to adopt TypeScript to catch bugs early in development.",
        "Họ đã quyết định áp dụng TypeScript để phát hiện lỗi sớm trong quá trình phát triển.",
        "Đặt câu hỏi với 'Why did they...?'",
        "Why did they decide to adopt TypeScript?",
        "Tại sao họ lại quyết định áp dụng TypeScript?",
        "Qu: Why | Aux: did | Subj: they | Verb: decide",
        "Hỏi lý do hành động trong quá khứ: Why + did + S + decide + to V?",
        json.dumps(["Why", "did", "they", "decide", "to", "adopt", "TypeScript", "?"])
    ),

    # ✨ 4. Present Perfect (7 drills - Core IELTS / Workplace)
    (
        "question_form", "Present Perfect", "✨", "B1",
        "I have worked as a software developer for over five years.",
        "Tôi đã làm việc như một lập trình viên phần mềm trong hơn năm năm.",
        "Đặt câu hỏi với 'How long...?' để hỏi về thời gian kéo dài đến nay.",
        "How long have you worked as a software developer?",
        "Bạn đã làm việc như một lập trình viên phần mềm trong bao lâu rồi?",
        "Qu: How long | Aux: have | Subj: you | Verb: worked",
        "Hiện tại hoàn thành (Kéo dài từ quá khứ đến hiện tại): How long + have/has + S + V3/ed?",
        json.dumps(["How", "long", "have", "you", "worked", "as", "a", "software", "developer", "?"])
    ),
    (
        "question_form", "Present Perfect", "✨", "A2",
        "She has already visited five European countries this year.",
        "Cô ấy đã đến thăm năm quốc gia châu Âu trong năm nay.",
        "Đặt câu hỏi với 'How many countries...?'",
        "How many countries has she visited this year?",
        "Cô ấy đã đến thăm bao nhiêu quốc gia trong năm nay?",
        "Qu: How many countries | Aux: has | Subj: she | Verb: visited",
        "Hỏi về số lượng trải nghiệm: How many + Noun + have/has + S + V3/ed? (Chủ ngữ 'she' đi với 'has').",
        json.dumps(["How", "many", "countries", "has", "she", "visited", "this", "year", "?"])
    ),
    (
        "question_form", "Present Perfect", "✨", "B1",
        "You have ever traveled solo to an English-speaking country.",
        "Bạn đã từng đi du lịch một mình đến một quốc gia nói tiếng Anh.",
        "Đặt câu hỏi trải nghiệm với 'Have you ever...?'",
        "Have you ever traveled solo to an English-speaking country?",
        "Bạn đã bao giờ đi du lịch một mình tới một quốc gia nói tiếng Anh chưa?",
        "Aux: Have | Subj: you | Adv: ever | Verb: traveled",
        "Hỏi về trải nghiệm cuộc đời (Ever): Have/Has + S + ever + V3/ed?",
        json.dumps(["Have", "you", "ever", "traveled", "solo", "to", "an", "English-speaking", "country", "?"])
    ),
    (
        "question_form", "Present Perfect", "✨", "B1",
        "The company has recently adopted automated CI/CD deployment pipelines.",
        "Công ty gần đây đã áp dụng quy trình triển khai CI/CD tự động.",
        "Đặt câu hỏi với 'What technology...?'",
        "What technology has the company recently adopted?",
        "Công ty gần đây đã áp dụng công nghệ gì?",
        "Qu: What technology | Aux: has | Subj: the company | Verb: adopted",
        "Hiện tại hoàn thành diễn tả hành động vừa mới xảy ra (Recently/Lately): What + has + S + V3/ed?",
        json.dumps(["What", "technology", "has", "the", "company", "recently", "adopted", "?"])
    ),
    (
        "question_form", "Present Perfect", "✨", "B1",
        "They have finished the quarterly financial report.",
        "Họ đã hoàn thành bản báo cáo tài chính quý.",
        "Đặt câu hỏi Yes/No với 'Have they... yet?'",
        "Have they finished the quarterly financial report yet?",
        "Họ đã hoàn thành báo cáo tài chính quý chưa?",
        "Aux: Have | Subj: they | Verb: finished | Adv: yet",
        "Câu hỏi với 'Yet' (Đã làm việc gì đó chưa): Have/Has + S + V3/ed + ... + yet?",
        json.dumps(["Have", "they", "finished", "the", "quarterly", "financial", "report", "yet", "?"])
    ),
    (
        "question_form", "Present Perfect", "✨", "B2",
        "Our engineering team has achieved significant performance optimization milestones.",
        "Đội ngũ kỹ thuật của chúng tôi đã đạt được những cột mốc tối ưu hóa hiệu suất đáng kể.",
        "Đặt câu hỏi với 'What milestones...?'",
        "What milestones has your engineering team achieved?",
        "Đội ngũ kỹ thuật của bạn đã đạt được những cột mốc nào?",
        "Qu: What milestones | Aux: has | Subj: your engineering team | Verb: achieved",
        "Nhấn mạnh thành quả đạt được (Milestones): [What + Noun] + have/has + S + achieved?",
        json.dumps(["What", "milestones", "has", "your", "engineering", "team", "achieved", "?"])
    ),
    (
        "question_form", "Present Perfect", "✨", "B2",
        "The security team has patched three zero-day vulnerabilities this week.",
        "Đội ngũ bảo mật đã vá ba lỗ hổng zero-day trong tuần này.",
        "Đặt câu hỏi với 'How many vulnerabilities...?'",
        "How many vulnerabilities has the security team patched?",
        "Đội ngũ bảo mật đã vá bao nhiêu lỗ hổng?",
        "Qu: How many vulnerabilities | Aux: has | Subj: the security team | Verb: patched",
        "Khoảng thời gian chưa kết thúc (This week): How many + Noun + has + S + patched?",
        json.dumps(["How", "many", "vulnerabilities", "has", "the", "security", "team", "patched", "?"])
    ),

    # ⏳ 5. Present Perfect Continuous (4 drills)
    (
        "question_form", "Present Perfect Continuous", "⏳", "B2",
        "He has been debugging this memory leak issue since this morning.",
        "Anh ấy đã liên tục gỡ lỗi rò rỉ bộ nhớ này từ sáng đến giờ.",
        "Đặt câu hỏi với 'How long has he...?' để nhấn mạnh tính liên tục.",
        "How long has he been debugging this memory leak?",
        "Anh ấy đã liên tục gỡ lỗi rò rỉ bộ nhớ này trong bao lâu rồi?",
        "Qu: How long | Aux: has | Subj: he | Aux2: been | Verb: debugging",
        "Hiện tại hoàn thành tiếp diễn: How long + have/has + S + been + V-ing? (Nhấn mạnh hành động diễn ra liên tục không ngắt quãng).",
        json.dumps(["How", "long", "has", "he", "been", "debugging", "this", "memory", "leak", "?"])
    ),
    (
        "question_form", "Present Perfect Continuous", "⏳", "B1",
        "You have been studying for the IELTS exam for six months.",
        "Bạn đã ôn thi IELTS liên tục trong sáu tháng qua.",
        "Đặt câu hỏi với 'How long have you been...?'",
        "How long have you been studying for the IELTS exam?",
        "Bạn đã ôn thi IELTS trong bao lâu rồi?",
        "Qu: How long | Aux: have | Subj: you | Aux2: been | Verb: studying",
        "Hỏi về quá trình ôn tập liên tục: How long + have you been + V-ing?",
        json.dumps(["How", "long", "have", "you", "been", "studying", "for", "the", "IELTS", "exam", "?"])
    ),
    (
        "question_form", "Present Perfect Continuous", "⏳", "B2",
        "The scientists have been conducting research on renewable solar cells all year.",
        "Các nhà khoa học đã tiến hành nghiên cứu về pin mặt trời tái tạo suốt cả năm qua.",
        "Đặt câu hỏi với 'What kind of research have they...?'",
        "What kind of research have they been conducting all year?",
        "Họ đã tiến hành loại nghiên cứu nào suốt cả năm qua?",
        "Qu: What kind of research | Aux: have | Subj: they | Aux2: been | Verb: conducting",
        "Cấu trúc: [What kind of research] + have/has + S + been + V-ing?",
        json.dumps(["What", "kind", "of", "research", "have", "they", "been", "conducting", "all", "year", "?"])
    ),
    (
        "question_form", "Present Perfect Continuous", "⏳", "B1",
        "It has been raining heavily for three consecutive hours.",
        "Trời đã mưa lớn liên tục suốt ba tiếng đồng hồ.",
        "Đặt câu hỏi với 'How long has it been...?'",
        "How long has it been raining heavily?",
        "Trời đã mưa lớn trong bao lâu rồi?",
        "Qu: How long | Aux: has | Subj: it | Aux2: been | Verb: raining",
        "Chủ ngữ giả 'It': How long + has + it + been + raining?",
        json.dumps(["How", "long", "has", "it", "been", "raining", "heavily", "?"])
    ),

    # ⏱️ 6. Past Continuous (4 drills)
    (
        "question_form", "Past Continuous", "⏱️", "B1",
        "I was writing unit tests when the fire alarm suddenly rang.",
        "Tôi đang viết các bài kiểm thử đơn vị thì chuông báo cháy bất ngờ reo.",
        "Đặt câu hỏi với 'What were you doing when...?'",
        "What were you doing when the fire alarm rang?",
        "Bạn đang làm gì khi chuông báo cháy reo?",
        "Qu: What | Aux: were | Subj: you | Verb: doing",
        "Quá khứ tiếp diễn kết hợp Quá khứ đơn (Hành động đang xảy ra thì có hành động khác xen vào): What + were + you + doing + when + S + V-past?",
        json.dumps(["What", "were", "you", "doing", "when", "the", "fire", "alarm", "rang", "?"])
    ),
    (
        "question_form", "Past Continuous", "⏱️", "B1",
        "She was presenting the quarterly roadmap yesterday at 3 PM.",
        "Cô ấy đang thuyết trình về lộ trình quý vào lúc 3 giờ chiều hôm qua.",
        "Đặt câu hỏi với 'What was she doing yesterday at 3 PM?'",
        "What was she doing yesterday at three PM?",
        "Cô ấy đang làm gì vào lúc ba giờ chiều hôm qua?",
        "Qu: What | Aux: was | Subj: she | Verb: doing",
        "Hành động đang diễn ra tại một thời điểm chính xác trong quá khứ: What + was/were + S + doing + at [mốc giờ]?",
        json.dumps(["What", "was", "she", "doing", "yesterday", "at", "three", "PM", "?"])
    ),
    (
        "question_form", "Past Continuous", "⏱️", "A2",
        "They were discussing the budget during the entire morning meeting.",
        "Họ đã bàn bạc về ngân sách trong suốt toàn bộ cuộc họp buổi sáng.",
        "Đặt câu hỏi với 'What were they discussing...?'",
        "What were they discussing during the morning meeting?",
        "Họ đang bàn bạc về điều gì trong cuộc họp buổi sáng?",
        "Qu: What | Aux: were | Subj: they | Verb: discussing",
        "Cấu trúc: What + were + they + discussing?",
        json.dumps(["What", "were", "they", "discussing", "during", "the", "morning", "meeting", "?"])
    ),
    (
        "question_form", "Past Continuous", "⏱️", "B1",
        "You were living in London when you decided to change your career.",
        "Bạn đang sống ở Luân Đôn khi bạn quyết định chuyển đổi nghề nghiệp.",
        "Đặt câu hỏi với 'Where were you living when...?'",
        "Where were you living when you changed your career?",
        "Bạn đang sống ở đâu khi bạn chuyển đổi nghề nghiệp?",
        "Qu: Where | Aux: were | Subj: you | Verb: living",
        "Cấu trúc: Where + were + you + living + when + S + V-past?",
        json.dumps(["Where", "were", "you", "living", "when", "you", "changed", "your", "career", "?"])
    ),

    # 🚀 7. Future: Will vs Be Going To (5 drills)
    (
        "question_form", "Future Forms", "🚀", "A2",
        "I am going to visit my grandparents this upcoming weekend.",
        "Tôi dự định sẽ đi thăm ông bà vào cuối tuần tới này.",
        "Đặt câu hỏi với 'What are you going to do...?' để hỏi dự định.",
        "What are you going to do this upcoming weekend?",
        "Bạn dự định sẽ làm gì vào cuối tuần tới này?",
        "Qu: What | Aux: are | Subj: you | Aux2: going to | Verb: do",
        "Tương lai gần (Kế hoạch/Dự định từ trước - Be going to): What + are/is + S + going to + V-inf?",
        json.dumps(["What", "are", "you", "going", "to", "do", "this", "upcoming", "weekend", "?"])
    ),
    (
        "question_form", "Future Forms", "🚀", "B1",
        "Artificial intelligence will transform software engineering workflows dramatically.",
        "Trí tuệ nhân tạo sẽ biến đổi các quy trình kỹ thuật phần mềm một cách mạnh mẽ.",
        "Đặt câu hỏi với 'How will AI transform...?' để hỏi dự đoán tương lai.",
        "How will AI transform software engineering workflows?",
        "Trí tuệ nhân tạo sẽ biến đổi quy trình kỹ thuật phần mềm như thế nào?",
        "Qu: How | Aux: will | Subj: AI | Verb: transform",
        "Tương lai đơn (Dự đoán tương lai - Will): How + will + S + V-inf?",
        json.dumps(["How", "will", "AI", "transform", "software", "engineering", "workflows", "?"])
    ),
    (
        "question_form", "Future Forms", "🚀", "B1",
        "The company is going to launch the beta version next month.",
        "Công ty dự định sẽ ra mắt phiên bản thử nghiệm vào tháng tới.",
        "Đặt câu hỏi với 'When is the company going to...?'",
        "When is the company going to launch the beta version?",
        "Khi nào công ty dự định sẽ ra mắt phiên bản thử nghiệm?",
        "Qu: When | Aux: is | Subj: the company | Aux2: going to | Verb: launch",
        "Dự định của tổ chức/công ty: When + is/are + S + going to + V-inf?",
        json.dumps(["When", "is", "the", "company", "going", "to", "launch", "the", "beta", "version", "?"])
    ),
    (
        "question_form", "Future Forms", "🚀", "A2",
        "You will attend the product launch ceremony tomorrow.",
        "Bạn sẽ tham dự lễ ra mắt sản phẩm vào ngày mai.",
        "Đặt câu hỏi Yes/No với 'Will you...?'",
        "Will you attend the product launch ceremony tomorrow?",
        "Bạn sẽ tham dự lễ ra mắt sản phẩm vào ngày mai chứ?",
        "Aux: Will | Subj: you | Verb: attend",
        "Câu hỏi Yes/No Tương lai đơn: Will + S + V-inf?",
        json.dumps(["Will", "you", "attend", "the", "product", "launch", "ceremony", "tomorrow", "?"])
    ),
    (
        "question_form", "Future Forms", "🚀", "B2",
        "Renewable energy will account for over fifty percent of global electricity by 2035.",
        "Năng lượng tái tạo sẽ chiếm hơn năm mươi phần trăm lượng điện toàn cầu vào năm 2035.",
        "Đặt câu hỏi với 'What percentage of electricity will renewable energy account for?'",
        "What percentage of electricity will renewable energy account for?",
        "Năng lượng tái tạo sẽ chiếm bao nhiêu phần trăm lượng điện?",
        "Qu: What percentage of electricity | Aux: will | Subj: renewable energy | Verb: account for",
        "Cấu trúc: [What percentage of + Noun] + will + S + account for?",
        json.dumps(["What", "percentage", "of", "electricity", "will", "renewable", "energy", "account", "for", "?"])
    ),

    # 🤝 8. Polite Indirect Questions (6 drills - Essential for Professional & Daily Life)
    (
        "indirect", "Indirect Questions", "🤝", "B1",
        "Where is the nearest subway transit station?",
        "Ga tàu điện ngầm gần nhất ở đâu?",
        "Chuyển sang câu hỏi gián tiếp lịch sự bắt đầu bằng 'Could you tell me...?'",
        "Could you tell me where the nearest subway station is?",
        "Bạn có thể cho tôi biết ga tàu điện ngầm gần nhất ở đâu không?",
        "Intro: Could you tell me | Qu: where | Subj: the nearest subway station | Verb: is",
        "Quy tắc vàng Câu hỏi gián tiếp (Indirect Question): Không đảo trợ động từ, trật tự từ trở về dạng khẳng định (Wh- + S + V). 'where is the station' -> 'where the station is'.",
        json.dumps(["Could", "you", "tell", "me", "where", "the", "nearest", "subway", "station", "is", "?"])
    ),
    (
        "indirect", "Indirect Questions", "🤝", "B1",
        "What time does the morning meeting start?",
        "Cuộc họp buổi sáng bắt đầu lúc mấy giờ?",
        "Chuyển sang câu hỏi lịch sự với 'Do you know what time...?'",
        "Do you know what time the morning meeting starts?",
        "Bạn có biết cuộc họp buổi sáng bắt đầu lúc mấy giờ không?",
        "Intro: Do you know | Qu: what time | Subj: the morning meeting | Verb: starts",
        "Lưu ý: Bỏ trợ động từ 'does', động từ chính 'start' chia theo chủ ngữ số ít -> 'starts'.",
        json.dumps(["Do", "you", "know", "what", "time", "the", "morning", "meeting", "starts", "?"])
    ),
    (
        "indirect", "Indirect Questions", "🤝", "B2",
        "Why was the software deployment postponed yesterday?",
        "Tại sao việc triển khai phần mềm lại bị hoãn vào hôm qua?",
        "Chuyển sang câu hỏi gián tiếp với 'Would you mind telling me why...?'",
        "Would you mind telling me why the software deployment was postponed?",
        "Bạn có phiền cho tôi biết tại sao việc triển khai phần mềm lại bị hoãn không?",
        "Intro: Would you mind telling me | Qu: why | Subj: the software deployment | Verb: was postponed",
        "Cấu trúc lịch sự cao cấp: Would you mind telling me + why + S + V?",
        json.dumps(["Would", "you", "mind", "telling", "me", "why", "the", "software", "deployment", "was", "postponed", "?"])
    ),
    (
        "indirect", "Indirect Questions", "🤝", "B1",
        "Is there a pharmacy nearby?",
        "Có hiệu thuốc nào ở gần đây không?",
        "Chuyển sang câu hỏi gián tiếp với 'Do you know if...?'",
        "Do you know if there is a pharmacy nearby?",
        "Bạn có biết liệu có hiệu thuốc nào ở gần đây không?",
        "Intro: Do you know | If/Whether | Subj: there | Verb: is a pharmacy nearby",
        "Câu hỏi Yes/No chuyển sang gián tiếp: Dùng 'if' hoặc 'whether' + S + V. 'is there' -> 'if there is'.",
        json.dumps(["Do", "you", "know", "if", "there", "is", "a", "pharmacy", "nearby", "?"])
    ),
    (
        "indirect", "Indirect Questions", "🤝", "B2",
        "How much does this cloud subscription package cost per year?",
        "Gói thuê bao đám mây này có giá bao nhiêu mỗi năm?",
        "Chuyển sang câu hỏi gián tiếp với 'Can you please explain how much...?'",
        "Can you please explain how much this cloud subscription costs?",
        "Bạn có thể vui lòng giải thích gói thuê bao đám mây này có giá bao nhiêu không?",
        "Intro: Can you please explain | Qu: how much | Subj: this cloud subscription | Verb: costs",
        "Bỏ trợ động từ 'does', động từ 'cost' thêm 's' theo chủ ngữ số ít: 'costs'.",
        json.dumps(["Can", "you", "please", "explain", "how", "much", "this", "cloud", "subscription", "costs", "?"])
    ),
    (
        "indirect", "Indirect Questions", "🤝", "B1",
        "Who is in charge of reviewing customer support tickets?",
        "Ai là người phụ trách việc xét duyệt các phiếu hỗ trợ khách hàng?",
        "Chuyển sang câu hỏi gián tiếp với 'Could you please let me know who...?'",
        "Could you please let me know who is in charge of support tickets?",
        "Bạn có thể vui lòng cho tôi biết ai là người phụ trách các phiếu hỗ trợ không?",
        "Intro: Could you please let me know | Qu: who | Verb: is in charge of...",
        "Khi 'Who' làm chủ ngữ, trật tự từ giữ nguyên: who + is in charge of...",
        json.dumps(["Could", "you", "please", "let", "me", "know", "who", "is", "in", "charge", "of", "support", "tickets", "?"])
    ),

    # 🏷️ 9. Tag Questions (Câu hỏi đuôi - 6 drills)
    (
        "tag_question", "Tag Questions", "🏷️", "B1",
        "You are coming to our team retrospective meeting tomorrow.",
        "Bạn sẽ đến cuộc họp hồi tưởng nhóm của chúng ta vào ngày mai.",
        "Thêm câu hỏi đuôi (Tag question) vào cuối câu.",
        "You are coming to the team meeting tomorrow, aren't you?",
        "Bạn sẽ đến cuộc họp nhóm vào ngày mai, có phải không?",
        "Statement (+): You are coming... | Tag (-): aren't you?",
        "Quy tắc câu hỏi đuôi: Mệnh đề khẳng định (+) đi với Đuôi phủ định (-). Trợ động từ 'are' -> 'aren't you?'.",
        json.dumps(["You", "are", "coming", "to", "the", "team", "meeting", "tomorrow", ",", "aren't", "you", "?"])
    ),
    (
        "tag_question", "Tag Questions", "🏷️", "B1",
        "She didn't receive the revised project proposal.",
        "Cô ấy đã không nhận được đề xuất dự án sửa đổi.",
        "Thêm câu hỏi đuôi (Tag question) vào cuối câu.",
        "She didn't receive the revised project proposal, did she?",
        "Cô ấy đã không nhận được đề xuất dự án sửa đổi, phải không?",
        "Statement (-): She didn't receive... | Tag (+): did she?",
        "Mệnh đề phủ định (-) đi với Đuôi khẳng định (+): didn't receive -> 'did she?'.",
        json.dumps(["She", "didn't", "receive", "the", "revised", "project", "proposal", ",", "did", "she", "?"])
    ),
    (
        "tag_question", "Tag Questions", "🏷️", "A2",
        "This coffee shop has free high-speed wifi.",
        "Quán cà phê này có wifi tốc độ cao miễn phí.",
        "Thêm câu hỏi đuôi với 'doesn't it?'",
        "This coffee shop has free high-speed wifi, doesn't it?",
        "Quán cà phê này có wifi tốc độ cao miễn phí, phải không?",
        "Statement (+): has (Hiện tại đơn) | Tag (-): doesn't it?",
        "Hiện tại đơn với động từ thường 'has' (chủ ngữ 'this coffee shop') -> Đuôi mượn trợ động từ 'doesn't it?'.",
        json.dumps(["This", "coffee", "shop", "has", "free", "high-speed", "wifi", ",", "doesn't", "it", "?"])
    ),
    (
        "tag_question", "Tag Questions", "🏷️", "B1",
        "They have already finalized the quarterly budget.",
        "Họ đã chốt xong ngân sách quý rồi.",
        "Thêm câu hỏi đuôi với 'haven't they?'",
        "They have already finalized the quarterly budget, haven't they?",
        "Họ đã chốt xong ngân sách quý rồi, phải không nào?",
        "Statement (+): have finalized | Tag (-): haven't they?",
        "Hiện tại hoàn thành: have finalized -> Đuôi 'haven't they?'.",
        json.dumps(["They", "have", "already", "finalized", "the", "quarterly", "budget", ",", "haven't", "they", "?"])
    ),
    (
        "tag_question", "Tag Questions", "🏷️", "B2",
        "We should double-check the database migration script before deployment.",
        "Chúng ta nên kiểm tra kỹ lại mã di chuyển dữ liệu trước khi triển khai.",
        "Thêm câu hỏi đuôi với 'shouldn't we?'",
        "We should double-check the migration script before deployment, shouldn't we?",
        "Chúng ta nên kiểm tra kỹ lại mã di chuyển trước khi triển khai, đúng không?",
        "Statement (+): should check | Tag (-): shouldn't we?",
        "Động từ khuyết thiếu (Modal verb): should -> Đuôi 'shouldn't we?'.",
        json.dumps(["We", "should", "double-check", "the", "migration", "script", "before", "deployment", ",", "shouldn't", "we", "?"])
    ),
    (
        "tag_question", "Tag Questions", "🏷️", "A2",
        "Let's grab a quick lunch together at the cafeteria.",
        "Chúng ta hãy cùng đi ăn trưa nhanh ở căng tin nhé.",
        "Thêm câu hỏi đuôi đề xuất với 'shall we?'",
        "Let's grab a quick lunch together at the cafeteria, shall we?",
        "Chúng ta cùng đi ăn trưa nhanh ở căng tin nhé, được không?",
        "Statement: Let's... | Tag: shall we?",
        "Trường hợp đặc biệt: Cấu trúc rủ rê/đề xuất bắt đầu bằng 'Let's...' luôn dùng câu hỏi đuôi là 'shall we?'.",
        json.dumps(["Let's", "grab", "a", "quick", "lunch", "together", "at", "the", "cafeteria", ",", "shall", "we", "?"])
    ),

    # 💡 10. Modal Verbs Questions (5 drills)
    (
        "question_form", "Modal Verbs", "💡", "B1",
        "We should prioritize fixing high-severity bugs first.",
        "Chúng ta nên ưu tiên sửa các lỗi có mức độ nghiêm trọng cao trước.",
        "Đặt câu hỏi với 'What should we prioritize...?'",
        "What should we prioritize fixing first?",
        "Chúng ta nên ưu tiên sửa cái gì trước?",
        "Qu: What | Aux: should | Subj: we | Verb: prioritize",
        "Câu hỏi với Modal Verb: Wh- + Modal (should/can/could/must) + S + V-inf?",
        json.dumps(["What", "should", "we", "prioritize", "fixing", "first", "?"])
    ),
    (
        "question_form", "Modal Verbs", "💡", "A2",
        "You can share your screen during the video call.",
        "Bạn có thể chia sẻ màn hình của mình trong cuộc gọi video.",
        "Đặt câu hỏi xin phép / khả năng với 'Can I...?'",
        "Can I share my screen during the video call?",
        "Tôi có thể chia sẻ màn hình trong cuộc gọi video được không?",
        "Aux: Can | Subj: I | Verb: share",
        "Hỏi xin phép / khả năng: Can/Could + S + V-inf?",
        json.dumps(["Can", "I", "share", "my", "screen", "during", "the", "video", "call", "?"])
    ),
    (
        "question_form", "Modal Verbs", "💡", "B1",
        "She would like to schedule a product demo next Tuesday.",
        "Cô ấy muốn lên lịch một buổi dùng thử sản phẩm vào thứ Ba tới.",
        "Đặt câu hỏi lịch sự với 'When would she like to...?'",
        "When would she like to schedule the product demo?",
        "Khi nào cô ấy muốn lên lịch buổi dùng thử sản phẩm?",
        "Qu: When | Aux: would | Subj: she | Verb: like to schedule",
        "Hỏi về mong muốn lịch sự: When + would + S + like + to V?",
        json.dumps(["When", "would", "she", "like", "to", "schedule", "the", "product", "demo", "?"])
    ),
    (
        "question_form", "Modal Verbs", "💡", "B2",
        "Applicants must submit their portfolio alongside their resume.",
        "Các ứng viên bắt buộc phải nộp hồ sơ năng lực cùng với sơ yếu lý lịch.",
        "Đặt câu hỏi bắt buộc với 'What must applicants submit?'",
        "What must applicants submit alongside their resume?",
        "Ứng viên bắt buộc phải nộp những gì cùng với sơ yếu lý lịch?",
        "Qu: What | Aux: must | Subj: applicants | Verb: submit",
        "Câu hỏi bắt buộc: What + must + S + submit?",
        json.dumps(["What", "must", "applicants", "submit", "alongside", "their", "resume", "?"])
    ),
    (
        "question_form", "Modal Verbs", "💡", "B1",
        "Could you please explain how this authentication token works?",
        "Bạn có thể vui lòng giải thích mã xác thực này hoạt động như thế nào không?",
        "Đặt câu hỏi yêu cầu lịch sự với 'Could you please explain...?'",
        "Could you please explain how this token works?",
        "Bạn có thể vui lòng giải thích mã xác thực này hoạt động như thế nào không?",
        "Aux: Could | Subj: you | Polite: please | Verb: explain",
        "Yêu cầu lịch sự: Could you please + V-inf + how S + V?",
        json.dumps(["Could", "you", "please", "explain", "how", "this", "token", "works", "?"])
    )
]

def seed_grammar_drills():
    for db_path in DB_PATHS:
        if not os.path.exists(db_path):
            print(f"⚠️ Skip: {db_path} not found.")
            continue

        print(f"\n🚀 Creating table and seeding grammar drills: {db_path}")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # 1. Create table
        c.execute("""
            CREATE TABLE IF NOT EXISTS grammar_drills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                tense_category TEXT,
                category_icon TEXT,
                level TEXT,
                prompt_context TEXT,
                prompt_vi TEXT,
                instruction TEXT,
                target_question TEXT UNIQUE,
                target_vi TEXT,
                quasm_breakdown TEXT,
                grammar_tip TEXT,
                scramble_words TEXT
            )
        """)

        # 2. Insert items
        inserted = 0
        for item in GRAMMAR_DRILLS:
            c.execute("""
                INSERT OR IGNORE INTO grammar_drills (
                    type, tense_category, category_icon, level,
                    prompt_context, prompt_vi, instruction,
                    target_question, target_vi, quasm_breakdown,
                    grammar_tip, scramble_words
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, item)
            if c.rowcount > 0:
                inserted += 1

        conn.commit()

        c.execute("SELECT count(*) FROM grammar_drills")
        total = c.fetchone()[0]

        c.execute("SELECT tense_category, count(*) FROM grammar_drills GROUP BY tense_category ORDER BY count(*) DESC")
        breakdown = c.fetchall()

        print(f"✅ Added {inserted} grammar drill questions! (Total now: {total})")
        print("📊 Tense breakdown:")
        for t, cnt in breakdown:
            print(f"   • {t}: {cnt} drills")

        conn.close()

if __name__ == "__main__":
    seed_grammar_drills()
    print("\n🎉 Completed Grammar & Question Drill database seeding!")
