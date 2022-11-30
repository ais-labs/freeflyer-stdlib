
import json

from python_freeflyer_interface.freeflyer import engine_utils

engine = engine_utils.get_engine('test_engine')

engine.load_missionplan('./tests/api_demo/python_freeflyer_api_demo.MissionPlan')

engine.run_to_apilabel('config_injection')

config = {
    "output_ephem_path_prefix": "./ConvergedTrajectory_",
    "patch_point_file_path":    "./heteroclinic.txt",
    "propagator_type":          "RK89",
    "show_visuals":             1,
    "start_epoch":              "Jan 01 2024 12:00:00.000",
    "use_ff_optimizer":         0,
}


engine.set_string('api_config_json', json.dumps(config))


engine.run_to_apilabel('main_execution_complete')

result = json.loads(engine.get_string('api_response_json'))

logs = engine.get_logs()

for log_line in logs:
    # todo: make utility function to parse logs and run it through proper
    #       python logging functions
    print(f'{log_line}')


print(result)
