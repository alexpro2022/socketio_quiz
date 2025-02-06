class Message:
    ON_CONNECT = "Пользователь {sid} подключился"
    ADDED_TO_WAITING_ROOM = "Пользователь {sid} добавлен в зал ожидания"
    GAME_STARTED = "Игра началась"
    GAME_NOT_FOUND = "Game with uid {game_uid} not found"
    GAME_OVER = "Игра закончена. Победил {player}"
    PLAYER_NOT_FOUND = "Player with sid {sid} not found"
