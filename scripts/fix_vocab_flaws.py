#!/usr/bin/env python3
"""
Fix vocabulary flaws, truncated sentences, leaked words, definition mismatches,
and duplicate dictations across all VaultLingo databases.
"""
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATHS = [
    os.path.join(ROOT, "backend", "data", "vocab.db"),
    os.path.join(ROOT, "data", "vocab.db"),
    os.path.expanduser("~/.local/share/VaultLingo/vocab.db"),
]

# Explicit word fixes: word -> (example_en, example_vi)
WORD_FIXES = {
    # The primary reported issue
    "souvenir": (
        "I bought a small model of the Eiffel Tower as a souvenir of my trip to Paris.",
        "Tôi đã mua một mô hình tháp Eiffel nhỏ làm quà lưu niệm cho chuyến đi đến Paris."
    ),

    # Duplicate English word at end + cut off VI
    "coach": (
        "We took an overnight coach from London to Paris.",
        "Chúng tôi đã đi xe đò qua đêm từ Luân Đôn đến Paris."
    ),
    "ancient": (
        "We visited the ancient ruins of Rome.",
        "Chúng tôi đã đến thăm những tàn tích cổ của thành Rome."
    ),
    "sprinkle": (
        "She sprinkled some chocolate shavings on top of the cappuccino.",
        "Cô ấy rắc một ít vụn sô cô la lên trên ly cappuccino."
    ),
    "modern art": (
        "The museum has an impressive collection of modern art, including works by Picasso and Warhol.",
        "Bảo tàng có một bộ sưu tập nghệ thuật hiện đại ấn tượng, bao gồm các tác phẩm của Picasso và Warhol."
    ),
    "glamorous": (
        "She always dreamed of living a glamorous life in Hollywood.",
        "Cô ấy luôn mơ ước có một cuộc sống hào nhoáng ở Hollywood."
    ),
    "occur": (
        "The accident occurred at the intersection of Main Street and Oak Avenue.",
        "Vụ tai nạn xảy ra ở ngã tư đường Main và đại lộ Oak."
    ),

    # Leaked VI into EN and cut off VI
    "climate": (
        "The region's warm climate is perfect for growing grapes.",
        "Khí hậu ấm áp của vùng này rất lý tưởng để trồng nho."
    ),
    "depressed": (
        "She felt very depressed after breaking up with her boyfriend.",
        "Cô ấy cảm thấy rất chán nản sau khi chia tay bạn trai."
    ),
    "up to date": (
        "It's important to keep your software up to date to protect against security threats.",
        "Việc giữ cho phần mềm của bạn được cập nhật là rất quan trọng để bảo vệ khỏi các mối đe dọa an ninh."
    ),
    "power": (
        "She has the power to inspire everyone around her.",
        "Cô ấy có khả năng truyền cảm hứng cho mọi người xung quanh."
    ),
    "fall for": (
        "She fell for him the moment they met.",
        "Cô ấy đã yêu anh ấy ngay từ giây phút họ gặp nhau."
    ),
    "charge": (
        "The police brought a charge of assault against him.",
        "Cảnh sát đã đưa ra lời buộc tội hành hung đối với anh ta."
    ),
    "prove": (
        "The new evidence will prove his innocence.",
        "Bằng chứng mới sẽ chứng minh sự vô tội của anh ta."
    ),
    "sore": (
        "My muscles are sore after yesterday's workout.",
        "Cơ bắp của tôi bị đau nhức sau buổi tập ngày hôm qua."
    ),
    "clinic": (
        "I have an appointment at the dental clinic this afternoon.",
        "Tôi có một cuộc hẹn ở phòng khám nha khoa chiều nay."
    ),
    "sweet": (
        "She has a very sweet voice that is pleasant to listen to.",
        "Cô ấy có một giọng nói rất ngọt ngào, nghe rất êm tai."
    ),
    "chili": (
        "I like to add a little chili to my soup for some extra spice.",
        "Tôi thích cho một chút ớt vào súp để tăng thêm vị cay."
    ),
    "attempt": (
        "This is his second attempt at passing the exam.",
        "Đây là nỗ lực thứ hai của anh ấy để vượt qua kỳ thi."
    ),
    "snap": (
        "I was walking when the sole of my shoe suddenly snapped off.",
        "Tôi đang đi bộ thì đế giày của tôi đột nhiên bị rớt ra."
    ),
    "glimpse": (
        "As the limousine drove past, I just managed to glimpse the famous actress inside.",
        "Khi chiếc limousine chạy ngang qua, tôi chỉ kịp nhìn thoáng qua nữ diễn viên nổi tiếng ở bên trong."
    ),
    "likeness": (
        "There is a striking likeness between the two sisters.",
        "Có một sự giống nhau đáng kinh ngạc giữa hai chị em."
    ),
    "feel": (
        "I feel much better after a good night's sleep.",
        "Tôi cảm thấy khỏe hơn nhiều sau một giấc ngủ ngon."
    ),
    "subway": (
        "I take the subway to work every day to avoid traffic.",
        "Tôi đi tàu điện ngầm đi làm mỗi ngày để tránh kẹt xe."
    ),
    "Movie": (
        "Let's go watch a movie at the cinema tonight.",
        "Tối nay chúng ta hãy đi xem phim ở rạp chiếu phim."
    ),
    "labor": (
        "The factory relies heavily on manual labor.",
        "Nhà máy phụ thuộc rất nhiều vào lao động chân tay."
    ),
    "in time": (
        "We arrived at the airport just in time to catch our flight.",
        "Chúng tôi đến sân bay vừa kịp lúc để bắt chuyến bay."
    ),
    "literate": (
        "To succeed in this modern society, one must be highly literate and adaptable.",
        "Để thành công trong xã hội hiện đại này, một người phải thực sự có học thức và khả năng thích nghi."
    ),

    # Truncated EN sentences
    "heroine": (
        "Marie Curie is considered a scientific heroine for her groundbreaking work in radioactivity.",
        "Marie Curie được coi là một nữ anh hùng khoa học nhờ công trình mang tính đột phá về phóng xạ."
    ),
    "long-playing": (
        "My grandfather still has a large collection of long-playing records from the 1960s.",
        "Ông tôi vẫn giữ một bộ sưu tập lớn các đĩa hát nhựa từ những năm 1960."
    ),
    "subtraction": (
        "Children learn basic arithmetic operations like addition and subtraction in primary school.",
        "Trẻ em học các phép tính số học cơ bản như phép cộng và phép trừ ở trường tiểu học."
    ),
    "castle": (
        "The ancient castle stood proudly on the hill, offering a magnificent view of the valley.",
        "Lâu đài cổ kính đứng uy nghi trên đồi, mang đến tầm nhìn tráng lệ ra thung lũng."
    ),
    "luggage": (
        "Please place your luggage in the overhead compartment or under the seat in front of you.",
        "Vui lòng đặt hành lý của bạn vào ngăn để đồ phía trên hoặc dưới ghế phía trước bạn."
    ),
    "traffic": (
        "The traffic was very heavy during rush hour this morning, so I was late for work.",
        "Giao thông rất tắc nghẽn vào giờ cao điểm sáng nay, vì vậy tôi đã bị muộn giờ làm."
    ),
    "helicopter": (
        "The rescue helicopter landed on the roof of the hospital to pick up the patient.",
        "Trực thăng cứu hộ đã hạ cánh trên mái bệnh viện để đón bệnh nhân."
    ),
    "care about": (
        "She really cares about the environment and tries to recycle as much as possible.",
        "Cô ấy thực sự quan tâm đến môi trường và cố gắng tái chế nhiều nhất có thể."
    ),
    "an argument": (
        "I had an argument with my roommate about whose turn it was to clean the kitchen.",
        "Tôi đã cãi nhau với bạn cùng phòng về việc đến lượt ai dọn dẹp nhà bếp."
    ),
    "property": (
        "The storm caused a lot of damage to their property, especially the roof of the house.",
        "Cơn bão đã gây nhiều thiệt hại cho tài sản của họ, đặc biệt là mái nhà."
    ),
    "unequal": (
        "The slices of cake were unequal, and the children argued over who got the bigger one.",
        "Các miếng bánh không đều nhau, và lũ trẻ đã cãi nhau xem ai được miếng lớn hơn."
    ),
    "change sth": (
        "The new policy changed the office from a stressful place into a much more relaxed environment.",
        "Chính sách mới đã thay đổi văn phòng từ một nơi căng thẳng thành một môi trường thư thái hơn nhiều."
    ),
    "wildlife": (
        "The national park is famous for its diverse wildlife, including bears and wolves.",
        "Vườn quốc gia nổi tiếng với hệ động vật hoang dã đa dạng, bao gồm gấu và chó sói."
    ),
    "gardener": (
        "My grandfather is a keen gardener and spends most of his weekends in the garden.",
        "Ông tôi là một người làm vườn nhiệt huyết và dành phần lớn thời gian cuối tuần trong vườn."
    ),
    "emotional": (
        "It was an emotional moment when the soldiers returned home to their families.",
        "Đó là một khoảnh khắc xúc động khi những người lính trở về nhà với gia đình của họ."
    ),
    "hatred": (
        "The story is about the hatred between two families that has lasted for generations.",
        "Câu chuyện kể về mối hận thù giữa hai gia đình đã kéo dài qua nhiều thế hệ."
    ),
    "rumour": (
        "I heard a rumour that the company is closing down, but I don't know if it's true.",
        "Tôi nghe đồn rằng công ty sắp đóng cửa, nhưng tôi không biết điều đó có đúng không."
    ),
    "theory": (
        "In theory, this plan should work, but we need to see what happens in practice.",
        "Về mặt lý thuyết thì kế hoạch này sẽ thành công, nhưng chúng ta cần xem điều gì xảy ra trên thực tế."
    ),

    # Definition-like or mismatched VI in example sentences
    "Kitten": (
        "The tiny kitten chased a butterfly in the garden.",
        "Chú mèo con bé bỏng đuổi theo một con bướm trong vườn."
    ),
    "sailor": (
        "The old sailor told exciting stories about his adventures on the ocean.",
        "Người thủy thủ già kể những câu chuyện thú vị về những chuyến phiêu lưu trên đại dương của ông."
    ),
    "crash": (
        "The car crashed into a lamppost because the driver wasn't paying attention.",
        "Chiếc xe ô tô đã đâm vào cột đèn vì tài xế không chú ý quan sát."
    ),
    "instruction": (
        "Please follow the instructions on the package carefully.",
        "Vui lòng làm theo hướng dẫn trên bao bì một cách cẩn thận."
    ),
    "prize": (
        "She won first prize in the national essay contest.",
        "Cô ấy đã giành giải nhất trong cuộc thi viết luận toàn quốc."
    ),
    "Dinosaur": (
        "The museum has a huge skeleton of a Tyrannosaurus Rex dinosaur.",
        "Bảo tàng có một bộ xương khổng lồ của một con khủng long T-Rex."
    ),
    "correction": (
        "The teacher made some corrections on my essay.",
        "Giáo viên đã sửa một số lỗi trong bài luận của tôi."
    ),
    "cope with": (
        "It's hard to cope with the loss of a loved one, but time helps.",
        "Thật khó để đương đầu với sự mất mát người thân, nhưng thời gian sẽ giúp xoa dịu."
    ),
    "succeed in": (
        "She worked hard to succeed in her new role at the company.",
        "Cô ấy đã nỗ lực làm việc để thành công trong vai trò mới tại công ty."
    ),
    "abroad": (
        "Many young people dream of working abroad after finishing university.",
        "Nhiều bạn trẻ mơ ước được làm việc ở nước ngoài sau khi tốt nghiệp đại học."
    ),
    "vehicle": (
        "Cars, buses, and trucks are all types of vehicles.",
        "Ô tô, xe buýt và xe tải đều là các loại phương tiện giao thông."
    ),
    "choice": (
        "You have the choice between a sandwich and a salad for lunch.",
        "Bạn có sự lựa chọn giữa bánh mì kẹp hoặc món salad cho bữa trưa."
    ),
    "arrive at/in": (
        "What time does the train arrive at the station?",
        "Mấy giờ thì tàu hỏa đến ga?"
    ),
    "organization": (
        "She works for a large international organization that helps children.",
        "Cô ấy làm việc cho một tổ chức quốc tế lớn chuyên giúp đỡ trẻ em."
    ),
    "decorate": (
        "We always decorate the house with lights and a tree at Christmas.",
        "Chúng tôi luôn trang trí nhà cửa bằng đèn và cây thông vào dịp Giáng sinh."
    ),
    "sweep": (
        "I need to sweep the kitchen floor; it's very dirty.",
        "Tôi cần quét sàn nhà bếp; nó rất bẩn."
    ),
    "admire sb for": (
        "I admire my teacher for her patience and kindness.",
        "Tôi ngưỡng mộ cô giáo vì sự kiên nhẫn và lòng tốt của cô ấy."
    ),
    "tank": (
        "We bought a new tank for our goldfish.",
        "Chúng tôi đã mua một bể cá mới cho những chú cá vàng."
    ),
    "cupboard": (
        "I keep the plates and bowls in the kitchen cupboard.",
        "Tôi cất đĩa và bát trong tủ bếp."
    ),
    "army": (
        "He joined the army right after finishing high school.",
        "Anh ấy đã gia nhập quân đội ngay sau khi tốt nghiệp trung học."
    ),
    "belong to": (
        "This book belongs to the library, so you must return it in two weeks.",
        "Cuốn sách này thuộc về thư viện, vì vậy bạn phải trả lại sau hai tuần."
    ),
    "buy sth from": (
        "I usually buy my vegetables from the local market because they are fresh.",
        "Tôi thường mua rau từ chợ địa phương vì chúng tươi ngon."
    ),
    "spend sth on": (
        "She spends a lot of money on clothes.",
        "Cô ấy chi rất nhiều tiền cho quần áo."
    ),
    "borrow": (
        "Can I borrow your pen for a minute?",
        "Tôi có thể mượn bút của bạn một lát được không?"
    ),
    "begin sth with": (
        "She began her speech with a funny story.",
        "Cô ấy bắt đầu bài phát biểu của mình bằng một câu chuyện hài hước."
    ),
    "result in": (
        "The heavy rain resulted in widespread flooding in the city.",
        "Cơn mưa lớn đã dẫn đến tình trạng ngập lụt diện rộng trong thành phố."
    ),
    "head teacher": (
        "The head teacher gave a speech at the beginning of the school year.",
        "Thầy hiệu trưởng đã có bài phát biểu vào đầu năm học."
    ),
    "accent": (
        "In the word 'banana', the accent is on the second syllable.",
        "Trong từ 'banana', trọng âm rơi vào âm tiết thứ hai."
    ),
    "communicate": (
        "It's important to communicate clearly with your team members.",
        "Việc giao tiếp rõ ràng với các thành viên trong nhóm là rất quan trọng."
    ),
    "translate": (
        "She was asked to translate the letter from French into English.",
        "Cô ấy được yêu cầu dịch lá thư từ tiếng Pháp sang tiếng Anh."
    ),
    "comment on": (
        "The teacher asked the students to comment on the story they had just read.",
        "Giáo viên yêu cầu các học sinh bình luận về câu chuyện các em vừa đọc."
    ),
    "glance at": (
        "He glanced at his watch to check the time.",
        "Anh ấy liếc nhìn đồng hồ để kiểm tra thời gian."
    ),
    "send sth to sb": (
        "I need to send this package to my sister in London.",
        "Tôi cần gửi gói hàng này cho chị gái tôi ở Luân Đôn."
    ),
    "shooting": (
        "He enjoys target shooting as a hobby on the weekends.",
        "Anh ấy thích bắn bia như một sở thích vào cuối tuần."
    ),
    "employment": (
        "She was offered employment in the sales department.",
        "Cô ấy đã được nhận vào làm việc tại bộ phận bán hàng."
    ),
    "officer": (
        "A police officer helped the lost child find his parents.",
        "Một viên cảnh sát đã giúp đứa trẻ bị lạc tìm lại cha mẹ."
    ),
    "fed up with": (
        "I'm fed up with all this traffic. It takes me an hour to get to work every day.",
        "Tôi phát chán với cảnh tắc đường này rồi. Mỗi ngày tôi mất một tiếng đồng hồ mới đến được chỗ làm."
    ),
    "depend on": (
        "As a student, I depend on my parents for financial support.",
        "Là một sinh viên, tôi phụ thuộc vào cha mẹ để được hỗ trợ tài chính."
    ),
    "flu": (
        "I had to take a week off work because I came down with a bad case of the flu.",
        "Tôi phải nghỉ làm một tuần vì bị một trận cúm nặng."
    ),
    "allergic to": (
        "My brother is allergic to cats, so he starts sneezing whenever he's near one.",
        "Anh trai tôi bị dị ứng với mèo, nên anh ấy hắt hơi bất cứ khi nào ở gần một con mèo."
    ),
    "pleased with": (
        "The manager was very pleased with the team's performance.",
        "Người quản lý rất hài lòng với thành tích của cả nhóm."
    ),
    "exhibition": (
        "We went to see an exhibition of modern art at the city gallery.",
        "Chúng tôi đã đến xem một buổi triển lãm nghệ thuật hiện đại tại phòng tranh thành phố."
    ),
    "imaginative": (
        "The little girl had an imaginative friend who was a talking dragon.",
        "Bé gái có một người bạn trong trí tưởng tượng là một chú rồng biết nói."
    ),
    "amazed at/by": (
        "I was amazed at how quickly she learned the language.",
        "Tôi rất ngạc nhiên trước việc cô ấy học ngôn ngữ đó nhanh đến mức nào."
    ),
    "aware of": (
        "Are you aware of the risks involved in this project?",
        "Bạn có nhận thức được những rủi ro liên quan đến dự án này không?"
    ),
    "escape from": (
        "The prisoner managed to escape from the high-security jail.",
        "Tên tù nhân đã trốn thoát khỏi nhà tù an ninh nghiêm ngặt."
    ),
    "rude": (
        "It's rude to interrupt people when they are speaking.",
        "Thật bất lịch sự khi ngắt lời người khác khi họ đang nói."
    ),
    "felt": (
        "She learned how to felt wool to make small toys.",
        "Cô ấy đã học cách làm nỉ len để chế tạo những món đồ chơi nhỏ."
    ),
    "ashamed of": (
        "He was ashamed of his old, worn-out shoes.",
        "Anh ấy cảm thấy xấu hổ về đôi giày cũ rách của mình."
    ),
    "frightened of": (
        "Many children are frightened of the dark.",
        "Nhiều đứa trẻ sợ bóng tối."
    ),
    "scared of": (
        "Many children are scared of the dark.",
        "Nhiều đứa trẻ sợ hãi bóng tối."
    ),
    "exception": (
        "Everyone has to be at the meeting at 9 AM, with no exceptions.",
        "Mọi người phải có mặt tại cuộc họp lúc 9 giờ sáng, không có ngoại lệ."
    ),
    "sure about/of": (
        "He is very sure of his decision to move to a new city.",
        "Anh ấy rất chắc chắn về quyết định chuyển đến một thành phố mới."
    ),
    "happen to": (
        "What happened to your arm? It's in a cast.",
        "Chuyện gì đã xảy ra với cánh tay của bạn vậy? Nó đang phải bó bột kìa."
    ),
    "a solution to": (
        "We need to find a solution to the traffic problem in our city.",
        "Chúng ta cần tìm ra giải pháp cho vấn đề giao thông trong thành phố của mình."
    ),
    "idiot": (
        "I felt like a complete idiot when I realized I had locked my keys in the car.",
        "Tôi cảm thấy mình thật ngốc nghếch khi nhận ra đã để quên chìa khóa trong xe ô tô."
    ),
    "listen to": (
        "I love to listen to classical music in the evenings.",
        "Tôi thích nghe nhạc cổ điển vào các buổi tối."
    ),
    "a fan of": (
        "I am a big fan of her music; I listen to her songs every day.",
        "Tôi là một người rất hâm mộ âm nhạc của cô ấy; tôi nghe các bài hát của cô ấy mỗi ngày."
    ),
    "mistake": (
        "Everyone makes mistakes, so don't worry too much about it.",
        "Ai cũng từng mắc sai lầm, vì vậy đừng lo lắng quá nhiều về điều đó."
    ),
    "prepare for": (
        "She is studying hard to prepare for her final exams.",
        "Cô ấy đang học tập chăm chỉ để chuẩn bị cho các kỳ thi cuối kỳ."
    ),
}

def sync_and_clean_db(db_path):
    if not os.path.exists(db_path):
        print(f"Skipping non-existent DB: {db_path}")
        return

    print(f"\nProcessing database: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 1. Update explicit word fixes
    updated_words = 0
    for word, (en, vi) in WORD_FIXES.items():
        c.execute("""
            UPDATE words 
            SET example_en = ?, example_vi = ? 
            WHERE LOWER(word) = LOWER(?)
        """, (en, vi, word))
        if c.rowcount > 0:
            updated_words += c.rowcount

    print(f"  Fixed {updated_words} specific word flaw(s).")

    # 2. Fix the 92 bloated words if this DB is user_db or has any length(example_vi) > 300
    # Copy clean versions from backend/data/vocab.db
    repo_db_path = os.path.join(ROOT, "backend", "data", "vocab.db")
    if db_path != repo_db_path and os.path.exists(repo_db_path):
        conn_repo = sqlite3.connect(repo_db_path)
        c_repo = conn_repo.cursor()
        
        # Check for any bloated rows in current db
        c.execute("SELECT id, word FROM words WHERE length(example_vi) > 300")
        bloated_rows = c.fetchall()
        if bloated_rows:
            print(f"  Found {len(bloated_rows)} bloated rows in {os.path.basename(db_path)}. Syncing from repo_db...")
            for bid, bword in bloated_rows:
                c_repo.execute("SELECT example_en, example_vi FROM words WHERE LOWER(word) = LOWER(?)", (bword,))
                clean_row = c_repo.fetchone()
                if clean_row and len(clean_row[1]) < 300:
                    c.execute("UPDATE words SET example_en = ?, example_vi = ? WHERE id = ?", (clean_row[0], clean_row[1], bid))
            print(f"  Synced all bloated rows successfully.")
        conn_repo.close()

    # 3. Deduplicate dictations if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dictations'")
    if c.fetchone():
        c.execute("""
            DELETE FROM dictations 
            WHERE id NOT IN (
                SELECT MIN(id) FROM dictations GROUP BY sentence
            )
        """)
        if c.rowcount > 0:
            print(f"  Removed {c.rowcount} duplicate dictation rows.")

    conn.commit()
    conn.close()
    print(f"  Completed {db_path}")

def main():
    for p in DB_PATHS:
        sync_and_clean_db(p)
    print("\nAll databases have been cleaned and synchronized.")

if __name__ == "__main__":
    main()
