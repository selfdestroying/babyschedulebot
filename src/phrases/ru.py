HELLO = "Привет {}, меня зовут Сонечка, я - искусственный интеллект, который помогает родителям легче взаимодействовать с детьми и радоваться жизни с малышом."
ABOUT_1 = "Я проанализировала информацию о тысячах детей и знаю, на что обращать внимание при составлении идеального графика сна и бодрствования."
ABOUT_2 = "Поняла. Будем с этим работать. Многие трудности, с которыми сталкиваются родители связаны с нарушением режима сна и бодрствования у малыша. Я помогу вам скорректировать режим так, чтобы ваш малыш рос довольным и развивался, а вы наслаждались родительством."
ABOUT_3 = "Записала! Если вдруг вы ошиблись, то всегда есть возможность всё отменить. В меню есть кнопка 'исправить'. Нажмите на на неё и вы сможете ещё раз ответить на мой вопрос."
ABOUT_4 = "Отлично! Очень рада с вами познакомиться. Сейчас я расскажу, что именно мы будем делать."
ABOUT_5 = "Я буду просить вас писать мне, что происходит с вашим малышом в течение дня: во сколько вы проснулись утром, когда ложитесь спать в дневные сны, во сколько укладываетесь спать в ночь."
ABOUT_6 = "Я проанализирую информацию и буду давать вам рекомендации в течние дня: как лучше выстроить график, сколько бодрствовать и спать, и когда лучше укладываться в ночной сон. Я также попрошу вас ставить оценку каждому дню и каждой ночи для того, чтобы мы смогли отслеживать прогресс."
REGISTER_CONFIRM = "Давайте зарегистрируемся"
ASK_PROBLEM = "Расскажите, чем я могу вам помочь?"
ASK_PHONE = "Подскажите ваш номер телефона"
ASK_EMAIL = "Напишите ваш email на него я смогу прислать ваш дневник сна"
ASK_CHILD_NAME = "Как зовут вашего малыша?"
ASK_CHILD_GENDER = "Это девочка или мальчик?"
ASK_CHILD_BIRTH_DATE: dict[str, str] = {
    "male": "Когда {} родился?",
    "female": "Когда {} родилась?",
}
ASK_PREV_NIGHT_START_SLEEP: dict[str, str] = {
    "male": "Во сколько {} уснул вчера в ночной сон?",
    "female": "Во сколько {} уснула вчера в ночной сон?",
}
ASK_NIGHT_WAKE_UP_COUNT = {
    "male": "Сколько раз {} просыпался ночью?",
    "female": "Сколько раз {} просыпалась ночью?",
}
ASK_PREV_NIGHT_END_SLEEP = {
    "male": "А во сколько {} проснулся сегодня утром?",
    "female": "А во сколько {} проснулся сегодня утром?",
}
ASK_FOOD_TYPE = "Как вы кормите ребёнка?"
ASK_PREV_NIGHT = (
    "Давайте начнём следить за графиком! И для начала расскажите мне про прошлую ночь."
)
GOOD_MORNING = {
    "male": "С Добрым утром! {} проснулся сегодня в {}.Давайте попробуем бодрствовать {} - {} часа, и ляжем в дневной сон в {}-{} Постарайтесь провести первую половину бодрствования активно, а последние полчаса успокаивайтесь и замедляйтесь, чтобы легче уснуть. Я пришлю напоминание, чтобы вы не забыли отметить время сна. Не волнуйтесь, оно будет без звука",
    "female": "С Добрым утром! {} проснулась сегодня в {}.Давайте попробуем бодрствовать {} - {} часа, и ляжем в дневной сон в {}-{} Постарайтесь провести первую половину бодрствования активно, а последние полчаса успокаивайтесь и замедляйтесь, чтобы легче уснуть. Я пришлю напоминание, чтобы вы не забыли отметить время сна. Не волнуйтесь, оно будет без звука",
}
DAY_FALL_ASLEEP = {"male": "Во сколько {} уснул?", "female": "Во сколько {} уснула?"}
DAY_WAKE_UP = {
    "male": "Во сколько {} проснулся?",
    "female": "Во сколько {} проснулась?",
}
NIGHT_FALL_ASLEEP = {
    "male": "Во сколько {} лег спать в ночной сон?",
    "female": "Во сколько {} легла спать в ночной сон?",
}

DAY_SLEEP_ANALYSIS = {
    "male": "{} поспал {}, а бодрствование было {}. Сон был длинным/коротким/в норме. Бодрствование было длинным/коротким/в норме. Сейчас давайте бодрствовать {} - {} часа и ляжем спать в следующий сон в {}-{}",
    "female": "{} поспала {}, а бодрствование было {}. Сон был длинным/коротким/в норме. Бодрствование было длинным/коротким/в норме. Сейчас давайте бодрствовать {} - {} часа и ляжем спать в следующий сон в {}-{}",
}

ASK_DAY_RATING = "Какую оценку вы бы поставили сегодняшнему дню?"
ASK_NIGHT_RATING = "Какую оценку вы бы поставили прошедшей ночи?"
NIGHT_RATING_1_4 = (
    "Боюсь представить, что это была за ночка! Не переживайте, мы справимся"
)
NIGHT_RATING_5_7 = "Тяжеловато, понимаю. Давайте работать над этим"
NIGHT_RATING_8_10 = "Отлично! Давайте закрепим результат"
WRONG_TIME = "Ой! Я вас не поняла, напишите, пожалуйста в формате ЧЧ:ММ"
PRESS_END_DAY_SLEEP_BUTTON = (
    'Нажмите в меню на кнопку "Отметить время дневного сна", когда ляжете спать'
)
