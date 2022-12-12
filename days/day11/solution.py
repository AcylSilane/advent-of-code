"""Solution for day 11"""
from __future__ import annotations
from typing import TextIO, Callable, List, Dict
import copy
import math
import operator
import functools

import logging

import coloredlogs

# At DEBUG level, we reproduce the example throwing log from the problem page
coloredlogs.install(level="INFO", fmt="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


class Item:
    def __init__(self, worry):
        self.worry = worry


class Monkey:
    def __init__(self,
                 index: int,
                 items: List[Item],
                 worry_update_fun: Callable[[int], int],
                 test_divisor: int,
                 target_true: int,
                 target_false: int):
        self.index = index
        self.items = items
        self.worry_update_fun = worry_update_fun
        self.test_divisor = test_divisor
        self.target_true = target_true
        self.target_false = target_false
        self._troop = None

        self.items_inspected = 0

    @classmethod
    def from_text(cls, text: str) -> Monkey:
        lines = [line.lstrip().rstrip() for line in text.split("\n")]
        for line in lines:
            prefix, suffix = line.split(":")
            suffix = suffix.lstrip().replace(",", "").split(" ")
            if prefix.startswith("Monkey"):
                index = int(line.split(" ")[-1][:-1])
            elif prefix == "Starting items":
                items = [Item(int(worry)) for worry in suffix]
            elif prefix == "Operation":
                update_operation, update_operand = suffix[-2:]

                op_table = {"+": operator.add,
                            "*": operator.mul}
                operation = op_table[update_operation]
                if update_operand == "old":
                    def worry_update_fun(current_worry: int):
                        return operation(current_worry, current_worry)
                else:
                    def worry_update_fun(current_worry: int):
                        return operation(current_worry, int(update_operand))
            elif prefix == "Test":
                test_divisor = int(suffix[-1])
            elif prefix == "If true":
                target_true = int(suffix[-1])
            elif prefix == "If false":
                target_false = int(suffix[-1])

        new_monkey = Monkey(index=index,
                            items=items,
                            worry_update_fun=worry_update_fun,
                            test_divisor=test_divisor,
                            target_true=target_true,
                            target_false=target_false)
        return new_monkey

    @property
    def troop(self):
        return self._troop

    @troop.setter
    def troop(self, new_troop: Troop):
        self._troop = new_troop

    def inspect_item(self, item: Item) -> None:
        self.items_inspected += 1
        logger.debug(f"\tMonkey inspects an item with a worry level of {item.worry}")
        old_worry = item.worry
        new_worry = self.worry_update_fun(old_worry)
        if not self.troop.is_hopeful:
            new_worry %= self.troop.max_divisor
        item.worry = new_worry
        logger.debug(f"\t\tWorry level is now {item.worry}.")

    def is_worried(self, item: Item) -> bool:
        result = (item.worry % self.test_divisor) == 0
        return result

    def throw_to(self, index: int, item: Item):
        logger.debug(f"\t\tItem with worry level {item.worry} thrown to monkey {index}")
        self.troop.monkeys[index].catch(item)

    def catch(self, item: Item):
        self.items.append(item)

    def execute_turn(self):
        logger.debug(f"Monkey {self.index}")
        while self.items:
            item = self.items.pop(0)
            self.inspect_item(item)
            if self.troop.is_hopeful:
                item.worry = int(math.floor(item.worry / 3))
            logger.debug(f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {item.worry}")
            if self.is_worried(item):
                logger.debug(f"\t\tCurrent level worry is divisible by {self.test_divisor}")
                self.throw_to(self.target_true, item)
            else:
                logger.debug(f"\t\tCurrent level worry is not divisible by {self.test_divisor}")
                self.throw_to(self.target_false, item)


class Troop:
    def __init__(self):
        self.monkeys = {}
        self.is_hopeful = True
        self.max_divisor = 1

    @classmethod
    def from_file(cls, file: TextIO) -> Troop:
        instance = cls()
        inputs = file.read().split("\n\n")
        monkeys = [Monkey.from_text(text) for text in inputs]
        for monkey in monkeys:
            monkey.troop = instance
        instance.monkeys = {monkey.index: monkey for monkey in monkeys}
        instance.max_divisor = functools.reduce(operator.mul, (monkey.test_divisor for monkey in monkeys))
        return instance

    def execute_round(self) -> Troop:
        for index in sorted(self.monkeys.keys()):
            self.monkeys[index].execute_turn()
        return self

    @property
    def monkey_business(self) -> Dict[int, int]:
        activities = {index: monkey.items_inspected for index, monkey in self.monkeys.items()}
        monkey_business = functools.reduce(operator.mul, sorted(activities.values())[-2:])
        return monkey_business


if __name__ == "__main__":
    with open("input.txt", "r") as inp:
        troop_1 = Troop.from_file(inp)
        troop_2 = copy.deepcopy(troop_1)

    for keepaway_round in range(20):
        troop_1.execute_round()

    print(f"Part 1: {troop_1.monkey_business}")

    troop_2.is_hopeful = False
    for keepaway_round in range(10000):
        troop_2.execute_round()

    print(f"Part 2: {troop_2.monkey_business}")
