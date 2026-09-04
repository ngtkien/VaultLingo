#!/usr/bin/env python3
"""Seed a varied, offline learning corpus into every VaultLingo database.

The application may run from the embedded database or an existing user copy;
therefore this script deliberately updates all three locations.  It is
idempotent: idioms and sentences have unique text, and listening rows use a
stable topic id.
"""
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATHS = [
    os.path.join(ROOT, "data", "vocab.db"),
    os.path.join(ROOT, "backend", "data", "vocab.db"),
    os.path.expanduser("~/.local/share/VaultLingo/vocab.db"),
]

IDIOMS = [
    ("A blessing in disguise", "A seemingly bad event that later has a positive result.", "Trong cái rủi có cái may."),
    ("A dime a dozen", "Very common and not special.", "Rất phổ biến, không hiếm."),
    ("Add fuel to the fire", "To make an already bad situation worse.", "Đổ thêm dầu vào lửa."),
    ("Beat around the bush", "To avoid saying something directly.", "Nói vòng vo."),
    ("Cost an arm and a leg", "To be extremely expensive.", "Đắt đỏ."),
    ("Get the ball rolling", "To begin an activity or process.", "Bắt đầu một việc."),
    ("Give someone a hand", "To help someone.", "Giúp một tay."),
    ("Go the extra mile", "To make more effort than expected.", "Nỗ lực hơn mức được mong đợi."),
    ("Hang in there", "To remain patient and not give up.", "Cố lên, đừng bỏ cuộc."),
    ("In hot water", "In trouble.", "Đang gặp rắc rối."),
    ("Keep an eye on", "To watch something carefully.", "Theo dõi cẩn thận."),
    ("Learn the ropes", "To learn how a job or activity works.", "Học việc, nắm cách vận hành."),
    ("Miss the boat", "To lose an opportunity.", "Bỏ lỡ cơ hội."),
    ("No pain, no gain", "Progress requires hard work or discomfort.", "Có công mài sắt, có ngày nên kim."),
    ("Pull someone's leg", "To joke with someone by trying to make them believe something untrue.", "Trêu đùa ai đó."),
    ("Put all your eggs in one basket", "To risk everything on one plan.", "Đặt tất cả vào một lựa chọn."),
    ("Speak of the devil", "Said when the person being discussed appears.", "Vừa nhắc Tào Tháo, Tào Tháo đến."),
    ("The best of both worlds", "The benefits of two different situations at once.", "Lợi cả đôi đường."),
    ("The tip of the iceberg", "A small visible part of a much larger problem.", "Phần nổi của tảng băng."),
    ("Time flies", "Time seems to pass very quickly.", "Thời gian trôi nhanh."),
    ("Up in the air", "Not decided or settled yet.", "Chưa được quyết định."),
    ("When pigs fly", "Something that will never happen.", "Chuyện không bao giờ xảy ra."),
    ("Wrap your head around", "To understand a difficult idea.", "Hiểu được một ý khó."),
    ("Your guess is as good as mine", "I do not know any more than you do.", "Tôi cũng không biết hơn bạn."),
    ("By the book", "According to the rules.", "Theo đúng quy định."),
    ("Get out of hand", "To become difficult to control.", "Trở nên mất kiểm soát."),
    ("Keep your chin up", "Stay positive in a difficult situation.", "Giữ tinh thần lạc quan."),
    ("Make ends meet", "To have just enough money for basic needs.", "Đủ tiền trang trải."),
    ("On cloud nine", "Extremely happy.", "Rất vui sướng."),
    ("Rain check", "To postpone an invitation until another time.", "Hẹn dịp khác."),
    ("Take the plunge", "To make a bold decision to begin something.", "Quyết tâm bắt đầu việc lớn."),
    ("The last straw", "The final problem that makes a situation unbearable.", "Giọt nước tràn ly."),
    ("Throw in the towel", "To stop trying or admit defeat.", "Bỏ cuộc."),
    ("Under your nose", "In a very obvious place.", "Ngay trước mắt."),
    ("Wrap up", "To finish something.", "Hoàn tất."),
    ("Zero in on", "To focus closely on something.", "Tập trung chính xác vào."),
    ("A win-win situation", "A result that benefits everyone involved.", "Tình huống đôi bên cùng có lợi."),
    ("Get cold feet", "To become nervous before doing something planned.", "Chùn bước vào phút chót."),
    ("Keep something under wraps", "To keep something secret.", "Giữ kín."),
    ("On the fence", "Unable to decide between two options.", "Đang phân vân."),
    ("Put yourself in someone's shoes", "To imagine another person's situation.", "Đặt mình vào vị trí người khác."),
    ("Read between the lines", "To find a hidden meaning.", "Đọc ý ngầm."),
    ("Rock the boat", "To cause trouble by changing a stable situation.", "Gây xáo trộn."),
    ("Take it with a pinch of salt", "To not believe something completely.", "Đón nhận với sự thận trọng."),
    ("The whole nine yards", "Everything possible or available.", "Toàn bộ mọi thứ."),
    ("Turn a blind eye", "To deliberately ignore something.", "Làm ngơ có chủ ý."),
    ("Water under the bridge", "A past problem that is no longer important.", "Chuyện đã qua."),
    ("Wear many hats", "To have several different roles or duties.", "Kiêm nhiệm nhiều vai trò."),
]

QUIZZES = [
    ("Prepositions", "🎯", "She is interested ___ learning more about cloud security.", ["A. in", "B. on", "C. at", "D. for"], "A", "We use interested in + noun or gerund.", "interested in + V-ing"),
    ("Collocations", "⚡", "Please ___ attention to the deadline in the project brief.", ["A. pay", "B. do", "C. make", "D. take"], "A", "The fixed collocation is pay attention.", "pay attention to"),
    ("Grammar", "⏳", "If I ___ more time, I would join the speaking club.", ["A. had", "B. have", "C. will have", "D. am having"], "A", "Second conditional uses If + past simple, would + verb.", "If I had..., I would..."),
    ("Business English", "💼", "Could you ___ the meeting until Thursday?", ["A. postpone", "B. delay to", "C. reschedule on", "D. put"], "A", "Postpone takes the object directly.", "postpone a meeting"),
    ("Verb patterns", "🧠", "She suggested ___ a short break before the presentation.", ["A. taking", "B. to take", "C. take", "D. took"], "A", "Suggest is followed by a gerund when suggesting an action.", "suggest + V-ing"),
    ("Articles", "📘", "He is ___ honest and reliable colleague.", ["A. an", "B. a", "C. the", "D. no article"], "A", "Honest starts with a vowel sound.", "an honest colleague"),
    ("Phrasal verbs", "🔧", "Please ___ the form before you submit it.", ["A. fill in", "B. fill up to", "C. fill out with", "D. fill over"], "A", "Fill in and fill out are both used for forms; fill in is the expected answer here.", "fill in a form"),
    ("Word choice", "📚", "The manager gave us useful ___ on the proposal.", ["A. feedback", "B. feedbacks", "C. an feedback", "D. a feedback"], "A", "Feedback is uncountable in standard English.", "some feedback"),
    ("Tenses", "⌛", "By next June, they ___ the new office building.", ["A. will have completed", "B. complete", "C. completed", "D. have completed"], "A", "Future perfect describes completion before a future time.", "will have + past participle"),
    ("Adjectives", "🌱", "This explanation is much ___ than the previous one.", ["A. clearer", "B. more clear", "C. clearest", "D. clearly"], "A", "Clear normally takes the comparative clearer.", "clearer than"),
    ("Workplace English", "🏢", "We need to ___ a decision before Friday.", ["A. make", "B. do", "C. create", "D. build"], "A", "The natural collocation is make a decision.", "make a decision"),
    ("Reported speech", "🗣️", "She said that she ___ the report the next day.", ["A. would send", "B. will send", "C. sends", "D. sent"], "A", "Will commonly becomes would in reported speech from a past reporting verb.", "said that she would"),
]

LISTENING_TOPICS = [
    ("Morning Routine", "☀️", "What do you usually do first in the morning?", "I drink a glass of water and make a short plan for the day.", "Do you eat breakfast at home?", "Yes, I usually have fruit, eggs, and coffee before I leave."),
    ("At the Library", "📚", "How long can I borrow this book?", "You can keep it for two weeks and renew it online once.", "Is there a quiet place to study?", "Yes, the second floor has silent study rooms."),
    ("Buying Groceries", "🛒", "Where can I find fresh vegetables?", "They are in aisle three beside the bakery section.", "Do you accept card payments?", "Yes, you can pay by card or mobile wallet."),
    ("Weekend Plans", "🌤️", "What are you doing this weekend?", "I am visiting my cousin and trying a new hiking trail.", "Will the weather be good?", "The forecast says it will be sunny on Saturday."),
    ("Coffee Shop", "☕", "Could I have a latte with less sugar?", "Certainly. Would you like it hot or iced?", "I would like it iced, please.", "Your drink will be ready at the counter in a few minutes."),
    ("Job Interview", "💼", "Why are you interested in this position?", "I enjoy solving practical problems and collaborating with a thoughtful team.", "What is one of your strengths?", "I communicate clearly and stay calm when priorities change."),
    ("Doctor's Appointment", "🩺", "How long have you had these symptoms?", "I have had a sore throat and a mild fever since yesterday.", "Have you taken any medicine?", "Only some paracetamol after dinner."),
    ("Planning a Trip", "✈️", "When would you like to travel?", "I would like to leave early Friday morning.", "Do you prefer a window or aisle seat?", "A window seat would be great, thank you."),
    ("Team Meeting", "🤝", "What should we discuss first?", "Let us review the timeline and the remaining risks.", "Who will write the meeting notes?", "I can take notes and send a summary after the meeting."),
    ("Learning English", "🌍", "How do you practise listening every day?", "I listen to short conversations and repeat useful phrases aloud.", "What helps you remember new words?", "I use example sentences and review them over several days."),
    ("At the Hotel", "🏨", "Is breakfast included with the room?", "Yes, breakfast is served from seven until ten.", "Could I check out later tomorrow?", "We can offer a late check-out until one o'clock."),
    ("Fitness Class", "🏃", "Is this class suitable for beginners?", "Yes, the instructor shows easier options for every exercise.", "What should I bring?", "Bring water, a towel, and comfortable shoes."),
    ("New Neighbour", "🏠", "Have you just moved into the building?", "Yes, I moved in last weekend from Da Nang.", "Please let me know if you need anything.", "Thank you. That is very kind of you."),
    ("Online Meeting", "💻", "Can everyone see my screen?", "Yes, but the text is a little small.", "I will zoom in on the chart.", "That looks much clearer now."),
    ("Restaurant Booking", "🍽️", "Do you have a table for four at seven?", "Yes, we have one near the window.", "Could you note that one guest is vegetarian?", "Of course, I have added that to your reservation."),
    ("Customer Support", "🎧", "My order has not arrived yet.", "I am sorry about that. Let me check the tracking details.", "When can I expect it?", "It should arrive by the end of tomorrow."),
    ("Museum Visit", "🖼️", "Is photography allowed in this gallery?", "Photography is allowed without flash in most rooms.", "Where does the guided tour begin?", "It starts beside the main entrance at two o'clock."),
    ("Tech Support", "🔧", "My laptop cannot connect to the network.", "Please restart it and check whether airplane mode is off.", "I have tried that already.", "Then I will create a support ticket for you."),
    ("Cooking Dinner", "🥘", "What are you making for dinner?", "I am making vegetable noodles with a light sauce.", "Can I help with anything?", "Yes, could you wash and chop the herbs?"),
    ("Study Group", "📝", "Which chapter are we reviewing today?", "We are reviewing the chapter about renewable energy.", "Should we divide the questions?", "Yes, then we can compare our answers together."),
    ("Bank Visit", "🏦", "I would like to open a savings account.", "May I see your identification and proof of address?", "Here are my documents.", "Thank you. I will explain the account options."),
    ("Weather Forecast", "🌧️", "Will it rain this afternoon?", "There may be light rain after three o'clock.", "Should I bring an umbrella?", "Yes, it would be a good idea."),
    ("Giving Directions", "🗺️", "How can I get to the train station?", "Walk straight for two blocks and turn left at the traffic lights.", "Is it far from here?", "No, it is about a ten-minute walk."),
    ("Project Update", "📊", "Are we still on schedule for the release?", "Yes, although we need to finish testing one more feature.", "Who is handling that task?", "Linh is leading it and will share an update tomorrow."),
]

def seed(conn):
    cur = conn.cursor()
    # Earlier enrichment runs did not have a uniqueness constraint, so first
    # retain one copy of any repeated sentence before enforcing it.
    cur.execute("DELETE FROM dictations WHERE id NOT IN (SELECT MIN(id) FROM dictations GROUP BY sentence)")
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_dictations_sentence_unique ON dictations(sentence)")
    cur.execute("DELETE FROM quizzes WHERE id NOT IN (SELECT MIN(id) FROM quizzes GROUP BY question)")
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_quizzes_question_unique ON quizzes(question)")
    for phrase, meaning, vi in IDIOMS:
        cur.execute("INSERT OR IGNORE INTO idioms (idiom, phonetic, meaning_en, meaning_vi, example, example_vi) VALUES (?, '', ?, ?, ?, '')",
                    (phrase, meaning, vi, f"Try to use '{phrase}' naturally in a conversation this week."))
    for category, icon, question, options, correct, explanation, tip in QUIZZES:
        cur.execute("INSERT OR IGNORE INTO quizzes (category, category_icon, question, options_json, correct, correct_sentence, explanation, tip) VALUES (?, ?, ?, ?, ?, '', ?, ?)",
                    (category, icon, question, json.dumps(options), correct, explanation, tip))
    # tts:// explicitly means that the app reads qa_json.  Unlike the old
    # external MP3 mapping, this guarantees that audio and transcript match.
    for topic_id, row in enumerate(LISTENING_TOPICS, start=101):
        title, icon, q1, a1, q2, a2 = row
        qa = [{"q": q1, "a": a1}, {"q": q2, "a": a2}]
        cur.execute("INSERT INTO listening_topics (topic_id, title, icon, audio_url, web_url, qa_json) VALUES (?, ?, ?, 'tts://lesson', '', ?) ON CONFLICT(topic_id) DO UPDATE SET title=excluded.title, icon=excluded.icon, audio_url=excluded.audio_url, web_url=excluded.web_url, qa_json=excluded.qa_json",
                    (topic_id, title, icon, json.dumps(qa)))
    # Existing records contain generated text paired with unrelated MP3s.
    # Switch them to TTS as well, retaining their transcript as the source.
    cur.execute("UPDATE listening_topics SET audio_url = 'tts://lesson' WHERE audio_url NOT LIKE 'tts://%'")
    conn.commit()

for path in DB_PATHS:
    if os.path.exists(path):
        try:
            with sqlite3.connect(path) as connection:
                seed(connection)
                print(f"Seeded {path}")
        except sqlite3.OperationalError as error:
            # Packaging/build environments can intentionally expose the
            # installed database read-only.  The bundled databases are still
            # updated; an installer can rerun this script with permission.
            print(f"Skipped {path}: {error}")
