
import json

from python_freeflyer_interface.freeflyer import engine_utils

engine = engine_utils.get_engine('test_engine')

engine.load_missionplan('./tests/api_demo/python_freeflyer_api_demo.MissionPlan')

engine.run_to_apilabel('config_injection')

config = {
    'circularize_seed_kms':        0.050,
    'circularize_perturb_kms':     0.001,
    'circularize_lower_limit_kms': -0.100,
    'circularize_upper_limit_kms': 0.100,
    'desired_sma_change_km':       25.0,
    'post_burn_ecc_tol':           1e-4,
    'raise_seed_kms':              0.050,
    'raise_perturb_kms':           0.001,
    'raise_lower_limit_kms':       -0.100,
    'raise_upper_limit_kms':       0.100,
    'sc_display_name':             "Endeavour",
    'sma_change_tol_km':           0.010,
    'test_message':                "light this candle",
}



engine.set_string('api_config_json', json.dumps(config))


engine.run_to_apilabel('main_execution_complete')

result = json.loads(engine.get_string('api_response_json'))

logs = engine.get_logs()

for log_line in logs:
    # todo: make utility function to parse logs and run it through proper
    #       python logging functions
    print(f'{log_line}')


print(f"missionplan start time: {result['missionplan_start_time']}")
print(f"missionplan duration: {result['missionplan_duration_sec']:.2f} seconds")
print(f"raise burn in-track delta-v: "
      f"{result['raise_burn_deltav_kms']:.5f} km/s"
)
print(f"circularize burn in-track delta-v: "
      f"{result['circularize_burn_deltav_kms']:.5f} km/s"
)
print(f"test message: {result['test_message']}")
