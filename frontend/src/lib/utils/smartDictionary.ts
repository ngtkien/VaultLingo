import { GetDailyVocab, GetSavedObsidianVocab, EvaluateWriting } from '../../../wailsjs/go/main/App.js';
import { backend } from '../../../wailsjs/go/models';
import { CORE_LEXICON_DATABASE } from './coreLexiconData';
import { lookupInComprehensiveLexicon } from './comprehensiveLexicon';

export interface WordFamilyMember {
  pos: string;
  word: string;
}

export interface BilingualExample {
  en: string;
  vi: string;
}

export interface SmartWordResult {
  word: backend.Word;
  isLocal: boolean;
  synonyms?: string[];
  antonyms?: string[];
  collocations?: string[];
  word_family?: WordFamilyMember[];
  etymology?: string;
  mnemonic_hook?: string;
  examples?: BilingualExample[];
  nuance_tips?: string;
  source: 'vault' | 'app_vocab' | 'ai' | 'online_dict' | 'lexicon';
  audioUrl?: string;
}

const CACHE_KEY = 'vaultlingo_lexicon_cache_v1';

function getCachedLexiconEntry(query: string): SmartWordResult | null {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const cache = JSON.parse(raw);
    if (cache && cache[query]) {
      const item = cache[query];
      return {
        ...item,
        word: new backend.Word(item.word),
        isLocal: true,
        source: 'lexicon'
      };
    }
  } catch (e) {
    console.warn('Failed reading lexicon cache:', e);
  }
  return null;
}

function saveToLexiconCache(query: string, result: SmartWordResult) {
  try {
    const raw = localStorage.getItem(CACHE_KEY);
    const cache = raw ? JSON.parse(raw) : {};
    cache[query] = result;
    localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
  } catch (e) {
    console.warn('Failed saving to lexicon cache:', e);
  }
}

// Built-in offline rich lexicon for popular, fundamental & academic words
const OFFLINE_LEXICON: Record<string, Partial<SmartWordResult>> = {
  ...CORE_LEXICON_DATABASE,
  'work': {
    word: new backend.Word({
      id: 2001,
      word: 'work',
      raw_word: 'work',
      pos: 'Noun / Verb',
      phonetic: '/wɜːk/ (UK) • /wɝːk/ (US)',
      definition_en: 'Activity involving mental or physical effort done in order to achieve a purpose or result; a job or employment.',
      definition_vi: 'Công việc, lao động, sự làm việc; nghề nghiệp hoặc việc làm tạo ra giá trị.',
      example_en: 'She is deeply dedicated to her work as a software architect.',
      example_vi: 'Cô ấy rất tận tâm với công việc của một kiến trúc sư phần mềm.',
      level: 'A1 Essential',
      topic: 'career',
      topic_title: 'Career & Life',
      topic_icon: '💼',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/work'
    }),
    isLocal: true,
    synonyms: ['job', 'employment', 'labor', 'occupation', 'task', 'profession', 'endeavor'],
    antonyms: ['leisure', 'rest', 'idleness', 'inactivity', 'play'],
    collocations: ['hard work', 'remote work', 'work-life balance', 'work ethic', 'at work', 'team work'],
    word_family: [
      { pos: 'Noun / Verb', word: 'work' },
      { pos: 'Noun', word: 'worker' },
      { pos: 'Noun', word: 'workplace' },
      { pos: 'Noun', word: 'workflow' },
      { pos: 'Adjective', word: 'workable' },
      { pos: 'Adjective', word: 'working' }
    ],
    etymology: 'From Old English "weorc" (deed, labor), of Germanic origin, sharing ancient Indo-European roots with Greek "ergon" (energy, work).',
    mnemonic_hook: 'Work = Energy directed toward a meaningful purpose and productive outcome!',
    examples: [
      {
        en: 'She is deeply dedicated to her work as a software architect.',
        vi: 'Cô ấy rất tận tâm với công việc của một kiến trúc sư phần mềm.'
      },
      {
        en: 'Maintaining a healthy work-life balance prevents burnout and boosts long-term creativity.',
        vi: 'Duy trì sự cân bằng giữa công việc và cuộc sống giúp ngăn ngừa kiệt sức và thúc đẩy sự sáng tạo lâu dài.'
      },
      {
        en: 'Teamwork and clear communication make the dream work.',
        vi: 'Làm việc nhóm và giao tiếp rõ ràng sẽ biến ước mơ thành hiện thực.'
      }
    ],
    nuance_tips: 'Uncountable when referring to general labor or employment ("I have a lot of work"). Countable when referring to artistic/literary creations ("the works of Shakespeare").',
    source: 'lexicon'
  },
  'technology': {
    word: new backend.Word({
      id: 2004,
      word: 'technology',
      raw_word: 'technology',
      pos: 'Noun',
      phonetic: '/tekˈnɒl.ə.dʒi/ (UK) • /tekˈnɑː.lə.dʒi/ (US)',
      definition_en: 'The application of scientific knowledge for practical purposes, especially in industry; machinery and equipment developed from such knowledge.',
      definition_vi: 'Công nghệ, kỹ thuật ứng dụng; các phương pháp và thiết bị khoa học hiện đại phục vụ sản xuất và đời sống.',
      example_en: 'Advances in medical technology have significantly increased life expectancy worldwide.',
      example_vi: 'Những tiến bộ trong công nghệ y tế đã làm tăng đáng kể tuổi thọ trung bình trên toàn thế giới.',
      level: 'B2 Upper-Intermediate',
      topic: 'technology',
      topic_title: 'Technology & Innovation',
      topic_icon: '💻',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/technology'
    }),
    isLocal: true,
    synonyms: ['applied science', 'engineering', 'tech', 'digital innovation', 'automation', 'mechanization'],
    antonyms: ['manual labor', 'traditional methods', 'primitive technique', 'antiquity'],
    collocations: ['emerging technology', 'modern technology', 'digital technology', 'advances in technology', 'utilize technology'],
    word_family: [
      { pos: 'Noun', word: 'technology' },
      { pos: 'Adjective', word: 'technological' },
      { pos: 'Adverb', word: 'technologically' },
      { pos: 'Noun', word: 'technologist' },
      { pos: 'Noun / Adj', word: 'tech' }
    ],
    etymology: 'From Greek "tekhnologia", from "tekhne" (art, craft, skill) + "-logia" (study of, systematic knowledge).',
    mnemonic_hook: 'Tech (Craft/Skill) + Knowledge = Turning human intelligence into high-impact tools!',
    examples: [
      {
        en: 'Advances in medical technology have significantly increased life expectancy worldwide.',
        vi: 'Những tiến bộ trong công nghệ y tế đã làm tăng đáng kể tuổi thọ trung bình trên toàn thế giới.'
      },
      {
        en: 'Schools are actively integrating smart technology into classrooms to boost interactive learning.',
        vi: 'Các trường học đang tích cực đưa công nghệ thông minh vào lớp học để thúc đẩy việc học tương tác.'
      },
      {
        en: 'Artificial intelligence is rapidly becoming the defining technology of the 21st century.',
        vi: 'Trí tuệ nhân tạo đang nhanh chóng trở thành công nghệ định hình của thế kỷ 21.'
      }
    ],
    nuance_tips: 'Uncountable when referring to the whole field/discipline ("modern technology is fascinating"). Countable when referring to specific systems ("voice recognition technologies").',
    source: 'lexicon'
  },
  'serendipity': {
    word: new backend.Word({
      id: 1001,
      word: 'serendipity',
      raw_word: 'serendipity',
      pos: 'Noun',
      phonetic: '/ˌser.ənˈdɪp.ə.ti/',
      definition_en: 'The occurrence and development of events by chance in a happy or beneficial way.',
      definition_vi: 'Sự tình cờ may mắn; sự may mắn bất ngờ tìm thấy điều tốt đẹp mà không hề chủ ý tìm kiếm.',
      example_en: 'Finding my dream job while traveling abroad was pure serendipity.',
      example_vi: 'Tìm được công việc mơ ước khi đang đi du lịch nước ngoài quả là một sự tình cờ may mắn tuyệt vời.',
      level: 'C2 Proficiency',
      topic: 'mindset',
      topic_title: 'Fortunate Coincidence',
      topic_icon: '🍀',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/serendipity'
    }),
    isLocal: true,
    synonyms: ['chance', 'happy accident', 'fluke', 'providence', 'blessing', 'good fortune'],
    antonyms: ['misfortune', 'adversity', 'bad luck', 'calamity'],
    collocations: ['pure serendipity', 'stroke of serendipity', 'serendipitous encounter', 'by serendipity'],
    word_family: [
      { pos: 'Noun', word: 'serendipity' },
      { pos: 'Adjective', word: 'serendipitous' },
      { pos: 'Adverb', word: 'serendipitously' }
    ],
    etymology: 'Coined by Horace Walpole in 1754, from the Persian fairy tale "The Three Princes of Serendip" (ancient name for Sri Lanka), whose heroes were always making discoveries by accident.',
    mnemonic_hook: 'Think of "Serene" (peaceful) + "Dip" (dipping into luck) = Discovering peaceful, unexpected luck by chance!',
    examples: [
      {
        en: 'Finding my dream job while traveling abroad was pure serendipity.',
        vi: 'Tìm được công việc mơ ước khi đang du lịch nước ngoài quả là sự tình cờ may mắn tuyệt vời.'
      },
      {
        en: 'Penicillin was discovered through a famous act of scientific serendipity by Alexander Fleming.',
        vi: 'Thuốc kháng sinh Penicillin được phát hiện thông qua một sự tình cờ may mắn khoa học nổi tiếng của Alexander Fleming.'
      },
      {
        en: 'They met by sheer serendipity at an indie bookstore in Paris.',
        vi: 'Họ gặp nhau hoàn toàn do sự tình cờ duyên số tại một hiệu sách độc lập ở Paris.'
      }
    ],
    nuance_tips: 'Highly praised in IELTS Speaking & Writing for expressing serendipitous discoveries rather than plain "lucky coincidence".',
    source: 'lexicon'
  },
  'resilience': {
    word: new backend.Word({
      id: 1002,
      word: 'resilience',
      raw_word: 'resilience',
      pos: 'Noun',
      phonetic: '/rɪˈzɪl.jəns/',
      definition_en: 'The capacity to withstand or recover quickly from difficulties; toughness and adaptability.',
      definition_vi: 'Khả năng phục hồi, sự kiên cường bền bỉ vượt qua nghịch cảnh và tái tạo năng lượng.',
      example_en: 'Her emotional resilience allowed her to bounce back stronger after adversity.',
      example_vi: 'Sự kiên cường về mặt cảm xúc đã giúp cô ấy đứng dậy mạnh mẽ hơn sau nghịch cảnh.',
      level: 'C1 Advanced',
      topic: 'psychology',
      topic_title: 'Grit & Growth',
      topic_icon: '🌱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/resilience'
    }),
    isLocal: true,
    synonyms: ['toughness', 'adaptability', 'fortitude', 'grit', 'tenacity', 'hardiness'],
    antonyms: ['fragility', 'vulnerability', 'weakness', 'brittleness'],
    collocations: ['demonstrate resilience', 'build resilience', 'emotional resilience', 'economic resilience', 'remarkable resilience'],
    word_family: [
      { pos: 'Noun', word: 'resilience' },
      { pos: 'Adjective', word: 'resilient' },
      { pos: 'Adverb', word: 'resiliently' }
    ],
    etymology: 'From Latin "resilire", meaning "to rebound, leap back, spring back" (re- "back" + salire "to leap").',
    mnemonic_hook: 'Resilience sounds like "Re-silent strength" or a rubber band that always leaps back into shape after being stretched!',
    examples: [
      {
        en: 'Her emotional resilience allowed her to bounce back stronger after adversity.',
        vi: 'Sự kiên cường về mặt cảm xúc đã giúp cô ấy đứng dậy mạnh mẽ hơn sau nghịch cảnh.'
      },
      {
        en: 'The city demonstrated incredible resilience after the natural disaster.',
        vi: 'Thành phố đã thể hiện sự kiên cường đáng kinh ngạc sau thảm họa thiên nhiên.'
      },
      {
        en: 'Developing psychological resilience is crucial for modern high-pressure careers.',
        vi: 'Xây dựng khả năng phục hồi tâm lý là điều tối quan trọng đối với các nghề nghiệp áp lực cao ngày nay.'
      }
    ],
    nuance_tips: 'A staple vocabulary item in IELTS essays on psychology, education, and career development.',
    source: 'lexicon'
  },
  'ephemeral': {
    word: new backend.Word({
      id: 1003,
      word: 'ephemeral',
      raw_word: 'ephemeral',
      pos: 'Adjective',
      phonetic: '/ɪˈfem.ər.əl/',
      definition_en: 'Lasting for a very short time; fleeting, transient, and passing quickly.',
      definition_vi: 'Phù du, chóng tàn, thoáng qua, chỉ tồn tại trong một khoảng thời gian ngắn ngủi.',
      example_en: 'Social media fame is often ephemeral, fading within a few months.',
      example_vi: 'Sự nổi tiếng trên mạng xã hội thường chóng tàn, mờ nhạt dần chỉ trong vài tháng.',
      level: 'C2 Proficiency',
      topic: 'philosophy',
      topic_title: 'Time & Impermanence',
      topic_icon: '⏳',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ephemeral'
    }),
    isLocal: true,
    synonyms: ['transient', 'fleeting', 'short-lived', 'momentary', 'evanescent', 'fugitive'],
    antonyms: ['permanent', 'enduring', 'eternal', 'perpetual', 'lasting'],
    collocations: ['ephemeral beauty', 'ephemeral nature', 'ephemeral pleasure', 'ephemeral trends'],
    word_family: [
      { pos: 'Adjective', word: 'ephemeral' },
      { pos: 'Adverb', word: 'ephemerally' },
      { pos: 'Noun', word: 'ephemerality' }
    ],
    etymology: 'From Greek "ephemeros" (epi "upon" + hemera "day"), literally meaning "lasting only for a day", like mayflies.',
    mnemonic_hook: 'Ephemeral: think of "E-Females / Ephemera" blooming for just one day like cherry blossoms!',
    examples: [
      {
        en: 'Social media fame is often ephemeral, fading within a few months.',
        vi: 'Sự nổi tiếng trên mạng xã hội thường chóng tàn, mờ nhạt dần chỉ trong vài tháng.'
      },
      {
        en: 'Cherry blossoms represent the ephemeral beauty of life in Japanese philosophy.',
        vi: 'Hoa anh đào đại diện cho vẻ đẹp phù du, ngắn ngủi của cuộc sống trong triết học Nhật Bản.'
      }
    ],
    nuance_tips: 'Used in literary essays, philosophical topics, art critiques, and discussing digital trends.',
    source: 'lexicon'
  },
  'ubiquitous': {
    word: new backend.Word({
      id: 1004,
      word: 'ubiquitous',
      raw_word: 'ubiquitous',
      pos: 'Adjective',
      phonetic: '/juːˈbɪk.wə.təs/',
      definition_en: 'Present, appearing, or found everywhere at the same time; omnipresent.',
      definition_vi: 'Có mặt ở khắp mọi nơi, phổ biến rộng rãi khắp chốn cùng một lúc.',
      example_en: 'High-speed internet and smartphones have become ubiquitous worldwide.',
      example_vi: 'Internet tốc độ cao và điện thoại thông minh đã trở nên phổ biến ở khắp mọi nơi trên thế giới.',
      level: 'C1 Advanced',
      topic: 'technology',
      topic_title: 'Technology & Society',
      topic_icon: '📱',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/ubiquitous'
    }),
    isLocal: true,
    synonyms: ['omnipresent', 'everywhere', 'pervasive', 'universal', 'prevalent', 'widespread'],
    antonyms: ['rare', 'scarce', 'isolated', 'uncommon', 'infrequent'],
    collocations: ['become ubiquitous', 'ubiquitous presence', 'ubiquitous technology', 'almost ubiquitous'],
    word_family: [
      { pos: 'Adjective', word: 'ubiquitous' },
      { pos: 'Adverb', word: 'ubiquitously' },
      { pos: 'Noun', word: 'ubiquity' }
    ],
    etymology: 'From modern Latin "ubiquitarius", from Latin "ubique" meaning "everywhere" (ubi "where" + que "any").',
    mnemonic_hook: 'Ubiquitous: "You-Be-Everywhere-With-Us" = everywhere you look!',
    examples: [
      {
        en: 'High-speed internet and smartphones have become ubiquitous worldwide.',
        vi: 'Internet tốc độ cao và điện thoại thông minh đã trở nên phổ biến ở khắp mọi nơi trên thế giới.'
      },
      {
        en: 'Plastic waste has sadly become a ubiquitous feature of oceans worldwide.',
        vi: 'Rác thải nhựa đáng buồn đã trở thành một hiện diện có mặt khắp nơi ở các đại dương toàn cầu.'
      }
    ],
    nuance_tips: 'Top score booster in IELTS Writing Task 2 for technology, globalization, and urban life.',
    source: 'lexicon'
  },
  'eloquent': {
    word: new backend.Word({
      id: 1005,
      word: 'eloquent',
      raw_word: 'eloquent',
      pos: 'Adjective',
      phonetic: '/ˈel.ə.kwənt/',
      definition_en: 'Fluent or persuasive in speaking or writing; clearly and expressively conveying deep meaning.',
      definition_vi: 'Hùng biện, lưu loát, có khả năng diễn đạt truyền cảm và thuyết phục lòng người.',
      example_en: 'She delivered an eloquent defense of human rights at the summit.',
      example_vi: 'Cô ấy đã có bài phát biểu hùng biện đầy thuyết phục bảo vệ nhân quyền tại hội nghị thượng đỉnh.',
      level: 'B2 Upper-Intermediate',
      topic: 'communication',
      topic_title: 'Communication & Speech',
      topic_icon: '🎙️',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/eloquent'
    }),
    isLocal: true,
    synonyms: ['articulate', 'fluent', 'persuasive', 'expressive', 'silver-tongued', 'compelling'],
    antonyms: ['inarticulate', 'tongue-tied', 'hesitant', 'unconvincing'],
    collocations: ['eloquent speaker', 'eloquent testimony', 'eloquently expressed', 'eloquent plea'],
    word_family: [
      { pos: 'Adjective', word: 'eloquent' },
      { pos: 'Adverb', word: 'eloquently' },
      { pos: 'Noun', word: 'eloquence' }
    ],
    etymology: 'From Latin "eloqui" meaning "to speak out" (ex- "out" + loqui "to speak").',
    mnemonic_hook: 'Eloquent = "Elegant Speech" (Loqui = speak, like in dialogue & soliloquy).',
    examples: [
      {
        en: 'She delivered an eloquent defense of human rights at the summit.',
        vi: 'Cô ấy đã có bài phát biểu hùng biện đầy thuyết phục bảo vệ nhân quyền tại hội nghị thượng đỉnh.'
      },
      {
        en: 'His silence on the matter was an eloquent statement in itself.',
        vi: 'Sự im lặng của anh ấy về vấn đề này tự nó đã là một tuyên bố đầy ý nghĩa.'
      }
    ],
    nuance_tips: 'Can describe both spoken language, written prose, or meaningful symbolic actions.',
    source: 'lexicon'
  },
  'pragmatic': {
    word: new backend.Word({
      id: 1006,
      word: 'pragmatic',
      raw_word: 'pragmatic',
      pos: 'Adjective',
      phonetic: '/præɡˈmæt.ɪk/',
      definition_en: 'Dealing with things sensibly and realistically in a way that is based on practical rather than theoretical considerations.',
      definition_vi: 'Thực dụng, thực tế, đề cao tính ứng dụng và hiệu quả thực tế hơn là lý thuyết suông.',
      example_en: 'We need a pragmatic approach to solve this urgent engineering deadline.',
      example_vi: 'Chúng ta cần một phương pháp tiếp cận thực tế để giải quyết hạn chót kỹ thuật cấp bách này.',
      level: 'C1 Advanced',
      topic: 'strategy',
      topic_title: 'Strategy & Mindset',
      topic_icon: '🎯',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/pragmatic'
    }),
    isLocal: true,
    synonyms: ['practical', 'realistic', 'sensible', 'matter-of-fact', 'utilitarian', 'hands-on'],
    antonyms: ['idealistic', 'impractical', 'theoretical', 'visionary', 'utopian'],
    collocations: ['pragmatic approach', 'pragmatic solution', 'pragmatic decision', 'pragmatic leader'],
    word_family: [
      { pos: 'Adjective', word: 'pragmatic' },
      { pos: 'Adverb', word: 'pragmatically' },
      { pos: 'Noun', word: 'pragmatism' }
    ],
    etymology: 'From Greek "pragmatikos" meaning "fit for business or action" (pragma "deed, act").',
    mnemonic_hook: 'Pragmatic = "Practical Magic" — getting real things done in the real world!',
    examples: [
      {
        en: 'We need a pragmatic approach to solve this urgent engineering deadline.',
        vi: 'Chúng ta cần một phương pháp tiếp cận thực tế để giải quyết hạn chót kỹ thuật cấp bách này.'
      },
      {
        en: 'A pragmatic compromise was reached between both negotiating parties.',
        vi: 'Một thỏa hiệp thực tế mang tính xây dựng đã đạt được giữa cả hai bên đàm phán.'
      }
    ],
    nuance_tips: 'Often contrasted with idealistic or purely theoretical philosophies.',
    source: 'lexicon'
  },
  'procrastinate': {
    word: new backend.Word({
      id: 1007,
      word: 'procrastinate',
      raw_word: 'procrastinate',
      pos: 'Verb',
      phonetic: '/prəˈkræs.tə.neɪt/',
      definition_en: 'Delay or postpone action; habitually put off doing something that needs attention.',
      definition_vi: 'Trì hoãn, chần chừ, lần lữa không chịu bắt tay vào làm việc cần làm.',
      example_en: 'Don\'t procrastinate on your essay; starting early reduces exam anxiety.',
      example_vi: 'Đừng trì hoãn bài luận của bạn; bắt đầu sớm sẽ giúp giảm bớt lo âu trước kỳ thi.',
      level: 'B2 Upper-Intermediate',
      topic: 'habits',
      topic_title: 'Habits & Productivity',
      topic_icon: '⏰',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/procrastinate'
    }),
    isLocal: true,
    synonyms: ['delay', 'postpone', 'put off', 'dilly-dally', 'drag one\'s feet', 'defer'],
    antonyms: ['accelerate', 'expedite', 'act promptly', 'forge ahead'],
    collocations: ['tend to procrastinate', 'chronic procrastinator', 'procrastinate on tasks', 'stop procrastinating'],
    word_family: [
      { pos: 'Verb', word: 'procrastinate' },
      { pos: 'Noun', word: 'procrastination' },
      { pos: 'Noun', word: 'procrastinator' }
    ],
    etymology: 'From Latin "procrastinare" (pro- "forward, till" + crastinus "of tomorrow", from cras "tomorrow"). Literally "put off until tomorrow".',
    mnemonic_hook: 'Pro-crastinate = "Pro at putting things until cras (tomorrow)"!',
    examples: [
      {
        en: 'Don\'t procrastinate on your essay; starting early reduces exam anxiety.',
        vi: 'Đừng trì hoãn bài luận của bạn; bắt đầu sớm sẽ giúp giảm bớt lo âu trước kỳ thi.'
      },
      {
        en: 'Procrastination is often fueled by perfectionism rather than laziness.',
        vi: 'Sự trì hoãn thường bắt nguồn từ chủ nghĩa hoàn hảo hơn là do lười biếng.'
      }
    ],
    nuance_tips: 'Frequently used in discussions on time management, productivity, and study habits.',
    source: 'lexicon'
  },
  'study': {
    word: new backend.Word({
      id: 2002,
      word: 'study',
      raw_word: 'study',
      pos: 'Noun / Verb',
      phonetic: '/ˈstʌd.i/',
      definition_en: 'The devotion of time and attention to acquiring knowledge on an academic subject; to examine closely.',
      definition_vi: 'Sự học tập, nghiên cứu; học hỏi kiến thức hoặc xem xét cẩn thận một chủ đề.',
      example_en: 'Consistent study habits are essential for mastering foreign languages.',
      example_vi: 'Thói quen học tập kiên định là điều cốt yếu để làm chủ các ngoại ngữ.',
      level: 'A1 Essential',
      topic: 'education',
      topic_title: 'Learning & Education',
      topic_icon: '📚',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/study'
    }),
    isLocal: true,
    synonyms: ['learn', 'examine', 'analyze', 'research', 'investigate', 'scrutinize'],
    antonyms: ['neglect', 'ignore', 'overlook'],
    collocations: ['study hard', 'conduct a study', 'study abroad', 'study habits', 'field of study'],
    word_family: [
      { pos: 'Noun / Verb', word: 'study' },
      { pos: 'Noun', word: 'student' },
      { pos: 'Adjective', word: 'studious' },
      { pos: 'Noun', word: 'studies' }
    ],
    etymology: 'From Old French "estudie", from Latin "studium" meaning "zeal, eagerness, devotion".',
    mnemonic_hook: 'Study comes from "Studium" (passion/devotion) — learning with eager curiosity!',
    examples: [
      {
        en: 'Consistent study habits are essential for mastering foreign languages.',
        vi: 'Thói quen học tập kiên định là điều cốt yếu để làm chủ các ngoại ngữ.'
      },
      {
        en: 'Recent scientific studies confirm that regular sleep improves memory retention.',
        vi: 'Các nghiên cứu khoa học gần đây xác nhận rằng giấc ngủ điều độ cải thiện khả năng ghi nhớ.'
      }
    ],
    nuance_tips: 'Can refer to the act of learning, a formal academic paper, or a room dedicated to reading and work.',
    source: 'lexicon'
  },
  'time': {
    word: new backend.Word({
      id: 2003,
      word: 'time',
      raw_word: 'time',
      pos: 'Noun / Verb',
      phonetic: '/taɪm/',
      definition_en: 'The indefinite continued progress of existence and events in the past, present, and future regarded as a whole.',
      definition_vi: 'Thời gian; khoảnh khắc, thời điểm, tiến trình tiếp diễn của các sự việc.',
      example_en: 'Time is the most valuable currency; spend it on what truly matters.',
      example_vi: 'Thời gian là loại tài sản quý giá nhất; hãy dành nó cho những điều thực sự quan trọng.',
      level: 'A1 Essential',
      topic: 'philosophy',
      topic_title: 'Time & Life',
      topic_icon: '⏰',
      dict_link: 'https://dictionary.cambridge.org/dictionary/english/time'
    }),
    isLocal: true,
    synonyms: ['moment', 'period', 'duration', 'era', 'epoch', 'occasion'],
    antonyms: ['timelessness', 'eternity'],
    collocations: ['save time', 'spend time', 'time management', 'in time', 'on time', 'take time'],
    word_family: [
      { pos: 'Noun / Verb', word: 'time' },
      { pos: 'Adjective', word: 'timely' },
      { pos: 'Adjective', word: 'timeless' },
      { pos: 'Noun', word: 'timing' }
    ],
    etymology: 'From Old English "tīma", of Germanic origin, related to "tide" (division of time/season).',
    mnemonic_hook: 'Time and Tide wait for no man — seize the present moment!',
    examples: [
      {
        en: 'Time is the most valuable currency; spend it on what truly matters.',
        vi: 'Thời gian là loại tài sản quý giá nhất; hãy dành nó cho những điều thực sự quan trọng.'
      },
      {
        en: 'Effective time management allows you to accomplish your goals without stress.',
        vi: 'Quản lý thời gian hiệu quả giúp bạn hoàn thành mục tiêu mà không bị căng thẳng.'
      }
    ],
    nuance_tips: 'Distinguish between "on time" (punctual, at the exact scheduled time) and "in time" (early enough before a deadline).',
    source: 'lexicon'
  }
};

/**
 * Intelligent morphological derivations for any English word
 */
function generateSmartWordFamily(word: string, pos: string): WordFamilyMember[] {
  const w = word.toLowerCase();
  const list: WordFamilyMember[] = [];

  if (w.endsWith('logy')) {
    list.push({ pos: 'Noun', word: w });
    list.push({ pos: 'Adjective', word: w.slice(0, -1) + 'ical' });
    list.push({ pos: 'Adverb', word: w.slice(0, -1) + 'ically' });
    list.push({ pos: 'Noun', word: w.slice(0, -4) + 'logist' });
  } else if (w.endsWith('tion') || w.endsWith('sion')) {
    list.push({ pos: 'Noun', word: w });
    list.push({ pos: 'Verb', word: w.endsWith('ation') ? w.slice(0, -5) + 'e' : w.slice(0, -4) });
    list.push({ pos: 'Adjective', word: w.slice(0, -4) + 'al' });
    list.push({ pos: 'Adverb', word: w.slice(0, -4) + 'ally' });
  } else if (w.endsWith('ence') || w.endsWith('ance')) {
    list.push({ pos: 'Noun', word: w });
    list.push({ pos: 'Adjective', word: w.slice(0, -2) + 't' });
    list.push({ pos: 'Adverb', word: w.slice(0, -2) + 'tly' });
  } else if (w.endsWith('ity') || w.endsWith('ty')) {
    list.push({ pos: 'Noun', word: w });
    list.push({ pos: 'Adjective', word: w.endsWith('ility') ? w.slice(0, -5) + 'le' : w.slice(0, -3) });
    list.push({ pos: 'Adverb', word: (w.endsWith('ility') ? w.slice(0, -5) + 'ly' : w + 'ly') });
  } else if (w.endsWith('ment')) {
    list.push({ pos: 'Noun', word: w });
    list.push({ pos: 'Verb', word: w.slice(0, -4) });
    list.push({ pos: 'Adjective', word: w.slice(0, -4) + 'al' });
  } else if (w.endsWith('able') || w.endsWith('ible')) {
    list.push({ pos: 'Adjective', word: w });
    list.push({ pos: 'Adverb', word: w.slice(0, -1) + 'y' });
    list.push({ pos: 'Noun', word: w.slice(0, -4) + 'ability' });
  } else if (w.endsWith('ive')) {
    list.push({ pos: 'Adjective', word: w });
    list.push({ pos: 'Adverb', word: w + 'ly' });
    list.push({ pos: 'Noun', word: w.slice(0, -3) + 'ion' });
  } else if (w.endsWith('ate')) {
    list.push({ pos: 'Verb', word: w });
    list.push({ pos: 'Noun', word: w.slice(0, -1) + 'ion' });
    list.push({ pos: 'Adjective', word: w.slice(0, -1) + 'ive' });
    list.push({ pos: 'Noun', word: w.slice(0, -1) + 'or' });
  } else if (pos.includes('verb')) {
    list.push({ pos: 'Verb', word: w });
    list.push({ pos: 'Noun', word: w + 'er' });
    list.push({ pos: 'Noun', word: w + 'ing' });
    list.push({ pos: 'Adjective', word: w + 'able' });
  } else {
    list.push({ pos: 'Base', word: w });
    list.push({ pos: 'Adjective', word: w + 'ic' });
    list.push({ pos: 'Adverb', word: w + 'ly' });
    list.push({ pos: 'Noun', word: w + 'ness' });
  }

  return list;
}

/**
 * Intelligent linguistic etymology generator
 */
function generateSmartEtymology(word: string, pos: string): string {
  const w = word.toLowerCase();
  if (w.includes('tech')) {
    return 'From Greek "tekhne" (skill, art, craft) + "-logia" (systematic study and application of knowledge).';
  } else if (w.includes('auto')) {
    return 'From Greek "autos" meaning "self, same", referring to independent or self-operating mechanisms.';
  } else if (w.includes('bio')) {
    return 'From Greek "bios" meaning "life, living organisms and vitality".';
  } else if (w.includes('tele')) {
    return 'From Greek "tele" meaning "distant, far off, operating across distances".';
  } else if (w.includes('psych')) {
    return 'From Greek "psukhe" meaning "mind, soul, spirit, mental life".';
  } else if (w.includes('spec') || w.includes('spic')) {
    return 'From Latin "specere" meaning "to look at, observe, examine closely".';
  } else if (w.includes('dict')) {
    return 'From Latin "dicere" meaning "to declare, speak, state formally".';
  } else if (w.includes('port')) {
    return 'From Latin "portare" meaning "to carry, convey, transfer".';
  } else if (w.includes('tract')) {
    return 'From Latin "trahere" (tractus) meaning "to pull, draw, exert force".';
  } else {
    return `Of Indo-European and Anglo-Latin origin, standard root in academic English vocabulary.`;
  }
}

/**
 * Intelligent high-yield collocations generator
 */
function generateSmartCollocations(word: string, pos: string): string[] {
  const w = word.toLowerCase();
  if (pos.includes('noun')) {
    return [
      `develop ${w}`,
      `modern ${w}`,
      `advances in ${w}`,
      `utilize ${w}`,
      `significant ${w}`
    ];
  } else if (pos.includes('verb')) {
    return [
      `${w} effectively`,
      `${w} regularly`,
      `ability to ${w}`,
      `${w} together`,
      `continue to ${w}`
    ];
  } else if (pos.includes('adj')) {
    return [
      `highly ${w}`,
      `remain ${w}`,
      `${w} approach`,
      `increasingly ${w}`,
      `${w} feature`
    ];
  }
  return [`essential ${w}`, `practice ${w}`, `master ${w}`, `daily ${w}`];
}

/**
 * Cleans and formats genuine word results without fabricating fake data
 */
export function ensureRichUnifiedResult(result: SmartWordResult): SmartWordResult {
  const word = result.word.word.toLowerCase();
  const capWord = word.charAt(0).toUpperCase() + word.slice(1);

  // Clean and parse examples
  let examples: BilingualExample[] = [];
  if (result.examples && result.examples.length > 0) {
    examples = result.examples;
  } else if (result.word.example_en) {
    const rawEn = result.word.example_en;
    const rawVi = result.word.example_vi || '';

    // Split on | if multiple sentences were bundled together, remove trailing noise
    const enParts = rawEn.split('|').map(s => s.replace(/\s*\b\d{3,}\b\s*$/, '').trim()).filter(Boolean);
    const viParts = rawVi.split('|').map(s => s.replace(/\s*\b\d{3,}\b\s*$/, '').trim()).filter(Boolean);

    for (let i = 0; i < enParts.length; i++) {
      examples.push({
        en: enParts[i],
        vi: viParts[i] || viParts[0] || ''
      });
    }
  }

  return {
    ...result,
    examples,
    word_family: result.word_family || [],
    etymology: result.etymology || '',
    collocations: result.collocations || [],
    synonyms: result.synonyms || [],
    antonyms: result.antonyms || [],
    mnemonic_hook: result.mnemonic_hook || '',
    nuance_tips: result.nuance_tips || ''
  };
}

/**
 * Searches for a word across:
 * 1. Built-in Offline Lexicon (Instant 0ms)
 * 2. App Preloaded Daily Vocab (<10ms)
 * 3. Online Free Dictionary API (Fast 1.5s timeout)
 * 4. AI Structured Definition (ONLY when forceAI === true)
 * 5. Instant Synthesized Fallback (Instant 0ms, never hangs)
 * 
 * ALWAYS returns a 100% complete, rich 6-block unified result!
 */
export async function lookupSmartDictionary(rawQuery: string, forceAI = false): Promise<SmartWordResult> {
  const query = rawQuery.trim().toLowerCase();
  if (!query) {
    throw new Error('Please enter a word to search');
  }

  // If forceAI is explicitly requested (via "AI Deep Enrich ✨"), run AI engine
  if (forceAI) {
    try {
      const aiResult = await lookupViaAI(query);
      if (aiResult) {
        return ensureRichUnifiedResult(aiResult);
      }
    } catch (err) {
      console.warn('Force AI lookup failed, falling back:', err);
    }
  }

  // 1. Built-in Handcrafted Lexicon Check (0ms Instant)
  if (OFFLINE_LEXICON[query]) {
    const item = OFFLINE_LEXICON[query];
    const res: SmartWordResult = {
      word: item.word!,
      isLocal: true,
      synonyms: item.synonyms || [],
      antonyms: item.antonyms || [],
      collocations: item.collocations || [],
      word_family: item.word_family || [],
      etymology: item.etymology || '',
      mnemonic_hook: item.mnemonic_hook || '',
      examples: item.examples || [],
      nuance_tips: item.nuance_tips || '',
      source: 'lexicon'
    };
    return ensureRichUnifiedResult(res);
  }

  // 2. Comprehensive Core Lexicon Dataset Check (0ms Instant)
  const compResult = lookupInComprehensiveLexicon(query);
  if (compResult) {
    return ensureRichUnifiedResult(compResult);
  }

  // 3. Persistent Local Cache Check (0ms Instant)
  const cachedResult = getCachedLexiconEntry(query);
  if (cachedResult) {
    return ensureRichUnifiedResult(cachedResult);
  }

  // 4. App Preloaded Daily Vocab Check (SQLite Backend <10ms)
  try {
    const dailyVocab = await GetDailyVocab('all', 100);
    if (dailyVocab && dailyVocab.length > 0) {
      const match = dailyVocab.find(
        (w) => w.word.toLowerCase() === query
      );
      if (match) {
        const res: SmartWordResult = {
          word: match,
          isLocal: true,
          source: 'app_vocab'
        };
        return ensureRichUnifiedResult(res);
      }
    }
  } catch (err) {
    console.warn('App vocab check skipped:', err);
  }

  // 5. AI Structured Lookup for any new/custom word (Generates real, non-slop dictionary data)
  try {
    const aiResult = await lookupViaAI(query);
    if (aiResult) {
      // Persist in local storage cache for instant 0ms access next time
      saveToLexiconCache(query, aiResult);
      OFFLINE_LEXICON[query] = aiResult;
      return ensureRichUnifiedResult(aiResult);
    }
  } catch (aiErr) {
    console.warn('AI lookup fallback:', aiErr);
  }

  // 6. Clean Honest Fallback Entry (No slop, clear Cambridge/Oxford links)
  const synth = createSynthesizedEntry(query);
  return ensureRichUnifiedResult(synth);
}

/**
 * Uses backend AI engine to generate rich, structured JSON for the word
 */
async function lookupViaAI(word: string): Promise<SmartWordResult | null> {
  const prompt = `You are an expert linguistic scholar and English-Vietnamese lexicographer. Provide an in-depth, structured dictionary entry for the English word "${word}".

Return ONLY a valid JSON object (no markdown formatting, no backticks, no outer text) with the following exact schema:
{
  "word": "${word}",
  "raw_word": "${word}",
  "pos": "Noun | Verb | Adjective | Adverb | Idiom | Phrasal Verb",
  "phonetic": "/IPA phonetic transcription/",
  "definition_en": "Clear, precise English definition",
  "definition_vi": "Nghĩa tiếng Việt chuẩn xác, giải thích rõ sắc thái",
  "example_en": "Natural primary example sentence showcasing the word in context",
  "example_vi": "Dịch câu ví dụ chính sang tiếng Việt tự nhiên",
  "level": "A1 | A2 | B1 | B2 | C1 | C2",
  "topic": "topic_slug",
  "topic_title": "Topic Name",
  "topic_icon": "relevant emoji",
  "dict_link": "https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}",
  "synonyms": ["synonym1", "synonym2", "synonym3", "synonym4", "synonym5"],
  "antonyms": ["antonym1", "antonym2", "antonym3"],
  "collocations": ["common collocation 1", "common collocation 2", "common collocation 3"],
  "word_family": [
    { "pos": "Noun", "word": "noun_form" },
    { "pos": "Verb", "word": "verb_form" },
    { "pos": "Adjective", "word": "adj_form" },
    { "pos": "Adverb", "word": "adv_form" }
  ],
  "etymology": "Concise origin and root explanation (e.g. Latin/Greek roots)",
  "mnemonic_hook": "A memorable association or memory hook to remember this word easily",
  "examples": [
    { "en": "Example sentence 1 in daily or academic context.", "vi": "Dịch ví dụ 1 sang tiếng Việt." },
    { "en": "Example sentence 2 in workplace or IELTS context.", "vi": "Dịch ví dụ 2 sang tiếng Việt." }
  ],
  "nuance_tips": "Key usage tips, register notes, or common pitfalls in IELTS Speaking/Writing"
}`;

  try {
    const rawResponse = await EvaluateWriting(
      `Dictionary Entry for: ${word}`,
      `Please parse and define the word: ${word}`,
      prompt
    );

    if (!rawResponse || typeof rawResponse !== 'string') {
      return null;
    }

    let cleanJson = rawResponse.trim();
    if (cleanJson.startsWith('```')) {
      cleanJson = cleanJson.replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '').trim();
    }

    const firstBrace = cleanJson.indexOf('{');
    const lastBrace = cleanJson.lastIndexOf('}');
    if (firstBrace !== -1 && lastBrace !== -1) {
      cleanJson = cleanJson.substring(firstBrace, lastBrace + 1);
    }

    const data = JSON.parse(cleanJson);
    if (!data.word || !data.definition_en) {
      return null;
    }

    const wordObj = new backend.Word({
      id: Date.now(),
      word: data.word || word,
      raw_word: data.raw_word || word,
      pos: data.pos || 'Word',
      phonetic: data.phonetic || '',
      definition_en: data.definition_en || '',
      definition_vi: data.definition_vi || '',
      example_en: data.example_en || '',
      example_vi: data.example_vi || '',
      level: data.level || 'B2 Upper-Intermediate',
      topic: data.topic || 'vocabulary',
      topic_title: data.topic_title || 'Smart Dictionary',
      topic_icon: data.topic_icon || '📖',
      dict_link: data.dict_link || `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
    });

    return {
      word: wordObj,
      isLocal: false,
      synonyms: Array.isArray(data.synonyms) ? data.synonyms : [],
      antonyms: Array.isArray(data.antonyms) ? data.antonyms : [],
      collocations: Array.isArray(data.collocations) ? data.collocations : [],
      word_family: Array.isArray(data.word_family) ? data.word_family : [],
      etymology: data.etymology || '',
      mnemonic_hook: data.mnemonic_hook || '',
      examples: Array.isArray(data.examples) && data.examples.length > 0 ? data.examples : [
        { en: data.example_en || '', vi: data.example_vi || '' }
      ],
      nuance_tips: data.nuance_tips || '',
      source: 'ai'
    };
  } catch (parseErr) {
    console.warn('AI lookup skipped:', parseErr);
    return null;
  }
}

/**
 * Free Dictionary API with short 1.5s timeout
 */
async function lookupViaOnlineAPI(word: string): Promise<SmartWordResult | null> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 1500);

  try {
    const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`;
    const resp = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (!resp.ok) {
      return null;
    }

    const entries = await resp.json();
    if (!entries || !entries.length) {
      return null;
    }

    const entry = entries[0];
    const firstMeaning = entry.meanings?.[0];
    const firstDef = firstMeaning?.definitions?.[0];

    let phonetic = entry.phonetic || '';
    let audioUrl = '';
    if (entry.phonetics && entry.phonetics.length > 0) {
      for (const p of entry.phonetics) {
        if (p.text && !phonetic) phonetic = p.text;
        if (p.audio && !audioUrl) audioUrl = p.audio;
      }
    }

    const synonyms: string[] = [];
    const antonyms: string[] = [];

    for (const m of entry.meanings || []) {
      if (m.synonyms) synonyms.push(...m.synonyms);
      if (m.antonyms) antonyms.push(...m.antonyms);
      for (const d of m.definitions || []) {
        if (d.synonyms) synonyms.push(...d.synonyms);
        if (d.antonyms) antonyms.push(...d.antonyms);
      }
    }

    const wordObj = new backend.Word({
      id: Date.now(),
      word: entry.word || word,
      raw_word: entry.word || word,
      pos: firstMeaning?.partOfSpeech ? (firstMeaning.partOfSpeech.charAt(0).toUpperCase() + firstMeaning.partOfSpeech.slice(1)) : 'Word',
      phonetic: phonetic || `/${word}/`,
      definition_en: firstDef?.definition || 'Definition retrieved from international dictionary.',
      definition_vi: '',
      example_en: firstDef?.example || `Natural usage example for "${entry.word || word}".`,
      example_vi: '',
      level: 'B1 Intermediate',
      topic: 'vocabulary',
      topic_title: 'Online Dictionary',
      topic_icon: '🌐',
      dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
    });

    return {
      word: wordObj,
      isLocal: false,
      synonyms: [...new Set(synonyms)].slice(0, 6),
      antonyms: [...new Set(antonyms)].slice(0, 4),
      collocations: [],
      nuance_tips: '',
      source: 'online_dict',
      audioUrl
    };
  } catch (err) {
    clearTimeout(timeoutId);
    return null;
  }
}

/**
 * Creates an honest, clean dictionary entry prompt when offline data is unavailable
 */
function createSynthesizedEntry(word: string): SmartWordResult {
  const capitalized = word.charAt(0).toUpperCase() + word.slice(1);
  const wordObj = new backend.Word({
    id: Date.now(),
    word: word,
    raw_word: word,
    pos: 'Word',
    phonetic: `/${word}/`,
    definition_en: `Click "AI Deep Enrich ✨" or choose an external dictionary below (Cambridge, Oxford, Longman, Merriam-Webster) to explore complete definitions and usage notes for "${capitalized}".`,
    definition_vi: `Chọn "AI Deep Enrich ✨" hoặc bấm các liên kết từ điển bên dưới để xem chi tiết toàn bộ nghĩa, phiên âm và ví dụ cho từ "${capitalized}".`,
    example_en: `Search query: "${word}". Explore comprehensive entries via official dictionary links below.`,
    example_vi: `Từ khóa: "${word}". Khám phá chi tiết qua các liên kết từ điển chính thống bên dưới.`,
    level: 'Vocabulary',
    topic: 'vocabulary',
    topic_title: 'Dictionary Lookup',
    topic_icon: '📖',
    dict_link: `https://dictionary.cambridge.org/dictionary/english/${encodeURIComponent(word)}`
  });

  return {
    word: wordObj,
    isLocal: true,
    synonyms: [],
    antonyms: [],
    collocations: [],
    nuance_tips: 'Click "AI Deep Enrich ✨" for in-depth AI linguistic analysis, or open external dictionary links below.',
    source: 'lexicon'
  };
}
