#!/usr/bin/env python3
"""Seed IELTS roadmap content into the bundled vocab.db.

Adds two content tables used by the Speaking Lab and Reading Lab:
  - speaking_prompts (part 1/2/3 question bank)
  - reading_passages (timed practice passages with IELTS-style questions)

Idempotent: drops and recreates both tables. Run from repo root:
    python3 scripts/seed_roadmap_content.py
"""
import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "vocab.db")

# ---------------------------------------------------------------------------
# Speaking prompt bank
# ---------------------------------------------------------------------------
# part: 1 = short answers, 2 = cue card long turn, 3 = discussion

SPEAKING_PROMPTS = [
    # ---- Part 1 (5 per topic) ----
    (1, "Work & Study", "Do you work or are you a student?", "Trả lời statement → reason → example ngắn."),
    (1, "Work & Study", "What do you find most interesting about your work or studies?", ""),
    (1, "Work & Study", "Do you prefer working in the morning or in the evening?", ""),
    (1, "Work & Study", "What skills do you need for your job or major?", ""),
    (1, "Work & Study", "Do you plan to change your job or major in the future?", ""),
    (1, "Home & Living", "Do you live in a house or an apartment?", ""),
    (1, "Home & Living", "What do you like most about your neighbourhood?", ""),
    (1, "Home & Living", "Is your home a quiet place to study?", ""),
    (1, "Home & Living", "How long have you lived there?", ""),
    (1, "Home & Living", "Would you like to move to a different place? Why?", ""),
    (1, "Hobbies & Free Time", "What do you usually do when you have free time?", ""),
    (1, "Hobbies & Free Time", "Do you prefer spending free time alone or with friends?", ""),
    (1, "Hobbies & Free Time", "Did you have the same hobbies when you were a child?", ""),
    (1, "Hobbies & Free Time", "Is there a new hobby you would like to try?", ""),
    (1, "Hobbies & Free Time", "How much free time do you have each week?", ""),
    (1, "Technology", "How often do you use a computer or smartphone?", ""),
    (1, "Technology", "What apps or devices do you use every day?", ""),
    (1, "Technology", "Do you think you spend too much time online?", ""),
    (1, "Technology", "Was it easy for you to learn to use new technology?", ""),
    (1, "Technology", "Is there any technology you do not like using?", ""),
    (1, "Education", "What subject did you enjoy most at school?", ""),
    (1, "Education", "Do you prefer studying alone or in a group?", ""),
    (1, "Education", "Is it better to learn from teachers or from the internet?", ""),
    (1, "Education", "What is the most difficult thing about learning English?", ""),
    (1, "Education", "Do you plan to study anything new this year?", ""),
    (1, "Health & Lifestyle", "Do you think you have a healthy lifestyle?", ""),
    (1, "Health & Lifestyle", "What do you do to relax after a busy day?", ""),
    (1, "Health & Lifestyle", "How many hours do you usually sleep?", ""),
    (1, "Health & Lifestyle", "Do you prefer cooking at home or eating out?", ""),
    (1, "Health & Lifestyle", "Is exercise important to you? Why?", ""),
    (1, "Environment", "Is the air clean where you live?", ""),
    (1, "Environment", "Do you recycle things at home?", ""),
    (1, "Environment", "Would you like to live closer to nature?", ""),
    (1, "Environment", "What environmental problem worries you most?", ""),
    (1, "Environment", "Do you think individuals can really help the environment?", ""),
    (1, "Daily Routine", "What is the first thing you do every morning?", ""),
    (1, "Daily Routine", "Do you follow the same routine every day?", ""),
    (1, "Daily Routine", "What part of your day do you enjoy most?", ""),
    (1, "Daily Routine", "Do you prefer planning your day or being spontaneous?", ""),
    (1, "Daily Routine", "How has your daily routine changed recently?", ""),
    # ---- Part 2 cue cards ----
    (2, "People", "Describe a person who has influenced you.", ""),
    (2, "People", "Describe a friend you enjoy spending time with.", ""),
    (2, "People", "Describe a teacher or colleague you respect.", ""),
    (2, "Places", "Describe a place you like to visit in your free time.", ""),
    (2, "Places", "Describe a city or town you would like to live in.", ""),
    (2, "Places", "Describe a quiet place where you can relax.", ""),
    (2, "Events", "Describe an important decision you made recently.", ""),
    (2, "Events", "Describe a time when you learned something new.", ""),
    (2, "Events", "Describe a difficult task you completed successfully.", ""),
    (2, "Objects", "Describe a piece of technology you find useful.", ""),
    (2, "Objects", "Describe a book or article that impressed you.", ""),
    (2, "Objects", "Describe something you own that is very old.", ""),
    (2, "Study & Work", "Describe a project you are proud of.", ""),
    (2, "Study & Work", "Describe a skill you want to improve.", ""),
    (2, "Study & Work", "Describe a time when you had to learn something quickly.", ""),
    # ---- Part 3 discussion ----
    (3, "Education", "Do you think online learning will replace classrooms?", ""),
    (3, "Education", "What makes a good teacher in your opinion?", ""),
    (3, "Education", "Should students choose their own subjects at school?", ""),
    (3, "Education", "Is it better to study abroad or in your own country?", ""),
    (3, "Technology", "How has technology changed the way people communicate?", ""),
    (3, "Technology", "Do you think social media does more harm than good?", ""),
    (3, "Technology", "Will AI create more jobs or destroy them?", ""),
    (3, "Technology", "Should children have limits on screen time?", ""),
    (3, "Environment", "Who should be responsible for protecting the environment: governments or individuals?", ""),
    (3, "Environment", "Do you think climate change can still be reversed?", ""),
    (3, "Environment", "Is public transport the best solution to pollution in cities?", ""),
    (3, "Society", "How has family life changed in your country?", ""),
    (3, "Society", "Do people work too much nowadays?", ""),
    (3, "Society", "Is it important to keep traditions alive?", ""),
    (3, "Society", "What will cities look like in fifty years?", ""),
]

# Part-2 cue bullets keyed by question text.
CUE_CARDS = {
    "Describe a person who has influenced you.": [
        "who this person is", "how you know them",
        "what they have done that influenced you", "and explain why they are important to you"],
    "Describe a friend you enjoy spending time with.": [
        "who this friend is", "when and where you met",
        "what you usually do together", "and explain why you enjoy their company"],
    "Describe a teacher or colleague you respect.": [
        "who this person is", "what they taught you or worked on with you",
        "what qualities they have", "and explain why you respect them"],
    "Describe a place you like to visit in your free time.": [
        "where it is", "how often you go there",
        "what you do there", "and explain why you like it"],
    "Describe a city or town you would like to live in.": [
        "where it is", "what it is like",
        "what you would do there", "and explain why you want to live there"],
    "Describe a quiet place where you can relax.": [
        "where it is", "when you go there",
        "what you do there", "and explain why it helps you relax"],
    "Describe an important decision you made recently.": [
        "what the decision was", "when you made it",
        "what the result was", "and explain why it was important"],
    "Describe a time when you learned something new.": [
        "what you learned", "why you decided to learn it",
        "how you learned it", "and explain how you felt about it"],
    "Describe a difficult task you completed successfully.": [
        "what the task was", "why it was difficult",
        "how you completed it", "and explain how you felt afterwards"],
    "Describe a piece of technology you find useful.": [
        "what it is", "when you started using it",
        "what you use it for", "and explain why it is useful to you"],
    "Describe a book or article that impressed you.": [
        "what it was about", "when you read it",
        "what you learned from it", "and explain why it impressed you"],
    "Describe something you own that is very old.": [
        "what it is", "how long you have had it",
        "what you use it for", "and explain why you still keep it"],
    "Describe a project you are proud of.": [
        "what the project was", "who you worked with",
        "what you did", "and explain why you are proud of it"],
    "Describe a skill you want to improve.": [
        "what the skill is", "why you want to improve it",
        "how you plan to practise", "and explain how it would help you"],
    "Describe a time when you had to learn something quickly.": [
        "what you had to learn", "why you had to learn it fast",
        "how you managed it", "and explain what the result was"],
}


# ---------------------------------------------------------------------------
# Reading passages
# ---------------------------------------------------------------------------
# questions_json: list of sections -> {type, instruction, items[]}
# types: tfng (TRUE/FALSE/NOT GIVEN), gapfill, matching_heading, mcq

def q_tfng(items):
    return {
        "type": "tfng",
        "instruction": "Do the following statements agree with the information in the passage? Write TRUE, FALSE or NOT GIVEN.",
        "items": [{"id": i + 1, "question": q, "answer": a, "explanation": e}
                  for i, (q, a, e) in enumerate(items)],
    }


def q_gapfill(start_id, instruction, items):
    return {
        "type": "gapfill",
        "instruction": instruction,
        "items": [{"id": start_id + i, "question": q, "answer": a, "explanation": e}
                  for i, (q, a, e) in enumerate(items)],
    }


def q_mcq(start_id, instruction, items):
    return {
        "type": "mcq",
        "instruction": instruction,
        "items": [{"id": start_id + i, "question": q, "options": opts,
                   "answer": a, "explanation": e}
                  for i, (q, opts, a, e) in enumerate(items)],
    }


PASSAGES = [
    # ── Passage 1 · band 5.0 · Education ──────────────────────────────
    {
        "title": "The Rise of Online Learning",
        "band_level": 5.0,
        "topic": "Education",
        "text": """Over the past two decades, online learning has moved from the margins of education to its centre. What began as simple recorded lectures uploaded to websites has grown into an industry offering interactive courses, live tutoring and internationally recognised certificates. Today, millions of students complete entire degrees without ever entering a physical classroom.

The advantages are easy to see. Students can study at their own pace, pause a lecture to take notes, and revisit difficult sections as often as they need. For people who work full-time or live far from universities, this flexibility is often the difference between studying and not studying at all. Cost is another factor: an online course usually requires no buildings, no printed materials and no travel, so tuition fees can be dramatically lower.

However, research suggests the picture is more complicated. Completion rates for online courses are famously low; on many platforms fewer than ten percent of enrolled students finish. Without the structure of a timetable and the presence of classmates, motivation tends to fade. Educators also point out that some skills are difficult to teach through a screen. Laboratory work, public speaking and teamwork all depend on real interaction, and employers still frequently prefer graduates who have practised these skills in person.

A third group of problems concerns attention. Studies of online learners show that many students watch lectures at double speed and skip readings entirely. The brain, researchers argue, does not easily form long-term memories from such rapid consumption. In addition, the same device used to study is also used for entertainment, and notifications are a constant source of interruption.

In response, many institutions now promote a "blended" model. Students watch theory videos at home and spend classroom time on discussion, practice and feedback. Early results are promising: courses redesigned this way show completion rates roughly twice as high as fully online equivalents. The lesson may be that technology works best when it supports, rather than replaces, human contact.""",
        "questions": [
            q_tfng([
                ("Online courses began as interactive live-tutoring platforms.", "FALSE",
                 "Paragraph 1 says they began as 'simple recorded lectures'; interactive courses came later."),
                ("Online learning is often the only option for people working full-time.", "TRUE",
                 "Paragraph 2: flexibility 'is often the difference between studying and not studying at all'."),
                ("Most students finish the online courses they enrol in.", "FALSE",
                 "Paragraph 3: 'fewer than ten percent of enrolled students finish'."),
                ("Employers always prefer graduates who studied online.", "FALSE",
                 "Paragraph 3 states employers 'frequently prefer' graduates with in-person skills — the opposite."),
                ("Blended courses show higher completion rates than fully online ones.", "TRUE",
                 "Final paragraph: completion rates are 'roughly twice as high'."),
            ]),
            q_gapfill(6, "Complete the sentences below. Write NO MORE THAN THREE WORDS from the passage.", [
                ("For people far from universities, flexibility can be the difference between studying and __________.", "not studying at all",
                 "Direct phrase from paragraph 2."),
                ("Laboratory work and teamwork depend on __________.", "real interaction",
                 "Paragraph 3 lists skills that 'depend on real interaction'."),
                ("Many students watch lectures at __________.", "double speed",
                 "Paragraph 4: 'watch lectures at double speed'."),
                ("In the blended model, classroom time is spent on discussion, practice and __________.", "feedback",
                 "Final paragraph: 'discussion, practice and feedback'."),
            ]),
        ],
    },
    # ── Passage 2 · band 5.0 · Technology ─────────────────────────────
    {
        "title": "How Smartphones Changed Our Memory",
        "band_level": 5.0,
        "topic": "Technology",
        "text": """Psychologists have long known that humans do not store every fact they encounter. Instead, we remember where to find things. A generation ago, people memorised telephone numbers; today most cannot recall the numbers of even their closest family members. Researchers call this tendency to rely on external storage "cognitive offloading", and smartphones have turned it into a daily habit.

A series of experiments illustrates the effect. In one study, participants who expected to look up information later were significantly worse at remembering it themselves. Simply knowing that the internet holds the answer appears to reduce the brain's effort to store it. Another experiment found that people who photographed museum objects remembered fewer details about them than people who looked without a camera.

Yet the story is not entirely negative. Offloading frees mental resources for other tasks. In one experiment, students allowed to save information to a computer performed better when learning new material afterwards. The researchers compared the process to clearing a desk: with the clutter removed, there is more space to think. Supporters of this view argue that memorising facts was never the point of education anyway; analysis and problem-solving matter more.

Critics respond that memory is not a warehouse but a workshop. Facts stored in long-term memory form the raw material of understanding; without them, critical thinking has nothing to work with. A person who knows nothing cannot evaluate what a search engine returns. There is also evidence that heavy phone use shortens attention spans, making deep reading — the kind needed for complex ideas — harder to sustain.

Most researchers now recommend a middle course: offload deliberately. Use the phone for information that does not need remembering, but practise recalling the knowledge that matters. In this view, the smartphone is neither an enemy nor a substitute brain — it is a tool whose value depends on how carefully it is used.""",
        "questions": [
            q_tfng([
                ("Most people today can remember close family phone numbers.", "FALSE",
                 "Paragraph 1: 'most cannot recall the numbers of even their closest family members'."),
                ("Knowing the internet holds an answer reduces memory effort.", "TRUE",
                 "Paragraph 2: 'Simply knowing that the internet holds the answer appears to reduce the brain's effort'."),
                ("People who photographed museum objects remembered them better.", "FALSE",
                 "Paragraph 2: they 'remembered fewer details' than those who just looked."),
                ("Saving information to a computer helped students learn new material.", "TRUE",
                 "Paragraph 3: they 'performed better when learning new material afterwards'."),
                ("All researchers believe phones damage memory.", "FALSE",
                 "Final paragraph: 'most researchers recommend a middle course', not condemnation."),
            ]),
            q_mcq(6, "Choose the correct answer.", [
                ("What is 'cognitive offloading'?",
                 ["Storing facts in long-term memory", "Relying on external storage instead of memory",
                  "Remembering phone numbers easily", "Learning through photographs"],
                 "B", "Paragraph 1 defines it as the tendency 'to rely on external storage'."),
                ("According to critics, long-term memory matters because it…",
                 ["helps us use search engines faster", "stores photographs safely",
                  "provides the raw material for understanding", "makes phones unnecessary"],
                 "C", "Paragraph 4: 'Facts stored in long-term memory form the raw material of understanding'."),
                ("What do most researchers recommend?",
                 ["Stop using smartphones", "Memorise everything",
                  "Offload deliberately and practise recall", "Use phones only for entertainment"],
                 "C", "Final paragraph: 'offload deliberately'."),
            ]),
        ],
    },
    # ── Passage 3 · band 5.5 · Environment ────────────────────────────
    {
        "title": "The Hidden Life of Urban Trees",
        "band_level": 5.5,
        "topic": "Environment",
        "text": """City trees are usually treated as decoration: a row of green to soften concrete streets. But a growing body of research suggests they are among the hardest-working pieces of infrastructure a city owns. A single mature tree can absorb more than twenty kilograms of carbon dioxide per year, filter harmful particles from the air, and lower street temperatures by several degrees during heatwaves.

The economic argument is surprisingly strong. One widely cited study in California calculated that for every dollar spent on planting and maintaining urban trees, cities received more than five dollars in benefits: cleaner air, reduced flooding, lower energy bills for cooling, and even higher property values on tree-lined streets. Trees also intercept rainwater, easing pressure on drainage systems during storms — an increasingly valuable service as rainfall becomes more intense.

Beneath the pavement, trees are connected. Through networks of fungi attached to their roots, trees exchange nutrients and chemical signals with their neighbours. Forest ecologists call this the 'wood wide web'. A healthy tree can share sugar with a sick neighbour, and a mother tree appears to favour her own seedlings. Urban planners now argue that a row of street trees is not a collection of ornaments but a community — and communities survive stress better than isolated individuals.

Yet city trees live hard lives. Confined to small pits of compacted soil, starved of water and attacked by pollution, the average street tree survives a fraction of its natural lifespan. The trees that thrive are usually those planted generously: wide pits, uncompacted soil, and space for roots to spread. Some cities now build 'suspended pavements' — engineered soil chambers beneath sidewalks — so that roots have room without breaking the concrete.

The lesson is quietly radical. Treating trees as infrastructure means budgeting for them like bridges: planting for the long term, maintaining them properly, and measuring their performance. A tree planted cheaply and abandoned is not an asset but a liability — one that dies early and has to be replaced at the city's expense.""",
        "questions": [
            q_tfng([
                ("A mature tree can absorb over 20 kg of CO2 annually.", "TRUE",
                 "Paragraph 1: 'more than twenty kilograms of carbon dioxide per year'."),
                ("Urban trees return more than five dollars per dollar spent.", "TRUE",
                 "Paragraph 2: 'more than five dollars in benefits' for every dollar."),
                ("Trees can share nutrients through fungal networks.", "TRUE",
                 "Paragraph 3 describes the 'wood wide web' exchanging nutrients."),
                ("Street trees live as long as forest trees.", "FALSE",
                 "Paragraph 4: they survive 'a fraction of their natural lifespan'."),
                ("Suspended pavements stop roots from breaking concrete.", "TRUE",
                 "Paragraph 4: roots get room 'without breaking the concrete'."),
            ]),
            q_gapfill(6, "Complete the notes below. Write NO MORE THAN TWO WORDS from the passage.", [
                ("Benefits include cleaner air, reduced flooding, lower cooling bills and higher __________.", "property values",
                 "Paragraph 2 lists the benefits."),
                ("Trees exchange nutrients and signals through networks of __________.", "fungi",
                 "Paragraph 3: 'networks of fungi attached to their roots'."),
                ("Street trees suffer from compacted soil, lack of water and __________.", "pollution",
                 "Paragraph 4: 'attacked by pollution'."),
                ("A cheap, abandoned tree is described as a __________, not an asset.", "liability",
                 "Final paragraph: 'not an asset but a liability'."),
            ]),
        ],
    },
    # ── Passage 4 · band 5.5 · Health ─────────────────────────────────
    {
        "title": "Why We Sleep",
        "band_level": 5.5,
        "topic": "Health",
        "text": """Every animal with a brain sleeps, yet for centuries nobody could say precisely why. Sleep is dangerous: a sleeping creature cannot hunt, cannot eat and cannot escape predators. That evolution kept it anyway suggests sleep performs something essential — and over the past two decades, neuroscientists have begun to discover what that is.

The first answer involves cleaning. During deep sleep, the space between brain cells expands and cerebrospinal fluid washes through in rhythmic waves, carrying away metabolic waste — including the proteins associated with Alzheimer's disease. The brain, in effect, runs its dishwasher at night. This may explain why a single sleepless night leaves thinking foggy and why chronic sleep loss is linked to long-term illness.

The second answer involves memory. Sleep does not simply store the day's experiences; it edits them. Studies show that during sleep the brain replays newly learned information, strengthens important connections and prunes weak ones. Students who slept after studying recalled significantly more than those who stayed awake — even when the waking group had more total hours to review. Motor skills improve too: pianists and athletes often find a difficult passage easier after a night's rest.

A third role is emotional regulation. The dreaming stage of sleep appears to process difficult experiences in a chemically calm environment, stripping memories of their emotional sting. People deprived of dreaming become more reactive and anxious, and several psychiatric conditions are now understood to involve disturbed sleep rather than merely causing it.

Yet modern society treats sleep as a luxury. Artificial light, late-night screens and round-the-clock work have shaved an hour or more from the average night's sleep over the past century. Public-health researchers describe the result as a quiet epidemic: shorter sleep is associated with weaker immunity, weight gain, depression and reduced productivity — the very performance the sleepless are chasing.

The prescription is old-fashioned but consistent: a cool, dark room; a regular bedtime; no screens in the last hour. In a world that prizes optimisation, the most powerful performance enhancer remains the one we do lying down.""",
        "questions": [
            q_tfng([
                ("Sleep prevents animals from escaping predators.", "TRUE",
                 "Paragraph 1: 'a sleeping creature… cannot escape predators'."),
                ("Brain-cleaning fluid flows only during deep sleep.", "NOT GIVEN",
                 "Passage says washing happens 'during deep sleep' but never claims it is exclusive to it."),
                ("Students who slept recalled more than those who stayed awake.", "TRUE",
                 "Paragraph 3 states this directly."),
                ("Dreaming removes the emotional pain from memories.", "TRUE",
                 "Paragraph 4: 'stripping memories of their emotional sting'."),
                ("Average sleep duration has fallen over the last century.", "TRUE",
                 "Paragraph 5: 'shaved an hour or more from the average night's sleep'."),
            ]),
            q_mcq(6, "Choose the correct answer.", [
                ("Why does the author call sleep 'the brain's dishwasher'?",
                 ["It fills the brain with fluid", "It removes metabolic waste",
                  "It works only at night", "It stops us dreaming"],
                 "B", "Paragraph 2: fluid 'carrying away metabolic waste'."),
                ("Sleep improves skills such as piano playing by…",
                 ["giving muscles time to rest", "replaying and strengthening new information",
                  "reducing the need for practice", "increasing practice hours"],
                 "B", "Paragraph 3: 'replays newly learned information, strengthens important connections'."),
                ("What is the 'quiet epidemic'?",
                 ["Alzheimer's disease spreading", "Too much screen time",
                  "Reduced sleep across society", "Depression among students"],
                 "C", "Paragraph 5 describes shortened sleep as the epidemic."),
            ]),
        ],
    },
    # ── Passage 5 · band 6.0 · Work ───────────────────────────────────
    {
        "title": "The Remote Work Experiment",
        "band_level": 6.0,
        "topic": "Work & Career",
        "text": """When offices around the world closed almost overnight, employers conducted an unplanned experiment on an unprecedented scale: could knowledge work survive outside the office? The results, several years on, have settled into something more complicated than either enthusiasts or sceptics predicted.

Productivity, the first concern, held up better than expected. Surveys of remote workers consistently report fewer interruptions, longer stretches of focused work and time reclaimed from commuting. One large analysis estimated that home workers gained the equivalent of an extra workday each week — time split between work tasks, rest and personal life. Yet averages hide sharp differences. Junior employees often struggled: without overhearing senior colleagues solve problems, their informal learning slowed. Several companies found that new hires took measurably longer to reach full competence remotely.

Collaboration proved more fragile. Planned video calls handled scheduled work efficiently, but innovation researchers noted a decline in 'weak ties' — the casual acquaintances between teams where unexpected ideas tend to form. Studies of communication data showed remote workers messaged their closest colleagues more and everyone else less, hardening the boundaries between groups. Creativity, which thrives on collision, suffered in ways that only became visible months later.

The office, it turned out, was not just a place to work but a device for belonging. Remote staff reported weaker attachment to their employers and higher willingness to quit — an effect economists called a hidden tax on flexibility. Companies that retained remote work most successfully tended to share three habits: deliberately scheduled in-person days, explicit norms about response times, and managers trained to evaluate outcomes rather than presence.

The experiment's real conclusion may be that location is a design choice, not a default. Work that is deep, individual and well-defined travels easily; work that is ambiguous, social or creative benefits from proximity. The organisations thriving today are those that stopped asking 'where should people work?' and started asking 'what does this task actually need?'""",
        "questions": [
            q_tfng([
                ("Remote workers experienced fewer interruptions on average.", "TRUE",
                 "Paragraph 2: 'fewer interruptions, longer stretches of focused work'."),
                ("Junior employees adapted to remote work faster than seniors.", "FALSE",
                 "Paragraph 2: 'Junior employees often struggled'; new hires took longer."),
                ("Remote workers communicated more with casual acquaintances.", "FALSE",
                 "Paragraph 3: 'messaged their closest colleagues more and everyone else less'."),
                ("Remote staff felt less loyal to their employers.", "TRUE",
                 "Paragraph 4: 'weaker attachment to their employers and higher willingness to quit'."),
                ("Successful remote companies measured hours at desks.", "FALSE",
                 "Paragraph 4: they 'evaluate outcomes rather than presence' — the opposite."),
            ]),
            q_mcq(6, "Choose the correct answer.", [
                ("What are 'weak ties'?",
                 ["Employees who rarely work", "Casual connections between different teams",
                  "Poor internet connections", "Friendships among managers"],
                 "B", "Paragraph 3: 'the casual acquaintances between teams'."),
                ("Why did creativity decline during remote work?",
                 ["People spent too long in meetings", "Fewer unexpected idea collisions occurred",
                  "Workers became less skilled", "Managers discouraged new ideas"],
                 "B", "Paragraph 3: 'Creativity, which thrives on collision, suffered'."),
                ("What does the author conclude about workplace location?",
                 ["Everyone should return to offices", "Remote work is always better",
                  "Location should match what the task needs", "Offices are obsolete"],
                 "C", "Final paragraph: 'what does this task actually need?'"),
            ]),
        ],
    },
    # ── Passage 6 · band 6.0 · Society ────────────────────────────────
    {
        "title": "The Attention Economy",
        "band_level": 6.0,
        "topic": "Society",
        "text": """In 1971, the economist Herbert Simon made a prediction that reads like a description of modern life: a wealth of information creates a poverty of attention. When information becomes abundant, he argued, attention becomes the scarce resource — and whatever captures attention captures value. Half a century later, an entire industry runs on Simon's insight.

Social media platforms, streaming services and news sites do not primarily sell content; they sell human attention to advertisers. The longer a user scrolls, the more advertisements they see, so every design decision serves engagement. Infinite scroll removes natural stopping points. Autoplay removes the moment of choice between videos. Notifications exploit the same variable-reward psychology that keeps gamblers at slot machines: the next refresh might bring something interesting.

The engineers who built these systems were often the first to worry about them. Several high-profile designers have publicly described their work as 'behavioural engineering' and confessed to installing blockers on their own phones. Their concern was not merely wasted time. Attention, they argue, is the foundation of thought; a mind continually interrupted cannot hold an idea long enough to examine it. Some researchers now speak of a 'cognitive environment' that can be polluted like air or water.

The numbers are sobering. The average smartphone user checks their device dozens of times a day, and heavy users exceed one hundred. Studies link fragmented attention to weaker reading comprehension, more errors at work and higher reported anxiety — though whether distraction causes these outcomes or merely accompanies them remains debated. What is not debated is the incentive structure: attention is the product being sold, and the market rewards whoever captures it most efficiently.

Responses have emerged at three levels. Individually, people adopt practices like notification limits, greyscale screens and scheduled 'deep work' hours. Institutionally, some schools and workplaces now protect phone-free time. Politically, regulators in several countries have proposed rules on autoplay defaults and children's feeds. Critics of regulation reply that attention has always been competed for — newspapers, radio and television fought the same battle — and that personal responsibility, not law, is the realistic defence.

Simon's prediction is no longer a prediction. The question it left open is whether attention, once spent, can be deliberately reclaimed — or whether scarcity, once created, is permanent.""",
        "questions": [
            q_tfng([
                ("Herbert Simon predicted information abundance creates attention scarcity.", "TRUE",
                 "Paragraph 1: 'a wealth of information creates a poverty of attention'."),
                ("Platforms profit mainly from selling content.", "FALSE",
                 "Paragraph 2: they 'sell human attention to advertisers', not content."),
                ("Some designers of these systems block them on their own phones.", "TRUE",
                 "Paragraph 3: 'confessed to installing blockers on their own phones'."),
                ("Distraction is proven to cause anxiety.", "FALSE",
                 "Paragraph 4: causation 'remains debated'."),
                ("Newspapers and television also competed for attention.", "TRUE",
                 "Paragraph 5: they 'fought the same battle'."),
            ]),
            q_gapfill(6, "Complete the summary below. Write NO MORE THAN THREE WORDS from the passage.", [
                ("Infinite scroll removes natural __________.", "stopping points",
                 "Paragraph 2 states this directly."),
                ("Notifications exploit __________ psychology similar to slot machines.", "variable-reward",
                 "Paragraph 2: 'the same variable-reward psychology'."),
                ("Some researchers call our shared attention a __________ that can be polluted.", "cognitive environment",
                 "Paragraph 3 quote."),
            ]),
            q_mcq(9, "Choose the correct answer.", [
                ("What is the 'hidden cost' of engagement-driven design, according to engineers?",
                 ["Expensive data plans", "A polluted cognitive environment",
                  "Poor quality content", "Slower devices"],
                 "B", "Paragraph 3 links the concern to a polluted 'cognitive environment'."),
                ("Which response level involves autoplay default rules?",
                 ["Individual", "Institutional", "Political", "None — it was never proposed"],
                 "C", "Paragraph 5: regulators proposed 'rules on autoplay defaults'."),
            ]),
        ],
    },
    # ── Passage 7 · band 6.5 · Science ────────────────────────────────
    {
        "title": "Farming Goes Vertical",
        "band_level": 6.5,
        "topic": "Science & Technology",
        "text": """The world's food supply depends on a thin layer of topsoil that took millennia to form — and is now being lost faster than it is created. Meanwhile, the majority of humanity lives in cities, far from the fields that feed them. Vertical farming proposes to address both problems at once: grow food indoors, in stacked layers, under artificial light, inside the cities that consume it.

The engineering is elegant. Hydroponic systems circulate water and dissolved nutrients directly to plant roots, using up to ninety-five percent less water than field agriculture. LED arrays tuned to specific wavelengths supply exactly the light each crop needs for photosynthesis — no more, no less — enabling year-round harvests immune to weather, drought and seasons. Because the environment is sealed, pesticides become unnecessary; because the farm sits inside the city, transport distance collapses to a few kilometres, and produce can be harvested hours rather than weeks before it is eaten.

Proponents argue the implications extend beyond vegetables. If a fraction of the world's cropland could be replaced by vertical farms, vast areas could return to forest — a far more effective carbon store than any machine yet designed. The vision is agriculture without farmland: food production as a utility, like electricity or water, delivered from anonymous warehouses.

The counterargument is physics. Sunlight is free; LEDs are not. Lighting dominates the energy budget of a vertical farm, and until electricity is both cheap and clean, each lettuce grown indoors carries a significant carbon cost. The economics currently work only for a narrow band of crops: fast-growing, high-value greens and herbs. Staples like wheat, rice and potatoes — the crops that actually feed the world — grow too slowly and too cheaply for indoor economics. A vertical farm that cannot grow calories, critics note, cannot replace a field.

A quieter question concerns what is optimised away. Field agriculture is ugly but not merely inefficient; soil microbes, pollinators and nutrient cycles perform work that no engineer has priced into a spreadsheet. Vertical farms that bypass these systems also lose their services and their resilience. The likely future, most analysts suggest, is not skyscraper farms replacing agriculture but a hybrid: cities growing perishable greens locally while distant fields continue supplying staples. Whether that niche justifies the hype depends on how much of the problem one expects technology to solve.""",
        "questions": [
            q_tfng([
                ("Hydroponics can use up to 95% less water than field farming.", "TRUE",
                 "Paragraph 2: 'up to ninety-five percent less water'."),
                ("Vertical farms still require some pesticides.", "FALSE",
                 "Paragraph 2: 'pesticides become unnecessary'."),
                ("LED lighting is the main energy cost of vertical farms.", "TRUE",
                 "Paragraph 4: 'Lighting dominates the energy budget'."),
                ("Wheat and rice are profitable vertical-farm crops.", "FALSE",
                 "Paragraph 4: staples 'grow too slowly and too cheaply for indoor economics'."),
                ("Most analysts predict vertical farms will fully replace fields.", "FALSE",
                 "Final paragraph predicts 'a hybrid', not replacement."),
            ]),
            q_mcq(6, "Choose the correct answer.", [
                ("What two problems does vertical farming aim to address?",
                 ["Water shortage and unemployment", "Topsoil loss and distance between farms and cities",
                  "Pesticide use and high prices", "Climate change and hunger"],
                 "B", "Paragraph 1: topsoil loss + cities far from fields."),
                ("Why can produce reach consumers quickly?",
                 ["Crops grow faster under LEDs", "Farms are inside the cities",
                  "Transport is subsidised", "Harvests are automated"],
                 "B", "Paragraph 2: 'the farm sits inside the city, transport distance collapses'."),
                ("What is the critics' 'physics' argument?",
                 ["LEDs cannot provide correct wavelengths", "Buildings cannot support farm weight",
                  "Artificial light carries a large energy cost", "Plants need real soil to grow"],
                 "C", "Paragraph 4: 'Sunlight is free; LEDs are not'."),
                ("What do soil microbes and pollinators represent?",
                 ["Problems eliminated by indoor farming", "Free ecosystem services lost indoors",
                  "Reasons food prices are rising", "Examples of natural inefficiency"],
                 "B", "Final paragraph: bypassing them 'lose[s] their services and their resilience'."),
            ]),
        ],
    },
    # ── Passage 8 · band 6.5 · Daily life / cities ────────────────────
    {
        "title": "The Fifteen-Minute City",
        "band_level": 6.5,
        "topic": "Urban Life",
        "text": """Urban planning once organised itself around the car. Zoning separated living from working, shopping from schooling, and the distance between them was conquered with roads. The result was the commute: a daily migration that for many consumes over an hour each way. The fifteen-minute city proposes the opposite geometry — every daily need within a quarter-hour's walk or bicycle ride from home.

The concept, formalised by the scientist Carlos Moreno, rests on a simple observation: time is the currency of urban life. A city that gives residents back their hours has made them richer in the only resource that cannot be saved. In a fifteen-minute neighbourhood, shops, schools, clinics, parks and workplaces cluster in mixed-use blocks rather than sprawling into separate zones. Streets widen their pavements and narrow their traffic lanes; ground floors host shops instead of blank walls.

Critics raise three objections. The first is practical: retrofitting existing cities is slow and expensive, and the model fits dense historic districts far better than car-dependent suburbs built around it never anticipating. The second is economic: proximity raises prices, and the neighbourhoods best suited to walkable density already tend to be the most expensive — risking a design that serves the affluent first. The third is political: during the pandemic, fringe commentators conflated the idea with restrictions on movement, and the misinformation has not entirely dissipated.

Evidence from early adopters is cautiously encouraging. Paris has removed parking for thousands of trees and bike lanes; Melbourne mapped resident access to daily needs and found striking inequality between districts — a finding that redirected investment to neglected outer suburbs. Portland's analysis suggested that a fifteen-minute structure could cut household driving by a measurable share, reducing both emissions and household transport costs.

Perhaps the deepest argument is epidemiological. Neighbourhoods designed for walking produce measurably better public health: more physical activity, less pollution, stronger 'eyes on the street' safety and — in a pattern sociologists find consistently — higher levels of casual social contact, the weak social tissue that isolation erodes. A commute is more than lost time, the research implies; it is a design choice that quietly decides who has time to be a neighbour.""",
        "questions": [
            q_tfng([
                ("Traditional zoning separated homes from workplaces.", "TRUE",
                 "Paragraph 1: 'Zoning separated living from working'."),
                ("Carlos Moreno invented the concept.", "TRUE",
                 "Paragraph 2: 'formalised by the scientist Carlos Moreno'."),
                ("Walkable neighbourhoods are usually the cheapest.", "FALSE",
                 "Paragraph 3: they 'tend to be the most expensive'."),
                ("Melbourne's mapping revealed unequal access between districts.", "TRUE",
                 "Paragraph 4: 'found striking inequality between districts'."),
                ("The model eliminates all car travel.", "NOT GIVEN",
                 "The passage describes reduced driving, never total elimination."),
            ]),
            q_gapfill(6, "Complete the sentences. Write NO MORE THAN TWO WORDS from the passage.", [
                ("Moreno observed that __________ is the currency of urban life.", "time",
                 "Paragraph 2: 'time is the currency of urban life'."),
                ("In fifteen-minute districts, daily needs cluster in __________ blocks.", "mixed-use",
                 "Paragraph 2: 'cluster in mixed-use blocks'."),
                ("During the pandemic, the idea was wrongly linked to restrictions on __________.", "movement",
                 "Paragraph 3: 'conflated the idea with restrictions on movement'."),
                ("Melbourne's finding redirected investment to neglected __________.", "outer suburbs",
                 "Paragraph 4: 'neglected outer suburbs'."),
            ]),
        ],
    },
]


def main():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()

    cur.execute("DROP TABLE IF EXISTS speaking_prompts")
    cur.execute("""
        CREATE TABLE speaking_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part INTEGER NOT NULL,
            topic TEXT DEFAULT '',
            question TEXT NOT NULL,
            cues_json TEXT DEFAULT '[]',
            hint_vi TEXT DEFAULT '',
            sample_ideas_json TEXT DEFAULT '[]'
        )
    """)

    for part, topic, question, hint in SPEAKING_PROMPTS:
        cues = json.dumps(CUE_CARDS.get(question, []), ensure_ascii=False)
        cur.execute(
            "INSERT INTO speaking_prompts(part, topic, question, cues_json, hint_vi) VALUES(?, ?, ?, ?, ?)",
            (part, topic, question, cues, hint),
        )

    cur.execute("DROP TABLE IF EXISTS reading_passages")
    cur.execute("""
        CREATE TABLE reading_passages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            band_level REAL DEFAULT 5.5,
            topic TEXT DEFAULT '',
            text TEXT NOT NULL,
            questions_json TEXT NOT NULL
        )
    """)

    for p in PASSAGES:
        cur.execute(
            "INSERT INTO reading_passages(title, band_level, topic, text, questions_json) VALUES(?, ?, ?, ?, ?)",
            (p["title"], p["band_level"], p["topic"], p["text"],
             json.dumps(p["questions"], ensure_ascii=False)),
        )

    db.commit()

    counts = {
        "speaking_prompts": cur.execute("SELECT COUNT(*) FROM speaking_prompts").fetchone()[0],
        "reading_passages": cur.execute("SELECT COUNT(*) FROM reading_passages").fetchone()[0],
    }
    by_part = cur.execute(
        "SELECT part, COUNT(*) FROM speaking_prompts GROUP BY part ORDER BY part").fetchall()
    db.close()
    print("Seeded:", counts, "| prompts by part:", by_part)


if __name__ == "__main__":
    main()
