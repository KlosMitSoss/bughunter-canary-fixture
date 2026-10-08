"""In-memory payout queue used only by the Bughunter development canary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Ticket:
    owner: str
    amount: int


class PayoutQueue:
    def __init__(self) -> None:
        self._balances: dict[str, int] = {}
        self._reserved: dict[str, int] = {}
        self._tickets: dict[int, Ticket] = {}
        self._next_ticket = 1

    def deposit(self, owner: str, amount: int) -> None:
        if not owner or amount <= 0:
            raise ValueError("deposit requires an owner and positive amount")
        self._balances[owner] = self.balance(owner) + amount

    def balance(self, owner: str) -> int:
        return self._balances.get(owner, 0)

    def reserved(self, owner: str) -> int:
        return self._reserved.get(owner, 0)

    def request_withdrawal(self, owner: str, amount: int) -> int:
        if not owner or amount <= 0:
            raise ValueError("withdrawal requires an owner and positive amount")
        if amount > self.balance(owner) - self.reserved(owner):
            raise ValueError("insufficient available balance")
        ticket_id = self._next_ticket
        self._next_ticket += 1
        self._tickets[ticket_id] = Ticket(owner, amount)
        self._reserved[owner] = self.reserved(owner) + amount
        return ticket_id

    def settle(self, ticket_id: int, payout: Callable[[str, int], None]) -> None:
        """Invoke the external payout callback for a pending ticket."""
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise KeyError("unknown or already settled ticket")
        payout(ticket.owner, ticket.amount)
        self._reserved[ticket.owner] -= ticket.amount
        self._balances[ticket.owner] -= ticket.amount
        self._tickets.pop(ticket_id, None)
