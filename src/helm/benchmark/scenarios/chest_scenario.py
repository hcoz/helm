from typing import List
import yaml
from importlib import resources
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
    """Medical multiple-choice question answering scenario for chest medicine.

    The task is to answer medical questions about chest medicine with a single letter only.

    Example:

        Answer the following questions with a single letter only.

        Question: A 36-year-old immunocompetent male patient was admitted to the hospital with prolonged recurrent fever, cough, anorexia and weight loss...
        A. Isoniazid, rifampicin, ethambutol and pyrazinamide for 6 months
        B. Rifampicin, ethambutol and pyrazinamide for 6 months
        C. Isoniazid, rifampicin, ethambutol and pyrazinamide for 2 months followed by rifampicin, and pyrazinamide for 4 months
        D. Streptomycin, rifampicin, ethambutol and pyrazinamide for 2 months followed by rifampicin, ethambutol and pyrazinamide for 4 months
        E. Moxifloxacin, rifampicin, ethambutol and pyrazinamide for 2 months followed by rifampicin and moxifloxacin for 4 months
        Answer: B"""

    name = "chest"
    description = "Answer medical multiple-choice questions about chest medicine."
    tags = ["question answering", "medical", "chest"]

    def __init__(self):
        self.yaml_path = "chest_test.yaml"
        self.instances_data = self._load_yaml_data()
        super().__post_init__()  # This sets the definition_path

    def _load_yaml_data(self):
        """Load the MCQ data from the YAML file using HELM's package-based approach."""
        try:
            # Use HELM's package-based approach to load YAML files
            yaml_content = resources.files("helm.benchmark.static").joinpath(self.yaml_path).read_text(encoding="utf-8")
            data = yaml.safe_load(yaml_content)
            return data
        except Exception as e:
            raise RuntimeError(f"Failed to load YAML data from {self.yaml_path}: {e}")

    def get_instances(self, output_path: str) -> List[Instance]:
        instances: List[Instance] = []

        if not self.instances_data or 'instances' not in self.instances_data:
            raise ValueError("Invalid YAML structure: 'instances' key not found")

        for i, instance_data in enumerate(self.instances_data['instances']):
            # Extract question data
            question_id = instance_data.get('id', f'Q{i+1}')
            question_text = instance_data.get('input', '')
            options = instance_data.get('options', [])
            correct_answer = instance_data.get('correct_answer', '')

            # Skip if missing required data
            if not question_text or not options or not correct_answer:
                continue

            # Handle multiple correct answers (some questions have multiple correct options)
            if isinstance(correct_answer, list):
                correct_answers = correct_answer
            else:
                correct_answers = [correct_answer]

            # Format the question with options
            formatted_question = f"{question_text}\n"
            for j, option in enumerate(options):
                option_letter = chr(65 + j)  # A, B, C, D, E...
                formatted_question += f"{option_letter}. {option}\n"

            # Create references for each option
            references = []
            for j, option in enumerate(options):
                option_letter = chr(65 + j)
                is_correct = option_letter in correct_answers
                references.append(
                    Reference(
                        Output(text=option_letter),
                        tags=[CORRECT_TAG] if is_correct else []
                    )
                )

            # Create the instance
            input_obj = Input(text=formatted_question)
            instance = Instance(
                input=input_obj,
                references=references,
                split=TEST_SPLIT  # All medical questions go to test split
            )
            instances.append(instance)

        return instances
