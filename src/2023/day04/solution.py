# Day 4 solution
from __future__ import annotations
from functools import cached_property, cache
import re
from typing import Set, List, Dict


class Card:
    def __init__(self, index: int, winning_numbers: Set[int], drawn_numbers: Set[int]):
        self.index = index
        self.winning_numbers = winning_numbers
        self.drawn_numbers = drawn_numbers
        self._deck = None

    @property
    def deck(self) -> List[Card]:
        return self._deck

    @deck.setter
    def deck(self, deck: List[Card]) -> None:
        self._deck = deck

    @classmethod
    def from_string(cls, string: str) -> Card:
        card_str, win_str, num_str = re.split(r"[:|]", string)
        index = int(card_str.strip().split()[-1])
        winning_numbers = {int(num) for num in win_str.strip().split()}
        drawn_numbers = {int(num) for num in num_str.strip().split()}
        return cls(index, winning_numbers, drawn_numbers)

    def __repr__(self) -> str:
        return f"{self.index}: {self.winning_numbers} | {self.drawn_numbers}"

    @cached_property
    def num_matches(self) -> int:
        return len(self.winning_numbers.intersection(self.drawn_numbers))

    @cached_property
    def part1_score(self) -> int:
        if self.num_matches == 0:
            return 0
        else:
            return 2 ** (self.num_matches - 1)

    @cached_property
    def direct_children(self) -> List[Card]:
        if self.deck is None:
            raise ValueError("Deck not set")

        indices = [self.index + i for i in range(1, self.num_matches + 1)]
        return [self.deck[index] for index in indices]

    @cache
    def explode(self) -> Dict[int: int]:
        if self.deck is None:
            raise ValueError("Deck not set")

        counts = {index: 0 for index in self.deck} | {self.index: 1}
        for child in self.direct_children:
            counts = self.add_dicts(counts, child.explode())

        return counts

    @staticmethod
    def add_dicts(d1: Dict[int, int], d2: Dict[int, int]) -> Dict[int, int]:
        """Add two dictionaries together. We know the keys are the same, don't need to check"""
        return {k: d1[k] + d2[k] for k in d1}



with open("input.txt") as inp:
    cards = {}
    for line in inp:
        card = Card.from_string(line)
        cards[card.index] = card

# Set the deck
for card in cards.values():
    card.deck = cards

part1_score = sum(card.part1_score for card in cards.values())
print(f"Part 1: {part1_score}")

# For part 2, every child card has to have an index higher than the parent
# So, if we iterate from the reverse, we can only hit the base case before the parent

part2_sums = {index: 0 for index in cards}
for card in reversed(cards.values()):
    part2_sums = Card.add_dicts(part2_sums, card.explode())
print(f"Part 2: {sum(part2_sums.values())}")
