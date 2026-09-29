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
# v2 expansion — wider topic coverage for the 24-week roadmap
# ---------------------------------------------------------------------------

SPEAKING_PROMPTS += [
    # ---- Part 1 (new topics) ----
    (1, "Travel & Holidays", "Do you like travelling?", ""),
    (1, "Travel & Holidays", "What kind of places do you like to visit?", ""),
    (1, "Travel & Holidays", "Do you prefer travelling alone or with other people?", ""),
    (1, "Travel & Holidays", "What was your best holiday ever?", ""),
    (1, "Travel & Holidays", "Is there a place you really want to visit one day?", ""),
    (1, "Food & Cooking", "Do you enjoy cooking?", ""),
    (1, "Food & Cooking", "What is your favourite dish from your country?", ""),
    (1, "Food & Cooking", "Do you prefer eating at home or in restaurants?", ""),
    (1, "Food & Cooking", "Did you learn to cook when you were a child?", ""),
    (1, "Food & Cooking", "Is there a foreign food you would like to try?", ""),
    (1, "Weather & Seasons", "What is the weather like where you live?", ""),
    (1, "Weather & Seasons", "Which season do you like best? Why?", ""),
    (1, "Weather & Seasons", "Do you prefer hot or cold weather?", ""),
    (1, "Weather & Seasons", "Does the weather ever affect your mood?", ""),
    (1, "Weather & Seasons", "What do you usually do on rainy days?", ""),
    (1, "Sport & Exercise", "Do you play any sports?", ""),
    (1, "Sport & Exercise", "How often do you exercise?", ""),
    (1, "Sport & Exercise", "Did you play sport when you were a child?", ""),
    (1, "Sport & Exercise", "Do you prefer watching sport or playing it?", ""),
    (1, "Sport & Exercise", "Is there a sport you would like to try?", ""),
    (1, "Music & Arts", "What kind of music do you usually listen to?", ""),
    (1, "Music & Arts", "Do you play a musical instrument?", ""),
    (1, "Music & Arts", "When do you usually listen to music?", ""),
    (1, "Music & Arts", "Have you ever been to a live concert?", ""),
    (1, "Music & Arts", "Did you learn music or art at school?", ""),
    (1, "Reading & Books", "Do you like reading?", ""),
    (1, "Reading & Books", "What kind of books do you prefer?", ""),
    (1, "Reading & Books", "Do you read more on paper or on a screen?", ""),
    (1, "Reading & Books", "What book did you enjoy as a child?", ""),
    (1, "Reading & Books", "Is there a book you would like to read again?", ""),
    # ---- Part 2 (new cue cards) ----
    (2, "Travel", "Describe a journey you remember well.", ""),
    (2, "People", "Describe a time when you helped someone.", ""),
    (2, "Objects", "Describe a gift you received that you really liked.", ""),
    (2, "Technology", "Describe a website or app you use often.", ""),
    (2, "Events", "Describe a family celebration you attended.", ""),
    (2, "Activities", "Describe a sport or outdoor activity you enjoy.", ""),
    # ---- Part 3 (new discussion) ----
    (3, "Travel", "How has tourism changed the places people visit?", ""),
    (3, "Food", "Do you think traditional food is disappearing? Why?", ""),
    (3, "Sport", "Should children be required to play sport at school?", ""),
    (3, "Technology", "Has the internet made people better informed or just more distracted?", ""),
    (3, "Family", "How have family celebrations changed in recent years?", ""),
    (3, "Society", "Is it better to give gifts of money or of objects? Why?", ""),
]

CUE_CARDS.update({
    "Describe a journey you remember well.": [
        "where you went", "who you travelled with",
        "what happened during the journey", "and explain why you remember it"],
    "Describe a time when you helped someone.": [
        "who you helped", "what the situation was",
        "what you did to help", "and explain how you felt about it"],
    "Describe a gift you received that you really liked.": [
        "what the gift was", "who gave it to you",
        "when you received it", "and explain why you liked it so much"],
    "Describe a website or app you use often.": [
        "what it is", "how you found it",
        "what you use it for", "and explain why it is useful to you"],
    "Describe a family celebration you attended.": [
        "what the celebration was", "who was there",
        "what happened", "and explain why it was special"],
    "Describe a sport or outdoor activity you enjoy.": [
        "what it is", "when and where you do it",
        "who you do it with", "and explain why you enjoy it"],
})


# ---------------------------------------------------------------------------
# Reading passages
# ---------------------------------------------------------------------------
# questions_json: list of sections -> {type, instruction, items[]}
# types: tfng (TRUE/FALSE/NOT GIVEN), gapfill, matching_heading, mcq

def q_tfng(items, start_id=1):
    return {
        "type": "tfng",
        "instruction": "Do the following statements agree with the information in the passage? Write TRUE, FALSE or NOT GIVEN.",
        "items": [{"id": start_id + i, "question": q, "answer": a, "explanation": e}
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


def q_heading(start_id, headings, items):
    """Matching-headings set. `headings` = [(roman, text)], items = [(label, answer_roman, explanation)]."""
    listing = "\n".join(f"{r}. {t}" for r, t in headings)
    return {
        "type": "matching_heading",
        "instruction": "Choose the correct heading for each paragraph from the list below.\n" + listing,
        "items": [{"id": start_id + i, "question": q,
                   "options": [r for r, _ in headings],
                   "answer": a, "explanation": e}
                  for i, (q, a, e) in enumerate(items)],
    }


PASSAGES += [
    # ── Passage 9 · band 5.0 · Culture ──────────────────────────────
    {
        "title": "A Brief History of Coffee",
        "band_level": 5.0,
        "topic": "Culture & History",
        "text": """Nobody knows exactly when humans first drank coffee, but the most famous story takes place in Ethiopia around the ninth century. According to legend, a goat herder named Kaldi noticed that his goats became unusually energetic after eating the red berries of a certain shrub. Kaldi tried the berries himself, felt the same lift, and carried them to a nearby monastery. The monks, the story goes, threw the berries onto a fire — and were immediately drawn back by the rich smell of the roasting beans.

Whether or not Kaldi existed, coffee certainly travelled across the Red Sea to Yemen by the fifteenth century. There, Sufi monks cultivated the plant and drank a brew of its beans to stay awake through long night-time rituals. Yemen's port of Mocha became the centre of the early coffee trade, and the drink spread through the Ottoman world into Persia, Egypt and Turkey, where coffee houses became famous places of conversation and chess.

Coffee reached Europe in the seventeenth century, arriving first through the trading port of Venice. It was controversial at first — some priests wanted it banned as a 'Muslim drink' — until, according to another famous story, Pope Clement VIII tasted it and approved. In London, coffee houses charged one penny to enter and became known as 'penny universities', where merchants, writers and scientists argued about everything from politics to physics.

European powers soon tried to break Yemen's monopoly. The Dutch smuggled seedlings to Java, the French planted them in the Caribbean, and the Portuguese established enormous estates in Brazil. Brazil's climate proved ideal, and by the nineteenth century it had become — and remains today — the largest coffee producer in the world.

The twentieth century brought coffee to the masses: instant coffee for soldiers, espresso machines for cafés, and finally the 'specialty' movement, which treats beans like wine, with tasting notes and single-origin farms. Today an estimated two billion cups are drunk every day. Whatever the truth of the Kaldi legend, a goat herder's observation on an Ethiopian hillside quietly reshaped the mornings of half the planet.""",
        "questions": [
            q_tfng([
                ("According to legend, coffee was discovered in Ethiopia.", "TRUE",
                 "Paragraph 1: the Kaldi story 'takes place in Ethiopia'."),
                ("Sufi monks drank coffee to stay awake during rituals.", "TRUE",
                 "Paragraph 2: they used it 'to stay awake through long night-time rituals'."),
                ("London coffee houses were expensive to enter.", "FALSE",
                 "Paragraph 3: they charged one penny — cheap enough to be 'penny universities'."),
                ("Brazil became the world's largest coffee producer.", "TRUE",
                 "Paragraph 4: 'it had become — and remains today — the largest coffee producer'."),
                ("Espresso machines were invented before instant coffee.", "NOT GIVEN",
                 "Both are mentioned in paragraph 5 but no order between them is stated."),
            ]),
            q_gapfill(6, "Complete the notes below. Write NO MORE THAN THREE WORDS from the passage.", [
                ("The Yemeni port of __________ was the centre of the early coffee trade.", "Mocha",
                 "Paragraph 2: 'Yemen's port of Mocha became the centre'."),
                ("London coffee houses became known as 'penny __________'.", "universities",
                 "Paragraph 3 quote."),
                ("The Dutch grew coffee on the island of __________.", "Java",
                 "Paragraph 4: 'smuggled seedlings to Java'."),
                ("An estimated __________ cups of coffee are drunk each day.", "two billion|2 billion",
                 "Final paragraph: 'an estimated two billion cups are drunk every day'."),
            ]),
        ],
    },
    # ── Passage 10 · band 5.5 · Technology ──────────────────────────
    {
        "title": "The Rise of Electric Bikes",
        "band_level": 5.5,
        "topic": "Technology & Transport",
        "text": """In the debate about cleaner transport, one machine has quietly outsold every electric car on the market: the electric bicycle. In several European countries, e-bikes now account for the majority of new bicycles sold, and global sales have grown faster than almost any other category of personal transport. The vehicle that was once mocked as a bicycle for lazy people has become the fastest-moving transport story of the decade.

The technology is deliberately modest. A typical 'pedelec' e-bike looks like an ordinary bicycle but hides a small battery and motor that add power only while the rider is pedalling. Most models offer assistance up to twenty-five kilometres per hour and a range of forty to one hundred kilometres per charge — enough for nearly every urban journey. Because the motor multiplies the rider's own effort rather than replacing it, hills flatten and headwinds disappear.

The appeal cuts across generations. Commuters arrive at work without needing a shower. Older riders keep cycling years after knees and lungs would otherwise have forced them to stop. Delivery companies, driven by the boom in online food orders, have adopted e-bikes as faster and cheaper than vans in dense city centres. For many families, an e-bike costs a fraction of a second car yet performs most of the same trips.

The problems are equally real. E-bikes cost two to four times more than conventional bicycles, and their weight makes them awkward to carry upstairs. Battery fires — usually from cheap, uncertified packs — have caused fatal blazes in apartment buildings. Theft is rampant because resale is easy. And regulators argue about where e-bikes belong: too fast for crowded cycle paths, too slow for traffic lanes.

Cities are responding differently. France has offered citizens subsidies worth hundreds of euros to trade cars for e-bikes, while other governments invest in secure parking and tougher battery standards. Transport analysts broadly agree on the direction of travel, if not the speed: the more interesting question is what e-bikes actually replace. If they mostly replace ordinary bicycles and buses, the environmental gain is modest. If they replace cars — even one household journey in ten — the humble e-bike may do more for clean transport than the electric car ever will.""",
        "questions": [
            q_tfng([
                ("E-bikes have sold better than electric cars.", "TRUE",
                 "Paragraph 1: it 'has quietly outsold every electric car on the market'."),
                ("A pedelec motor works even when the rider stops pedalling.", "FALSE",
                 "Paragraph 2: the motor adds power 'only while the rider is pedalling'."),
                ("Delivery companies helped drive e-bike adoption.", "TRUE",
                 "Paragraph 3: they 'have adopted e-bikes as faster and cheaper than vans'."),
                ("All e-bike battery fires involve certified batteries.", "FALSE",
                 "Paragraph 4: fires come 'usually from cheap, uncertified packs'."),
                ("France pays people to swap cars for e-bikes.", "TRUE",
                 "Paragraph 5: subsidies 'to trade cars for e-bikes'."),
            ]),
            q_mcq(6, "Choose the correct answer.", [
                ("What does a pedelec e-bike do?",
                 ["Replaces pedalling entirely", "Multiplies the rider's own effort",
                  "Only works downhill", "Charges while braking"],
                 "B", "Paragraph 2: 'the motor multiplies the rider's own effort rather than replacing it'."),
                ("Which problem is NOT mentioned in the passage?",
                 ["High purchase price", "Factory pollution",
                  "Battery fires", "Theft"],
                 "B", "Paragraph 4 lists cost, weight, fires and theft — pollution is never raised."),
                ("According to analysts, the key question about e-bikes is…",
                 ["how fast they can go", "what transport they actually replace",
                  "whether subsidies will continue", "how long batteries last"],
                 "B", "Final paragraph: 'the more interesting question is what e-bikes actually replace'."),
            ]),
        ],
    },
    # ── Passage 11 · band 6.0 · Science — matching headings ─────────
    {
        "title": "How Vaccines Changed the World",
        "band_level": 6.0,
        "topic": "Science & Health",
        "text": """A. For most of human history, infectious disease was the great unpredictable force of life. Smallpox alone killed roughly one in three of the people it infected and scarred or blinded millions more, reshaping wars, dynasties and entire civilisations. Long before science understood viruses, communities in Asia and Africa practised variolation — deliberately scratching material from a smallpox pustule into a healthy person's skin. It was dangerous, but those who survived gained real immunity, and the practice carried a quiet idea that would eventually change medicine: a small dose of disease could defend against a large one.

B. The decisive step came from an English country doctor. Edward Jenner had noticed a piece of local folklore: milkmaids who caught cowpox, a mild disease, seemed never to catch smallpox. In 1796 he tested the observation directly, transferring fluid from a cowpox sore on a milkmaid's hand into the arm of an eight-year-old boy, and later exposing the boy to smallpox itself. The boy did not fall ill. Jenner called the method 'vaccination', from vacca, the Latin for cow — and for the first time, immunity could be created safely and deliberately rather than survived by luck.

C. The nineteenth and twentieth centuries turned Jenner's trick into a science. Louis Pasteur weakened the rabies virus in his laboratory and used it to save a bitten boy, proving that laboratories could manufacture weakened versions of pathogens — 'attenuated' vaccines — on demand. The pattern repeated through the next hundred years: vaccines for diphtheria, tetanus, pertussis, measles and polio each converted a feared killer into a scheduled childhood injection.

D. What began as a technique became a global strategy. Vaccination was the first medical tool powerful enough to aim not merely at treatment but at eradication — the permanent removal of a disease from the planet. After a decade-long campaign of surveillance and targeted immunisation, the World Health Organization declared smallpox eradicated in 1980: the only human disease ever eliminated deliberately. Polio has since been pushed to a handful of districts in two countries. These campaigns revealed that success depends as much on logistics — cold storage, transport, funding and trust — as on the vaccine itself.

E. Modern vaccines arrive with modern tensions. When the coronavirus pandemic began, mRNA technology produced effective vaccines within a year — a speed that would have astonished Pasteur — yet the same era saw the rise of vaccine hesitancy, fuelled by misinformation spreading faster than any virus. Meanwhile the economics remain skewed: diseases of wealthy nations attract research budgets, while diseases of poor regions wait decades. The tool that conquered smallpox has never been more powerful. Whether it is used as powerfully everywhere is the unfinished question.""",
        "questions": [
            q_heading(1, [
                ("i", "A disease that shaped history"),
                ("ii", "The first scientific breakthrough"),
                ("iii", "A century of expansion"),
                ("iv", "Eradication on a global scale"),
                ("v", "New technology, old obstacles"),
                ("vi", "The manufacture of modern vaccines"),
                ("vii", "The ethics of laboratory research"),
            ], [
                ("Paragraph A", "i",
                 "This paragraph describes how smallpox 'reshaped wars, dynasties and entire civilisations'."),
                ("Paragraph B", "ii",
                 "Jenner's 1796 experiment is described as 'the decisive step' — the first vaccine."),
                ("Paragraph C", "iii",
                 "Covers the 19th–20th century expansion from Pasteur to polio vaccines."),
                ("Paragraph D", "iv",
                 "About eradication campaigns — smallpox 1980 and polio 'near-eradicated'."),
                ("Paragraph E", "v",
                 "mRNA speed plus hesitancy and inequity — new tech, old problems."),
            ]),
            q_tfng([
                ("Variolation was used before Jenner's experiment.", "TRUE",
                 "Paragraph A: communities 'practised variolation' long before vaccines."),
                ("Jenner took cowpox material from a milkmaid.", "TRUE",
                 "Paragraph B: 'fluid from a cowpox sore on a milkmaid's hand'."),
                ("Smallpox was declared eradicated in 1980.", "TRUE",
                 "Paragraph D states this directly."),
                ("Polio has been completely eliminated worldwide.", "FALSE",
                 "Paragraph D: polio remains in 'a handful of districts in two countries'."),
                ("mRNA vaccines were developed over twenty years.", "NOT GIVEN",
                 "Paragraph E says they were produced 'within a year' during the pandemic; it does not date the underlying research."),
            ], 6),
        ],
    },
    # ── Passage 12 · band 6.5 · Psychology ──────────────────────────
    {
        "title": "The Psychology of Procrastination",
        "band_level": 6.5,
        "topic": "Psychology",
        "text": """Everyone procrastinates, yet for decades psychology misunderstood why. The obvious explanation — laziness, or poor time management — fails on inspection: chronic procrastinators are often busy people who delay important tasks while energetically completing trivial ones. The researcher Timothy Pychyl offers a sharper definition: procrastination is the voluntary delay of an intended action despite expecting to be worse off for it. This is not a scheduling failure. It is an emotion-regulation failure — we avoid the task to avoid the feeling the task provokes.

Neuroscience describes the mechanism as a tug-of-war. The limbic system, the brain's fast emotional centre, detects that a task triggers boredom, anxiety or self-doubt and votes for immediate relief: anything else, now. The prefrontal cortex, seat of planning, knows the delay will cost more later but is slower and weaker. Economists call the resulting distortion 'present bias': the mind values relief this minute far above rewards next month. A deadline only defeats the loop when the panic of the final hour finally outweighs the discomfort of the task.

Researchers identify several procrastinating personalities. 'Arousal' procrastinators delay deliberately, claiming they work best under deadline pressure — though studies show their last-minute work contains more errors. 'Avoiders' procrastinate from fear: of failure, of success, or of others' judgement. 'Decisional' procrastinators cannot choose between options, and postpone the choice itself. Around fifteen to twenty percent of adults qualify as chronic procrastinators, and the habit correlates with measurably worse outcomes: lower grades, higher stress, poorer sleep and even weakened immunity — the stress of the delayed task never truly goes away.

The surprising finding is what fixes it. Logic suggests harsher discipline; the evidence points the opposite way. In a widely cited study, psychologist Michael Wohl found that students who forgave themselves for procrastinating on a first exam procrastinated significantly less when preparing for the second. Self-criticism, it turns out, adds another unpleasant emotion to the task — making avoidance more, not less, attractive. Practical strategies share a gentler logic: 'implementation intentions' (deciding in advance that at 9 a.m. tomorrow you will write page one), breaking tasks into steps too small to fear, and designing the environment so the distraction is harder than the work.

Procrastination, then, is less a character flaw than a conflict between the brain's two clocks — one that lives in this moment and one that lives in the future. The task is never the real enemy; the feeling attached to it is. Which suggests the most productive question is not 'How do I force myself to work?' but 'What am I actually avoiding feeling?'""",
        "questions": [
            q_tfng([
                ("Chronic procrastinators are usually inactive people.", "FALSE",
                 "Paragraph 1: they are 'often busy people who delay important tasks while energetically completing trivial ones'."),
                ("The limbic system seeks immediate emotional relief.", "TRUE",
                 "Paragraph 2: it 'votes for immediate relief'."),
                ("Arousal procrastinators produce better work under pressure.", "FALSE",
                 "Paragraph 3: last-minute work 'contains more errors'."),
                ("Roughly one fifth of adults are chronic procrastinators.", "TRUE",
                 "Paragraph 3: 'fifteen to twenty percent of adults'."),
                ("Forgiving yourself led to less procrastination later.", "TRUE",
                 "Paragraph 4: students who forgave themselves 'procrastinated significantly less'."),
            ]),
            q_mcq(6, "Choose the correct answer.", [
                ("According to paragraph 1, procrastination is best described as…",
                 ["a time-management failure", "an emotion-regulation failure",
                  "a lack of intelligence", "a type of laziness"],
                 "B", "Pychyl's definition frames it as avoiding the feeling the task provokes."),
                ("What is 'present bias'?",
                 ["Preferring gifts today over tomorrow", "Overvaluing immediate relief over future reward",
                  "Focusing only on current tasks", "A type of memory error"],
                 "B", "Paragraph 2: 'values relief this minute far above rewards next month'."),
                ("What did Wohl's study of students find?",
                 ["Self-criticism improves performance", "Deadlines eliminate procrastination",
                  "Self-forgiveness reduces future procrastination", "Procrastinators fail their exams"],
                 "C", "Paragraph 4: forgiving students 'procrastinated significantly less' on the next exam."),
                ("Which strategy is NOT suggested in the passage?",
                 ["Implementation intentions", "Breaking tasks into small steps",
                  "Stricter self-punishment", "Redesigning the environment"],
                 "C", "Paragraph 4 warns self-criticism backfires; punishment is never recommended."),
            ]),
        ],
    },
]


# ---------------------------------------------------------------------------
# IELTS Writing prompts (Task 2 essays + Task 1 reports)
# level: 'ielts' = Task 2 (250+ words, 40 min) · 'ielts_t1' = Task 1 (150+ words, 20 min)
# ---------------------------------------------------------------------------

IELTS_WRITING = [
    # ---- Task 2 · opinion ----
    ("ielts", "Free University for Everyone?", "Education · Opinion", "🎓", 250, 320,
     "Đề opinion kinh điển. Quyết định rõ agree hay disagree ngay từ intro, 2 body paragraph bảo vệ lập trường.",
     "Some people believe that university education should be free for all students. To what extent do you agree or disagree? Give reasons for your answer and include any relevant examples from your own knowledge or experience.",
     ["I largely agree that higher education should be publicly funded because…",
      "The strongest argument for free tuition is…",
      "Admittedly, opponents claim that…, however…"],
     ["State your position clearly in the introduction — examiners penalise vague thesis statements.",
      "One body paragraph per argument: reason → explanation → example.",
      "A short concession ('Admittedly…') raises your Task Response score."],
     ["tuition fees", "publicly funded", "equal access to education", "a burden on taxpayers"]),
    ("ielts", "Has Technology Made Life Harder?", "Technology · Opinion", "💻", 250, 320,
     "Đề agree/disagree về công nghệ. Tránh liệt kê — chọn 2 ý sâu và phát triển bằng ví dụ cụ thể.",
     "Some people argue that technology has made our lives more complicated rather than simpler. To what extent do you agree or disagree? Give reasons for your answer and include relevant examples.",
     ["While technology undeniably solves many problems, I agree that it adds complexity because…",
      "A clear example of this complication is…",
      "On the other hand, it would be unfair to ignore…"],
     ["Pick a side — 'partly agree' is allowed but must still be a clear position.",
      "Use one concrete example per paragraph (a real app, habit or trend).",
      "End each body paragraph by linking back to the question."],
     ["digital overload", "constant connectivity", "a double-edged sword", "streamline daily tasks"]),
    # ---- Task 2 · discussion ----
    ("ielts", "Remote Work: Boon or Burden?", "Work · Discussion", "🏠", 250, 320,
     "Dạng Discuss both views — body 1 trình bày view A khách quan, body 2 view B, kết luận mới nói ý kiến của bạn.",
     "Some people think that remote working benefits employees, while others believe it damages teamwork and company culture. Discuss both views and give your own opinion.",
     ["Supporters of remote work argue that…",
      "On the other hand, critics point out that…",
      "In my view, the benefits outweigh the drawbacks provided that…"],
     ["Present BOTH sides objectively before giving your opinion — that is the task.",
      "Keep your own opinion for the final body or conclusion, not the intro.",
      "Use distancing language for other views ('Supporters claim…', 'Critics argue…')."],
     ["flexible schedule", "face-to-face collaboration", "team cohesion", "a healthy work-life balance"]),
    # ---- Task 2 · positive/negative development ----
    ("ielts", "The Rise of Living Alone", "Society · Development", "🚪", 250, 320,
     "Is this a positive or negative development? Có thể chọn 'mostly positive/negative' miễn là lập luận nhất quán.",
     "More people are choosing to live alone than in the past. Is this a positive or negative development? Give reasons for your answer and include any relevant examples.",
     ["In my view, this trend is largely positive/negative because…",
      "One major consequence of living alone is…",
      "However, this development also brings…"],
     ["'Trend/development' essays want consequences and implications, not just pros/cons lists.",
      "Acknowledge the other side briefly, then explain why yours wins.",
      "Anchor the essay in a real context — cost of housing, social media, ageing populations."],
     ["social isolation", "financial independence", "ageing population", "community ties"]),
    # ---- Task 2 · problem / solution ----
    ("ielts", "Choking Cities", "Environment · Problem/Solution", "🌫️", 250, 320,
     "Đề 2 câu hỏi: problems + solutions. Body 1 nêu 1-2 vấn đề, body 2 nêu giải pháp tương ứng.",
     "Air pollution in many cities is getting worse. What problems does this cause for people living there, and what measures could be taken to solve it?",
     ["The most serious consequence of urban air pollution is…",
      "To tackle this problem, governments should…",
      "In addition, individuals can contribute by…"],
     ["Match each problem with a solution — examiners look for direct pairing.",
      "Use precise vocabulary: 'respiratory diseases' beats 'bad for health'.",
      "Solutions at two levels (government + individual) show range."],
     ["respiratory diseases", "congestion charging", "renewable energy", "public transport infrastructure"]),
    # ---- Task 2 · two-part question ----
    ("ielts", "The Vanishing Family Dinner", "Family · Two-part", "🍽️", 250, 320,
     "Đề hỏi kép: Why? + positive or negative? Trả lời đủ cả hai, một body cho mỗi câu hỏi.",
     "Nowadays, people spend less time with their families than in the past. Why is this happening, and is it a positive or negative trend?",
     ["There are two main reasons why family time is shrinking…",
      "In my opinion, this is a negative development because…",
      "Another factor contributing to this trend is…"],
     ["Answer BOTH questions explicitly — losing one caps Task Response at band 5.",
      "Body 1 = causes, Body 2 = evaluation. Keep them separate.",
      "Finish with a one-sentence recommendation or prediction for a strong conclusion."],
     ["demanding work schedules", "weaken family bonds", "the pursuit of career goals", "emotional support"]),
    # ---- Task 1 · line chart ----
    ("ielts_t1", "Internet Access by Country", "Report · Line Graph", "📈", 150, 200,
     "Task 1 line graph. Overview = xu hướng chung (tất cả tăng, A dẫn đầu). Detail = số liệu so sánh cụ thể.",
     "The chart shows the percentage of households with internet access in three countries from 2000 to 2020.\n\nData — Country A: 5% (2000) → 45% (2005) → 70% (2010) → 85% (2015) → 92% (2020) · Country B: 3% → 18% → 40% → 62% → 78% · Country C: 15% → 30% → 50% → 72% → 85%.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
     ["Overall, internet access rose dramatically in all three countries, with Country A maintaining the lead throughout the period.",
      "In 2000, Country C had the highest access rate at 15%, whereas…",
      "By 2020, the figure for Country A had climbed to…"],
     ["Paragraph 2 = overview FIRST (main trends, no data). Examiners score this heavily.",
      "Never list every number — select: highest, lowest, biggest change, convergence points.",
      "Use varied trend language: 'climbed', 'plunged', 'levelled off', 'narrowed the gap'."],
     ["rose steadily", "remained the highest", "narrowed the gap", "a dramatic increase"]),
    # ---- Task 1 · bar chart ----
    ("ielts_t1", "Average Commute Times", "Report · Bar Chart", "🚇", 150, 200,
     "Bar chart so sánh 4 thành phố ở 2 năm. Nhóm cities theo xu hướng thay vì liệt kê từng cái.",
     "The bar chart compares average one-way commute times (in minutes) in four cities in 2015 and 2025.\n\nData — London: 45 → 50 · Paris: 38 → 44 · Tokyo: 42 → 46 · Berlin: 30 → 32.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
     ["Overall, commute times increased in all four cities, with London consistently recording the longest journeys.",
      "Berlin remained the most commuter-friendly city, at just…",
      "The largest rise was seen in…"],
     ["Group data: 'London and Tokyo, the two longest commutes…' shows synthesis.",
      "Compare across years AND across cities in every paragraph.",
      "Numbers must be reported accurately — wrong data costs Task Achievement."],
     ["recorded the longest commute", "saw a marginal increase", "consistently the lowest", "respectively"]),
    # ---- Task 1 · pie charts ----
    ("ielts_t1", "Where the Money Goes", "Report · Pie Charts", "🥧", 150, 200,
     "Hai pie charts 1990 vs 2020. Bắt trend: category nào tăng/giảm mạnh nhất.",
     "The pie charts show how a typical household divided its spending between five categories in 1990 and 2020.\n\nData — Housing: 25% → 35% · Food: 30% → 15% · Transport: 15% → 20% · Leisure: 10% → 15% · Other: 20% → 15%.\n\nSummarise the information by selecting and reporting the main features, and make comparisons where relevant. Write at least 150 words.",
     ["Overall, housing became the dominant expense by 2020, while the share spent on food halved.",
      "In 1990, food accounted for the largest proportion at 30%, but…",
      "The proportion devoted to leisure saw a modest rise from…"],
     ["Use proportion language: 'accounted for', 'made up', 'represented a third of'.",
      "Lead with the biggest changes (Housing +10, Food −15), then minor ones.",
      "An overview naming the 2 biggest shifts earns more than listing all five."],
     ["accounted for the largest share", "halved", "saw a significant increase", "respectively"]),
    # ---- Task 1 · process ----
    ("ielts_t1", "How Paper Is Recycled", "Report · Process", "♻️", 150, 200,
     "Process diagram — dùng passive voice và sequencers. Không có opinion, chỉ mô tả các giai đoạn.",
     "The diagram shows the process by which waste paper is recycled into new paper products.\n\nStages: 1. Collection — used paper is gathered from homes and offices → 2. Sorting — paper is separated from plastic and metal → 3. Pulping — paper is mixed with water and chemicals to form pulp → 4. De-inking — ink and glue are removed → 5. Pressing — pulp is pressed into thin sheets → 6. Drying — sheets are dried and rolled onto reels.\n\nSummarise the information by selecting and reporting the main features. Write at least 150 words.",
     ["Overall, the recycling of paper is a six-stage linear process, beginning with collection and ending with dried paper reels.",
      "Once the waste paper has been collected, it is sorted…",
      "At the de-inking stage,…"],
     ["Passive voice is essential for processes: 'is collected', 'are removed'.",
      "Use sequencers: Initially → Following this → Subsequently → Finally.",
      "Group stages into 2 paragraphs (1–3 and 4–6) instead of six tiny ones."],
     ["is gathered from", "is separated into", "is transformed into", "the final stage"]),
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

    # ------------------------------------------------------------------
    # IELTS writing prompts + dedupe of legacy duplicated rows
    # ------------------------------------------------------------------
    cur.execute("DELETE FROM writing_prompts WHERE id NOT IN (SELECT MIN(id) FROM writing_prompts GROUP BY title)")
    cur.execute("DELETE FROM writing_prompts WHERE level IN ('ielts', 'ielts_t1')")
    for (level, title, category, icon, tmin, tmax, sit_vi, prompt, starters, tips, vocab) in IELTS_WRITING:
        cur.execute(
            """INSERT INTO writing_prompts
               (level, title, category, category_icon, target_min, target_max,
                situation_vi, prompt, sentence_starters_json, guide_tips_json, suggested_vocab_json)
               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (level, title, category, icon, tmin, tmax, sit_vi, prompt,
             json.dumps(starters, ensure_ascii=False),
             json.dumps(tips, ensure_ascii=False),
             json.dumps(vocab, ensure_ascii=False)),
        )

    db.commit()

    counts = {
        "speaking_prompts": cur.execute("SELECT COUNT(*) FROM speaking_prompts").fetchone()[0],
        "reading_passages": cur.execute("SELECT COUNT(*) FROM reading_passages").fetchone()[0],
        "writing_prompts": cur.execute("SELECT COUNT(*) FROM writing_prompts").fetchone()[0],
    }
    by_part = cur.execute(
        "SELECT part, COUNT(*) FROM speaking_prompts GROUP BY part ORDER BY part").fetchall()
    db.close()
    print("Seeded:", counts, "| prompts by part:", by_part)


if __name__ == "__main__":
    main()
