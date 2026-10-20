# Optional Modules

Game Creator 2 Core plus PlayMaker 2 form the integration's Core boundary. Optional GC2 modules extend available gameplay capabilities when installed. You do not need them for the basic door connection.

## Available Adapter Families

| GC2 module | Integration family |
| --- | --- |
| Behavior | Behavior execution and control actions. |
| Dialogue | Dialogue actions and event adapter. |
| Inventory | Item/equipment operations, wealth, and bag observation. |
| Melee | Weapon and block control actions. |
| Perception | Sensing actions and event adapter. |
| Quests | Quest lifecycle/state operations and observation. |
| Shooter | Shooter weapon/control actions. |
| Stats | Stat actions, binding endpoint, and observation. |
| Traversal | Traversal actions and state queries. |

Look for the corresponding **Game Creator 2/[Module]** category in PlayMaker, and use the workspace's Action Palette to inspect installed capabilities. The original qualified project included all nine families.

## Detection and Assembly Boundaries

An editor integration manager detects installed modules from their folders, assembly definitions, or known types. It synchronizes the corresponding `GC2_MODULE_…` defines and the separate Modules assembly references.

Runtime Core lives in `PlayMakerGC2.Core.Runtime`; optional adapters live in `PlayMakerGC2.Modules.Runtime`. Editor tooling has separate editor assemblies. Module detection is an import/editor workflow and should complete before testing a player build.

## Add a Module to a Project

1. Install a supported GC2 module and allow it to compile.
2. Let Unity process the import and integration assembly synchronization.
3. Open **Project Overview** and confirm the module is detected.
4. Re-index if the palette remains stale, then inspect the corresponding action family.
5. Configure the module's native gameplay objects first; add an explicit PlayMaker action or a native GC2 Actions call.
6. Exercise the behavior in Play Mode and a representative player build.

If compilation fails, inspect the missing assembly and installed module version. Do not add all module references to the Core assembly or fake a detection define without installing its dependency.

## Compose Through Native GC2 Actions

A module's native Instructions and Conditions can be authored in GC2 and invoked through the generic execution/condition bridge. Prefer this when a small native Actions routine already expresses the behavior.

For example, an FSM can own `Conversation` state while a GC2 Actions routine invokes an installed Dialogue module. Pass the correct Self/Target, wait if needed, and send a completion notification back to the FSM. A dedicated wrapper is useful when its supported operation matches the job; it is not a replacement for every module API.

## Keep Data and Lifetimes Explicit

A stat endpoint or observable source is an explicit adapter, not automatic ownership of all module data. Inventory, Quests, and other modules retain their own stores, save rules, and lifecycle behavior.

The presence of a module in Project Overview does not certify every module version or every combination. See [Compatibility](compatibility.md) for the qualified baseline and known test limitations.
