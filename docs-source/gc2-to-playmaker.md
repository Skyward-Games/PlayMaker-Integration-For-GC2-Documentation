# GC2 → PlayMaker Reference

Native Instructions, Conditions, Events, and Properties appear below **PlayMaker** in Game Creator 2 selectors. Paths below reflect the current implementation.

## Instructions

| Selector path | Purpose |
| --- | --- |
| `PlayMaker/Send PlayMaker Event` | Send a local event to one strictly resolved FSM. |
| `PlayMaker/Broadcast PlayMaker Global Event` | Displayed as **Broadcast Named PlayMaker Event**; broadcast a name. |
| `PlayMaker/Run PlayMaker FSM` | Execute a scene or prefab FSM with mappings and lifecycle handling. |
| `PlayMaker/Routines/Run Gameplay Routine` | Execute a reusable Gameplay Routine asset. |
| `PlayMaker/Enable PlayMaker FSM` | Enable the selected component. |
| `PlayMaker/Disable PlayMaker FSM` | Disable the selected component. |
| `PlayMaker/Restart PlayMaker FSM` | Restart the selected FSM. |
| `PlayMaker/State/Wait for PlayMaker FSM State` | Wait for a state with timeout/cancellation. |
| `PlayMaker/State/Wait for PlayMaker FSM or State to Finish` | Wait for the selected completion target. |
| `PlayMaker/Find/Find PlayMaker FSM` | Store a search result in a GC2 property destination. |
| `PlayMaker/Find/Find All PlayMaker FSMs` | Collect matching owners into a compatible list. |

### Send PlayMaker Event

Configure **Target**, **FSM Name**, and **Event Name**. Leave the FSM name blank only when the target has exactly one FSM. The graph decides whether the event causes a transition.

Delivery follows native PlayMaker active/startup behavior. The bridge does not add a deferred queue for arbitrary disabled components. Verify the enabled state and event handler before sending.

### Broadcast Named PlayMaker Event

This broadcasts a string name to active PlayMaker FSM components and bridge listeners. It does not dispatch a native `GlobalEventAsset` or carry native EventData. Use [Gameplay Events](events-and-signals.md#typed-gameplay-events) for typed event data.

### Run and Wait

Use [Callable Routines](callable-routines.md) for mappings and lifecycle policies. Use a state wait when the graph owns the work and GC2 only needs to observe it. Keep success, timeout, canceled, and invalid-target outcomes separate where exposed.

## Conditions

| Selector path | Test |
| --- | --- |
| `PlayMaker/State/Has PlayMaker FSM` | Target resolves. |
| `PlayMaker/Is PlayMaker FSM Enabled` | Component is enabled. |
| `PlayMaker/State/Is PlayMaker FSM Running` | FSM is actively running. |
| `PlayMaker/State/Is PlayMaker FSM Finished` | FSM has finished. |
| `PlayMaker/Is PlayMaker State Active` | State is active; prefer full-path matching in nested graphs. |
| `PlayMaker/Variables/Enum Equals` | Enum equality. |
| `PlayMaker/Variables/Enum Compare` | Enum comparison with selected operator. |

Other utility Conditions cover uniqueness, state existence, variables, collections, and Singletons. See [Singletons & Utilities](singletons-and-utilities.md).

## Events and Triggers

| Selector path | Observes |
| --- | --- |
| `PlayMaker/On PlayMaker State Enter` | Entry into a selected state. |
| `PlayMaker/On PlayMaker State Exit` | Exit from a selected state. |
| `PlayMaker/On PlayMaker FSM Finished` | FSM completion. |
| `PlayMaker/On PlayMaker Global Event` | Displayed as **On Named PlayMaker Bridge Event**; bridge name broadcasts. |

These are GC2 Trigger events. Utility Events additionally observe availability/loss, state changes, enabled/disabled state, and variable changes. A first baseline observation is not automatically a gameplay change notification.

## Typed Variable Properties

Choose `PlayMaker/Variables` in a compatible GC2 property field. Getter/setter availability depends on the property's type.

| Selector suffix | PlayMaker data |
| --- | --- |
| `Bool`, `Number`, `Integer`, `String` | Scalars; Number uses PlayMaker Float. |
| `Game Object` | GameObject reference. |
| `Vector3` | Compatible vector-based fields. |
| `Quaternion` | Compatible rotation fields. |
| `Color`, `Texture`, `Sprite`, `Material` | Typed values and asset references. |
| `Audio`, `Animation` | AudioClip / AnimationClip references. |

Local references need an owner, FSM identity, and variable identity. Global access references the appropriate PlayMaker global variable asset where exposed. Missing getters may return the native default after warning; zero/false/null does not prove successful resolution.

State properties appear under `PlayMaker/State`: **Current State**, **FSM Enabled**, **FSM Running**, and **FSM Finished**.

## Extended PlayMaker Systems

Selectors also expose PlayMaker Data Tables, Enums, Save & Load, object pooling, Interactions, and Widgets. Data Table operations cover row CRUD, cell reads/writes, search, sorting, and save/load. Widget operations include meters, selected rows, paging, animated lists, target managers, and minimaps.

These operate on the corresponding **PlayMaker** subsystem objects. They are distinct from optional GC2 module adapters and do not automatically synchronize save systems.
