"""
FreeFlyer Engine

A wrapper around the native FreeFlyer Python API

"""

# native imports
from enum import IntEnum
import logging
import os


# third party imports


# local imports
from aisolutions.freeflyer.runtimeapi.DiagnosticLevel import DiagnosticLevel
from aisolutions.freeflyer.runtimeapi.RuntimeApiEngine import RuntimeApiEngine
from aisolutions.freeflyer.runtimeapi.RuntimeApiException \
        import RuntimeApiException

from .. import config


log = logging.getLogger(__name__)

class FreeFlyerEngineOutput(IntEnum):
    """
    Values related to aisolutions.freeflyer.runtimeapi
                      .ConsoleOutputProcessingMethod
                      .ConsoleOutputProcessingMethod
    """
    REDIRECT_TO_API  = 0
    REDIRECT_TO_HOST = 1
    SUPPRESS         = 2


class FreeFlyerEngineWindowMode(IntEnum):
    """
    Values related to aisolutions.freeflyer.runtimeapi
                      .WindowedOutputMode.WindowedOutputMode
    """
    NO_WINDOWS            = 0
    SHOW_FULL_UI          = 1
    UNCONSTRAINED_WINDOWS = 2
    IMAGES_ONLY           = 3


class FreeFlyerEngineHandles(dict):
    """
    Singleton that is essentially just a global dictionary. Stores instances
    of FreeFlyerEngineHandle for retrieval.
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = {}
        return cls.instance


def get_engine(
        engine_name='',
        engine_output=FreeFlyerEngineOutput.REDIRECT_TO_API,
        window_mode=FreeFlyerEngineWindowMode.NO_WINDOWS,
    ):
    """
    Generates or retrieves a handle to the FreeFlyer engine.
    """

    engines = FreeFlyerEngineHandles()

    if engine_name in engines:
        log.info("using existing engine: %s", engine_name)
        return engines[engine_name]

    log.info("engine '%s' doesn't exist. creating new engine", engine_name)

    log.debug("freeflyer exe path: %s", engine_output)
    log.debug("engine output: %s", engine_output)
    log.debug("window mode: %s", window_mode)

    raw_freeflyer_engine = RuntimeApiEngine(
        config.FF_EXE_PATH,
        consoleOutputProcessingMethod=engine_output,
        windowedOutputMode=window_mode,
    )

    engines[engine_name] = FreeFlyerEngineHandle(
        engine=raw_freeflyer_engine,
        name=engine_name,
    )

    return engines[engine_name]



class FreeFlyerEngineHandle():
    """
    FreeFlyerEngineHandle
    A wrapper around the native FreeFlyer Python API
    """

    def __init__(self, engine, name):
        self.engine = engine
        self.name = name


    def run_to_apilabel(self, label):
        """
        Attempts to execute the loaded FreeFlyer missionplan to
        the specified ApiLabel.
        """

        assert label is not None
        assert label != ''

        try:
            self.execute_until_api_label(label)
        except RuntimeApiException as freeflyer_exception:
            print('oops %s', freeflyer_exception)


    def get_runtime_errors(self):
        """
        Returns any runtime errors experienced by FreeFlyer. These are
        the errors that would be seen in the yellow box if running
        in FreeFlyer IDE mode.
        """
        diagnostics = self.engine.getMissionPlanDiagnostics(
            diagnosticLevel=DiagnosticLevel.IncludeSourceDetails
        )

        return diagnostics.errors


    def load_missionplan(self, missionplan_path):
        """
        Loads a missionplan into the FreeFlyer engine.
        """

        log.debug('loading missionplan: %s', missionplan_path)

        if not os.path.isfile(missionplan_path):
            raise IOError(f"missionplan '{missionplan_path}' does not exist")

        result = self.load_missionplan_from_file(missionplan_path)
        result = self.prepare_missionplan()

        return result


    def get_logs(self):
        """
        Retrieves console logs, splits into a list of lines, and adds
        the current engine's name to each log line.
        """
        raw_console_lines = self.get_console_output().split('\n')

        console_lines = []
        for console_line in raw_console_lines:
            if console_line == '':
                continue # no blank lines

            console_lines.append(f"[{self.name}]{console_line}")

        return console_lines



    #### pass-throughs of native FreeFlyer methods ############################
    #### doesn't change anything other than using more pythonic naming ########

    def destroy_engine(self):
        """
        Pass-through for FreeFlyer API function destroyEngine
        """
        return self.engine.destroyEngine()

    def execute_until_api_label(self, label):
        """
        Pass-through for FreeFlyer API function executeUntilApiLabel
        """
        return self.engine.executeUntilApiLabel(label)

    def get_console_output(self):
        """
        Pass-through for FreeFlyer API function getConsoleOutput
        """
        return self.engine.getConsoleOutput()

    def get_string(self, name):
        """
        Pass-through for FreeFlyer API function getString
        """
        return self.engine.getExpressionString(name)

    def get_variable(self, name):
        """
        Pass-through for FreeFlyer API function getVariable
        """
        return self.engine.getExpressionVariable(name)

    def load_missionplan_from_file(self, missionplan_path):
        """
        Pass-through for FreeFlyer API function loadMissionPlanFromFile
        """
        return self.engine.loadMissionPlanFromFile(missionplan_path)

    def prepare_missionplan(self):
        """
        Pass-through for FreeFlyer API function prepareMissionPlan
        """
        return self.engine.prepareMissionPlan()

    def set_string(self, name, value):
        """
        Pass-through for FreeFlyer API function setString
        """
        return self.engine.setExpressionString(name, value)

    def set_variable(self, name, value):
        """
        Pass-through for FreeFlyer API function setVariable
        """
        return self.engine.setExpressionVariable(name, value)
