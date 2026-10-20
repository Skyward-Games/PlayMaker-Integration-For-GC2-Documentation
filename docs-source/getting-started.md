# Getting Started

Build a small connection first: click a door in Game view, let PlayMaker choose the state, and let Game Creator 2 perform the opening routine.

## Requirements

| Dependency | Qualified Core V1 baseline |
| --- | --- |
| Unity | `6000.4.6f1` |
| Game Creator 2 Core | `2.18.60` |
| PlayMaker 2 | `2.0.0-beta.80` |
| Integration documented here | `1.1.3` |

PlayMaker and GC2 are separate dependencies. This is a qualified baseline, not a minimum-version guarantee. Unity `6000.6.0f1` also has later focused validation; see [Compatibility](compatibility.md).

## Install and Open

1. Install Game Creator 2 Core and PlayMaker 2. Resolve their compilation errors before continuing.
2. Import the integration distribution. An Assets-based import resides at `Assets/Plugins/SkywardGames/PlayMakerGC2/`.
3. Wait for Unity to finish compiling. For a UPM installation, use its location under Packages rather than moving files into Assets manually.
4. Open **Game Creator > PlayMaker 2**, or **PlayMaker > Game Creator 2**. Both open the Integration Workspace.
5. Open **Project Overview** to inspect the environment and installed modules. Use **Re-Index** after importing content if the workspace is stale.

## Verify the Import

| Where to look | Entry to find |
| --- | --- |
| PlayMaker Action Browser, `Game Creator 2/Core` | `Run GC2 Actions`, `Run GC2 Instructions`, `Check GC2 Conditions` |
| PlayMaker Action Browser, `Game Creator 2/Events` | `Emit GC2 Signal`, `Wait for GC2 Signal` |
| PlayMaker Action Browser, `Game Creator 2/Variables` | `Get GC2 Name Variable`, `Set GC2 Name Variable` |
| GC2 Instruction selector | `PlayMaker/Send PlayMaker Event` |
| GC2 Condition selector | `PlayMaker/Is PlayMaker State Active` |
| Compatible GC2 Number property selector | `PlayMaker/Variables/Number` |

If these entries are missing, check the Unity Console before configuring a scene. Optional module nodes require their corresponding GC2 modules.

## First Workflow: State-Driven Door

Open the supplied reference scene:

`Assets/Plugins/SkywardGames/PlayMakerGC2/Core/Examples/Scenes/01_StateDrivenDoor.unity`

1. Enter Play Mode and click **Door — Click in Game View**.
2. Select the door and inspect **Door State FSM** in PlayMaker.
3. Follow `Closed → Opening → Open`. In `Opening`, inspect **Run GC2 Actions** and its referenced **Open Door — GC2 Actions** component.
4. Inspect the native GC2 cursor-click Trigger. It sends `Interact` to **Door State FSM**.
5. Inspect the completion transition. Waiting for GC2 prevents the FSM from reporting `Open` before the routine finishes.

**Expected result:** clicking the door starts the opening routine; PlayMaker enters `Open` after completion. If nothing happens, check the Trigger's target, exact FSM name, `Interact` transition, enabled state, and Game view focus.

## Rebuild the Connection Yourself

1. Add a PlayMaker FSM to a test door. Name it `Door State FSM`.
2. Create `Closed`, `Opening`, and `Open` states. Add an `Interact` transition from `Closed` to `Opening`.
3. Add a native GC2 Actions component containing the door-opening Instructions you want to run.
4. In `Opening`, add **Run GC2 Actions** from `Game Creator 2/Core`. Assign the Actions component, enable **Wait Until Complete**, and set **Completed Event** to `Opened`.
5. Add an `Opened` transition from `Opening` to `Open`. Assign **Failure Event** and **Busy Event** if the graph needs recovery branches.
6. Add a native GC2 cursor-click Trigger to the interactive door. Add **Send PlayMaker Event** from `PlayMaker/Send PlayMaker Event`, target the door, enter `Door State FSM`, and select `Interact`.
7. Enter Play Mode and click the door. Confirm the same state progression as the supplied example.

::: warning Name the FSM explicitly
A blank FSM name is accepted only when the target has exactly one FSM component. Multiple matching FSMs produce an ambiguity diagnostic; the normal target resolver does not choose the first one.
:::

## Next Steps

Read [FSMs & GC2](fsms-and-gc2.md) for context and ownership, then use the [Integration Workspace](integration-workspace.md) to discover capabilities. Start data transfer with [one-shot Name Variables](variable-bridging.md#one-shot-name-variable-transfer).
