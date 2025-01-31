class Event:
    MESSAGE = "message"


class ClientEvent(Event):
    GET_TOPICS = "get_topics"
    GET_QUESTIONS = "get_questions"
    JOIN_GAME = "join_game"
    ANSWER = "answer"


class ServerEvent(Event):
    class Error:
        NOT_FOUND = "not_found_error"
        VALIDATION = "validation_error"

    class Game:
        TOPICS = "topics"
        GAME = "game"
        OVER = "over"
        JOINED = "joined_game"
