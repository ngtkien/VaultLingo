import { backend } from '../../../wailsjs/go/models';
import type { SmartWordResult } from './smartDictionary';

/**
 * High-Yield Oxford 3000 Core Vocabulary Lexicon
 * Covering top essential words across technology, science, education, work, society, psychology, mindset, and daily life.
 */
export const CORE_LEXICON_DATABASE: Record<string, Partial<SmartWordResult>> = {
  'keyboard': {
    word: new backend.Word({
      id: 2998,
      word: 'keyboard',
      raw_word: 'keyboard',
      pos: 'Noun',
      phonetic: '/ˈkiː.bɔːd/ (UK) • /ˈkiː.bɔːrd/ (US)',
      definition_en: 'A panel of keys that operate a computer, typewriter, or musical instrument.',
      definition_vi: 'Bàn phím máy tính, bàn phím điều khiển hoặc bàn phím nhạc cụ (đàn piano/organ).',
      example_en: 'She prefers using a mechanical keyboard for software engineering and writing.',
      example_vi: 'Cô ấy thích sử dụng bàn phím cơ để lập trình phần mềm và viết lách.',
      level: 'A1 Essential',
      topic: 'technology',
      topic_title: 'Hardware & Tech',
      topic_icon: '⌨️',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/keyboard'
    }),
    isLocal: true,
    synonyms: ['keypad', 'console', 'input device', 'piano keyboard'],
    antonyms: [],
    collocations: ['mechanical keyboard', 'wireless keyboard', 'type on a keyboard', 'keyboard shortcuts', 'QWERTY keyboard', 'keyboard layout'],
    word_family: [
      { pos: 'Noun', word: 'keyboard' },
      { pos: 'Noun', word: 'keyboardist' },
      { pos: 'Noun', word: 'key' },
      { pos: 'Noun', word: 'keypad' }
    ],
    etymology: 'Compound of "key" (Old English cǣg) + "board" (Old English bord). Originally designated musical instrument keys before typewriters and computers.',
    mnemonic_hook: 'Key + Board = The board of keys that unlocks digital creation with your fingertips!',
    examples: [
      {
        en: 'She prefers using a mechanical keyboard for software engineering and writing.',
        vi: 'Cô ấy thích sử dụng bàn phím cơ để lập trình phần mềm và viết lách.'
      },
      {
        en: 'Mastering keyboard shortcuts significantly boosts your daily coding efficiency.',
        vi: 'Thành thạo các phím tắt trên bàn phím giúp nâng cao đáng kể hiệu suất lập trình hàng ngày.'
      },
      {
        en: 'He played a mesmerizing melody on the electronic keyboard during the concert.',
        vi: 'Anh ấy đã chơi một giai điệu đầy mê hoặc trên cây đàn phím điện tử trong buổi hòa nhạc.'
      }
    ],
    nuance_tips: 'Countable noun. "Keyboard" refers to full alphanumeric input boards, while "keypad" refers to smaller numeric blocks (such as on ATMs or door locks).',
    source: 'lexicon'
  },
  'computer': {
    word: new backend.Word({
      id: 2997,
      word: 'computer',
      raw_word: 'computer',
      pos: 'Noun',
      phonetic: '/kəmˈpjuː.tər/ (UK) • /kəmˈpjuː.t̬ɚ/ (US)',
      definition_en: 'An electronic device for storing and processing data, typically in binary form, according to instructions given to it in a variable program.',
      definition_vi: 'Máy vi tính, thiết bị điện tử xử lý và lưu trữ dữ liệu số theo chương trình.',
      example_en: 'Modern computers can execute billions of calculations per second with remarkable precision.',
      example_vi: 'Máy tính hiện đại có thể thực hiện hàng tỷ phép tính mỗi giây với độ chính xác đáng kinh ngạc.',
      level: 'A1 Essential',
      topic: 'technology',
      topic_title: 'Computing & Digital Life',
      topic_icon: '💻',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/computer'
    }),
    isLocal: true,
    synonyms: ['PC', 'workstation', 'laptop', 'machine', 'server', 'processor'],
    antonyms: [],
    collocations: ['personal computer', 'computer science', 'computer programming', 'use a computer', 'computer network', 'computer software'],
    word_family: [
      { pos: 'Noun', word: 'computer' },
      { pos: 'Verb', word: 'compute' },
      { pos: 'Noun', word: 'computation' },
      { pos: 'Adjective', word: 'computational' },
      { pos: 'Noun', word: 'computing' }
    ],
    etymology: 'From Latin "computare" (to calculate together, reckon), from "com-" (together) + "putare" (to think, reckon). Originally designated human mathematicians.',
    mnemonic_hook: 'Compute (Calculate) + er (Machine) = The ultimate thinking and calculating machine!',
    examples: [
      {
        en: 'Modern computers can execute billions of calculations per second with remarkable precision.',
        vi: 'Máy tính hiện đại có thể thực hiện hàng tỷ phép tính mỗi giây với độ chính xác đáng kinh ngạc.'
      },
      {
        en: 'Studying computer science opens doors to innovative careers in artificial intelligence.',
        vi: 'Học ngành khoa học máy tính mở ra cánh cửa tới các nghề nghiệp đổi mới sáng tạo trong trí tuệ nhân tạo.'
      }
    ],
    nuance_tips: 'Historically referred to a person who calculated tables before electronic machines were invented in the 1940s.',
    source: 'lexicon'
  },
  'internet': {
    word: new backend.Word({
      id: 2996,
      word: 'internet',
      raw_word: 'internet',
      pos: 'Noun',
      phonetic: '/ˈɪn.tə.net/ (UK) • /ˈɪn.t̬ɚ.net/ (US)',
      definition_en: 'A global computer network providing a variety of information and communication facilities, consisting of interconnected networks.',
      definition_vi: 'Mạng internet, mạng lưới máy tính toàn cầu kết nối thông tin và liên lạc.',
      example_en: 'The internet has democratized access to education and global market opportunities.',
      example_vi: 'Mạng internet đã bình đẳng hóa việc tiếp cận giáo dục và các cơ hội thị trường toàn cầu.',
      level: 'A1 Essential',
      topic: 'technology',
      topic_title: 'Global Connectivity',
      topic_icon: '🌐',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/internet'
    }),
    isLocal: true,
    synonyms: ['World Wide Web', 'web', 'net', 'cyberspace', 'online network'],
    antonyms: ['offline network'],
    collocations: ['access the internet', 'browse the internet', 'high-speed internet', 'on the internet', 'internet connection', 'internet access'],
    word_family: [
      { pos: 'Noun', word: 'internet' },
      { pos: 'Noun', word: 'intranet' },
      { pos: 'Noun', word: 'network' },
      { pos: 'Adjective', word: 'online' }
    ],
    etymology: 'Portmanteau of "interconnected" + "network", coined in the 1970s during TCP/IP development.',
    mnemonic_hook: 'Inter (Global) + Net (Network) = The world\'s giant invisible net connecting all human knowledge!',
    examples: [
      {
        en: 'The internet has democratized access to education and global market opportunities.',
        vi: 'Mạng internet đã bình đẳng hóa việc tiếp cận giáo dục và các cơ hội thị trường toàn cầu.'
      },
      {
        en: 'Reliable internet connectivity is essential for distributed remote engineering teams.',
        vi: 'Kết nối internet ổn định là điều cốt lõi cho các đội ngũ kỹ sư làm việc từ xa.'
      }
    ],
    nuance_tips: 'Almost always preceded by "the" ("on the internet", "surf the internet").',
    source: 'lexicon'
  },
  'music': {
    word: new backend.Word({
      id: 2995,
      word: 'music',
      raw_word: 'music',
      pos: 'Noun',
      phonetic: '/ˈmjuː.zɪk/',
      definition_en: 'Vocal or instrumental sounds combined in such a way as to produce beauty of form, harmony, and expression of emotion.',
      definition_vi: 'Âm nhạc; giai điệu và thanh âm nghệ thuật thể hiện cảm xúc con người.',
      example_en: 'Listening to instrumental music improves concentration during analytical problem solving.',
      example_vi: 'Nghe nhạc không lời giúp cải thiện sự tập trung trong khi giải quyết vấn đề phân tích.',
      level: 'A1 Essential',
      topic: 'art',
      topic_title: 'Arts & Harmony',
      topic_icon: '🎵',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/music'
    }),
    isLocal: true,
    synonyms: ['melody', 'harmony', 'tune', 'song', 'composition', 'soundtrack', 'score'],
    antonyms: ['silence', 'cacophony', 'noise'],
    collocations: ['listen to music', 'play music', 'classical music', 'background music', 'music industry', 'live music'],
    word_family: [
      { pos: 'Noun', word: 'music' },
      { pos: 'Noun', word: 'musician' },
      { pos: 'Adjective', word: 'musical' },
      { pos: 'Adverb', word: 'musically' },
      { pos: 'Noun', word: 'musicality' }
    ],
    etymology: 'From Greek "mousike tekhne" (art of the Muses), the mythological patron goddesses of poetry, music, and learning.',
    mnemonic_hook: 'Music = The sacred art of the Muses that speaks directly to the heart!',
    examples: [
      {
        en: 'Listening to instrumental music improves concentration during analytical problem solving.',
        vi: 'Nghe nhạc không lời giúp cải thiện sự tập trung trong khi giải quyết vấn đề phân tích.'
      },
      {
        en: 'Music serves as a universal language that transcends cultural and linguistic barriers.',
        vi: 'Âm nhạc đóng vai trò như một ngôn ngữ phổ quát vượt qua mọi rào cản văn hóa và ngôn ngữ.'
      }
    ],
    nuance_tips: 'Uncountable noun in English (never say "a music"; use "a song", "a piece of music", or "a track").',
    source: 'lexicon'
  },
  'food': {
    word: new backend.Word({
      id: 2994,
      word: 'food',
      raw_word: 'food',
      pos: 'Noun',
      phonetic: '/fuːd/',
      definition_en: 'Any nutritious substance that people or animals eat or drink in order to maintain life and growth.',
      definition_vi: 'Thức ăn, thực phẩm, lương thực cung cấp năng lượng và duy trì sự sống.',
      example_en: 'Wholesome, nutritious food is essential for sustaining high cognitive performance.',
      example_vi: 'Thực phẩm lành mạnh, giàu dinh dưỡng là điều thiết yếu để duy trì hiệu suất tư duy cao.',
      level: 'A1 Essential',
      topic: 'health',
      topic_title: 'Health & Nutrition',
      topic_icon: '🍲',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/food'
    }),
    isLocal: true,
    synonyms: ['nourishment', 'sustenance', 'nutrition', 'cuisine', 'fare', 'meal'],
    antonyms: ['starvation', 'poison'],
    collocations: ['healthy food', 'food industry', 'organic food', 'fast food', 'food security', 'delicious food'],
    word_family: [
      { pos: 'Noun', word: 'food' },
      { pos: 'Verb', word: 'feed' },
      { pos: 'Noun', word: 'feeder' },
      { pos: 'Noun', word: 'foodstuff' }
    ],
    etymology: 'From Old English "fōda" (nourishment), of Germanic origin, closely related to "feed" and "fodder".',
    mnemonic_hook: 'Food = Fuel that revitalizes your body and mind every single day!',
    examples: [
      {
        en: 'Wholesome, nutritious food is essential for sustaining high cognitive performance.',
        vi: 'Thực phẩm lành mạnh, giàu dinh dưỡng là điều thiết yếu để duy trì hiệu suất tư duy cao.'
      },
      {
        en: 'Traditional cuisine reflects the rich cultural heritage and geography of a nation.',
        vi: 'Ẩm thực truyền thống phản ánh di sản văn hóa và địa lý phong phú của một quốc gia.'
      }
    ],
    nuance_tips: 'Uncountable in general contexts ("healthy food"). Countable ("foods") when referring to specific types ("fermented foods").',
    source: 'lexicon'
  },
  'phone': {
    word: new backend.Word({
      id: 2999,
      word: 'phone',
      raw_word: 'phone',
      pos: 'Noun / Verb',
      phonetic: '/fəʊn/ (UK) • /foʊn/ (US)',
      definition_en: 'A telephone or mobile device used for voice communication, messaging, and digital access; to contact someone by telephone.',
      definition_vi: 'Điện thoại, thiết bị liên lạc cầm tay; gọi điện thoại cho ai đó.',
      example_en: 'She answered her phone immediately when the client called.',
      example_vi: 'Cô ấy nhấc điện thoại ngay lập tức khi khách hàng gọi đến.',
      level: 'A1 Essential',
      topic: 'technology',
      topic_title: 'Communication & Tech',
      topic_icon: '📱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/phone'
    }),
    isLocal: true,
    synonyms: ['telephone', 'cellphone', 'mobile', 'smartphone', 'handset', 'call', 'ring'],
    antonyms: ['hang up'],
    collocations: ['answer the phone', 'mobile phone', 'smart phone', 'on the phone', 'phone call', 'phone number', 'pick up the phone'],
    word_family: [
      { pos: 'Noun / Verb', word: 'phone' },
      { pos: 'Noun', word: 'telephone' },
      { pos: 'Adjective', word: 'phonetic' },
      { pos: 'Noun', word: 'phonetics' }
    ],
    etymology: 'Shortened from "telephone", from Greek "tele" (far, distant) + "phone" (voice, sound). Literally "distant sound".',
    mnemonic_hook: 'Tele (Distant) + Phone (Voice) = Bringing distant voices right next to your ear!',
    examples: [
      {
        en: 'She answered her phone immediately when the client called.',
        vi: 'Cô ấy nhấc điện thoại ngay lập tức khi khách hàng gọi đến.'
      },
      {
        en: 'Smartphones have revolutionized global communication and digital commerce.',
        vi: 'Điện thoại thông minh đã cách mạng hóa truyền thông toàn cầu và thương mại số.'
      },
      {
        en: 'I will phone you tomorrow morning to confirm our meeting time.',
        vi: 'Tôi sẽ gọi điện thoại cho bạn vào sáng mai để xác nhận giờ họp.'
      }
    ],
    nuance_tips: 'Colloquial abbreviation of telephone. As a verb: "phone someone" (do NOT say "phone to someone").',
    source: 'lexicon'
  },
  'book': {
    word: new backend.Word({
      id: 3000,
      word: 'book',
      raw_word: 'book',
      pos: 'Noun / Verb',
      phonetic: '/bʊk/',
      definition_en: 'A written or printed work consisting of pages glued or sewn together along one side and bound in covers; to reserve accommodation, a seat, or tickets.',
      definition_vi: 'Quyển sách, tác phẩm viết; đặt chỗ trước, đặt vé, đăng ký trước.',
      example_en: 'She was reading an insightful book on cognitive psychology.',
      example_vi: 'Cô ấy đang đọc một cuốn sách sâu sắc về tâm lý học nhận thức.',
      level: 'A1 Essential',
      topic: 'education',
      topic_title: 'Literature & Learning',
      topic_icon: '📖',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/book'
    }),
    isLocal: true,
    synonyms: ['volume', 'publication', 'tome', 'novel', 'manual', 'reserve', 'schedule'],
    antonyms: ['cancel', 'cancel reservation'],
    collocations: ['read a book', 'write a book', 'publish a book', 'book a flight', 'book a hotel', 'open a book', 'by the book'],
    word_family: [
      { pos: 'Noun / Verb', word: 'book' },
      { pos: 'Noun', word: 'booking' },
      { pos: 'Noun', word: 'booklet' },
      { pos: 'Noun', word: 'bookstore' },
      { pos: 'Adjective', word: 'bookish' }
    ],
    etymology: 'From Old English "bōc" (document, book), of Germanic origin, traditionally linked to the beech tree ("bēce") on which ancient runes were inscribed.',
    mnemonic_hook: 'Book = Bound Pages of Knowledge — open a book to open your world!',
    examples: [
      {
        en: 'She was reading an insightful book on cognitive psychology.',
        vi: 'Cô ấy đang đọc một cuốn sách sâu sắc về tâm lý học nhận thức.'
      },
      {
        en: 'We need to book the flight tickets well in advance before prices rise.',
        vi: 'Chúng ta cần đặt vé máy bay từ sớm trước khi giá vé tăng.'
      },
      {
        en: 'Doing everything by the book ensures safety, compliance, and excellence.',
        vi: 'Làm mọi thứ đúng theo quy tắc và quy chuẩn đảm bảo tính an toàn và xuất sắc.'
      }
    ],
    nuance_tips: 'Noun: countable ("two books"). Verb: "book a flight/table". Idioms: "by the book" (strictly following rules), "in my book" (in my opinion).',
    source: 'lexicon'
  },
  'school': {
    word: new backend.Word({
      id: 3014,
      word: 'school',
      raw_word: 'school',
      pos: 'Noun / Verb',
      phonetic: '/skuːl/',
      definition_en: 'An institution for educating children or students; to educate or train someone.',
      definition_vi: 'Trường học, cơ sở giáo dục; rèn luyện, đào tạo.',
      example_en: 'Education at school shapes a child\'s worldview and social skills.',
      example_vi: 'Giáo dục tại trường học định hình thế giới quan và kỹ năng xã hội của trẻ.',
      level: 'A1 Essential',
      topic: 'education',
      topic_title: 'Education & Community',
      topic_icon: '🏫',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/school'
    }),
    isLocal: true,
    synonyms: ['academy', 'institution', 'college', 'seminary', 'train', 'educate'],
    antonyms: [],
    collocations: ['go to school', 'high school', 'school curriculum', 'school district', 'after school'],
    word_family: [
      { pos: 'Noun / Verb', word: 'school' },
      { pos: 'Noun', word: 'schooling' },
      { pos: 'Noun', word: 'schoolchild' },
      { pos: 'Adjective', word: 'scholastic' }
    ],
    etymology: 'From Greek "skhole" (leisure, philosophy, lecture), which evolved into places where lectures were held during free time.',
    mnemonic_hook: 'School comes from "Skhole" (creative leisure) — dedicated time to cultivate the mind!',
    examples: [
      {
        en: 'Education at school shapes a child\'s worldview and social skills.',
        vi: 'Giáo dục tại trường học định hình thế giới quan và kỹ năng xã hội của trẻ.'
      },
      {
        en: 'He schooled himself in modern programming languages through self-study.',
        vi: 'Anh ấy tự rèn luyện các ngôn ngữ lập trình hiện đại thông qua tự học.'
      }
    ],
    nuance_tips: 'British English often uses "at school" without an article when referring to being a student.',
    source: 'lexicon'
  },
  'friend': {
    word: new backend.Word({
      id: 3015,
      word: 'friend',
      raw_word: 'friend',
      pos: 'Noun',
      phonetic: '/frend/',
      definition_en: 'A person whom one knows and with whom one has a bond of mutual affection and trust.',
      definition_vi: 'Bạn bè, người bạn gắn bó thân thiết và tin cậy lẫn nhau.',
      example_en: 'A loyal friend offers comfort during times of adversity.',
      example_vi: 'Một người bạn trung thành mang lại sự an ủi trong những lúc nghịch cảnh.',
      level: 'A1 Essential',
      topic: 'relationships',
      topic_title: 'Relationships & Trust',
      topic_icon: '🤝',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/friend'
    }),
    isLocal: true,
    synonyms: ['companion', 'ally', 'confidant', 'pal', 'comrade', 'buddy'],
    antonyms: ['enemy', 'foe', 'adversary', 'rival'],
    collocations: ['close friend', 'make friends', 'childhood friend', 'loyal friend', 'circle of friends'],
    word_family: [
      { pos: 'Noun', word: 'friend' },
      { pos: 'Noun', word: 'friendship' },
      { pos: 'Adjective', word: 'friendly' },
      { pos: 'Adjective', word: 'unfriendly' },
      { pos: 'Noun', word: 'friendliness' }
    ],
    etymology: 'From Old English "frēond" (friend, lover), of Germanic origin, related to "frēon" (to love, free).',
    mnemonic_hook: 'Friend = Someone who makes you feel Free and Endeared!',
    examples: [
      {
        en: 'A loyal friend offers comfort during times of adversity.',
        vi: 'Một người bạn trung thành mang lại sự an ủi trong những lúc nghịch cảnh.'
      },
      {
        en: 'They have maintained a deep friendship for over twenty years.',
        vi: 'Họ đã duy trì một tình bạn sâu sắc trong suốt hơn hai mươi năm.'
      }
    ],
    nuance_tips: 'Contrast "friend" (close personal relationship) with "acquaintance" (casual person you know).',
    source: 'lexicon'
  },
  'ability': {
    word: new backend.Word({
      id: 3001,
      word: 'ability',
      raw_word: 'ability',
      pos: 'Noun',
      phonetic: '/əˈbɪl.ə.ti/',
      definition_en: 'Possession of the means or skill to do something; talent or proficiency.',
      definition_vi: 'Khả năng, năng lực, tài năng làm được một việc gì đó.',
      example_en: 'Her ability to solve complex mathematical problems impressed everyone.',
      example_vi: 'Khả năng giải quyết các bài toán phức tạp của cô ấy khiến mọi người thán phục.',
      level: 'A2 Elementary',
      topic: 'skills',
      topic_title: 'Skills & Potential',
      topic_icon: '⚡',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ability'
    }),
    isLocal: true,
    synonyms: ['capability', 'capacity', 'skill', 'talent', 'competence', 'proficiency'],
    antonyms: ['inability', 'incapacity', 'limitation', 'weakness'],
    collocations: ['proven ability', 'natural ability', 'ability to adapt', 'demonstrate ability', 'artistic ability'],
    word_family: [
      { pos: 'Noun', word: 'ability' },
      { pos: 'Adjective', word: 'able' },
      { pos: 'Verb', word: 'enable' },
      { pos: 'Adjective', word: 'unable' },
      { pos: 'Noun', word: 'inability' }
    ],
    etymology: 'From Middle English "habilite", from Latin "habilitas" (aptitude), from "habilis" (handy, capable).',
    mnemonic_hook: 'Able + ity = Having the tools and talent to make things happen!',
    examples: [
      {
        en: 'Her ability to solve complex mathematical problems impressed everyone.',
        vi: 'Khả năng giải quyết các bài toán phức tạp của cô ấy khiến mọi người thán phục.'
      },
      {
        en: 'Developing the ability to communicate clearly is essential for leadership.',
        vi: 'Phát triển khả năng giao tiếp rõ ràng là điều cốt lõi cho vai trò lãnh đạo.'
      }
    ],
    nuance_tips: 'Often paired with the preposition "to" + infinitive ("ability to lead").',
    source: 'lexicon'
  },
  'achieve': {
    word: new backend.Word({
      id: 3002,
      word: 'achieve',
      raw_word: 'achieve',
      pos: 'Verb',
      phonetic: '/əˈtʃiːv/',
      definition_en: 'Successfully bring about or reach a desired objective or result by effort, skill, or courage.',
      definition_vi: 'Đạt được, hoàn thành mục tiêu sau khi đã nỗ lực và cố gắng.',
      example_en: 'With consistent discipline, you can achieve your long-term ambitions.',
      example_vi: 'Với sự kỷ luật kiên định, bạn có thể đạt được những hoài bão dài hạn của mình.',
      level: 'B1 Intermediate',
      topic: 'success',
      topic_title: 'Goals & Achievement',
      topic_icon: '🏆',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/achieve'
    }),
    isLocal: true,
    synonyms: ['accomplish', 'attain', 'fulfill', 'reach', 'realize', 'gain'],
    antonyms: ['fail', 'lose', 'abandon', 'surrender'],
    collocations: ['achieve goals', 'achieve success', 'achieve results', 'hard to achieve', 'achieve greatness'],
    word_family: [
      { pos: 'Verb', word: 'achieve' },
      { pos: 'Noun', word: 'achievement' },
      { pos: 'Noun', word: 'achiever' },
      { pos: 'Adjective', word: 'achievable' }
    ],
    etymology: 'From Old French "achever" (to bring to an end), from "a chef" (to the head/finish line).',
    mnemonic_hook: 'Achieve = Reaching the Chief (A-Chef) summit of your goals!',
    examples: [
      {
        en: 'With consistent discipline, you can achieve your long-term ambitions.',
        vi: 'Với sự kỷ luật kiên định, bạn có thể đạt được những hoài bão dài hạn của mình.'
      },
      {
        en: 'The team achieved remarkable milestones ahead of the product launch deadline.',
        vi: 'Đội ngũ đã đạt được những cột mốc đáng kinh ngạc trước thời hạn ra mắt sản phẩm.'
      }
    ],
    nuance_tips: 'Implies effort and persistence ("achieve a goal"), distinct from simply receiving something by chance.',
    source: 'lexicon'
  },
  'benefit': {
    word: new backend.Word({
      id: 3003,
      word: 'benefit',
      raw_word: 'benefit',
      pos: 'Noun / Verb',
      phonetic: '/ˈben.ɪ.fɪt/',
      definition_en: 'An advantage or profit gained from something; to receive positive advantage.',
      definition_vi: 'Lợi ích, phúc lợi; mang lại hoặc nhận được điều tích cực, có lợi.',
      example_en: 'Regular physical exercise offers immense health benefits for the brain and body.',
      example_vi: 'Tập thể dục thường xuyên mang lại vô số lợi ích sức khỏe cho cả thể chất và tinh thần.',
      level: 'A2 Elementary',
      topic: 'wellness',
      topic_title: 'Value & Growth',
      topic_icon: '🎁',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/benefit'
    }),
    isLocal: true,
    synonyms: ['advantage', 'profit', 'gain', 'perk', 'merit', 'asset'],
    antonyms: ['drawback', 'disadvantage', 'detriment', 'harm', 'loss'],
    collocations: ['mutual benefit', 'enormous benefit', 'benefit from', 'fringe benefits', 'health benefits'],
    word_family: [
      { pos: 'Noun / Verb', word: 'benefit' },
      { pos: 'Adjective', word: 'beneficial' },
      { pos: 'Adverb', word: 'beneficially' },
      { pos: 'Noun', word: 'beneficiary' }
    ],
    etymology: 'From Latin "benefactum" (good deed), from "bene" (well, good) + "facere" (to do).',
    mnemonic_hook: 'Bene (Good) + Fit = Something good that fits into your life perfectly!',
    examples: [
      {
        en: 'Regular physical exercise offers immense health benefits for the brain and body.',
        vi: 'Tập thể dục thường xuyên mang lại vô số lợi ích sức khỏe cho cả thể chất và tinh thần.'
      },
      {
        en: 'Both organizations will benefit greatly from this international collaboration.',
        vi: 'Cả hai tổ chức sẽ hưởng lợi rất lớn từ sự hợp tác quốc tế này.'
      }
    ],
    nuance_tips: 'Can be used as a noun ("the benefits of study") or verb with "from" ("benefit from experience").',
    source: 'lexicon'
  },
  'challenge': {
    word: new backend.Word({
      id: 3004,
      word: 'challenge',
      raw_word: 'challenge',
      pos: 'Noun / Verb',
      phonetic: '/ˈtʃæl.ɪndʒ/',
      definition_en: 'A call to take part in a contest or fight; a task or situation that tests someone\'s abilities.',
      definition_vi: 'Thử thách, thách thức; tình huống đòi hỏi nỗ lực và kiểm tra năng lực.',
      example_en: 'Embracing difficult challenges is the fastest way to accelerate personal growth.',
      example_vi: 'Đón nhận những thử thách khó khăn là con đường nhanh nhất để thúc đẩy sự trưởng thành cá nhân.',
      level: 'B1 Intermediate',
      topic: 'growth',
      topic_title: 'Adversity & Growth',
      topic_icon: '⛰️',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/challenge'
    }),
    isLocal: true,
    synonyms: ['obstacle', 'trial', 'test', 'confrontation', 'hurdle', 'test of strength'],
    antonyms: ['ease', 'simplicity', 'comfort', 'peace'],
    collocations: ['face a challenge', 'overcome a challenge', 'major challenge', 'pose a challenge', 'meet the challenge'],
    word_family: [
      { pos: 'Noun / Verb', word: 'challenge' },
      { pos: 'Adjective', word: 'challenging' },
      { pos: 'Noun', word: 'challenger' }
    ],
    etymology: 'From Old French "chalenge" (dispute, false accusation), from Latin "calumnia" (trickery, legal claim).',
    mnemonic_hook: 'Challenge = A mountain that calls your inner Champion to rise!',
    examples: [
      {
        en: 'Embracing difficult challenges is the fastest way to accelerate personal growth.',
        vi: 'Đón nhận những thử thách khó khăn là con đường nhanh nhất để thúc đẩy sự trưởng thành cá nhân.'
      },
      {
        en: 'Transitioning to clean energy poses a significant economic challenge for developing countries.',
        vi: 'Chuyển đổi sang năng lượng sạch đặt ra một thách thức kinh tế lớn cho các quốc gia đang phát triển.'
      }
    ],
    nuance_tips: 'Often viewed positively in modern English as an opportunity to demonstrate skill rather than a pure problem.',
    source: 'lexicon'
  },
  'communication': {
    word: new backend.Word({
      id: 3005,
      word: 'communication',
      raw_word: 'communication',
      pos: 'Noun',
      phonetic: '/kəˌmjuː.nɪˈkeɪ.ʃən/',
      definition_en: 'The imparting or exchanging of information or news by speaking, writing, or using some other medium.',
      definition_vi: 'Sự giao tiếp, truyền đạt thông tin, sự liên lạc giữa các cá nhân hoặc tổ chức.',
      example_en: 'Transparent communication is the cornerstone of effective team collaboration.',
      example_vi: 'Giao tiếp minh bạch là nền tảng của sự hợp tác nhóm hiệu quả.',
      level: 'B1 Intermediate',
      topic: 'communication',
      topic_title: 'Language & Connection',
      topic_icon: '💬',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/communication'
    }),
    isLocal: true,
    synonyms: ['interaction', 'dialogue', 'correspondence', 'transmission', 'exchange', 'connection'],
    antonyms: ['isolation', 'silence', 'misunderstanding', 'alienation'],
    collocations: ['effective communication', 'interpersonal communication', 'communication skills', 'open communication', 'breakdown in communication'],
    word_family: [
      { pos: 'Noun', word: 'communication' },
      { pos: 'Verb', word: 'communicate' },
      { pos: 'Adjective', word: 'communicative' },
      { pos: 'Noun', word: 'communicator' }
    ],
    etymology: 'From Latin "communicare" meaning "to share, make common, impart", from "communis" (common).',
    mnemonic_hook: 'Commune + Action = Making thoughts common and shared among people!',
    examples: [
      {
        en: 'Transparent communication is the cornerstone of effective team collaboration.',
        vi: 'Giao tiếp minh bạch là nền tảng của sự hợp tác nhóm hiệu quả.'
      },
      {
        en: 'Digital communication has transformed how global businesses connect with customers.',
        vi: 'Truyền thông kỹ thuật số đã thay đổi cách thức các doanh nghiệp toàn cầu kết nối với khách hàng.'
      }
    ],
    nuance_tips: 'Uncountable when referring to the general process of exchanging ideas; countable ("communications") for networks or messages.',
    source: 'lexicon'
  },
  'develop': {
    word: new backend.Word({
      id: 3006,
      word: 'develop',
      raw_word: 'develop',
      pos: 'Verb',
      phonetic: '/dɪˈvel.əp/',
      definition_en: 'Grow or cause to grow and become more mature, advanced, or elaborate.',
      definition_vi: 'Phát triển, mở rộng, hoàn thiện, tiến hóa lên mức độ cao hơn.',
      example_en: 'Engineers continuously develop new software features to enhance user security.',
      example_vi: 'Các kỹ sư liên tục phát triển những tính năng phần mềm mới để nâng cao tính bảo mật cho người dùng.',
      level: 'A2 Elementary',
      topic: 'technology',
      topic_title: 'Growth & Innovation',
      topic_icon: '🚀',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/develop'
    }),
    isLocal: true,
    synonyms: ['expand', 'evolve', 'advance', 'cultivate', 'enhance', 'grow', 'foster'],
    antonyms: ['deteriorate', 'decline', 'stagnate', 'regress', 'wither'],
    collocations: ['develop skills', 'develop software', 'develop strategy', 'rapidly develop', 'develop potential'],
    word_family: [
      { pos: 'Verb', word: 'develop' },
      { pos: 'Noun', word: 'development' },
      { pos: 'Noun', word: 'developer' },
      { pos: 'Adjective', word: 'developed' },
      { pos: 'Adjective', word: 'developing' }
    ],
    etymology: 'From Old French "desveloper" (to unwrap, unfold), the opposite of "enveloper" (to wrap up).',
    mnemonic_hook: 'Develop = Un-wrapping (De-velop) hidden potential into full reality!',
    examples: [
      {
        en: 'Engineers continuously develop new software features to enhance user security.',
        vi: 'Các kỹ sư liên tục phát triển những tính năng phần mềm mới để nâng cao tính bảo mật cho người dùng.'
      },
      {
        en: 'She traveled abroad to develop a broader cultural perspective.',
        vi: 'Cô ấy đi du lịch nước ngoài để phát triển một góc nhìn văn hóa rộng mở hơn.'
      }
    ],
    nuance_tips: 'Frequently used in academic writing for countries ("developed/developing nations") and ideas ("develop an argument").',
    source: 'lexicon'
  },
  'education': {
    word: new backend.Word({
      id: 3007,
      word: 'education',
      raw_word: 'education',
      pos: 'Noun',
      phonetic: '/ˌedʒ.ʊˈkeɪ.ʃən/',
      definition_en: 'The process of receiving or giving systematic instruction, especially at a school or university.',
      definition_vi: 'Giáo dục, sự dạy dỗ, quá trình tiếp thu kiến thức và kỹ năng có hệ thống.',
      example_en: 'Quality education empowers individuals to build a prosperous future.',
      example_vi: 'Nền giáo dục chất lượng trao quyền cho các cá nhân xây dựng một tương lai thịnh vượng.',
      level: 'A1 Essential',
      topic: 'education',
      topic_title: 'Learning & Society',
      topic_icon: '🎓',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/education'
    }),
    isLocal: true,
    synonyms: ['schooling', 'instruction', 'pedagogy', 'training', 'tutelage', 'enlightenment'],
    antonyms: ['ignorance', 'illiteracy'],
    collocations: ['higher education', 'quality education', 'pursue education', 'formal education', 'education system'],
    word_family: [
      { pos: 'Noun', word: 'education' },
      { pos: 'Verb', word: 'educate' },
      { pos: 'Adjective', word: 'educational' },
      { pos: 'Noun', word: 'educator' }
    ],
    etymology: 'From Latin "educatio" (a breeding, bringing up), from "educere" (to lead forth, draw out potential).',
    mnemonic_hook: 'Educe (draw out) + Action = Drawing out the inner brilliance of human minds!',
    examples: [
      {
        en: 'Quality education empowers individuals to build a prosperous future.',
        vi: 'Nền giáo dục chất lượng trao quyền cho các cá nhân xây dựng một tương lai thịnh vượng.'
      },
      {
        en: 'Investing in public education yields tremendous economic returns for society.',
        vi: 'Đầu tư vào giáo dục công mang lại lợi ích kinh tế to lớn cho toàn xã hội.'
      }
    ],
    nuance_tips: 'High-frequency IELTS Task 2 topic. Contrast "formal education" (schools) with "informal education" (life experience).',
    source: 'lexicon'
  },
  'environment': {
    word: new backend.Word({
      id: 3008,
      word: 'environment',
      raw_word: 'environment',
      pos: 'Noun',
      phonetic: '/ɪnˈvaɪ.rən.mənt/',
      definition_en: 'The surroundings or conditions in which a person, animal, or plant lives or operates; the natural world.',
      definition_vi: 'Môi trường sống, môi trường tự nhiên xung quanh; điều kiện và hoàn cảnh sinh hoạt.',
      example_en: 'Protecting the natural environment is a collective responsibility for all nations.',
      example_vi: 'Bảo vệ môi trường tự nhiên là trách nhiệm chung của tất cả các quốc gia.',
      level: 'B1 Intermediate',
      topic: 'environment',
      topic_title: 'Ecology & Nature',
      topic_icon: '🌍',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/environment'
    }),
    isLocal: true,
    synonyms: ['surroundings', 'ecosystem', 'nature', 'habitat', 'milieu', 'atmosphere'],
    antonyms: ['unnatural setting'],
    collocations: ['protect the environment', 'work environment', 'natural environment', 'environmental protection', 'hostile environment'],
    word_family: [
      { pos: 'Noun', word: 'environment' },
      { pos: 'Adjective', word: 'environmental' },
      { pos: 'Adverb', word: 'environmentally' },
      { pos: 'Noun', word: 'environmentalist' }
    ],
    etymology: 'From Old French "environner" (to encircle, surround), from "environ" (around, circuit).',
    mnemonic_hook: 'Environ (Round/Around) + Ment = Everything that surrounds and sustains life around you!',
    examples: [
      {
        en: 'Protecting the natural environment is a collective responsibility for all nations.',
        vi: 'Bảo vệ môi trường tự nhiên là trách nhiệm chung của tất cả các quốc gia.'
      },
      {
        en: 'A supportive work environment encourages creative experimentation and employee loyalty.',
        vi: 'Một môi trường làm việc cởi mở khuyến khích sự thử nghiệm sáng tạo và gắn kết của nhân viên.'
      }
    ],
    nuance_tips: 'Use the definite article "the environment" when referring to the natural world and climate.',
    source: 'lexicon'
  },
  'experience': {
    word: new backend.Word({
      id: 3009,
      word: 'experience',
      raw_word: 'experience',
      pos: 'Noun / Verb',
      phonetic: '/ɪkˈspɪə.ri.əns/',
      definition_en: 'Practical contact with and observation of facts or events; knowledge or skill gained over time.',
      definition_vi: 'Kinh nghiệm, sự trải nghiệm, sự từng trải; trải qua một sự việc.',
      example_en: 'Hands-on experience is often more valuable than pure theoretical study.',
      example_vi: 'Kinh nghiệm thực hành thường có giá trị hơn rất nhiều so với lý thuyết thuần túy.',
      level: 'A2 Elementary',
      topic: 'career',
      topic_title: 'Wisdom & Life',
      topic_icon: '🧭',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/experience'
    }),
    isLocal: true,
    synonyms: ['knowledge', 'practical skill', 'encounter', 'trial', 'familiarity', 'background'],
    antonyms: ['inexperience', 'ignorance', 'naivety'],
    collocations: ['gain experience', 'hands-on experience', 'valuable experience', 'past experience', 'customer experience'],
    word_family: [
      { pos: 'Noun / Verb', word: 'experience' },
      { pos: 'Adjective', word: 'experienced' },
      { pos: 'Adjective', word: 'inexperienced' },
      { pos: 'Adjective', word: 'experiential' }
    ],
    etymology: 'From Latin "experientia" (trial, proof, experiment), from "experiri" (to try, test).',
    mnemonic_hook: 'Experiment + Persistence = Valuable Experience gained from living through it!',
    examples: [
      {
        en: 'Hands-on experience is often more valuable than pure theoretical study.',
        vi: 'Kinh nghiệm thực hành thường có giá trị hơn rất nhiều so với lý thuyết thuần túy.'
      },
      {
        en: 'Traveling alone taught her to embrace new cultures and experience independence.',
        vi: 'Đi du lịch một mình đã dạy cô ấy cách đón nhận những nền văn hóa mới và trải nghiệm sự tự lập.'
      }
    ],
    nuance_tips: 'Uncountable when referring to accumulated skill ("5 years of experience"); countable when referring to specific events ("an unforgettable experience").',
    source: 'lexicon'
  },
  'focus': {
    word: new backend.Word({
      id: 3010,
      word: 'focus',
      raw_word: 'focus',
      pos: 'Noun / Verb',
      phonetic: '/ˈfəʊ.kəs/',
      definition_en: 'The center of interest or activity; to adapt to the prevailing level of light or direct attention.',
      definition_vi: 'Sự tập trung, tâm điểm; hướng toàn bộ sự chú ý vào một mục tiêu.',
      example_en: 'Deep focus allows creative professionals to produce high-caliber work quickly.',
      example_vi: 'Sự tập trung sâu giúp các chuyên gia sáng tạo tạo ra những sản phẩm chất lượng cao nhanh chóng.',
      level: 'A2 Elementary',
      topic: 'mindset',
      topic_title: 'Mindset & Concentration',
      topic_icon: '🎯',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/focus'
    }),
    isLocal: true,
    synonyms: ['concentration', 'attention', 'center', 'core', 'focal point', 'spotlight'],
    antonyms: ['distraction', 'dispersion', 'neglect', 'carelessness'],
    collocations: ['maintain focus', 'focus on', 'laser focus', 'primary focus', 'shift focus'],
    word_family: [
      { pos: 'Noun / Verb', word: 'focus' },
      { pos: 'Adjective', word: 'focused' },
      { pos: 'Noun', word: 'focal' },
      { pos: 'Adjective', word: 'unfocused' }
    ],
    etymology: 'From Latin "focus" meaning "domestic hearth, fireplace" (the center of home warmth and light).',
    mnemonic_hook: 'Focus was the Fireplace (hearth) — the bright, warm center of all attention!',
    examples: [
      {
        en: 'Deep focus allows creative professionals to produce high-caliber work quickly.',
        vi: 'Sự tập trung sâu giúp các chuyên gia sáng tạo tạo ra những sản phẩm chất lượng cao nhanh chóng.'
      },
      {
        en: 'The keynote speaker focused on sustainable innovations in modern renewable energy.',
        vi: 'Diễn giả chính đã tập trung vào các đổi mới bền vững trong ngành năng lượng tái tạo hiện đại.'
      }
    ],
    nuance_tips: 'Always takes the preposition "on" when used as a verb ("focus on solutions").',
    source: 'lexicon'
  },
  'unpleasant': {
    word: new backend.Word({
      id: 3011,
      word: 'unpleasant',
      raw_word: 'unpleasant',
      pos: 'Adjective',
      phonetic: '/ʌnˈplez.ənt/',
      definition_en: 'Causing discomfort, dissatisfaction, or unhappiness; disagreeable or offensive to the senses or feelings.',
      definition_vi: 'Khó chịu, không vừa ý, làm phiền lòng, đáng ghét; gây cảm giác không thoải mái.',
      example_en: 'The medicine had an unpleasant taste, but it cured the fever quickly.',
      example_vi: 'Thuốc có vị khá khó chịu nhưng đã hạ cơn sốt rất nhanh chóng.',
      level: 'B1 Intermediate',
      topic: 'feelings',
      topic_title: 'Sensations & Feelings',
      topic_icon: '😣',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/unpleasant'
    }),
    isLocal: true,
    synonyms: ['disagreeable', 'distasteful', 'uncomfortable', 'offensive', 'obnoxious', 'irritating'],
    antonyms: ['pleasant', 'delightful', 'enjoyable', 'agreeable', 'comforting'],
    collocations: ['unpleasant smell', 'unpleasant surprise', 'unpleasant experience', 'unpleasant truth', 'unpleasant side effects'],
    word_family: [
      { pos: 'Adjective', word: 'unpleasant' },
      { pos: 'Adjective', word: 'pleasant' },
      { pos: 'Adverb', word: 'unpleasantly' },
      { pos: 'Noun', word: 'unpleasantness' },
      { pos: 'Verb / Noun', word: 'please' },
      { pos: 'Noun', word: 'pleasure' }
    ],
    etymology: 'Formed from prefix "un-" (not) + Old French "plaisant" (agreeable, pleasing), from Latin "placere" (to please).',
    mnemonic_hook: 'Un + Pleasant = The opposite of pleasing; something that feels uncomfortable or grating!',
    examples: [
      {
        en: 'The medicine had an unpleasant taste, but it cured the fever quickly.',
        vi: 'Thuốc có vị khá khó chịu nhưng đã hạ cơn sốt rất nhanh chóng.'
      },
      {
        en: 'She had the unpleasant task of informing the staff about the budget cuts.',
        vi: 'Cô ấy phải đảm nhận nhiệm vụ khó xử là thông báo cho nhân viên về việc cắt giảm ngân sách.'
      },
      {
        en: 'Addressing an unpleasant truth early prevents catastrophic problems later.',
        vi: 'Đối diện với sự thật mất lòng từ sớm giúp ngăn ngừa những vấn đề thảm họa về sau.'
      }
    ],
    nuance_tips: 'Commonly collocated with sensory nouns (unpleasant smell/taste) as well as social duties (unpleasant task/truth).',
    source: 'lexicon'
  },
  'knowledge': {
    word: new backend.Word({
      id: 3012,
      word: 'knowledge',
      raw_word: 'knowledge',
      pos: 'Noun',
      phonetic: '/ˈnɒl.ɪdʒ/',
      definition_en: 'Facts, information, and skills acquired through experience or education; the theoretical or practical understanding of a subject.',
      definition_vi: 'Tri thức, kiến thức, sự hiểu biết tích lũy qua học tập và trải nghiệm thực tế.',
      example_en: 'Continuous reading expands your knowledge base and sharpens critical thinking.',
      example_vi: 'Đọc sách liên tục mở rộng kho tàng tri thức và rèn giũa tư duy phản biện của bạn.',
      level: 'A2 Elementary',
      topic: 'education',
      topic_title: 'Wisdom & Learning',
      topic_icon: '🧠',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/knowledge'
    }),
    isLocal: true,
    synonyms: ['wisdom', 'understanding', 'expertise', 'insight', 'erudition', 'comprehension'],
    antonyms: ['ignorance', 'illiteracy', 'inexperience'],
    collocations: ['gain knowledge', 'profound knowledge', 'knowledge base', 'knowledge transfer', 'thirst for knowledge'],
    word_family: [
      { pos: 'Noun', word: 'knowledge' },
      { pos: 'Verb', word: 'know' },
      { pos: 'Adjective', word: 'knowledgeable' },
      { pos: 'Adverb', word: 'knowledgeably' },
      { pos: 'Verb', word: 'acknowledge' }
    ],
    etymology: 'From Middle English "knowleche", from "knowen" (to know) + suffix "-leche" (action/state).',
    mnemonic_hook: 'Know + Ledge = The standing ledge of facts and insights upon which you see the world!',
    examples: [
      {
        en: 'Continuous reading expands your knowledge base and sharpens critical thinking.',
        vi: 'Đọc sách liên tục mở rộng kho tàng tri thức và rèn giũa tư duy phản biện của bạn.'
      },
      {
        en: 'Knowledge without practical application remains merely potential power.',
        vi: 'Kiến thức mà không có sự ứng dụng thực tế thì chỉ dừng lại ở mức tiềm năng.'
      }
    ],
    nuance_tips: 'Uncountable noun in standard English (do NOT say "a knowledge" or "knowledges"; use "a wealth of knowledge").',
    source: 'lexicon'
  },
  'opportunity': {
    word: new backend.Word({
      id: 3013,
      word: 'opportunity',
      raw_word: 'opportunity',
      pos: 'Noun',
      phonetic: '/ˌɒp.əˈtʃuː.nə.ti/',
      definition_en: 'A set of circumstances that makes it possible to do something; a favorable chance for advancement.',
      definition_vi: 'Cơ hội, thời cơ, dịp thuận lợi để thực hiện hoặc đạt được điều gì đó.',
      example_en: 'Every unexpected challenge carries within it the seed of an equal opportunity.',
      example_vi: 'Mỗi thử thách bất ngờ đều mang trong mình hạt mầm của một cơ hội tương đương.',
      level: 'B1 Intermediate',
      topic: 'career',
      topic_title: 'Growth & Advancement',
      topic_icon: '🚪',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/opportunity'
    }),
    isLocal: true,
    synonyms: ['chance', 'opening', 'occasion', 'favorable moment', 'prospect', 'break'],
    antonyms: ['misfortune', 'obstacle', 'disadvantage', 'setback'],
    collocations: ['seize an opportunity', 'golden opportunity', 'miss an opportunity', 'equal opportunity', 'provide opportunity'],
    word_family: [
      { pos: 'Noun', word: 'opportunity' },
      { pos: 'Adjective', word: 'opportune' },
      { pos: 'Noun', word: 'opportunist' },
      { pos: 'Adjective', word: 'opportunistic' }
    ],
    etymology: 'From Latin "opportunitas", from "opportunus" (favorable, literally "coming toward the port/harbor").',
    mnemonic_hook: 'Port + Unity = The favorable wind blowing ships directly into the harbor of success!',
    examples: [
      {
        en: 'Every unexpected challenge carries within it the seed of an equal opportunity.',
        vi: 'Mỗi thử thách bất ngờ đều mang trong mình hạt mầm của một cơ hội tương đương.'
      },
      {
        en: 'Technological disruption creates unprecedented career opportunities for adaptable professionals.',
        vi: 'Sự đột phá công nghệ tạo ra những cơ hội nghề nghiệp chưa từng có cho những nhân sự biết thích nghi.'
      }
    ],
    nuance_tips: 'Followed by "to" + infinitive ("opportunity to learn") or "for" + noun ("opportunity for growth").',
    source: 'lexicon'
  }
};
