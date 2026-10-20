# FAQ

## Do I Need PlayMaker and Game Creator 2?

Yes. Install both separately before importing the integration. GC2 optional modules are required only for the corresponding module workflows.

## Does This Convert FSMs into GC2 Graphs?

No automatic graph conversion is part of this workflow. Keep both native authoring models and connect them through explicit execution, data, and event boundaries.

## Does It Support PlayMaker 1.9 or Every Unity 6 Release?

The qualified baseline uses PlayMaker `2.0.0-beta.80`. No support claim is made here for PlayMaker 1.9 or every Unity 6 update. See [Compatibility](compatibility.md) for exact versions and later focused checks.

## Can I Leave the FSM Name Blank?

Only when the target has exactly one matching FSM. Use a unique name for multi-FSM objects. Dedicated first-match search utilities are an explicit alternative.

## Can GC2 Wait for PlayMaker?

Yes. Use state/completion waits, **Run PlayMaker FSM**, or a reusable **Gameplay Routine** depending on ownership and the result boundary. See [Callable Routines](callable-routines.md).

## Can PlayMaker Run GC2 Module Gameplay?

Yes, by executing native GC2 Actions/Instructions or evaluating Conditions for installed modules, and through supported module adapters. The module remains responsible for its own gameplay and data. See [Optional Modules](optional-modules.md).

## Are Variables Automatically Shared or Saved?

A direct property or action performs one transfer. Ongoing synchronization requires an explicitly added/configured Property Binder. GC2 and PlayMaker retain their own save ownership.

## Why Does Property Binder Only Preview in Edit Mode?

Automatic value updates run in Play Mode. **Synchronize Now** is the intentional editor write/reconciliation operation; review direction and structure settings first.

## Does a Singleton Query Create the Instance?

No. Query selectors are side-effect free. Use an explicit creation operation. Version 1.1.3 keeps registration names independent of source asset names and preserves missing selections with warnings.

## Are the Six Scenes All Complete Product Examples?

They are small reference scenes. The current callable and enemy-AI scene names overstate their serialized configuration; [Examples](examples.md) explains the actual contents and provides a callable setup exercise.

## Does Publishing This Site Change My Installed Plugin?

No. This repository contains documentation sources, generated pages, media, and build/check tools. It does not modify the plugin or create a new Unity distribution.

## Where Do I Get Help?

Start with [Troubleshooting](troubleshooting.md), then contact the [Skyward Games Discord](https://discord.gg/DTXjRH5TVz) with exact versions, configuration, diagnostics, and a minimal reproduction.
