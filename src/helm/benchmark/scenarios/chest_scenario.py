from typing import List
from helm.benchmark.scenarios.scenario import (
    Scenario,
    Instance,
    Reference,
    TRAIN_SPLIT,
    TEST_SPLIT,
    CORRECT_TAG,
    Input,
    Output,
)

class ChestScenario(Scenario):
    """Simple multiple-choice question answering scenario for tutorials and debugging.

    The task is to answer questions about whether two-digit numbers are even or odd.

    Example:

        Answer the following questions with a single letter only.

        Question: Is 24 even or odd?
        A. Even
        B. Odd
        Answer: A"""

    name = "chest"
    description = "Answer if two-digit numbers are even or odd."
    tags = ["question answering"]

    def get_instances(self, output_path: str) -> List[Instance]:
        instances: List[Instance] = []
        for i in range(10, 100):
            # NOTE: For simplicity, the input text and reference output text
            # is the same for all instances.
            # However, for most question answering scenarios, the input text
            # and reference output text can vary between questions.
            input = Input(text=f"Is {i} even or odd?")
            references = [
                Reference(Output(text="Even"), tags=[CORRECT_TAG] if i % 2 == 0 else []),
                Reference(Output(text="Odd"), tags=[CORRECT_TAG] if i % 2 == 1 else []),
            ]
            split = TRAIN_SPLIT if i <= 20 else TEST_SPLIT
            instance = Instance(input=input, references=references, split=split)
            instances.append(instance)
        return instances
