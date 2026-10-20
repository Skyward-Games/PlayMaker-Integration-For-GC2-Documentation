# Troubleshooting

Start with the Unity Console, then reproduce one interaction in the workspace's **Execution Trace**. Inspect the actual resolved objects and identities before changing the graph.

## Diagnostic Codes

| Code | Check |
| --- | --- |
| `MissingTarget` | Target property/variable currently resolves to a live GameObject. |
| `FsmNotFound` | Exact FSM name, object, and component lifetime. |
| `FsmAmbiguous` | Multiple matching components; supply a unique name. |
| `MissingIdentifier` | Event, state, or variable identifier is filled and valid. |
| `ActionsBusy` | Existing run and Reject/Join policy. |
| `ActionsLifecycleFailure` | Actions reference, lifecycle, context, and underlying message. |
| `ConditionsValidationFailure` | Conditions configuration and context; separate error from false. |
| `VariableOwnerMissing` | Local owner or global asset is assigned. |
| `VariableNotFound` | Variable identity/path and scope. |
| `VariableAmbiguous` | Duplicate or non-unique variable identity. |
| `VariableTypeMismatch` | Correct typed action/property and destination type. |
| `VariableConversionFailure` | Range, finite values, and compatible references. |

The record's operation, target, identifier, expected type, remediation, and message provide context. Some logs are rate-limited; a repeated failure does not necessarily produce one message per frame.

## My FSM Does Not Receive the Event

1. Inspect the runtime Target object and exact FSM Name.
2. Confirm the event's spelling and an active transition/handler.
3. Check enabled/active state and PlayMaker startup semantics.
4. Distinguish local events, bridge broadcasts, native global event assets, and GC2 Signals.
5. Remove unintended event echoes and repeat with Trace.

The bridge does not retain arbitrary events for disabled FSMs.

## Multiple FSMs or Renamed Components

Blank names succeed only with one matching FSM. Duplicate names are ambiguous even if the component used to resolve successfully. Rename to unique identities or use an explicitly chosen search utility.

Failed lookup results are not permanently cached. Correcting the identity allows the next access to retry.

## GC2 Actions Are Busy or Do Not Stop

Reject leaves an existing run unchanged and can send Busy Event. Join requires waiting and does not own/cancel the existing run. Detached runs continue after the PlayMaker action finishes.

Owned cancellation is cooperative. Check whether the native/third-party Instruction observes GC2 cancellation. Completion of a GC2 task also does not prove every Instruction avoided a logged exception.

## Variable Read Is Stale, Zero, False, or Null

Check store scope, live owner, FSM name, variable identity/path, and selected type. Direct Name Variable Number actions use PlayMaker Float; use the dedicated Integer route when needed.

Failed PlayMaker reads preserve output. GC2 property getters may warn and return a native default because the base getter has no independent success result. Inspect diagnostics before accepting the value.

## Property Binder Does Not Update in Edit Mode

Edit Mode previews matches. Automatic value updates run in Play Mode. **Synchronize Now** is an explicit write/reconciliation action.

Check Synchronize Values, direction/authority, trigger, matched types, and explicit rules. Structure synchronization is a separate advanced setting. Do not use structural deletion to solve an ordinary missing-value problem.

## Signal Is Missing or Fires Twice

Compare serialized normalized Signal IDs and the configured invoker. A waiting action listens only while active; a prior Signal is not queued for it. Check receiver lifetime and repeated send nodes.

Separate the native Signal route from named PlayMaker bridge broadcasts. Repeated native delivery is not globally deduplicated.

## Singleton Selector Shows a Missing Entry

Open Settings and inspect the saved registration name. Version 1.1.3 preserves missing selections with a warning. It does not silently substitute another entry.

Queries do not instantiate a manager or instance. Use the explicit creation operation and check name collisions.

## Optional Module Actions Are Missing

Verify that the actual module compiles, that Project Overview detects it, and that import-time define/assembly synchronization has completed. Re-index if the palette is stale. Inspect compilation errors before adding references manually.

## Callable Scene Does Not Have Mappings

The current bundled `05_CallableFsmRoutines.unity` reuses the door event flow. Follow the [callable setup exercise](examples.md#05-callable-fsm-routines) rather than looking for mappings that are not serialized there.

## Request Support

Use the [Skyward Games Discord](https://discord.gg/DTXjRH5TVz). Include integration, Unity, GC2, and PlayMaker versions; installed modules; the exact selector/action; expected/actual behavior; Console message; and a minimal reproduction. Include target/context settings and whether the issue occurs in Edit Mode, Play Mode, or a player build.
