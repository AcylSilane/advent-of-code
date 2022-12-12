"""Solution to day 10"""
from __future__ import annotations

from typing import TextIO, Tuple
from abc import ABC, abstractmethod
import logging

import coloredlogs

# Currently logged things:
#   - at DEBUG level, instructions when they begin and end execution. Also register value updates.
#   - at INFO level, signal strength monitors when they execute
coloredlogs.install(level="WARNING", fmt="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


class Register:
    def __init__(self, initial_value=1):
        self.value = initial_value

    def __add__(self, other):
        self.value += other
        logger.debug(f"Register set to {self.value}")
        return self

    def __repr__(self):
        return f"<Register at {id(self)}, value={self.value}>"


class Clock:
    def __init__(self):
        self.time = 1
        self.monitors = []

    def __repr__(self):
        return f"<Clock at {id(self)}, time={self.time}>"

    def tick(self):
        self.time += 1
        for monitor in self.monitors:
            monitor.execute()

    def register_monitor(self, monitor: Monitor):
        self.monitors.append(monitor)


class Instruction(ABC):
    def __init__(self, simulated_machine: SimulatedMachine):
        self.clock = simulated_machine.clock
        self.simulated_machine = simulated_machine
        self.name = "instruction"

    @property
    @abstractmethod
    def cycle_time(self) -> int:
        ...

    @abstractmethod
    def operation(self, argv):
        ...

    def execute(self, argv) -> None:
        logger.debug(f"{self.name} {argv} starting on tick {self.clock.time}")
        for _ in range(self.cycle_time - 1):
            self.clock.tick()

        # The operation must happen at the end of the cycle time
        self.operation(argv)
        self.clock.tick()
        logger.debug(
            f"{self.name} {argv} complete on tick {self.clock.time}, eax at {self.simulated_machine.eax.value}")


class Noop(Instruction):
    def __init__(self, simulated_machine: SimulatedMachine):
        super().__init__(simulated_machine)
        self.name = "noop"

    @property
    def cycle_time(self) -> int:
        return 1

    def operation(self, argv):
        return None


class Addx(Instruction):
    def __init__(self, simulated_machine: SimulatedMachine):
        super().__init__(simulated_machine)
        self.name = "addx"

    @property
    def cycle_time(self) -> int:
        return 2

    def operation(self, argv):
        amount = int(argv[0])
        self.simulated_machine.eax += amount


class SimulatedMachine:
    def __init__(self):
        self.clock = Clock()
        self.eax = Register()

        self.instruction_set = {
            "noop": Noop(self),
            "addx": Addx(self)
        }

        self.crt = CRT(self)
        self.monitor = SignalStrengthTracker(self)
        self.clock.register_monitor(self.monitor)
        self.clock.register_monitor(self.crt)
        self.crt.execute()

    def __repr__(self):
        return f"<SimulatedMachine at {id(self)}, clock={self.clock}, eax={self.eax}>"

    def read_tape(self, file: TextIO):
        for line in file:
            argv = line.strip().split()
            instruction = self.instruction_set[argv[0]]
            args = argv[1:]
            instruction.execute(args)


class Monitor(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...


class SignalStrengthTracker(Monitor):
    def __init__(self, simulated_machine):
        self.simulated_machine = simulated_machine
        self.monitored_times = (20, 60, 100, 140, 180, 220)
        self.total_signal_strength = 0

    def execute(self):
        if self.simulated_machine.clock.time in self.monitored_times:
            signal_strength = self.simulated_machine.eax.value * self.simulated_machine.clock.time
            self.total_signal_strength += signal_strength
            logger.info(f"Signal strength on tick {self.simulated_machine.clock.time} is {signal_strength}. " +
                        f"Total strength so far is {self.total_signal_strength}")


class CRT(Monitor):
    def __init__(self, simulated_machine):
        self.simulated_machine = simulated_machine
        self.screen_width = 40
        self.screen_height = 6

        self.screen_state = []
        for _ in range(self.screen_height):
            self.screen_state.append(["."] * self.screen_width)

    @property
    def beam_position(self) -> Tuple[int, int]:
        beam_row, beam_column = divmod(self.simulated_machine.clock.time-1, self.screen_width)
        return beam_row, beam_column

    @property
    def sprite_range(self) -> Tuple[int, int, int]:
        center = self.simulated_machine.eax.value
        sprite_range = (center - 1, center, center + 1)
        return sprite_range

    def execute(self) -> None:
        beam_row, beam_column = self.beam_position

        if beam_row < 6 and beam_column in self.sprite_range:
            self.screen_state[beam_row][beam_column] = "#"

    def show(self):
        return "\n".join(["".join(row) for row in self.screen_state])


if __name__ == "__main__":
    comms_system = SimulatedMachine()
    with open("input.asm", "r") as tape:
        comms_system.read_tape(tape)

    print(f"Part 1: {comms_system.monitor.total_signal_strength}")
    print("Part 2:")
    print(comms_system.crt.show())
