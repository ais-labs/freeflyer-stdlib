# freeflyer-stdlib
A standard library of useful utilities, procedures, constants, and interfaces for use in FreeFlyer.

## Requirements
 - Currently tested with FreeFlyer 7.7.1.55976
 - Set Windows environment variable `FREEFLYER_STDLIB` to point to `freeflyer_stdlib` directory in this repo. e.g. `C:/Users/username/Documents/repos/freeflyer-stdlib/freeflyer_stdlib`
 - If using the Python API, set Windows environment variable `PYTHONPATH` to include the `Runtime API/python/src` directory of the desired FreeFlyer version. e.g. `C:/Users/username/Documents/FreeFlyer/FreeFlyer 7.7.1.55976 (64-Bit)/Runtime API/python/src`

## Suggestions
 - All standard library modules contain brief one-liner summaries of each of the procedures in the module, and all procedures include a more detailed description at their definition. It is well worth the user's time to at least review the one-liner summaries so as to not replicate existing functionality.
 - Familiarize yourself with the contents of `freeflyer_stdlib/global_constants` especially `freeflyer_magic_number.ffmodule`. There are a number of constant variables with semantic names that correspond to various "magic" numbers normally used in FreeFlyer. "Magic" meaning "devoid of any context and a number that just magically makes it work." Rather than using `my_impulsive_burn.AttitudeSystem = 1;` use `my_impulsive_burn.AttitudeSystem = IMPULSIVE_BURN_ATT__VNB;`. Note that the constants use a double underscore to separate a sort of namespace for that constant from the specific constant.

## Contributing
 - Contributions to the FreeFlyer standard library are extremely welcome. Please submit contributions in the form of a merge request.
 - All contributions must adhere to the guidance laid out in `coding_standard.md` and will be subject to the judgment of the current repo maintainer.
