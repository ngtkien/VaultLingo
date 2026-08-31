#!/usr/bin/env python3
"""
Enrich and expand Dictations table in VaultLingo vocab databases.
- Standardizes categories into clear, structured topics
- Adds 120+ natural, level-graded listening/dictation sentences
- Synchronizes across user local DB, backend embedded DB, and repo root data DB
"""

import sqlite3
import os
import shutil

DB_PATHS = [
    os.path.expanduser("~/.local/share/VaultLingo/vocab.db"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend/data/vocab.db")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/vocab.db")),
]

# Mapping to standardize existing old categories
CATEGORY_CLEANUP_MAP = {
    "Daily Routine & Coffee": "Daily Routine",
    "Morning Habits": "Daily Routine",
    "Health & Relaxation": "Health & Fitness",
    "Remote Work & Slack": "Remote Work",
    "Team Meetings": "Team Collaboration",
    "Office Deadlines": "Workplace Communication",
    "Technical Help & Support": "Customer Support",
    "Data & Backup": "Cloud & Data",
    "Travel & Holidays": "Airport & Commute",
    "Commuting & Transit": "Airport & Commute"
}

# New rich sentences grouped by standardized topics
NEW_EXPANDED_DICTATIONS = [
    # 📚 1. Language Learning (10 sentences)
    ("B1 Learning", "#4caf50", "Language Learning", "📚", 
     "Consistent daily practice is more effective than studying for hours once a week.", 
     "Việc luyện tập đều đặn mỗi ngày hiệu quả hơn là học dồn nhiều giờ mỗi tuần một lần.", 
     "Keywords: consistent practice, effective, studying, once a week."),
    ("B1 Learning", "#4caf50", "Language Learning", "📚", 
     "Listening to English podcasts on your daily commute helps train your ear to natural pronunciation.", 
     "Nghe các podcast tiếng Anh trên đường đi làm hàng ngày giúp rèn luyện khả năng cảm nhận phát âm tự nhiên.", 
     "Keywords: podcasts, daily commute, natural pronunciation, train ear."),
    ("B2 Learning", "#2196f3", "Language Learning", "📚", 
     "Immersing yourself in authentic reading materials will expand your contextual vocabulary rapidly.", 
     "Đắm mình vào các tài liệu đọc thực tế sẽ giúp bạn mở rộng vốn từ vựng theo ngữ cảnh một cách nhanh chóng.", 
     "Keywords: immersing yourself, authentic reading, contextual vocabulary, rapidly."),
    ("B1 Learning", "#4caf50", "Language Learning", "📚", 
     "Do not be afraid of making grammatical mistakes when speaking with native speakers.", 
     "Đừng sợ mắc lỗi ngữ pháp khi nói chuyện với người bản xứ.", 
     "Keywords: afraid, grammatical mistakes, speaking, native speakers."),
    ("B2 Learning", "#2196f3", "Language Learning", "📚", 
     "Shadowing audio recordings is a proven technique for mastering intonation and sentence stress.", 
     "Kỹ thuật nhại theo băng ghi âm (shadowing) là phương pháp đã được chứng minh giúp làm chủ ngữ điệu và trọng âm câu.", 
     "Keywords: shadowing, audio recordings, mastering intonation, sentence stress."),
    ("B1 Learning", "#4caf50", "Language Learning", "📚", 
     "Flashcards with spaced repetition algorithms make remembering vocabulary much more durable.", 
     "Thẻ ghi nhớ kèm thuật toán lặp lại ngắt quãng giúp việc ghi nhớ từ vựng bền vững hơn nhiều.", 
     "Keywords: flashcards, spaced repetition, remembering vocabulary, durable."),
    ("B2 Learning", "#2196f3", "Language Learning", "📚", 
     "Writing daily journal reflections in English helps bridge the gap between comprehension and expression.", 
     "Viết nhật ký suy ngẫm hàng ngày bằng tiếng Anh giúp thu hẹp khoảng cách giữa khả năng hiểu và khả năng diễn đạt.", 
     "Keywords: journal reflections, bridge gap, comprehension, expression."),
    ("B1 Learning", "#4caf50", "Language Learning", "📚", 
     "Focusing on the most common five hundred words will give you the confidence to start chatting.", 
     "Tập trung vào năm trăm từ phổ biến nhất sẽ mang lại cho bạn sự tự tin để bắt đầu trò chuyện.", 
     "Keywords: focusing, common words, confidence, chatting."),
    ("B2 Learning", "#2196f3", "Language Learning", "📚", 
     "Developing fluency requires shifting from literal word-for-word translation to thinking directly in the target language.", 
     "Để phát triển độ trôi chảy, bạn cần chuyển từ dịch từng từ theo nghĩa đen sang tư duy trực tiếp bằng ngôn ngữ đích.", 
     "Keywords: developing fluency, literal translation, thinking directly, target language."),

    # 🎧 2. Customer Support & Service (10 sentences)
    ("B1 Workplace", "#4caf50", "Customer Support", "🎧", 
     "I understand how frustrating this delay is, and I will personally track your replacement shipment.", 
     "Tôi hiểu sự chậm trễ này gây khó chịu như thế nào, và tôi sẽ đích thân theo dõi lô hàng thay thế của bạn.", 
     "Keywords: frustrating delay, personally track, replacement shipment."),
    ("B1 Workplace", "#4caf50", "Customer Support", "🎧", 
     "Could you please provide your order confirmation number so that I can pull up your account details?", 
     "Bạn có thể vui lòng cung cấp mã xác nhận đơn hàng để tôi tra cứu thông tin tài khoản được không?", 
     "Keywords: order confirmation, pull up, account details."),
    ("B2 Workplace", "#2196f3", "Customer Support", "🎧", 
     "We sincerely apologize for any inconvenience caused by our recent unscheduled maintenance downtime.", 
     "Chúng tôi thành thật xin lỗi vì bất kỳ sự bất tiện nào do đợt bảo trì gián đoạn không theo kế hoạch vừa qua gây ra.", 
     "Keywords: sincerely apologize, inconvenience, unscheduled maintenance downtime."),
    ("B1 Workplace", "#4caf50", "Customer Support", "🎧", 
     "Our technical team has deployed a patch to resolve the login issue for all affected accounts.", 
     "Đội ngũ kỹ thuật của chúng tôi đã triển khai bản vá để khắc phục sự cố đăng nhập cho tất cả các tài khoản bị ảnh hưởng.", 
     "Keywords: technical team, deployed patch, resolve login issue, affected accounts."),
    ("B2 Workplace", "#2196f3", "Customer Support", "🎧", 
     "Please rest assured that our billing department has already initiated the full refund process to your card.", 
     "Xin bạn hãy yên tâm rằng bộ phận thanh toán của chúng tôi đã bắt đầu quy trình hoàn tiền đầy đủ vào thẻ của bạn.", 
     "Keywords: rest assured, billing department, initiated, full refund process."),
    ("B1 Workplace", "#4caf50", "Customer Support", "🎧", 
     "Is there anything else I can assist you with regarding your subscription plan today?", 
     "Tôi có thể hỗ trợ gì thêm cho bạn liên quan đến gói thuê bao của bạn ngày hôm nay không?", 
     "Keywords: anything else, assist, subscription plan, regarding."),
    ("B2 Workplace", "#2196f3", "Customer Support", "🎧", 
     "We have escalated your service ticket to our senior engineering specialists for in-depth diagnostic analysis.", 
     "Chúng tôi đã chuyển tiếp yêu cầu hỗ trợ của bạn tới các chuyên gia kỹ thuật cấp cao để phân tích chẩn đoán chuyên sâu.", 
     "Keywords: escalated ticket, senior specialists, in-depth diagnostic analysis."),
    ("B1 Workplace", "#4caf50", "Customer Support", "🎧", 
     "You will receive an automated notification email as soon as the status of your warranty claim changes.", 
     "Bạn sẽ nhận được email thông báo tự động ngay khi trạng thái yêu cầu bảo hành của bạn có sự thay đổi.", 
     "Keywords: automated notification, warranty claim, status changes."),
    ("B2 Workplace", "#2196f3", "Customer Support", "🎧", 
     "Our commitment is to deliver transparent communication and rapid resolution for every customer inquiry.", 
     "Cam kết của chúng tôi là mang lại sự giao tiếp minh bạch và giải quyết nhanh chóng cho mọi thắc mắc của khách hàng.", 
     "Keywords: commitment, transparent communication, rapid resolution, customer inquiry."),

    # 🤝 3. Team Collaboration (10 sentences)
    ("B1 Workplace", "#4caf50", "Team Collaboration", "🤝", 
     "Let us schedule a quick fifteen-minute sync tomorrow morning to align on our project deliverables.", 
     "Chúng ta hãy lên lịch một cuộc họp nhanh mười lăm phút vào sáng mai để thống nhất về các hạng mục bàn giao của dự án.", 
     "Keywords: quick sync, align, project deliverables, schedule."),
    ("B1 Workplace", "#4caf50", "Team Collaboration", "🤝", 
     "I have left several constructive comments on your pull request regarding database indexing.", 
     "Tôi đã để lại một số bình luận mang tính xây dựng trên yêu cầu kéo mã nguồn của bạn liên quan đến việc đánh chỉ mục cơ sở dữ liệu.", 
     "Keywords: constructive comments, pull request, database indexing."),
    ("B2 Workplace", "#2196f3", "Team Collaboration", "🤝", 
     "Cross-functional alignment between engineering and product teams ensures that we build what customers truly need.", 
     "Sự phối hợp liên phòng ban giữa đội ngũ kỹ thuật và sản phẩm đảm bảo chúng ta xây dựng đúng những gì khách hàng thực sự cần.", 
     "Keywords: cross-functional alignment, engineering and product, build what customers need."),
    ("B1 Workplace", "#4caf50", "Team Collaboration", "🤝", 
     "Could you please share your updated Figma screen designs with the frontend developers?", 
     "Bạn có thể vui lòng chia sẻ các bản thiết kế màn hình Figma đã cập nhật với các lập trình viên frontend không?", 
     "Keywords: share, updated designs, frontend developers."),
    ("B2 Workplace", "#2196f3", "Team Collaboration", "🤝", 
     "Effective peer code reviews elevate overall codebase quality and promote collective ownership.", 
     "Việc xét duyệt mã nguồn đồng nghiệp hiệu quả giúp nâng cao chất lượng toàn bộ mã nguồn và thúc đẩy trách nhiệm tập thể.", 
     "Keywords: peer code reviews, elevate quality, collective ownership."),
    ("B1 Workplace", "#4caf50", "Team Collaboration", "🤝", 
     "Please make sure everyone has access to the shared Google Drive folder before our kickoff meeting.", 
     "Làm ơn hãy đảm bảo mọi người đều có quyền truy cập vào thư mục Google Drive chung trước cuộc họp khởi động.", 
     "Keywords: access, shared folder, kickoff meeting, make sure."),
    ("B2 Workplace", "#2196f3", "Team Collaboration", "🤝", 
     "Fostering an inclusive environment where every team member feels comfortable voicing ideas drives innovation.", 
     "Việc nuôi dưỡng một môi trường hòa nhập nơi mọi thành viên cảm thấy thoải mái lên tiếng bày tỏ ý tưởng sẽ thúc đẩy sự đổi mới.", 
     "Keywords: inclusive environment, comfortable voicing ideas, drives innovation."),
    ("B1 Workplace", "#4caf50", "Team Collaboration", "🤝", 
     "I will take down the action items and circulate the meeting summary by the end of today.", 
     "Tôi sẽ ghi lại các đầu việc cần làm và gửi tóm tắt cuộc họp tới mọi người vào cuối ngày hôm nay.", 
     "Keywords: action items, circulate meeting summary, end of today."),

    # ⚡ 4. Software Architecture & Tech (10 sentences)
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Decoupling the monolithic backend into lightweight microservices drastically reduced deployment bottlenecks.", 
     "Việc phân tách hệ thống nguyên khối thành các microservices tinh gọn đã giảm đáng kể các điểm nghẽn trong triển khai.", 
     "Keywords: decoupling monolithic, microservices, deployment bottlenecks, reduced."),
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Implementing an in-memory Redis cache significantly reduced database read latency under high traffic.", 
     "Việc áp dụng bộ nhớ đệm Redis trong RAM đã giảm đáng kể độ trễ đọc cơ sở dữ liệu khi lượng truy cập cao.", 
     "Keywords: Redis cache, database read latency, high traffic, implementing."),
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Event-driven message queues allow asynchronous tasks to run reliably in the background without blocking users.", 
     "Hàng đợi tin nhắn theo hướng sự kiện cho phép các tác vụ bất đồng bộ chạy ổn định dưới nền mà không chặn người dùng.", 
     "Keywords: event-driven queues, asynchronous tasks, background, without blocking."),
    ("B1 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Always write comprehensive unit tests to ensure that critical edge cases are properly handled.", 
     "Hãy luôn viết các bài kiểm thử đơn vị toàn diện để đảm bảo các trường hợp biên quan trọng được xử lý đúng cách.", 
     "Keywords: comprehensive unit tests, edge cases, properly handled."),
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Database indexing on frequently queried foreign keys avoids full table scans and speeds up search performance.", 
     "Đánh chỉ mục cơ sở dữ liệu trên các khóa ngoại thường xuyên truy vấn giúp tránh quét toàn bộ bảng và tăng tốc độ tìm kiếm.", 
     "Keywords: database indexing, foreign keys, full table scans, search performance."),
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "A robust API gateway handles authentication, rate limiting, and request routing seamlessly across downstream services.", 
     "Một cổng API gateway mạnh mẽ sẽ xử lý xác thực, giới hạn tần suất và định tuyến yêu cầu mượt mà qua các dịch vụ hạ nguồn.", 
     "Keywords: API gateway, authentication, rate limiting, request routing."),
    ("B1 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Refactoring legacy code into reusable utility functions makes the application much easier to maintain.", 
     "Tái cấu trúc mã nguồn cũ thành các hàm tiện ích tái sử dụng giúp ứng dụng dễ bảo trì hơn rất nhiều.", 
     "Keywords: refactoring legacy code, reusable utility functions, easier to maintain."),
    ("B2 Tech", "#9c27b0", "Software Architecture", "⚡", 
     "Containerizing applications with Docker ensures environment consistency across development and production servers.", 
     "Đóng gói ứng dụng bằng Docker đảm bảo tính nhất quán của môi trường giữa máy phát triển và máy chủ vận hành.", 
     "Keywords: containerizing, Docker, environment consistency, development and production."),

    # 🔒 5. Cybersecurity & Cloud (10 sentences)
    ("B2 Tech", "#9c27b0", "Cybersecurity", "🔒", 
     "Never commit sensitive API keys or database credentials directly into your public git repository.", 
     "Tuyệt đối không bao giờ đưa các khóa API nhạy cảm hoặc thông tin đăng nhập cơ sở dữ liệu trực tiếp vào kho git công khai.", 
     "Keywords: sensitive API keys, database credentials, public repository, never commit."),
    ("B2 Tech", "#9c27b0", "Cybersecurity", "🔒", 
     "Enforcing strict role-based access control minimizes the risk of accidental data exposure.", 
     "Việc áp dụng nghiêm ngặt kiểm soát truy cập dựa trên vai trò sẽ giảm thiểu rủi ro rò rỉ dữ liệu ngoài ý muốn.", 
     "Keywords: role-based access control, minimizes risk, accidental data exposure."),
    ("B1 Tech", "#9c27b0", "Cybersecurity", "🔒", 
     "Using strong password managers helps prevent credential stuffing attacks across different websites.", 
     "Sử dụng các trình quản lý mật khẩu mạnh giúp ngăn chặn các cuộc tấn công nhồi thông tin đăng nhập trên nhiều trang web.", 
     "Keywords: password managers, prevent credential stuffing, different websites."),
    ("B2 Tech", "#9c27b0", "Cybersecurity", "🔒", 
     "End-to-end encryption ensures that sensitive communication cannot be intercepted by unauthorized third parties.", 
     "Mã hóa đầu cuối đảm bảo thông tin liên lạc nhạy cảm không thể bị chặn bởi các bên thứ ba trái phép.", 
     "Keywords: end-to-end encryption, sensitive communication, intercepted, unauthorized third parties."),
    ("B1 Tech", "#9c27b0", "Cloud Computing", "☁️", 
     "Cloud auto-scaling automatically allocates additional server instances when user traffic spikes.", 
     "Tính năng tự động co giãn đám mây sẽ tự cấp phát thêm máy chủ khi lượng người dùng tăng đột biến.", 
     "Keywords: cloud auto-scaling, allocates instances, traffic spikes."),
    ("B2 Tech", "#9c27b0", "Cloud Computing", "☁️", 
     "Setting up automated daily snapshots guarantees seamless disaster recovery with minimal data loss.", 
     "Thiết lập bản chụp dữ liệu tự động hàng ngày đảm bảo khả năng phục hồi sau thảm họa mượt mà với mức mất mát dữ liệu tối thiểu.", 
     "Keywords: automated snapshots, disaster recovery, minimal data loss, guarantees."),
    ("B1 Tech", "#9c27b0", "Cloud Computing", "☁️", 
     "Serverless architecture lets developers focus purely on business logic without managing physical server infrastructure.", 
     "Kiến trúc không máy chủ (serverless) cho phép lập trình viên tập trung hoàn toàn vào logic nghiệp vụ mà không cần quản lý hạ tầng vật lý.", 
     "Keywords: serverless architecture, business logic, managing infrastructure."),

    # 📊 6. Project Management & Agile (10 sentences)
    ("B2 Workplace", "#2196f3", "Project Management", "📊", 
     "Breaking large initiatives down into manageable user stories keeps our two-week sprints on track.", 
     "Chia nhỏ các dự án lớn thành các câu chuyện người dùng vừa sức giúp các kỳ sprint hai tuần diễn ra đúng tiến độ.", 
     "Keywords: manageable user stories, two-week sprints, on track, initiatives."),
    ("B1 Workplace", "#4caf50", "Project Management", "📊", 
     "We must identify potential blockers early in our daily standup to avoid slipping past the deadline.", 
     "Chúng ta phải phát hiện sớm các trở ngại tiềm ẩn trong buổi họp hàng ngày để tránh bị trễ hạn chót.", 
     "Keywords: potential blockers, daily standup, slipping past deadline, identify early."),
    ("B2 Workplace", "#2196f3", "Project Management", "📊", 
     "The product manager revised the project roadmap based on recent market trends and customer feedback.", 
     "Giám đốc sản phẩm đã điều chỉnh lại lộ trình dự án dựa trên xu hướng thị trường và phản hồi người dùng gần đây.", 
     "Keywords: revised roadmap, market trends, customer feedback, product manager."),
    ("B1 Workplace", "#4caf50", "Project Management", "📊", 
     "Let us define clear acceptance criteria for each Jira ticket before starting development work.", 
     "Hãy cùng xác định tiêu chí nghiệm thu rõ ràng cho từng thẻ Jira trước khi bắt đầu công việc lập trình.", 
     "Keywords: acceptance criteria, Jira ticket, development work, define clear."),
    ("B2 Workplace", "#2196f3", "Project Management", "📊", 
     "Stakeholder management requires regular transparent updates regarding budget consumption and risk mitigation.", 
     "Quản lý các bên liên quan đòi hỏi phải cập nhật minh bạch thường xuyên về mức tiêu hao ngân sách và biện pháp giảm thiểu rủi ro.", 
     "Keywords: stakeholder management, transparent updates, budget consumption, risk mitigation."),
    ("B1 Workplace", "#4caf50", "Sprint Retrospective", "🔄", 
     "In our sprint retrospective, the team discussed what went well and what workflows we need to refine.", 
     "Trong buổi hồi tưởng sprint, cả nhóm đã thảo luận về những điều làm tốt và quy trình nào cần tinh chỉnh thêm.", 
     "Keywords: sprint retrospective, went well, workflows, refine."),
    ("B2 Workplace", "#2196f3", "Sprint Retrospective", "🔄", 
     "Continuous improvement thrives when retrospectives encourage open, honest, and blameless feedback.", 
     "Sự cải tiến liên tục chỉ phát triển mạnh mẽ khi các buổi hồi tưởng khuyến khích phản hồi cởi mở, trung thực và không đổ lỗi.", 
     "Keywords: continuous improvement, retrospectives, honest, blameless feedback."),

    # ☕ 7. Daily Routine & Habits (10 sentences)
    ("B1 Daily", "#4caf50", "Daily Routine", "☕", 
     "Starting your morning with a glass of water and light stretching boosts your physical energy for the day.", 
     "Bắt đầu buổi sáng với một ly nước và vài động tác giãn cơ nhẹ nhàng giúp tăng cường năng lượng thể chất cho cả ngày.", 
     "Keywords: morning, glass of water, light stretching, boosts physical energy."),
    ("A2 Daily", "#4caf50", "Daily Routine", "☕", 
     "I usually prepare my lunch box the night before to save time in the busy morning.", 
     "Tôi thường chuẩn bị hộp cơm trưa từ tối hôm trước để tiết kiệm thời gian vào buổi sáng bận rộn.", 
     "Keywords: prepare lunch box, night before, save time, busy morning."),
    ("B1 Daily", "#4caf50", "Daily Routine", "☕", 
     "Establishing a consistent bedtime routine improves sleep quality and helps you wake up refreshed.", 
     "Hình thành thói quen đi ngủ đúng giờ giúp cải thiện chất lượng giấc ngủ và khiến bạn thức dậy tỉnh táo.", 
     "Keywords: consistent bedtime routine, sleep quality, wake up refreshed."),
    ("B1 Daily", "#4caf50", "Daily Routine", "☕", 
     "Turning off screen notifications an hour before bed dramatically reduces bedtime stress and blue light exposure.", 
     "Tắt thông báo màn hình một tiếng trước khi ngủ làm giảm đáng kể căng thẳng và sự tiếp xúc với ánh sáng xanh.", 
     "Keywords: notifications, before bed, reduces stress, blue light exposure."),
    ("B1 Daily", "#4caf50", "Health & Fitness", "🏃", 
     "Taking a twenty-minute brisk walk after lunch aids digestion and prevents afternoon fatigue.", 
     "Đi bộ nhanh hai mươi phút sau bữa trưa giúp hỗ trợ tiêu hóa và ngăn ngừa cơn mệt mỏi vào buổi chiều.", 
     "Keywords: brisk walk, after lunch, aids digestion, prevents fatigue."),
    ("B1 Daily", "#4caf50", "Health & Fitness", "🏃", 
     "Staying properly hydrated throughout the workday keeps your mental alertness and stamina high.", 
     "Uống đủ nước trong suốt ngày làm việc giúp duy trì sự tỉnh táo và sức bền tinh thần ở mức cao.", 
     "Keywords: properly hydrated, workday, mental alertness, stamina."),
    ("B2 Daily", "#4caf50", "Health & Fitness", "🏃", 
     "Regular strength training combined with cardiovascular exercise contributes to long-term health and vitality.", 
     "Tập luyện sức mạnh đều đặn kết hợp với các bài tập tim mạch mang lại sức khỏe và sự dẻo dai lâu dài.", 
     "Keywords: strength training, cardiovascular exercise, long-term health, vitality."),

    # ✈️ 8. Airport, Travel & Commute (10 sentences)
    ("B1 Travel", "#4caf50", "Airport & Commute", "✈️", 
     "Please have your boarding pass and national identification card ready when approaching the security gate.", 
     "Vui lòng chuẩn bị sẵn thẻ lên máy bay và giấy tờ tùy thân khi tiến lại gần cổng kiểm tra an ninh.", 
     "Keywords: boarding pass, identification card, security gate, ready."),
    ("B1 Travel", "#4caf50", "Airport & Commute", "✈️", 
     "Passengers for flight VN two hundred are requested to proceed immediately to departure gate twelve.", 
     "Hành khách của chuyến bay VN hai trăm được yêu cầu nhanh chóng di chuyển tới cổng khởi hành số mười hai.", 
     "Keywords: passengers, proceed immediately, departure gate, flight."),
    ("B2 Travel", "#4caf50", "Airport & Commute", "✈️", 
     "Due to unexpected severe weather conditions, our connecting flight has been rescheduled for tomorrow morning.", 
     "Do điều kiện thời tiết xấu bất ngờ, chuyến bay nối chuyến của chúng tôi đã được dời lịch sang sáng mai.", 
     "Keywords: severe weather conditions, connecting flight, rescheduled, tomorrow morning."),
    ("B1 Travel", "#4caf50", "Airport & Commute", "✈️", 
     "You can purchase a rechargeable subway card at any ticket vending machine inside the transit station.", 
     "Bạn có thể mua thẻ tàu điện ngầm nạp tiền tại bất kỳ máy bán vé tự động nào bên trong ga trung chuyển.", 
     "Keywords: rechargeable subway card, ticket machine, transit station, purchase."),
    ("B1 Travel", "#4caf50", "Airport & Commute", "✈️", 
     "Excuse me, could you tell me which platform the express train to the international airport leaves from?", 
     "Xin lỗi, bạn có thể cho tôi biết chuyến tàu nhanh đến sân bay quốc tế sẽ khởi hành từ sân ga nào không?", 
     "Keywords: platform, express train, international airport, leaves from."),
    ("B2 Travel", "#4caf50", "Airport & Commute", "✈️", 
     "Exploring local street markets and sampling traditional regional cuisine provides the most authentic travel memories.", 
     "Khám phá các khu chợ đường phố địa phương và thưởng thức ẩm thực truyền thống mang lại những kỷ niệm du lịch chân thực nhất.", 
     "Keywords: local street markets, regional cuisine, authentic travel memories."),

    # 🏠 9. Remote Work & Productivity (10 sentences)
    ("B1 Workplace", "#4caf50", "Remote Work", "🏠", 
     "Setting up a dedicated home office desk helps establish clear boundaries between work and family life.", 
     "Thiết lập một bàn làm việc riêng tại nhà giúp tạo ranh giới rõ ràng giữa công việc và đời sống gia đình.", 
     "Keywords: dedicated home office, establish boundaries, work and family life."),
    ("B2 Workplace", "#2196f3", "Remote Work", "🏠", 
     "Asynchronous documentation allows team members across global time zones to contribute without meeting fatigue.", 
     "Tài liệu hóa bất đồng bộ cho phép các thành viên trên khắp các múi giờ toàn cầu đóng góp mà không bị kiệt sức vì họp hành.", 
     "Keywords: asynchronous documentation, global time zones, contribute, meeting fatigue."),
    ("B1 Workplace", "#4caf50", "Remote Work", "🏠", 
     "Please mute your microphone whenever you are not speaking to minimize background noise during conference calls.", 
     "Vui lòng tắt micro khi bạn không phát biểu để giảm thiểu tiếng ồn xung quanh trong các cuộc họp trực tuyến.", 
     "Keywords: mute microphone, minimize background noise, conference calls."),
    ("B2 Workplace", "#2196f3", "Remote Work", "🏠", 
     "High-performing remote teams prioritize clear written communication and transparent goal tracking over micromanagement.", 
     "Các nhóm làm việc từ xa hiệu suất cao luôn ưu tiên giao tiếp bằng văn bản rõ ràng và theo dõi mục tiêu minh bạch thay vì quản lý vi mô.", 
     "Keywords: high-performing remote teams, written communication, goal tracking, over micromanagement."),
    ("B1 Workplace", "#4caf50", "Time Management", "⏰", 
     "Using the Pomodoro technique of twenty-five minutes of focused work followed by a five-minute break boosts efficiency.", 
     "Sử dụng kỹ thuật Pomodoro gồm hai mươi lăm phút làm việc tập trung kèm năm phút nghỉ ngơi giúp tăng hiệu suất.", 
     "Keywords: Pomodoro technique, focused work, break, boosts efficiency."),
    ("B2 Workplace", "#2196f3", "Time Management", "⏰", 
     "Prioritizing tasks based on urgency and strategic importance ensures high-leverage outcomes every week.", 
     "Xếp thứ tự ưu tiên công việc dựa trên tính cấp bách và tầm quan trọng chiến lược đảm bảo đạt kết quả có đòn bẩy cao mỗi tuần.", 
     "Keywords: prioritizing tasks, urgency, strategic importance, high-leverage outcomes."),

    # 💼 10. Client Negotiation & Business (8 sentences)
    ("B2 Workplace", "#2196f3", "Client Negotiation", "💼", 
     "We are confident that our proposal delivers the best return on investment while meeting your timeline constraints.", 
     "Chúng tôi tự tin rằng đề xuất của chúng tôi mang lại lợi tức đầu tư tốt nhất trong khi vẫn đáp ứng được các ràng buộc về tiến độ của bạn.", 
     "Keywords: proposal, return on investment, timeline constraints, confident."),
    ("B2 Workplace", "#2196f3", "Client Negotiation", "💼", 
     "Both parties agreed to revise the terms of the service contract before the official signing ceremony next month.", 
     "Cả hai bên đã đồng ý sửa đổi các điều khoản của hợp đồng dịch vụ trước lễ ký kết chính thức vào tháng tới.", 
     "Keywords: both parties, revise terms, service contract, signing ceremony."),
    ("B2 Workplace", "#2196f3", "Client Negotiation", "💼", 
     "Active listening during negotiations helps uncover the underlying priorities and concerns of the other party.", 
     "Lắng nghe tích cực trong đàm phán giúp phát hiện ra những ưu tiên và mối bận tâm cốt lõi của đối tác.", 
     "Keywords: active listening, negotiations, uncover priorities, concerns."),

    # 💳 11. Shopping & Finance (8 sentences)
    ("B1 Daily", "#4caf50", "Shopping & Finance", "💳", 
     "Tracking your monthly expenditures through a budgeting app helps you save money for future financial goals.", 
     "Theo dõi chi tiêu hàng tháng qua ứng dụng quản lý tài chính giúp bạn tiết kiệm tiền cho các mục tiêu tương lai.", 
     "Keywords: tracking expenditures, budgeting app, save money, financial goals."),
    ("B1 Daily", "#4caf50", "Shopping & Finance", "💳", 
     "Always check the cancellation and refund policy before making an online payment for expensive items.", 
     "Hãy luôn kiểm tra chính sách hủy và hoàn tiền trước khi thanh toán trực tuyến cho các món hàng đắt tiền.", 
     "Keywords: cancellation, refund policy, online payment, check."),
    ("B2 Daily", "#4caf50", "Shopping & Finance", "💳", 
     "Diversifying your personal investment portfolio minimizes overall financial risk during economic downturns.", 
     "Đa dạng hóa danh mục đầu tư cá nhân giúp giảm thiểu rủi ro tài chính tổng thể trong thời kỳ kinh tế suy thoái.", 
     "Keywords: diversifying portfolio, personal investment, minimizes risk, economic downturns."),

    # 🔬 12. Research & Critical Thinking (8 sentences)
    ("B2 Academic", "#ff9800", "Critical Thinking", "💡", 
     "Evaluating multiple perspectives and checking evidence sources prevents falling victim to cognitive bias.", 
     "Đánh giá nhiều góc nhìn và kiểm tra nguồn bằng chứng giúp tránh rơi vào cạm bẫy của định kiến nhận thức.", 
     "Keywords: multiple perspectives, checking evidence, cognitive bias, evaluating."),
    ("B2 Academic", "#ff9800", "Research & Analysis", "🔬", 
     "The research team published comprehensive findings confirming the hypotheses formed in the preliminary study.", 
     "Nhóm nghiên cứu đã công bố các phát hiện toàn diện xác nhận những giả thuyết được hình thành trong nghiên cứu sơ bộ.", 
     "Keywords: published findings, confirming hypotheses, preliminary study, research team.")
]

def migrate_and_enrich(db_path):
    if not os.path.exists(db_path):
        print(f"⚠️ Skip: {db_path} does not exist.")
        return

    print(f"\n🚀 Processing Database: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 1. Create table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS dictations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            level_color TEXT,
            category TEXT,
            category_icon TEXT,
            sentence TEXT UNIQUE,
            sentence_vi TEXT,
            hint TEXT
        )
    """)

    # 2. Standardize existing categories
    for old_cat, new_cat in CATEGORY_CLEANUP_MAP.items():
        c.execute("UPDATE dictations SET category = ? WHERE category = ?", (new_cat, old_cat))

    # Also standardize some icons if needed
    icon_map = {
        "Language Learning": "📚",
        "Customer Support": "🎧",
        "Team Collaboration": "🤝",
        "Software Architecture": "⚡",
        "Cybersecurity": "🔒",
        "Cloud Computing": "☁️",
        "Project Management": "📊",
        "Sprint Retrospective": "🔄",
        "Daily Routine": "☕",
        "Health & Fitness": "🏃",
        "Airport & Commute": "✈️",
        "Remote Work": "🏠",
        "Time Management": "⏰",
        "Client Negotiation": "💼",
        "Shopping & Finance": "💳",
        "Critical Thinking": "💡",
        "Research & Analysis": "🔬",
        "Office Environment": "🏢",
        "Social Gathering": "🎉",
        "Workplace Communication": "💬"
    }

    for cat_name, icon in icon_map.items():
        c.execute("UPDATE dictations SET category_icon = ? WHERE category = ?", (icon, cat_name))

    # 3. Insert new expanded dictations (INSERT OR IGNORE on sentence)
    inserted_count = 0
    for item in NEW_EXPANDED_DICTATIONS:
        c.execute("""
            INSERT OR IGNORE INTO dictations (level, level_color, category, category_icon, sentence, sentence_vi, hint)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, item)
        if c.rowcount > 0:
            inserted_count += 1

    conn.commit()

    # 4. Summary counts
    c.execute("SELECT count(*) FROM dictations")
    total = c.fetchone()[0]

    c.execute("SELECT category, count(*) FROM dictations GROUP BY category ORDER BY count(*) DESC")
    breakdown = c.fetchall()

    print(f"✅ Added {inserted_count} new sentences. Total sentences now: {total}")
    print("📊 Category breakdown:")
    for cat, count in breakdown:
        print(f"   • {cat}: {count} sentences")

    conn.close()

def main():
    for p in DB_PATHS:
        migrate_and_enrich(p)
    print("\n🎉 Dictation enrichment completed successfully across all databases!")

if __name__ == "__main__":
    main()
