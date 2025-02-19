from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, Field

NonNegativeInt = Annotated[int, Field(ge=0)]
StrType = Annotated[str, Field(min_length=1)]


class Topic(BaseModel):
    pk: NonNegativeInt
    name: StrType


class Answer(BaseModel):
    index: NonNegativeInt
    game_uid: UUID


class BM(BaseModel):
    @classmethod
    def model_validate(cls, obj):
        return super().model_validate(
            obj.model_dump() if isinstance(obj, BaseModel) else obj
        )


# Question =======================================================
class QuestionOut(BM):
    pk: NonNegativeInt
    topic: NonNegativeInt
    text: StrType
    options: list[StrType]


class Question(QuestionOut):
    answer: NonNegativeInt


# Player ===========================================================
class PlayerOut(BaseModel):
    sid: StrType
    name: StrType
    score: NonNegativeInt = 0


class Player(PlayerOut):
    question_pointer: NonNegativeInt = 0


# GAME ==============================================================
class JoinGame(BaseModel):
    topic_pk: NonNegativeInt
    name: StrType


class GameBase(BaseModel):
    uid: UUID


class GameOut(GameBase):
    players: list[PlayerOut]
    current_question: QuestionOut
    question_count: NonNegativeInt

    def model_dump(self):
        dump = super().model_dump()
        dump["uid"] = str(self.uid)
        return dump


class Game(GameBase):
    questions: list[Question]
    players: list[Player]

    def init(self):
        for p in self.players:
            assert p.score == 0
            assert p.question_pointer == 0
        return self.output()

    def output(self, player: Player | None = None):
        q_pointer = 0 if player is None else player.question_pointer
        return GameOut(
            **self.model_dump(),
            current_question=self.questions[q_pointer],
            question_count=len(self.questions) - q_pointer,
        ).model_dump()


class ServiceToWeb(BaseModel):
    event: Any
    data: Any | None = None
    to: Any | None = None
    room: Any | None = None
