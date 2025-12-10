import cvxpy as cp
from pathlib import Path
import re
from pydantic import BaseModel, Field, field_validator


class Machine(BaseModel):

    indicator_lights: list[int] = Field(..., description="Desired light pattern for the machine")
    buttons: list[tuple[int, ...]] = Field(..., description="Button activations for the machine")
    joltages: list[int] = Field(..., description="Joltages for the machine")

    @field_validator("indicator_lights", mode="before")
    @classmethod
    def parse_indicator_lights(cls, v) -> list[int]:
        v = v.strip("[]")
        return [0 if el == "." else 1 for el in str(v)]
    
    @field_validator("buttons", mode="before")
    @classmethod
    def parse_buttons(cls, v) -> list[tuple[int, ...]]:
        buttons = [button.strip("()") for button in v]
        buttons = [tuple(int(el) for el in button if el != ",") for button in buttons]
        return buttons
    
    @field_validator("joltages", mode="before")
    @classmethod
    def parse_joltages(cls, v) -> list[int]:
        v = v.strip("{}")
        return [int(el) for el in str(v).split(",")]
    
            
def parse_input(filepath: Path) -> list[Machine]:
    with open(filepath, "r") as file:
        lines = file.readlines()

    machines = []
    for line in lines:
        machines.append(
            Machine(
                indicator_lights=re.search(r"\[\S+\]", line).group(),
                buttons=re.findall(r"\(\S+\)", line),
                joltages=re.search(r"\{\S+\}", line).group(),
            )
        )

    return machines

class Optimizer:
    def __init__(self, machine: Machine, is_button_binary: bool):
        self.machine = machine
        self.num_buttons = len(machine.buttons)

        # Each button is a binary variable (pressed or not pressed)
        if is_button_binary:
            self.button_vars = cp.Variable(self.num_buttons, boolean=True)
        else:
            self.button_vars = cp.Variable(self.num_buttons, integer=True, nonneg=True)

        # Auxiliary variables to do mod 2 operations for lighting constraints
        if is_button_binary:
            self.auxillary_vars = cp.Variable(len(self.machine.indicator_lights), integer=True)
            
    def create_constraints(self, *, for_lighting: bool, for_joltage: bool) -> list[cp.Constraint]:
        
        constraints = []
        for idx in range(0, len(self.machine.indicator_lights)):
            button_effects = [j for j, button in enumerate(self.machine.buttons) if idx in button]

            if for_lighting:
                # The sum of the pressed buttons' effects must match the indicator lights
                constraints.append(
                    cp.sum(self.button_vars[button_effects]) - 2 * self.auxillary_vars[idx] == self.machine.indicator_lights[idx]
                )
                
            if for_joltage:
                # Each button press raises the joltage and must match the desired joltage
                constraints.append(cp.sum(self.button_vars[button_effects]) == self.machine.joltages[idx])

        return constraints
    
    
    def solve(self, *, for_lighting: bool, for_joltage: bool) -> list[int]:
        constraints = self.create_constraints(for_lighting=for_lighting, for_joltage=for_joltage)
        objective = cp.Minimize(cp.sum(self.button_vars))
        problem = cp.Problem(objective, constraints)
        problem.solve()
        return [round(var) for var in self.button_vars.value]

def main(filepath: Path, *, for_lighting: bool, for_joltage: bool) -> int:
    machines = parse_input(filepath)
    total_presses = 0
    for machine in machines:
        optimizer = Optimizer(machine, is_button_binary=True if for_lighting else False)
        solution = optimizer.solve(for_lighting=for_lighting, for_joltage=for_joltage)
        total_presses += sum(solution)

    return total_presses


if __name__ == "__main__":
    result = main(Path("inputs/day10.txt"), for_lighting=True, for_joltage=False)
    print(f"Part 1: {result}")

    result = main(Path("inputs/day10.txt"), for_lighting=False, for_joltage=True)
    print(f"Part 2: {result}")