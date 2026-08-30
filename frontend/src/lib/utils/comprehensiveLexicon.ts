import { backend } from '../../../wailsjs/go/models';
import type { SmartWordResult, BilingualExample } from './smartDictionary';

export interface LexiconEntry {
  pos: string;
  phonetic: string;
  def_en: string;
  def_vi: string;
  ex_en: string;
  ex_vi: string;
  level?: string;
  topic?: string;
  topic_title?: string;
  topic_icon?: string;
  synonyms?: string[];
  antonyms?: string[];
  collocations?: string[];
  word_family?: { pos: string; word: string }[];
  etymology?: string;
  mnemonic_hook?: string;
}

/**
 * Massive High-Frequency English-Vietnamese Core Lexicon Dataset
 * Curated from Oxford 3000 / Cambridge Core standards.
 */
export const COMPREHENSIVE_LEXICON_DATA: Record<string, LexiconEntry> = {
  // Technology, Computing & Hardware
  'keyboard': {
    pos: 'Noun',
    phonetic: '/ˈkiː.bɔːd/',
    def_en: 'A panel of keys that operate a computer, typewriter, or musical instrument.',
    def_vi: 'Bàn phím máy tính hoặc nhạc cụ (piano, organ).',
    ex_en: 'She typed rapidly on her mechanical keyboard.',
    ex_vi: 'Cô ấy gõ rất nhanh trên bàn phím cơ của mình.',
    level: 'A1 Essential',
    topic: 'technology',
    topic_title: 'Hardware & Tech',
    topic_icon: '⌨️',
    collocations: ['mechanical keyboard', 'wireless keyboard', 'type on a keyboard', 'keyboard shortcuts'],
    word_family: [{ pos: 'Noun', word: 'keyboard' }, { pos: 'Noun', word: 'keyboardist' }]
  },
  'mouse': {
    pos: 'Noun',
    phonetic: '/maʊs/',
    def_en: 'A small handheld device that controls a computer cursor; a small rodent.',
    def_vi: 'Chuột máy tính; con chuột.',
    ex_en: 'Click the left button on your mouse to select an option.',
    ex_vi: 'Nhấp nút chuột trái để chọn một tùy chọn.',
    level: 'A1 Essential',
    topic: 'technology',
    topic_title: 'Hardware & Tech',
    topic_icon: '🖱️',
    collocations: ['wireless mouse', 'mouse cursor', 'click a mouse', 'mouse pad']
  },
  'screen': {
    pos: 'Noun / Verb',
    phonetic: '/skriːn/',
    def_en: 'A flat panel or area on an electronic device on which images and data are displayed.',
    def_vi: 'Màn hình hiển thị; sàng lọc, che chắn.',
    ex_en: 'Staring at a computer screen for too long causes eye strain.',
    ex_vi: 'Nhìn vào màn hình máy tính quá lâu sẽ gây mỏi mắt.',
    level: 'A1 Essential',
    topic: 'technology',
    topic_title: 'Display & Devices',
    topic_icon: '🖥️',
    collocations: ['computer screen', 'touch screen', 'screen time', 'split screen']
  },
  'laptop': {
    pos: 'Noun',
    phonetic: '/ˈlæp.tɒp/',
    def_en: 'A portable computer suitable for use while traveling.',
    def_vi: 'Máy tính xách tay, laptop.',
    ex_en: 'She carried her lightweight laptop to the coffee shop.',
    ex_vi: 'Cô ấy mang theo chiếc máy tính xách tay mỏng nhẹ tới quán cà phê.',
    level: 'A1 Essential',
    topic: 'technology',
    topic_title: 'Computing',
    topic_icon: '💻',
    collocations: ['open a laptop', 'laptop battery', 'gaming laptop', 'work on a laptop']
  },
  'software': {
    pos: 'Noun',
    phonetic: '/ˈsɒft.weər/',
    def_en: 'The programs and operating information used by a computer.',
    def_vi: 'Phần mềm máy tính, các chương trình và ứng dụng.',
    ex_en: 'Our engineering team develops open-source software for education.',
    ex_vi: 'Đội ngũ kỹ sư của chúng tôi phát triển phần mềm nguồn mở phục vụ giáo dục.',
    level: 'A2 Elementary',
    topic: 'technology',
    topic_title: 'Software & Dev',
    topic_icon: '💾',
    collocations: ['software engineer', 'install software', 'software update', 'open-source software'],
    word_family: [{ pos: 'Noun', word: 'software' }, { pos: 'Noun', word: 'hardware' }]
  },
  'hardware': {
    pos: 'Noun',
    phonetic: '/ˈhɑːd.weər/',
    def_en: 'The physical components that make up a computer or electronic system.',
    def_vi: 'Phần cứng máy tính, linh kiện thiết bị vật lý.',
    ex_en: 'Upgrading the hardware significantly improved rendering speeds.',
    ex_vi: 'Nâng cấp phần cứng đã cải thiện đáng kể tốc độ kết xuất đồ họa.',
    level: 'B1 Intermediate',
    topic: 'technology',
    topic_title: 'Hardware & Systems',
    topic_icon: '🔧',
    collocations: ['computer hardware', 'hardware upgrade', 'hardware component']
  },
  'server': {
    pos: 'Noun',
    phonetic: '/ˈsɜː.vər/',
    def_en: 'A computer or program that manages access to a centralized resource or service in a network.',
    def_vi: 'Máy chủ, hệ thống quản lý dữ liệu và dịch vụ mạng.',
    ex_en: 'The database server handles millions of requests every minute.',
    ex_vi: 'Máy chủ cơ sở dữ liệu xử lý hàng triệu yêu cầu mỗi phút.',
    level: 'B1 Intermediate',
    topic: 'technology',
    topic_title: 'Cloud & Infrastructure',
    topic_icon: '🖧',
    collocations: ['cloud server', 'web server', 'server crash', 'connect to a server'],
    word_family: [{ pos: 'Noun', word: 'server' }, { pos: 'Verb', word: 'serve' }, { pos: 'Noun', word: 'service' }]
  },
  'network': {
    pos: 'Noun / Verb',
    phonetic: '/ˈnet.wɜːk/',
    def_en: 'A group of interconnected people or computer systems.',
    def_vi: 'Mạng lưới, hệ thống kết nối máy tính hoặc kết nối xã hội.',
    ex_en: 'A secure local area network protects internal company communications.',
    ex_vi: 'Một mạng nội bộ an toàn bảo vệ các thông tin trao đổi nội bộ công ty.',
    level: 'B1 Intermediate',
    topic: 'technology',
    topic_title: 'Networks & Connectivity',
    topic_icon: '🌐',
    collocations: ['computer network', 'social network', 'network connection', 'secure network']
  },
  'database': {
    pos: 'Noun',
    phonetic: '/ˈdeɪ.tə.beɪs/',
    def_en: 'A structured set of data held in a computer, especially one that is accessible in various ways.',
    def_vi: 'Cơ sở dữ liệu, kho lưu trữ thông tin có cấu trúc.',
    ex_en: 'The application queries the SQLite database to retrieve vocabulary items.',
    ex_vi: 'Ứng dụng truy vấn cơ sở dữ liệu SQLite để lấy các mục từ vựng.',
    level: 'B1 Intermediate',
    topic: 'technology',
    topic_title: 'Data & Databases',
    topic_icon: '🗄️',
    collocations: ['relational database', 'database management', 'query a database', 'database backup']
  },
  'data': {
    pos: 'Noun',
    phonetic: '/ˈdeɪ.tə/',
    def_en: 'Facts and statistics collected together for reference or analysis.',
    def_vi: 'Dữ liệu, số liệu, thông tin được thu thập để phân tích.',
    ex_en: 'Data privacy and security are paramount in modern software design.',
    ex_vi: 'Quyền riêng tư và bảo mật dữ liệu là điều tối quan trọng trong thiết kế phần mềm hiện đại.',
    level: 'A2 Elementary',
    topic: 'technology',
    topic_title: 'Data Science',
    topic_icon: '📊',
    collocations: ['data analysis', 'collect data', 'data privacy', 'data science', 'process data']
  },
  'security': {
    pos: 'Noun',
    phonetic: '/sɪˈkjʊə.rə.ti/',
    def_en: 'The state of being free from danger or threat; safety precautions.',
    def_vi: 'Sự an ninh, an toàn, bảo mật; biện pháp bảo vệ.',
    ex_en: 'Two-factor authentication adds an indispensable layer of account security.',
    ex_vi: 'Xác thực hai yếu tố bổ sung một lớp bảo mật không thể thiếu cho tài khoản.',
    level: 'B1 Intermediate',
    topic: 'technology',
    topic_title: 'Cybersecurity & Safety',
    topic_icon: '🛡️',
    collocations: ['cyber security', 'national security', 'security measure', 'tight security'],
    word_family: [{ pos: 'Noun', word: 'security' }, { pos: 'Adjective', word: 'secure' }, { pos: 'Verb', word: 'secure' }, { pos: 'Adverb', word: 'securely' }]
  },

  // Everyday Objects & Household
  'window': {
    pos: 'Noun',
    phonetic: '/ˈwɪn.dəʊ/',
    def_en: 'An opening in the wall or roof of a building or vehicle that is fitted with glass; an area on a computer screen.',
    def_vi: 'Cửa sổ; cửa sổ hiển thị trên màn hình máy tính.',
    ex_en: 'Open the window to let fresh morning air circulate through the room.',
    ex_vi: 'Mở cửa sổ để không khí trong lành buổi sáng lưu thông vào phòng.',
    level: 'A1 Essential',
    topic: 'home',
    topic_title: 'Home & Architecture',
    topic_icon: '🪟',
    collocations: ['open a window', 'close a window', 'window frame', 'browser window']
  },
  'door': {
    pos: 'Noun',
    phonetic: '/dɔːr/',
    def_en: 'A hinged, sliding, or revolving barrier at the entrance to a building, room, or vehicle.',
    def_vi: 'Cửa ra vào, cánh cửa.',
    ex_en: 'Opportunity often knocks on the door when you least expect it.',
    ex_vi: 'Cơ hội thường gõ cửa vào những lúc bạn ít ngờ tới nhất.',
    level: 'A1 Essential',
    topic: 'home',
    topic_title: 'Home & Structure',
    topic_icon: '🚪',
    collocations: ['open the door', 'lock the door', 'front door', 'knock on the door']
  },
  'table': {
    pos: 'Noun',
    phonetic: '/ˈteɪ.bəl/',
    def_en: 'A piece of furniture with a flat top and one or more legs; a systematic arrangement of data.',
    def_vi: 'Cái bàn; bảng số liệu, bảng biểu.',
    ex_en: 'They gathered around the dining table for an evening meal.',
    ex_vi: 'Họ quây quần bên bàn ăn cho bữa tối.',
    level: 'A1 Essential',
    topic: 'home',
    topic_title: 'Furniture & Living',
    topic_icon: '🪑',
    collocations: ['round table', 'dining table', 'table of contents', 'sit at a table']
  },
  'chair': {
    pos: 'Noun / Verb',
    phonetic: '/tʃeər/',
    def_en: 'A separate seat for one person, typically with four legs and a back; to preside over a meeting.',
    def_vi: 'Cái ghế; chủ trì một cuộc họp.',
    ex_en: 'An ergonomic chair supports proper posture during long coding sessions.',
    ex_vi: 'Một chiếc ghế công thái học hỗ trợ tư thế đúng trong những buổi lập trình kéo dài.',
    level: 'A1 Essential',
    topic: 'home',
    topic_title: 'Furniture & Work',
    topic_icon: '🪑',
    collocations: ['office chair', 'armchair', 'sit in a chair', 'chair a meeting']
  },
  'bottle': {
    pos: 'Noun / Verb',
    phonetic: '/ˈbɒt.əl/',
    def_en: 'A container with a narrow neck, used for storing drinks or other liquids.',
    def_vi: 'Cái chai, bình đựng nước/chất lỏng.',
    ex_en: 'Carry a reusable water bottle to stay hydrated throughout the day.',
    ex_vi: 'Mang theo một bình nước tái sử dụng để luôn đủ nước suốt cả ngày.',
    level: 'A1 Essential',
    topic: 'daily',
    topic_title: 'Daily Essentials',
    topic_icon: '🍾',
    collocations: ['water bottle', 'bottle of wine', 'plastic bottle', 'reusable bottle']
  },
  'car': {
    pos: 'Noun',
    phonetic: '/kɑːr/',
    def_en: 'A road vehicle, typically with four wheels, powered by an internal combustion engine or electric motor.',
    def_vi: 'Xe hơi, xe ô tô.',
    ex_en: 'Electric cars produce zero direct emissions and operate quietly.',
    ex_vi: 'Xe ô tô điện không thải khí trực tiếp và vận hành rất êm ái.',
    level: 'A1 Essential',
    topic: 'travel',
    topic_title: 'Transportation',
    topic_icon: '🚗',
    collocations: ['drive a car', 'electric car', 'park a car', 'car rental']
  },
  'city': {
    pos: 'Noun',
    phonetic: '/ˈsɪt.i/',
    def_en: 'A large town, typically with a high population density and advanced infrastructure.',
    def_vi: 'Thành phố, đô thị lớn.',
    ex_en: 'The city center is filled with historic landmarks and vibrant markets.',
    ex_vi: 'Trung tâm thành phố có nhiều địa danh lịch sử và những khu chợ sôi động.',
    level: 'A1 Essential',
    topic: 'society',
    topic_title: 'Urban Life',
    topic_icon: '🏙️',
    collocations: ['city center', 'smart city', 'capital city', 'live in a city']
  },
  'country': {
    pos: 'Noun',
    phonetic: '/ˈkʌn.tri/',
    def_en: 'A nation with its own government, occupying a particular territory; rural area.',
    def_vi: 'Quốc gia, đất nước; vùng nông thôn.',
    ex_en: 'Traveling to another country broadens your linguistic and cultural horizons.',
    ex_vi: 'Du lịch đến một đất nước khác mở rộng chân trời ngôn ngữ và văn hóa của bạn.',
    level: 'A1 Essential',
    topic: 'society',
    topic_title: 'Geography & Nations',
    topic_icon: '🌏',
    collocations: ['foreign country', 'develop a country', 'countryside', 'across the country']
  },
  'world': {
    pos: 'Noun',
    phonetic: '/wɜːld/',
    def_en: 'The earth, together with all of its countries and peoples; a particular sphere of activity.',
    def_vi: 'Thế giới, địa cầu, toàn bộ nhân loại.',
    ex_en: 'Curiosity is the key that unlocks the wonders of the natural world.',
    ex_vi: 'Sự tò mò là chìa khóa mở ra những điều kỳ diệu của thế giới tự nhiên.',
    level: 'A1 Essential',
    topic: 'nature',
    topic_title: 'World & Cosmos',
    topic_icon: '🌍',
    collocations: ['around the world', 'world peace', 'world economy', 'modern world']
  },
  'life': {
    pos: 'Noun',
    phonetic: '/laɪf/',
    def_en: 'The condition that distinguishes animals and plants from inorganic matter; human existence.',
    def_vi: 'Cuộc sống, sự sống, sinh mệnh.',
    ex_en: 'Living a meaningful life requires aligning daily actions with core values.',
    ex_vi: 'Sống một cuộc đời ý nghĩa đòi hỏi bạn phải gắn kết hành động hàng ngày với các giá trị cốt lõi.',
    level: 'A1 Essential',
    topic: 'mindset',
    topic_title: 'Life & Purpose',
    topic_icon: '🌱',
    collocations: ['daily life', 'quality of life', 'way of life', 'save a life', 'live a life']
  },
  'water': {
    pos: 'Noun / Verb',
    phonetic: '/ˈwɔː.tər/',
    def_en: 'A colorless, transparent, odorless liquid that forms the seas, lakes, rivers, and rain and is the basis of the fluids of living organisms.',
    def_vi: 'Nước; tưới nước cho cây.',
    ex_en: 'Clean drinking water is a fundamental human necessity.',
    ex_vi: 'Nước uống sạch là một nhu cầu cơ bản tối thiết của con người.',
    level: 'A1 Essential',
    topic: 'nature',
    topic_title: 'Nature & Vitality',
    topic_icon: '💧',
    collocations: ['drink water', 'fresh water', 'glass of water', 'water supply', 'boil water']
  },
  'money': {
    pos: 'Noun',
    phonetic: '/ˈmʌn.i/',
    def_en: 'A current medium of exchange in the form of coins and banknotes.',
    def_vi: 'Tiền bạc, tiền tệ, tài chính.',
    ex_en: 'Financial literacy teaches individuals how to manage money wisely.',
    ex_vi: 'Kiến thức tài chính dạy cho các cá nhân cách quản lý tiền bạc một cách khôn ngoan.',
    level: 'A1 Essential',
    topic: 'finance',
    topic_title: 'Finance & Wealth',
    topic_icon: '💰',
    collocations: ['save money', 'spend money', 'make money', 'earn money', 'invest money']
  },
  'health': {
    pos: 'Noun',
    phonetic: '/helθ/',
    def_en: 'The state of being free from illness or injury; overall physical and mental wellbeing.',
    def_vi: 'Sức khỏe, tình trạng thể chất và tinh thần tốt.',
    ex_en: 'Good health is the ultimate foundation for achieving your dreams.',
    ex_vi: 'Sức khỏe tốt là nền tảng tối cao để đạt được những ước mơ của bạn.',
    level: 'A1 Essential',
    topic: 'health',
    topic_title: 'Wellness & Vitality',
    topic_icon: '🩺',
    collocations: ['good health', 'health care', 'mental health', 'public health', 'in good health'],
    word_family: [{ pos: 'Noun', word: 'health' }, { pos: 'Adjective', word: 'healthy' }, { pos: 'Adjective', word: 'unhealthy' }, { pos: 'Adverb', word: 'healthily' }]
  },
  'travel': {
    pos: 'Verb / Noun',
    phonetic: '/ˈtræv.əl/',
    def_en: 'Make a journey, typically of some length or abroad; the action of traveling.',
    def_vi: 'Du lịch, đi lại, chuyến hành trình.',
    ex_en: 'She loves to travel and immerse herself in diverse global cultures.',
    ex_vi: 'Cô ấy thích đi du lịch và đắm mình vào những nền văn hóa đa dạng trên thế giới.',
    level: 'A1 Essential',
    topic: 'travel',
    topic_title: 'Journeys & Discovery',
    topic_icon: '✈️',
    collocations: ['travel abroad', 'travel by train', 'travel agency', 'business travel', 'travel expenses']
  },
  'home': {
    pos: 'Noun / Adverb',
    phonetic: '/həʊm/',
    def_en: 'The place where one lives permanently, especially as a member of a family or household.',
    def_vi: 'Ngôi nhà, tổ ấm, quê hương.',
    ex_en: 'There is no place quite as comforting and peaceful as home.',
    ex_vi: 'Không có nơi nào bình yên và dễ chịu như ngôi nhà của mình.',
    level: 'A1 Essential',
    topic: 'home',
    topic_title: 'Home & Comfort',
    topic_icon: '🏡',
    collocations: ['go home', 'at home', 'stay at home', 'feel at home', 'home sweet home']
  },
  'art': {
    pos: 'Noun',
    phonetic: '/ɑːt/',
    def_en: 'The expression or application of human creative skill and imagination.',
    def_vi: 'Nghệ thuật, hội họa, tài hoa sáng tạo.',
    ex_en: 'Modern art challenges viewers to perceive reality from new angles.',
    ex_vi: 'Nghệ thuật hiện đại thách thức người xem cảm nhận hiện thực từ những góc nhìn mới.',
    level: 'A1 Essential',
    topic: 'art',
    topic_title: 'Creative Arts',
    topic_icon: '🎨',
    collocations: ['work of art', 'art gallery', 'fine art', 'modern art', 'art exhibition'],
    word_family: [{ pos: 'Noun', word: 'art' }, { pos: 'Noun', word: 'artist' }, { pos: 'Adjective', word: 'artistic' }, { pos: 'Adverb', word: 'artistically' }]
  },
  'game': {
    pos: 'Noun',
    phonetic: '/ɡeɪm/',
    def_en: 'A form of play or sport, especially a competitive one played according to rules.',
    def_vi: 'Trò chơi, trận đấu thể thao hoặc trò chơi điện tử.',
    ex_en: 'Playing chess is an intellectually stimulating strategy game.',
    ex_vi: 'Chơi cờ vua là một trò chơi chiến lược kích thích trí tuệ.',
    level: 'A1 Essential',
    topic: 'entertainment',
    topic_title: 'Play & Strategy',
    topic_icon: '🎮',
    collocations: ['play a game', 'video game', 'board game', 'game plan', 'win a game']
  },
  'science': {
    pos: 'Noun',
    phonetic: '/ˈsaɪ.əns/',
    def_en: 'The systematic study of the structure and behavior of the physical and natural world through observation and experiment.',
    def_vi: 'Khoa học, nghiên cứu có hệ thống về thế giới tự nhiên.',
    ex_en: 'Science empowers humanity to cure diseases and explore the cosmos.',
    ex_vi: 'Khoa học trao quyền cho nhân loại chữa khỏi bệnh tật và khám phá vũ trụ.',
    level: 'A2 Elementary',
    topic: 'science',
    topic_title: 'Science & Discovery',
    topic_icon: '🔬',
    collocations: ['natural science', 'computer science', 'science fiction', 'scientific research'],
    word_family: [{ pos: 'Noun', word: 'science' }, { pos: 'Noun', word: 'scientist' }, { pos: 'Adjective', word: 'scientific' }, { pos: 'Adverb', word: 'scientifically' }]
  },
  'language': {
    pos: 'Noun',
    phonetic: '/ˈlæŋ.ɡwɪdʒ/',
    def_en: 'The principal method of human communication, consisting of words used in a structured and conventional way.',
    def_vi: 'Ngôn ngữ, tiếng nói, chữ viết dùng để giao tiếp.',
    ex_en: 'Mastering a foreign language opens a window into another worldview.',
    ex_vi: 'Làm chủ một ngoại ngữ mở ra cánh cửa dẫn vào một thế giới quan mới.',
    level: 'A1 Essential',
    topic: 'communication',
    topic_title: 'Linguistics & Speech',
    topic_icon: '🗣️',
    collocations: ['foreign language', 'native language', 'body language', 'programming language', 'learn a language'],
    word_family: [{ pos: 'Noun', word: 'language' }, { pos: 'Noun', word: 'linguistics' }, { pos: 'Noun', word: 'linguist' }, { pos: 'Adjective', word: 'linguistic' }]
  },
  'system': {
    pos: 'Noun',
    phonetic: '/ˈsɪs.təm/',
    def_en: 'A set of connected things or parts forming a complex whole.',
    def_vi: 'Hệ thống, mạng lưới liên kết có cấu trúc.',
    ex_en: 'A robust operating system manages hardware and software resources seamlessly.',
    ex_vi: 'Một hệ điều hành mạnh mẽ quản lý các tài nguyên phần cứng và phần mềm một cách liền mạch.',
    level: 'B1 Intermediate',
    topic: 'technology',
    topic_title: 'Systems & Architecture',
    topic_icon: '⚙️',
    collocations: ['operating system', 'education system', 'solar system', 'system architecture', 'design a system'],
    word_family: [{ pos: 'Noun', word: 'system' }, { pos: 'Adjective', word: 'systematic' }, { pos: 'Adverb', word: 'systematically' }, { pos: 'Verb', word: 'systematize' }]
  },
  'phone': {
    pos: 'Noun / Verb',
    phonetic: '/fəʊn/ (UK) • /foʊn/ (US)',
    def_en: 'A telephone or mobile device used for voice communication, messaging, and digital access; to contact someone by telephone.',
    def_vi: 'Điện thoại, thiết bị liên lạc cầm tay; gọi điện thoại cho ai đó.',
    ex_en: 'She answered her phone immediately when the client called.',
    ex_vi: 'Cô ấy nhấc điện thoại ngay lập tức khi khách hàng gọi đến.',
    level: 'A1 Essential',
    topic: 'technology',
    topic_title: 'Communication & Tech',
    topic_icon: '📱',
    collocations: ['answer the phone', 'mobile phone', 'smart phone', 'on the phone', 'phone call', 'phone number', 'pick up the phone'],
    word_family: [{ pos: 'Noun / Verb', word: 'phone' }, { pos: 'Noun', word: 'telephone' }, { pos: 'Adjective', word: 'phonetic' }, { pos: 'Noun', word: 'phonetics' }]
  },
  'book': {
    pos: 'Noun / Verb',
    phonetic: '/bʊk/',
    def_en: 'A written or printed work consisting of pages glued or sewn together along one side and bound in covers; to reserve accommodation, a seat, or tickets.',
    def_vi: 'Quyển sách, tác phẩm viết; đặt chỗ trước, đặt vé, đăng ký trước.',
    ex_en: 'She was reading an insightful book on cognitive psychology.',
    ex_vi: 'Cô ấy đang đọc một cuốn sách sâu sắc về tâm lý học nhận thức.',
    level: 'A1 Essential',
    topic: 'education',
    topic_title: 'Literature & Learning',
    topic_icon: '📖',
    collocations: ['read a book', 'write a book', 'publish a book', 'book a flight', 'book a hotel', 'open a book', 'by the book'],
    word_family: [{ pos: 'Noun / Verb', word: 'book' }, { pos: 'Noun', word: 'booking' }, { pos: 'Noun', word: 'booklet' }, { pos: 'Noun', word: 'bookstore' }, { pos: 'Adjective', word: 'bookish' }]
  },
  'school': {
    pos: 'Noun / Verb',
    phonetic: '/skuːl/',
    def_en: 'An institution for educating children or students; to educate or train someone.',
    def_vi: 'Trường học, cơ sở giáo dục; rèn luyện, đào tạo.',
    ex_en: 'Education at school shapes a child\'s worldview and social skills.',
    ex_vi: 'Giáo dục tại trường học định hình thế giới quan và kỹ năng xã hội của trẻ.',
    level: 'A1 Essential',
    topic: 'education',
    topic_title: 'Education & Community',
    topic_icon: '🏫',
    collocations: ['go to school', 'high school', 'school curriculum', 'school district', 'after school']
  },
  'friend': {
    pos: 'Noun',
    phonetic: '/frend/',
    def_en: 'A person whom one knows and with whom one has a bond of mutual affection and trust.',
    def_vi: 'Bạn bè, người bạn gắn bó thân thiết và tin cậy lẫn nhau.',
    ex_en: 'A loyal friend offers comfort during times of adversity.',
    ex_vi: 'Một người bạn trung thành mang lại sự an ủi trong những lúc nghịch cảnh.',
    level: 'A1 Essential',
    topic: 'relationships',
    topic_title: 'Relationships & Trust',
    topic_icon: '🤝',
    collocations: ['close friend', 'make friends', 'childhood friend', 'loyal friend', 'circle of friends'],
    word_family: [{ pos: 'Noun', word: 'friend' }, { pos: 'Noun', word: 'friendship' }, { pos: 'Adjective', word: 'friendly' }, { pos: 'Adjective', word: 'unfriendly' }]
  },
  'ability': {
    pos: 'Noun',
    phonetic: '/əˈbɪl.ə.ti/',
    def_en: 'Possession of the means or skill to do something; talent or proficiency.',
    def_vi: 'Khả năng, năng lực, tài năng làm được một việc gì đó.',
    ex_en: 'Her ability to solve complex mathematical problems impressed everyone.',
    ex_vi: 'Khả năng giải quyết các bài toán phức tạp của cô ấy khiến mọi người thán phục.',
    level: 'A2 Elementary',
    topic: 'skills',
    topic_title: 'Skills & Potential',
    topic_icon: '⚡',
    collocations: ['proven ability', 'natural ability', 'ability to adapt', 'demonstrate ability'],
    word_family: [{ pos: 'Noun', word: 'ability' }, { pos: 'Adjective', word: 'able' }, { pos: 'Verb', word: 'enable' }, { pos: 'Adjective', word: 'unable' }]
  },
  'achieve': {
    pos: 'Verb',
    phonetic: '/əˈtʃiːv/',
    def_en: 'Successfully bring about or reach a desired objective or result by effort, skill, or courage.',
    def_vi: 'Đạt được, hoàn thành mục tiêu sau khi đã nỗ lực và cố gắng.',
    ex_en: 'With consistent discipline, you can achieve your long-term ambitions.',
    ex_vi: 'Với sự kỷ luật kiên định, bạn có thể đạt được những hoài bão dài hạn của mình.',
    level: 'B1 Intermediate',
    topic: 'success',
    topic_title: 'Goals & Achievement',
    topic_icon: '🏆',
    collocations: ['achieve goals', 'achieve success', 'achieve results', 'hard to achieve'],
    word_family: [{ pos: 'Verb', word: 'achieve' }, { pos: 'Noun', word: 'achievement' }, { pos: 'Adjective', word: 'achievable' }]
  },
  'benefit': {
    pos: 'Noun / Verb',
    phonetic: '/ˈben.ɪ.fɪt/',
    def_en: 'An advantage or profit gained from something; to receive positive advantage.',
    def_vi: 'Lợi ích, phúc lợi; mang lại hoặc nhận được điều tích cực, có lợi.',
    ex_en: 'Regular physical exercise offers immense health benefits for the brain and body.',
    ex_vi: 'Tập thể dục thường xuyên mang lại vô số lợi ích sức khỏe cho cả thể chất và tinh thần.',
    level: 'A2 Elementary',
    topic: 'wellness',
    topic_title: 'Value & Growth',
    topic_icon: '🎁',
    collocations: ['mutual benefit', 'enormous benefit', 'benefit from', 'health benefits'],
    word_family: [{ pos: 'Noun / Verb', word: 'benefit' }, { pos: 'Adjective', word: 'beneficial' }, { pos: 'Adverb', word: 'beneficially' }]
  },
  'challenge': {
    pos: 'Noun / Verb',
    phonetic: '/ˈtʃæl.ɪndʒ/',
    def_en: 'A call to take part in a contest or fight; a task or situation that tests someone\'s abilities.',
    def_vi: 'Thử thách, thách thức; tình huống đòi hỏi nỗ lực và kiểm tra năng lực.',
    ex_en: 'Embracing difficult challenges is the fastest way to accelerate personal growth.',
    ex_vi: 'Đón nhận những thử thách khó khăn là con đường nhanh nhất để thúc đẩy sự trưởng thành cá nhân.',
    level: 'B1 Intermediate',
    topic: 'growth',
    topic_title: 'Adversity & Growth',
    topic_icon: '⛰️',
    collocations: ['face a challenge', 'overcome a challenge', 'major challenge', 'meet the challenge'],
    word_family: [{ pos: 'Noun / Verb', word: 'challenge' }, { pos: 'Adjective', word: 'challenging' }]
  },
  'develop': {
    pos: 'Verb',
    phonetic: '/dɪˈvel.əp/',
    def_en: 'Grow or cause to grow and become more mature, advanced, or elaborate.',
    def_vi: 'Phát triển, mở rộng, hoàn thiện, tiến hóa lên mức độ cao hơn.',
    ex_en: 'Engineers continuously develop new software features to enhance user security.',
    ex_vi: 'Các kỹ sư liên tục phát triển những tính năng phần mềm mới để nâng cao tính bảo mật cho người dùng.',
    level: 'A2 Elementary',
    topic: 'technology',
    topic_title: 'Growth & Innovation',
    topic_icon: '🚀',
    collocations: ['develop skills', 'develop software', 'develop strategy', 'rapidly develop'],
    word_family: [{ pos: 'Verb', word: 'develop' }, { pos: 'Noun', word: 'development' }, { pos: 'Noun', word: 'developer' }, { pos: 'Adjective', word: 'developed' }]
  },
  'education': {
    pos: 'Noun',
    phonetic: '/ˌedʒ.ʊˈkeɪ.ʃən/',
    def_en: 'The process of receiving or giving systematic instruction, especially at a school or university.',
    def_vi: 'Giáo dục, sự dạy dỗ, quá trình tiếp thu kiến thức và kỹ năng có hệ thống.',
    ex_en: 'Quality education empowers individuals to build a prosperous future.',
    ex_vi: 'Nền giáo dục chất lượng trao quyền cho các cá nhân xây dựng một tương lai thịnh vượng.',
    level: 'A1 Essential',
    topic: 'education',
    topic_title: 'Learning & Society',
    topic_icon: '🎓',
    collocations: ['higher education', 'quality education', 'pursue education', 'education system'],
    word_family: [{ pos: 'Noun', word: 'education' }, { pos: 'Verb', word: 'educate' }, { pos: 'Adjective', word: 'educational' }]
  },
  'environment': {
    pos: 'Noun',
    phonetic: '/ɪnˈvaɪ.rən.mənt/',
    def_en: 'The surroundings or conditions in which a person, animal, or plant lives or operates; the natural world.',
    def_vi: 'Môi trường sống, môi trường tự nhiên xung quanh; điều kiện và hoàn cảnh sinh hoạt.',
    ex_en: 'Protecting the natural environment is a collective responsibility for all nations.',
    ex_vi: 'Bảo vệ môi trường tự nhiên là trách nhiệm chung của tất cả các quốc gia.',
    level: 'B1 Intermediate',
    topic: 'environment',
    topic_title: 'Ecology & Nature',
    topic_icon: '🌍',
    collocations: ['protect the environment', 'work environment', 'natural environment', 'environmental protection'],
    word_family: [{ pos: 'Noun', word: 'environment' }, { pos: 'Adjective', word: 'environmental' }, { pos: 'Noun', word: 'environmentalist' }]
  },
  'experience': {
    pos: 'Noun / Verb',
    phonetic: '/ɪkˈspɪə.ri.əns/',
    def_en: 'Practical contact with and observation of facts or events; knowledge or skill gained over time.',
    def_vi: 'Kinh nghiệm, sự trải nghiệm, sự từng trải; trải qua một sự việc.',
    ex_en: 'Hands-on experience is often more valuable than pure theoretical study.',
    ex_vi: 'Kinh nghiệm thực hành thường có giá trị hơn rất nhiều so với lý thuyết thuần túy.',
    level: 'A2 Elementary',
    topic: 'career',
    topic_title: 'Wisdom & Life',
    topic_icon: '🧭',
    collocations: ['gain experience', 'hands-on experience', 'valuable experience', 'past experience'],
    word_family: [{ pos: 'Noun / Verb', word: 'experience' }, { pos: 'Adjective', word: 'experienced' }, { pos: 'Adjective', word: 'inexperienced' }]
  },
  'focus': {
    pos: 'Noun / Verb',
    phonetic: '/ˈfəʊ.kəs/',
    def_en: 'The center of interest or activity; to direct attention.',
    def_vi: 'Sự tập trung, tâm điểm; hướng toàn bộ sự chú ý vào một mục tiêu.',
    ex_en: 'Deep focus allows creative professionals to produce high-caliber work quickly.',
    ex_vi: 'Sự tập trung sâu giúp các chuyên gia sáng tạo tạo ra những sản phẩm chất lượng cao nhanh chóng.',
    level: 'A2 Elementary',
    topic: 'mindset',
    topic_title: 'Mindset & Concentration',
    topic_icon: '🎯',
    collocations: ['maintain focus', 'focus on', 'laser focus', 'primary focus'],
    word_family: [{ pos: 'Noun / Verb', word: 'focus' }, { pos: 'Adjective', word: 'focused' }]
  },
  'unpleasant': {
    pos: 'Adjective',
    phonetic: '/ʌnˈplez.ənt/',
    def_en: 'Causing discomfort, dissatisfaction, or unhappiness; disagreeable or offensive.',
    def_vi: 'Khó chịu, không vừa ý, làm phiền lòng, đáng ghét; gây cảm giác không thoải mái.',
    ex_en: 'The medicine had an unpleasant taste, but it cured the fever quickly.',
    ex_vi: 'Thuốc có vị khá khó chịu nhưng đã hạ cơn sốt rất nhanh chóng.',
    level: 'B1 Intermediate',
    topic: 'feelings',
    topic_title: 'Sensations & Feelings',
    topic_icon: '😣',
    collocations: ['unpleasant smell', 'unpleasant surprise', 'unpleasant experience', 'unpleasant truth'],
    word_family: [{ pos: 'Adjective', word: 'unpleasant' }, { pos: 'Adjective', word: 'pleasant' }, { pos: 'Noun', word: 'unpleasantness' }]
  },
  'knowledge': {
    pos: 'Noun',
    phonetic: '/ˈnɒl.ɪdʒ/',
    def_en: 'Facts, information, and skills acquired through experience or education.',
    def_vi: 'Tri thức, kiến thức, sự hiểu biết tích lũy qua học tập và trải nghiệm thực tế.',
    ex_en: 'Continuous reading expands your knowledge base and sharpens critical thinking.',
    ex_vi: 'Đọc sách liên tục mở rộng kho tàng tri thức và rèn giũa tư duy phản biện của bạn.',
    level: 'A2 Elementary',
    topic: 'education',
    topic_title: 'Wisdom & Learning',
    topic_icon: '🧠',
    collocations: ['gain knowledge', 'profound knowledge', 'knowledge base', 'knowledge transfer'],
    word_family: [{ pos: 'Noun', word: 'knowledge' }, { pos: 'Verb', word: 'know' }, { pos: 'Adjective', word: 'knowledgeable' }]
  },
  'opportunity': {
    pos: 'Noun',
    phonetic: '/ˌɒp.əˈtʃuː.nə.ti/',
    def_en: 'A set of circumstances that makes it possible to do something; a favorable chance for advancement.',
    def_vi: 'Cơ hội, thời cơ, dịp thuận lợi để thực hiện hoặc đạt được điều gì đó.',
    ex_en: 'Every unexpected challenge carries within it the seed of an equal opportunity.',
    ex_vi: 'Mỗi thử thách bất ngờ đều mang trong mình hạt mầm của một cơ hội tương đương.',
    level: 'B1 Intermediate',
    topic: 'career',
    topic_title: 'Growth & Advancement',
    topic_icon: '🚪',
    collocations: ['seize an opportunity', 'golden opportunity', 'miss an opportunity', 'equal opportunity'],
    word_family: [{ pos: 'Noun', word: 'opportunity' }, { pos: 'Adjective', word: 'opportune' }]
  }
};

/**
 * Searches the high-frequency comprehensive lexicon instantly (0ms)
 */
export function lookupInComprehensiveLexicon(rawQuery: string): SmartWordResult | null {
  const query = rawQuery.trim().toLowerCase();
  const entry = COMPREHENSIVE_LEXICON_DATA[query];
  if (!entry) return null;

  const wordObj = new backend.Word({
    id: Date.now(),
    word: query,
    raw_word: query,
    pos: entry.pos,
    phonetic: entry.phonetic,
    definition_en: entry.def_en,
    definition_vi: entry.def_vi,
    example_en: entry.ex_en,
    example_vi: entry.ex_vi,
    level: entry.level || 'A2 Elementary',
    topic: entry.topic || 'vocabulary',
    topic_title: entry.topic_title || 'Core Lexicon',
    topic_icon: entry.topic_icon || '📖',
    dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(query)}`
  });

  const examples: BilingualExample[] = [
    { en: entry.ex_en, vi: entry.ex_vi }
  ];

  return {
    word: wordObj,
    isLocal: true,
    synonyms: entry.synonyms || [],
    antonyms: entry.antonyms || [],
    collocations: entry.collocations || [],
    word_family: entry.word_family || [],
    etymology: entry.etymology || '',
    mnemonic_hook: entry.mnemonic_hook || '',
    examples,
    nuance_tips: '',
    source: 'lexicon'
  };
}
