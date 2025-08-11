from helm.benchmark.adaptation.common_adapter_specs import (
    get_multiple_choice_joint_adapter_spec,
)
from helm.benchmark.metrics.common_metric_specs import (
    get_exact_match_metric_specs,
)
from helm.benchmark.run_spec import RunSpec, run_spec_function
from helm.benchmark.scenarios.scenario import ScenarioSpec


@run_spec_function("chest")
def get_chest_run_spec() -> RunSpec:
    scenario_spec = ScenarioSpec(class_name="helm.benchmark.scenarios.simple_scenarios.SimpleMCQAScenario")
    adapter_spec = get_multiple_choice_joint_adapter_spec(
        instructions="Answer the following questions with a single letter only.",
        input_noun="Question",
        output_noun="Answer",
    )
    metric_specs = get_exact_match_metric_specs()
    return RunSpec(
        name="chest",
        scenario_spec=scenario_spec,
        adapter_spec=adapter_spec,
        metric_specs=metric_specs,
        groups=["chest"],
    )

