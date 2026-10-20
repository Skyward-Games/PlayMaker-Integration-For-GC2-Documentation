# Compatibility

Compatibility statements distinguish a qualified baseline from focused follow-up checks. A package manifest's Unity version is not a guarantee that every engine or dependency combination has been tested.

## Qualified Core V1 Baseline

| Dependency | Qualified version |
| --- | --- |
| Unity | `6000.4.6f1` |
| Game Creator 2 Core | `2.18.60` |
| PlayMaker | `2.0.0-beta.80` |
| Optional modules in the qualified project | Behavior, Dialogue, Inventory, Melee, Perception, Quests, Shooter, Stats, Traversal |

PlayMaker beta.80 remains a beta dependency. Other Unity 6 updates, GC2 versions, later PlayMaker betas/releases, and module combinations need their own validation.

## Later Focused Validation

| Release | Recorded validation |
| --- | --- |
| 1.1.0 | Unity 6000.4.6f1: EditMode/PlayMode checks and standalone player compilation recorded as passing. |
| 1.1.2 | Unity 6000.6.0f1: 42 focused EditMode tests, 8 focused PlayMode tests, and player script compilation passed. |
| 1.1.3 | Unity 6000.6.0f1: 48 focused EditMode tests and 9 focused PlayMode tests passed, including Singleton rename coverage. UPM contents verified. |

These are release records, not tests rerun by this documentation refresh. The 1.1.3 focused results do not establish that the complete broader suite is green.

## Known Broader Test Limitations

The 1.1.2 release records five broader EditMode failures involving binding synchronization, a Unity version expectation, state hierarchy expectations, and the configured Console Singleton during domain reload. Two broader PlayMode failures involve the Character fixture and native GC2 Signal delivery.

The subsequent 1.1.3 entry records focused Singleton and packaging checks; it does not claim those broader failures were all resolved. Reproduce and assess the relevant paths before relying on them in a shipping configuration.

## Assemblies and Installation

Core requires GC2 Core and PlayMaker runtime/editor assemblies. Optional module references remain in the separately managed module integration assembly. Player runtime builds do not reference UnityEditor; automated test assemblies are separate.

Import dependencies first. The Assets distribution belongs under `Assets/Plugins/SkywardGames/PlayMakerGC2/`; package installations use their Packages location. Do not relocate the integration to the legacy `Assets/Plugins/PlayMakerGC2/` path shown in some older guides.

## Behavioral Limits

- Normal FSM targets require exactly one match. Blank names are ambiguous on multi-FSM objects.
- Cancellation is cooperative; joined/detached work is not owned by the waiting action.
- Direct data transfers do not synchronize stores or register save data.
- Property Binder automatic updates run in Play Mode; editor writes require an explicit authoring action.
- Named bridge broadcasts are not native GlobalEventAsset dispatches and do not carry native EventData.
- Dynamic targets still require runtime verification even after a clean authoring scan.
- Scene 05 currently reuses the door event flow, and scene 06 contains the guard flow rather than the larger hierarchy described in its README object. See [Examples](examples.md).

## Qualify Your Project

For a new supported combination, check compilation, serialization/reload, EditMode, PlayMode, example behavior, import/reimport, and a representative target-platform build. Also test the particular optional module versions, pause/cancellation behavior, scene transitions, and dynamic targets your project uses.

This documentation publication does not add hosted HelpURL metadata to the plugin. Existing contextual help behavior follows the installed package.
