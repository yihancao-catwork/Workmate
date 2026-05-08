from enum import Enum


class PetState(str, Enum):
    RESTING = "resting"
    WALKING = "walking"
    DRAGGED = "dragged"


class PetStateMachine:
    def __init__(self) -> None:
        self.state = PetState.RESTING

    def start_walking(self) -> None:
        if self.state != PetState.DRAGGED:
            self.state = PetState.WALKING

    def start_drag(self) -> None:
        self.state = PetState.DRAGGED

    def end_drag(self) -> None:
        self.state = PetState.RESTING

    def rest(self) -> None:
        if self.state != PetState.DRAGGED:
            self.state = PetState.RESTING