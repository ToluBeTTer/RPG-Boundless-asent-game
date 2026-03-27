from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .character import Character
from .quests import QuestLog

ClientCommand = Literal["move", "attack", "meditate", "heartbeat", "chat"]


@dataclass
class ChatMessage:
    tick: int
    player_id: str
    text: str


@dataclass
class PlayerSession:
    player_id: str
    character: Character
    zone: str = "Verdant Frontier"
    x: int = 0
    y: int = 0
    quest_log: QuestLog = field(default_factory=QuestLog)
    party_id: str | None = None


@dataclass
class WorldState:
    tick: int = 0
    sessions: dict[str, PlayerSession] = field(default_factory=dict)
    parties: dict[str, set[str]] = field(default_factory=dict)
    chat_log: list[ChatMessage] = field(default_factory=list)


class GameServerState:
    def __init__(self):
        self.state = WorldState()

    def connect_player(self, player_id: str, character: Character) -> PlayerSession:
        session = PlayerSession(player_id=player_id, character=character)
        self.state.sessions[player_id] = session
        return session

    def disconnect_player(self, player_id: str) -> None:
        session = self.state.sessions.pop(player_id, None)
        if not session or not session.party_id:
            return
        party = self.state.parties.get(session.party_id)
        if party:
            party.discard(player_id)
            if not party:
                del self.state.parties[session.party_id]

    def create_party(self, leader_id: str, party_id: str) -> None:
        self.state.parties[party_id] = {leader_id}
        self.state.sessions[leader_id].party_id = party_id

    def join_party(self, player_id: str, party_id: str) -> bool:
        if party_id not in self.state.parties:
            return False
        self.state.parties[party_id].add(player_id)
        self.state.sessions[player_id].party_id = party_id
        return True

    def apply_command(self, player_id: str, command: ClientCommand, payload: dict | None = None) -> None:
        payload = payload or {}
        session = self.state.sessions[player_id]
        character = session.character

        if command == "move":
            session.x += int(payload.get("dx", 0))
            session.y += int(payload.get("dy", 0))
        elif command == "attack":
            character.spend_stamina(5)
        elif command == "meditate":
            character.train_soul(1)
            character.essence_pool = min(150, character.essence_pool + 5)
        elif command == "heartbeat":
            pass
        elif command == "chat":
            text = str(payload.get("text", ""))[:200]
            self.state.chat_log.append(ChatMessage(self.state.tick, player_id, text))

    def tick(self) -> None:
        self.state.tick += 1
        for session in self.state.sessions.values():
            char = session.character
            char.stamina = min(100, char.stamina + 2)
            char.essence_pool = min(150, char.essence_pool + 1)
