# Introduction

**PlayMaker 2 Integration for Game Creator 2** connects PlayMaker's state machines with native Game Creator 2 gameplay. An FSM decides which behavior should run; GC2 performs the authored gameplay work. Both tools keep their own graphs and data ownership.

## Your First Connection

:::flow
- 01 | GC2 interaction | A native Trigger sends `Interact` to a named FSM.
- 02 | PlayMaker state | The door moves from `Closed` to `Opening`.
- 03 | GC2 routine | `Run GC2 Actions` executes the opening behavior and waits.
- 04 | PlayMaker completion | The completion event moves the FSM to `Open`.
:::

Start with the [door walkthrough](getting-started.md#first-workflow-state-driven-door), then inspect the [six reference scenes](examples.md).

## What You Can Build

:::cards
- ↔ | Native gameplay from FSMs | Run GC2 Actions or inline Instructions; branch on native Conditions. | playmaker-to-gc2.md
- ◇ | FSM-aware GC2 logic | Send events, inspect states, wait for completion, and read typed FSM variables. | gc2-to-playmaker.md
- ≋ | Explicit data access | Read and write on demand, transfer lists, or opt into Property Binder synchronization. | variable-bridging.md
- ↗ | Events with a clear destination | Use local events, GC2 Signals, or typed Gameplay Events. | events-and-signals.md
- ▶ | Reusable FSM routines | Expose typed inputs, outputs, completion rules, and execution policies to GC2. | callable-routines.md
- ⌕ | One integration workspace | Discover capabilities, scaffold templates, inspect relationships, and diagnose execution. | integration-workspace.md
:::

![PlayMaker state graph connected to a native GC2 gameplay event emitter](assets/media/bridge-overview.png "A state-driven graph and a GC2 event endpoint, reproduced from the bundled manual.")

## Choose a Learning Path

| Your goal | Start here | Continue with |
| --- | --- | --- |
| Make your first connection | [Getting Started](getting-started.md) | [Examples](examples.md) |
| Reuse GC2 gameplay in a state | [PlayMaker → GC2](playmaker-to-gc2.md) | [Context mapping](fsms-and-gc2.md#map-self-and-target) |
| Drive an FSM from GC2 | [GC2 → PlayMaker](gc2-to-playmaker.md) | [Callable Routines](callable-routines.md) |
| Share gameplay data | [Variables & Property Binder](variable-bridging.md) | [Singletons & Utilities](singletons-and-utilities.md) |
| Diagnose a connection | [Integration Workspace](integration-workspace.md) | [Troubleshooting](troubleshooting.md) |
| Extend with C# | [Scripting API](scripting-api.md) | [Compatibility](compatibility.md) |

## Requirements at a Glance

Install **Game Creator 2 Core** and **PlayMaker 2** before importing the integration. Optional GC2 modules add capabilities when installed; they are not required for the Core door example.

This site documents **v1.1.3**. The original qualified baseline uses Unity `6000.4.6f1`, GC2 Core `2.18.60`, and PlayMaker `2.0.0-beta.80`. Later focused checks ran on Unity `6000.6.0f1`. See [Compatibility](compatibility.md) for the distinction and [Changelog](changelog.md) for the release history.

## Documentation & Artwork Disclosure

::: note Package documentation and authorized artwork
Offline documentation in PDF and self-contained HTML is included with the package. Online documentation is also available for the package on this website.

All artwork featuring the Game Creator 2 (GC2) symbol was duly authorized by Marti and follows Game Creator's publication and branding guidelines.
:::

::: tip Keep each tool's strengths
Use PlayMaker for durable states and transitions. Author gameplay sequences in native GC2 Actions, and connect the two with explicit events, context, and variable transfers.
:::
