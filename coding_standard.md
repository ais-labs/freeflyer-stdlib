# Introduction
This coding standard is intended to serve as guidance more than a rigid ruleset. A perfectly rigid coding standard would need to be excessively verbose and still not be capable of covering all possible cases. This is intended to be a living document that will be updated from time to time.

Suggestions for additions or changes to the coding standard are welcome; please suggest them to the current repository maintainer.

It is believed that the guidance in this document would benefit most missions/projects, but that is left to their developers' discretion. However, new code being added to this repository must adhere to this document.

The most important rule in this document is this: **write code that communicates.**

# General
 - Only code using the Nanosecond mode shall be accepted.
 - At all times there shall be a string in scope named `CODE_LOCATION` to be used by logging macros. It must be declared near the top of the boilerplate freeform and must be updated at the top of each subsequent freeform. This is so that logs can state where the log line is coming from.
 - In the case of freeforms, `CODE_LOCATION` shall start with `FFN` where `N` is the number of the current freeform. There should also be an extremely short string to describe the freeform. e.g. `CODE_LOCATION = 'FF4 sc setup';`
 - In the case of procedures, `CODE_LOCATION` shall contain the verbatim name of the procedure.
 - The `global_constants/config.ffmodule` is assumed to be in scope and the missionplan will fail without it. Developers are welcome to import their own version of the `config.ffmodule` file if the default values are not acceptable, but all fields must be present.
 - All freeforms shall start with a blank line and end with a blank line. This makes the missionplan XML much easier to read and thus review in a merge request.
 - Try to keep related data together. Rather than making three `Array`s and a `StringArray` with the understanding that they should all align with the same index, make a `Struct` with three `Variable` fields and a `String` field and then make a `List` of that `Struct`. That way the data can't possible be mixed up since it's treated as a single concept. Since you already consider a single concept in your head, consider a single concept in your code.

# Separation of concerns
 - "Separation of Concerns" is a computer science best practice that recommends walling off unrelated parts of an application from each other, allowing easier development and debugging. The intent is for the code associated with each task in the missionplan to be able to abstract away all other tasks to well-defined interfaces. That way, if one needs to be changed, only that section is affected. As an example, if it is decided that a missionplan's plot generation needs to be changed from FreeFlyer-native to an external MATLAB application, the code that performs targeting or ephem ingestion should not be affected by this change. From their point of view they still just "send the stuff that needs to be plotted to the code that does the plotting". The fact that under the hood the plotting code is simply passing the data to FreeFlyer-native plotting functions or to something else is not information that the other code should or need to have in order to perform its job. For a more detailed explanation, see the [Wikipedia article on Separation of Concerns](https://en.wikipedia.org/wiki/Separation_of_concerns).
- A good rule of thumb for enforcing the separation of concerns is to ask yourself "what does this procedure / missionplan / piece of code do?" If your answer includes the word "and" then there's a good chance it should be broken down into smaller pieces.

# Magic Numbers/Strings
 - A "magic" number or string is one which is included in the code completely devoid of context. These are extremely dangerous and difficult to maintain and outside of very limited circumstances (i.e. extreme sanity checks) will not be accepted.
     - `landsat7.MassTotal = config.landsat7_mass_kg + 57; // bad, what does that 57 represent? what if it changes and this is missed since there is no context?`
     - `product_output += "ITAR restricted"; // bad, this message should be in a config shared by all code in the project in case the ITAR message changes`
     - `For i = 0 to input.Count-1; // good, the zero isn't an arbitrary number, it's just the start of the array. Similarly, the -1 is OK since .Count-1 is the end of the array`


# Hard-coded Numbers/String
 - Avoid using raw hard-coded numbers and strings in code logic. These values that are being compared against can be changed, and hunting them down in the code is time consuming and error-prone. Instead, when possible those values should be declared as constant `Variable`s and `String`s so they can be given semantic names.
     - `If (config.tank_mode = 3); // bad, no context, and the '3' might change`
     - `If (config.tank_mode = TANK_BLOWDOWN); // good`

# Constants
 - `Constant`s are your friend. If you don't expect a number or string to change, make it a `Constant` so that if it unexpectedly is changed FreeFlyer alerts you.
 - See [Naming](#naming) section for details, but briefly: constants that are being calculated should remain in `snake_case` while constants that are being declared/asserted should be `ALL_CAPS_SNAKE_CASE`
     - `Constant Variable init_sma = sc.A; // good, init_sma is being calculated, so use snake_case`
     - `Constant Variable RESULT_SUCCESS = 0; // good, we are just giving this magic number a name, so ALL_CAPS`

# Globals
 - `Global`s are to be used exceedingly sparingly, and generally just for boilerplate infrastructure reasons. "I didn't want to pass this variable down through three procedures" is not a sufficient reason to necessitate a `Global`. An overreliance on `Global`s is dangerous and quickly leads to unmaintainable code.
# Naming
 - "Variables", meaning anything that is being instantiated such as a `Variable`, `TimeSpan`, `String`, `PlotWindow`, `Spacecraft` instance of a custom struct, etc, shall be named using `snake_case`.
     - `Variable desired_range_km;  // good`
     - `String error_message;       // good`
     - `List<StringArray> name_map; // good`
     - `TimeSpan cool___timespan;   // bad`
     - `Variable MaximumAltitude;   // bad`
 - Procedures shall be named using `camelCase`. Optional: prepend a `_` to procedure name to indicate it is only intended for internal use in that module.
     - `Define Procedure logDebug();                       // good`
     - `Define Procedure initSpacecraftPropulsionSystem(); // good`
     - `Define Procedure _calcHeight();                    // good, _ prefix indicates it is only intended for internal use`
     - `Define Procedure calcRIC();                        // edge case. use judgement on if calcRic() is better`
     - `Define Procedure PlotMnvr();                       // bad, this is TitleCase`
 - Struct definitions shall be named using `TitleCase`.
     - `Struct ManeuverParameters;      // good`
     - `Struct TelemetryRequestResults; // good`
     - `Struct orbitParameters;         // bad, this is camelCase`
     - `Struct spacecraft_details;      // bad, this is snake_case`
 - Use semantic and descriptive names. A variable's name should make it obvious what is for and rely as little as possible on a greater context.
     - `Variable ratio;                     // bad. ratio for what?`
     - `Variable chaser_tank_mix_ratio;     // good, explains what it's for and what it applies to`
     - `String name;                        // bad`
     - `String client_sc_display_name;      // good`
     - `String ip_address;                  // bad. to what? for what? used when?`
     - `String telemetry_server_ip_address; // good.`
 - When a `Constant` is being assigned a calculated value, it should use `snake_case` like usual. But if it is being used with a pre-defined value (typically to avoid a magic number/string) it should be `ALL_CAPS_SNAKE_CASE`.
     - `Global Constant Variable IMPULSIVE_BURN_ATT__VNB = 1; // good, we're giving a semantic name to a magic number, so ALL_CAPS`
     - `Constant Variable init_sma = sc.A; // good, we don't know what init_sma will be ahead of time but we don't expect it to change. So it's a constant, but a snake_case constant`
     - `Constant String SC_DISPLAY_NAME = config.display_name; // bad, we're not replacing a magic string, we're assigning from config, so snake_case is appropriate here`
     - `Constant Variable pi = 3.14159; // bad, we're just giving a semantic name to a number, so ALL_CAPS is appropriate`
 - No [Hungarian Notation](https://en.wikipedia.org/wiki/Hungarian_notation). Variables should be named such that needing to explicitly call out the type is not required. In addition, FreeFlyer is a strongly typed language that is generally developed in its IDE. Simply hovering the mouse over a variable in question will reveal its type.
     - `Variable v_altitude_km; // bad, don't prepend the type`
     - `Variable altitude_km; // good`
     - `Vector sun_to_earth_vector; // good, the 'vector' in the name is referring to the concept of a vector, not the FreeFlyer type.`
     - `PlotWindow pwInPlane; // bad`
     - `PlotWindow in_plane_plot; // good`
 - When applicable, variables should end with the units the variable uses.
     - `Variable postburn_sma; // bad, no units`
     - `Variable postburn_sma_km; // good`
     - `Variable init_tank_pressure; // bad, no units`
     - `Variable init_tank_pressure_kpa; // good`
     - `TimeSpan burn_duration_sec; // bad, TimeSpans are unitless`


# Comments
 - All variables shall include a `///` comment when declared. The FreeFlyer IDE will show the `///` comment to users who hover over the variable and it forces the developer to think about what a particular variable actually does.
     - `Variable desired_postburn_sma_km; (bad, no comment at all)`
     - `Variable desired_postburn_sma_km; // desired semimajor axis after the burn (bad, should be ///, not //)`
     - `Variable desired_postburn_sma_km; /// desired semimajor axis after the burn (good)`
 - Comments should strive to add additional context. Sometimes a tautological comment is unavoidable for extremely simple variables, but in general comments are a great chance to add extra context.
     - `String error_message; /// the error message (bad, no additional context)`
     - `String error_message; /// used to return error messages from this procedure to the caller (good)`
 - Code modules (external files of FreeFlyer script that is imported) shall include a documentation block at the top of the code that lists every procedure in the module along with a one-liner description of each procedure. If applicable, include a list of other modules that must be included first in order for this module to work.
 - Procedure and Struct definitions shall be preceded by a documentation block that explains what the purpose of the procedure or struct is, what assumptions are being made, etc.
 - When defining a procedure or struct, every argument or field in the procedure/struct should be on its own line and have a `//` comment explaining what it is
**Example:**
```
Define Procedure overrideSpacecraftMassAndTanks(
        Variable expected_sc_mass_total_kg, // total spacecraft mass (dry + fuel + ox)
        Variable fuel_tank_mass_kg,         // fuel tank mass (kg)
        Variable ox_tank_mass_kg,           // oxidizer tank mass (kg)
        Variable sc_vehicle_dry_mass_kg,    // spacecraft dry mass (kg)
        Variable tank_mix_ratio,            // oxidizer/fuel mixture ratio
        Variable tank_pressure_kpa          // pressure for both tanks (kPa)
);
```


# Whitespace
 - Use spaces, not tabs. Specifically, use four spaces for indendation. This is a debate that is as old as programming, but in this repo tabs will not be accepted. The rationale is that people will often attempt to align text in their code and if they use a mishmash of tabs and spaces then this alignment often breaks. With spaces what you see is what you get.
 - Do not include any trailing whitespace. That is, there should not be a bunch of spaces hanging out at the end of the line past the last visible character. Given the difficulty in viewing whitespace in FreeFlyer this rule will likely be applied with some leniency, but there are plenty of external tools that can easily and automatically remove trailing whitespace. It's even possible to use a [Git hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) to call such a process before committing so the developer never has to think about it.
 - This isn't always possible, especially when declaring variables with a long `///` comment, but avoid code lines that are longer than 120 characters. Almost every long line can be easily broken up across multiple lines. This improves readability, makes code easier to review in merge requests, and allows for splitting the screen to view two sections of code at once without confusing wrapping.
 - Aligning along comments, equals signs, commas, etc, is appreciated but not strictly required. In general, if it would add to the readabilty of the code, please consider aligning sections of code with extra whitespace.

# Legacy FreeFlyer
 - Do not use the optional `then` term. It's just extra typing/reading and does nothing.
     - `If (a == b) then; // bad, no then`
     - `If (a == b); // good`
 - Do not use the optional `step 1` term in a `For` loop. Only use `step` for other increments.
     - `For i = 0 to input.Count-1 step 1; // bad, step 1 is the default`
     - `For i = 0 to input.Count-1; // good`
     - `For i = 0 to input.Count-1 step 2; // good, a non-1 step is fine`
 - Use `TimeSpan`s instead of storing time in `Variables` with a particular unit. That is, don't just make `Variable`s that store a number of days. `TimeSpan`s allow the developer to handle time without worrying about units until they need to. That is, two `TimeSpan`s can be added together even if one was made from seconds and one was made from days, and it's not until we actually go to add it to a product or plot with `my_timespan.ToSeconds()` that we have to worry about units.

# Operators and Commands
 - Rather than `a = a + b;` and `a = a - b;` use the combined operators, listed below:
     - `a += b; // equivalent to a = a + b;`
     - `a -= b; // equivalent to a = a - b;`
     - `a *= b; // equivalent to a = a * b;`
     - `a /= b; // equivalent to a = a / b;`
     - `a %= b; // equivalent to a = a % b;`
 - Do not use the `++` operator, use ` += 1`. There is no need for a special case for `1` and using the general `+=` makes it easier to switch to another number if necessary.
 - Do not use the `switch` command. `switch` was introduced in an era of much slower computers in order to assist compilers in making more performant code. FreeFlyer is an interpreted language and will not even benefit from this negligible performance increase. Additionally, `switch` can only do simple comparisons when definine cases. An `If/ElseIf` tree allows for arbitrary checks. The only acceptable use of a `switch` is if the developer wants to flow through multiple cases by omitting the `Break;` at the end of a case block, though in such a case there would be questions about such a strange implementation.



# Procedures
 - All procedure definitions shall group their arguments by input, modify, and output. These sections shall be denoted with a `//` comment (example below)
 - An "input" argument is one that is never changed and simply used as configuration or to calculate something else. e.g. a desired spacecraft SMA after a burn.
 - A "modify" argument is one that we need to read and also change. e.g. a `Spacecraft` being propagated to a desired condition.
 - An "output" argument is one that is only being used to return a result. The procedure is free to (and expected to) overwrite or reset this variable. e.g. an error message returning details about a problem in the procedure.
 - It is preferred that the arguments in each section be sorted alphabetically. However, semantic ordering is also acceptable (e.g. sorting `start_time` before `end_time` since readers will expect to read the start before the end). Arbitrary order, or "as arguments were added to the procedure" is not acceptable.
 - All procedures shall have a `String` named "err" as an output argument. As an exception to the above rule, the `err` string shall always be the first output argument. The only exception to this is certain boilerplate procedures that are extremely simple or which are so fundamental that their errors cannot be reported anyway, e.g. an initMyStruct() which just sets a struct to certain values, or a central logging feature, respectively.
 - All procedures shall set the `err` string to an empty string on its first line. This ensures that the error message is fresh for when we start writing it or adding to it.
 - All procedures shall declare a `Constant` `String` named `CODE_LOCATION` containing the verbatim name of the procedure as it is required by the logging macros. This should be done immediately after safing the `err` string.
 - All local variables instantiated in a procedure must be explicitly set to a value before their first use, either through normal calculation, or by being intentionally set to a known safe/default value. This is to protect against a quirk of the FreeFlyer language, where in the case of a procedure being called in a loop, the scope of the procedure will persist between calls! The result is that if variables aren't explicitly set to known safe values, it is possible to be using values from the previous run of the procedure. This is a very tricky bug to track down.
 - The `EndProcedure;` command shall be followed by a `//` comment with the verbatim name of the procedure being closed.

**Example:**
```
// ingests JSON via a string, or a filename as a fallback, and populates a provided struct
Define Procedure ingestJSON(
        // input
        String   json_fallback_file_path,   // if json_string is blank, this path will be ingested
        String   json_string,               // serialized JSON in a string
        Variable missing_property_behavior, // used for JsonInterface.MissingPropertyBehavior (0 for ignore, 1 for error)

        // modify
        // (N/A)

        // output
        String err,   // error message
        Config config // Config struct to populate
    );
    err = '';

    Constant String CODE_LOCATION = 'ingestJSON'; /// code location for logging

    // [...] code goes here
EndProcedure; // ingestJSON
```



# Logging levels
 - Logging procedures are provided as part of this repo. They all take the form of `logLevel(string)`, where `Level` is one of: crit, error, warn, info, debug, verbose. These levels are explained below:
    - logCrit: used in situations where an unrecoverable error has been encountered. This differs from a situation where the missionplan can no longer successfully complete its task. For instance, if targeting fails, the missionplan can still gracefully shut down, sending information about the failed targeting to the end user for analysis. In most cases, the action immediately after a critical log will be to immediately halt execution of the missionplan. A critical error indicates that the missionplan itself is broken. This is the missionplan's developer saying to the end user "I have made a mistake on my end and the missionplan needs to be fixed"
    - logError: used for situations where the missionplan can no longer complete its assigned task. Rather than indicating that the missionplan is broken, it indicates that there has been an operational error or that the assigned task was impossible to complete. Examples include being unable to open a file for writing, having a targeter fail to converge, or losing a socket connection. This is the missionplan's developer saying to end user "I can't complete my task using what you've given me"
    - logWarn: used for situations that are unusual and noteworthy but may not be errors. These may indicate that something is taking longer than expected, that the input data may be suspect, or a variable is outside of expected bounds. An example of a warning may be a maneuver set to take place 100 years in the future, or a delta-v calculated to be several kilometers per second. This is the missionplan's developer asking the end user "did you really mean to do this?"
    - logInfo: used to express normal behavior as the application progresses. Examples may include "beginning targeting for Maneuver 1" or "writing Plot 'SMA During AR&D' to directory 'C:/....'". Info level logs should be used for items that the operator may need to take note of for typical usage of the application. Users should avoid including redundant or information that is better suited to the debugging process.
    - logDebug: used to express low level information that may aid in debugging a malfunctioning application. Examples may include how long a particular process took to complete, when sockets connections are made, when JSON serialization is beginning, and so on. These messages are primarily for use during development and are intended to be disabled by default in operations, only enabled if a problem is encountered.
    - logVerbose: used for temporary extreme-level logging while debugging a particular problem. Examples include which iteration of a loop the application is executing, values of intermediate variables (variables that are only intended for use in calculating other variables), or the values of expressions to be evaluated when branching. No verbose logs should ever be used outside of development.

