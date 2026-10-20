# Examples & Walkthroughs

Reference scenes live in:

`Assets/Plugins/SkywardGames/PlayMakerGC2/Core/Examples/Scenes/`

Install dependencies, allow compilation to finish, and start from [Getting Started](getting-started.md). For UPM installations, browse the corresponding package location. These scenes demonstrate integration boundaries rather than production game systems.

## Scene Overview

| Scene | What the serialized scene currently demonstrates |
| --- | --- |
| `01_StateDrivenDoor.unity` | Click → local event → FSM state → waited GC2 Actions. |
| `02_GuardStateFlow.unity` | Inline Conditions → GC2 Actions → native Signal. |
| `03_SharedBoundaryData.unity` | Explicit Name Variable exchange and a typed FSM property. |
| `04_CoreGameModeBoundary.unity` | Durable game mode around a Core GC2 activity. |
| `05_CallableFsmRoutines.unity` | Currently reuses door event execution; see setup exercise below. |
| `06_EnemyAiOrchestration.unity` | Currently reuses guard-state execution under an AI controller. |

The scene contents were inspected for this documentation refresh. Names and README objects in scenes 05 and 06 describe a broader intended example than the current serialized configuration.

## 01 — State-Driven Door

**Prerequisite:** Core dependencies only.

1. Open the scene and select **Door — Click in Game View**.
2. Inspect the cursor-click Trigger's **Send PlayMaker Event**: FSM `Door State FSM`, event `Interact`.
3. Open that FSM. Inspect `Closed`, `Opening`, and `Open`.
4. In `Opening`, inspect **Run GC2 Actions**, its waited task, and the `Opened` completion event.
5. Enter Play Mode, click the door, and inspect the Console and active FSM state.

**Expected:** GC2 logs the opening routine's start/completion and the FSM reaches `Open` after the task. This demonstrates execution coordination; inspect the authored Actions before assuming a particular animation is present.

**If it fails:** check Game view focus, target/FSM identity, `Interact` transition, and Actions reference. See the [rebuild exercise](getting-started.md#rebuild-the-connection-yourself).

## 02 — Guard State Flow

**Prerequisite:** Core dependencies; the scene's perception-themed start object is an authored Core demonstration.

1. Select **Guard** and open `Guard AI`.
2. Inspect the `Spotted` transition from Patrol.
3. In **Alert — Check GC2 Conditions Inline**, inspect the embedded Conditions and True/False branches.
4. Inspect **Alert — Run GC2 Actions**, then **Chase — Emit GC2 Signal**.
5. Enter Play Mode and inspect the native **Enemy-Alerted Receiver** Trigger and Console.

**Expected:** the enabled guard-senses condition allows the alert routine, then `Enemy-Alerted` reaches the native GC2 receiver.

**If it fails:** check the guard-senses condition, explicit context, Signal normalization, and receiver lifetime. A false condition is a valid branch, not an evaluation error.

## 03 — Shared Boundary Data

**Prerequisite:** Core dependencies and the scene's existing variable stores.

1. Select **Shared Data Owner** and inspect its `Shared Boundary Data` FSM and Local Name Variables.
2. Inspect **Explicit One-Shot Exchange**: **Set GC2 Name Variable** and **Get GC2 Name Variable**.
3. Inspect **GC2 Property — Read PlayMaker Variable**, which targets `Player-Speed-In-PlayMaker`.
4. Enter Play Mode and inspect both stores and the Console.

**Expected:** PlayMaker writes/reads the authored GC2 values; GC2 samples the typed PlayMaker value. The scene transfers at explicit points and does not establish continuous binding.

**If it fails:** compare store scope, exact variable identity, Float/Number pairing, and the `Exchange-Data` event path.

## 04 — Core Game Mode Boundary

**Prerequisite:** Core dependencies; no Dialogue module is required.

1. Select **Game Mode Owner** and open `Game Mode`.
2. Inspect `Exploration → Activity` on `Activity-Started`.
3. Inspect the waited **Core Activity — GC2 Actions** routine and `Activity-Finished` transition.
4. Enter Play Mode and follow the Console messages and state.

**Expected:** the Core source begins an activity, the FSM waits for GC2, then returns to Exploration.

**If it fails:** check the activity source, FSM target, waited completion, and the completion transition. Replacing the activity with Dialogue would be a separate module-specific exercise.

## 05 — Callable FSM Routines {#05-callable-fsm-routines}

::: warning Current scene limitation
The bundled file currently contains `Door State FSM`, `Interact`, and `RunGc2Actions`. It does not serialize a Run PlayMaker FSM / Run Gameplay Routine caller or typed input/output mappings. Its README label should not be taken as proof that those mappings are configured.
:::

Use a separate working copy for this callable setup exercise:

1. Create an FSM named `Callable Test` with an input Float `InputValue` and output Float `ResultValue`.
2. Author a bounded operation that sets ResultValue from InputValue and reaches a genuine PlayMaker finish path. Verify it in PlayMaker first.
3. In GC2, add **Run PlayMaker FSM**, choose Scene Object, target this host, and set FSM Name to `Callable Test`.
4. Map a constant Number into InputValue, and ResultValue into an existing compatible GC2 Number destination.
5. Enable waiting, set a finite timeout, and choose a start/lifecycle policy suitable for this test object.
6. Run the GC2 Actions list. Confirm the output after completion, then test timeout and interruption separately.

For a reusable definition, author a [Gameplay Routine asset](callable-routines.md#author-a-gameplay-routine-asset). A named completion state must be configured as State Reached if it is not an actual FSM finish.

## 06 — Enemy AI Orchestration

**Prerequisite:** the shipped scene's existing Core configuration.

1. Select **Enemy AI Controller** and open `Guard AI`.
2. Inspect Patrol, **Alert — Check GC2 Conditions Inline**, **Alert — Run GC2 Actions**, and **Chase — Emit GC2 Signal**.
3. Inspect the **Enemy-Alerted Receiver** and the start-demo object.
4. Enter Play Mode and follow the condition → routine → Signal boundary.

**Expected:** this serialized scene demonstrates the same guard-state integration pattern as scene 02 under the AI controller name.

The README object's Idle/Investigate/Combat/Retreat description is an intended larger AI pattern, not the current graph. Extending it with Character locomotion or optional Perception is further authoring work; see [Optional Modules](optional-modules.md).

## Adapt a Scene Safely

Keep one owner per state/value, name FSMs explicitly, and use Trace to observe one interaction before adding more connections. Test cancellation, missing targets, and busy calls as well as the happy path. Record required optional modules when sharing a scene with another project.
