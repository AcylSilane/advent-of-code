# Day 6
from __future__ import annotations
from typing import Literal, List
from functools import total_ordering
import collections

Card = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


@total_ordering
class Hand:
    type_order = {
        "five_of_a_kind": 7,
        "four_of_a_kind": 6,
        "full_house": 5,
        "three_of_a_kind": 4,
        "two_pair": 3,
        "one_pair": 2,
        'high_card': 1,
    }
    card_order = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        '9': 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    is_part2 = False

    def __init__(self, cards: List[Card], bid: int):
        self.cards = cards
        self.bid = bid

    def copy(self) -> Hand:
        return Hand(self.cards.copy(), self.bid)

    @classmethod
    def from_string(cls, string: str) -> Hand:
        hand, bid = string.strip().split()
        return cls(list(hand), int(bid))

    @classmethod
    def set_part2(cls):
        cls.card_order["J"] = 1
        cls.is_part2 = True

    def __repr__(self) -> str:
        return f"Hand({self.cards}, {self.bid}, {self.hand_type})"

    @property
    def hand_type(self) -> str:
        if self.is_part2:
            non_jack_counts = collections.Counter([card for card in self.cards if card != "J"])
            if non_jack_counts:
                most_abundant = non_jack_counts.most_common(1)[0][0]
            else:
                most_abundant = "J"

            fixed_hand = []
            for card in self.cards:
                if card == "J":
                    fixed_hand.append(most_abundant)
                else:
                    fixed_hand.append(card)
            counts = collections.Counter(fixed_hand)
        else:
            counts = collections.Counter(self.cards)
        counts = sorted(list(counts.values()))

        if counts == [5]:
            result = "five_of_a_kind"
        elif counts == [1, 4]:
            result = "four_of_a_kind"
        elif counts == [2, 3]:
            result = "full_house"
        elif counts == [1, 1, 3]:
            result = "three_of_a_kind"
        elif counts == [1, 2, 2]:
            result = "two_pair"
        elif counts == [1, 1, 1, 2]:
            result = "one_pair"
        elif counts == [1, 1, 1, 1, 1]:
            result = "high_card"
        else:
            raise ValueError("Invalid hand")

        return result

    def card_value(self, card: Card) -> int:
        return self.card_order[card]

    def __lt__(self, other: Hand) -> bool:
        if self.hand_type == other.hand_type:
            for card1, card2 in zip(self.cards, other.cards):
                if self.card_value(card1) != self.card_value(card2):
                    return self.card_value(card1) < self.card_value(card2)
            else:
                raise ValueError("Invalid hand")
        else:
            return self.type_order[self.hand_type] < self.type_order[other.hand_type]

    def __eq__(self, other: Hand) -> bool:
        if self.hand_type == other.hand_type:
            for card1, card2 in zip(self.cards, other.cards):
                if self.card_value(card1) != self.card_value(card2):
                    return False
            else:
                return True
        else:
            return self.type_order[self.hand_type] == self.type_order[other.hand_type]


with open("input.txt", "r") as inp:
    hands = [Hand.from_string(line) for line in inp]

part1_acc = 0
for rank, hand in enumerate(sorted(hands), start=1):
    part1_acc += hand.bid * rank
print(f"Part 1: {part1_acc}")

Hand.set_part2()

part2_acc = 0
for rank, hand in enumerate(sorted(hands), start=1):
    part2_acc += hand.bid * rank
print(f"Part 2: {part2_acc}")
