from src.pydantic.schemas import Question, Topic


def dz(x, y):
    return dict(zip(x, y))


topic_title = ("pk", "name")
TOPICS = [
    Topic(**dz(topic_title, args))
    for args in (
        (5, "Языки программирования"),
        (6, "Персоны"),
        (7, "Сети и протоколы"),
    )
]


def question(text, amount=4):
    return text, [f"{text} option-{i + 1}" for i in range(amount)], 1


def topic_questions(start_pk, topic_pk, topic, amount=5):
    return [
        (start_pk + i, topic_pk, *question(f"{topic} question-{i + 1}"))
        for i in range(amount)
    ]


question_title = ("pk", "topic", "text", "options", "answer")
QUESTIONS = [
    Question(**dz(question_title, args))
    for args in (
        (
            1,
            6,
            "Кто является первым автором языка программирования C++?",
            ["Линус Торвальдс", "Бьёрн Страуструп", "Джеймс Гослинг", "Кен Томпсон"],
            2,
        ),
        (
            2,
            6,
            "Какому из этих IT-специалистов принадлежит заслуга создания World Wide Web",
            ["Тим Бернерс-Ли", "Винтон Серф", "Роберт Кан", "Пол Мокапетрис"],
            1,
        ),
        (
            3,
            6,
            "Кто является основателем компании Oracle и её долговременным CEO?",
            ["Ларри Эллисон", "Скотт МакНили", "Боб Майнер", "Эд Оатс"],
            1,
        ),
        (
            4,
            6,
            "Кого считают изобретателем мыши компьютера?",
            ["Алан Тьюринг", "Уильям Инглиш", "Дуглас Энгельбарт", "Стив Джобс"],
            3,
        ),
        (
            5,
            6,
            "Кто является первым автором языка программирования Ruby?",
            ["Юкихиро Мацумото", "Мацуо Исимото", "Хидэси Масуи", "Сяруко Симото"],
            1,
        ),
        (
            6,
            6,
            "Кто разработал язык запросов SQL?",
            [
                "Дональд Чеймберлин",
                "Ларри Эллисон",
                "Майкл Стоунбрейкер",
                "Эдгар Ф. Кодд",
            ],
            4,
        ),
        *topic_questions(7, 5, "Языки программирования"),
        *topic_questions(12, 7, "Сети и протоколы"),
    )
]
