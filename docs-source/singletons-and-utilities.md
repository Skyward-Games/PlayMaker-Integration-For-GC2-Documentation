# Singletons & Utilities

GC2's **PlayMaker** selectors provide search, lifecycle waits, variable operations, collections, and persistent Singleton shortcuts. Singletons use the same runtime operations with a registered target identity.

## Search and Selection

| Utility | Scope / selection policy |
| --- | --- |
| Get FSM By Name | Requires one match in the selected scope. |
| Get First FSM By Name | Returns the first matching owner deliberately. |
| Get First FSM | Returns the first owner containing any FSM deliberately. |
| Find PlayMaker FSM | Search and store the result. |
| Find All PlayMaker FSMs | Collect matching owners without duplicates. |
| FSM Count / FSM Exists | Inspect a query without executing gameplay. |

Search scopes include the target GameObject, its Hierarchy, and Loaded Scenes. Set the hierarchy root explicitly; a missing root is not permission to search every scene.

Ordinary FSM targets remain strict. A first-match search is an explicit alternative, not the implicit behavior of blank FSM names.

## Register a Singleton

1. Open the Integration Workspace's **Settings**.
2. Add an entry to the Singleton FSM settings.
3. Choose an FSM template or prefab source and provide its registration name.
4. In a GC2 selector under **PlayMaker/Singletons**, select that registered identity. Use its Settings shortcut if configuration is missing.
5. Use an explicit instantiation/run operation when the instance must be created. Query selectors alone do not create the manager or an instance.
6. Verify lifecycle and persistence across the scene transitions your game uses.

Version **1.1.3** stores registration names independently from source prefab/template names. Renaming the source asset preserves the registration identity. Missing selections remain visible with a warning rather than silently switching to the first entry.

::: note Queries do not instantiate
The Singleton property and existence checks are side-effect free. A null or false result can mean the runtime instance does not exist yet. Choose an explicit creation operation instead of repeatedly querying and expecting creation.
:::

## Singleton Shortcuts

Under **PlayMaker/Singletons**, use the selected entry's GameObject, FSM variables, enabled/running/finished state, events, or execution operations. Available Instructions include get/instantiate, register/unregister, enable/disable/restart/run, event sending, and waits.

An existing unrelated object registered under the same name is a collision, not an object to replace automatically. Resolve the registration identity and target explicitly.

## Waits and Lifecycle Observation

| Wait / observer | Use |
| --- | --- |
| FSM Availability | Wait for a target to become resolvable. |
| FSM State | Wait for a selected state/path. |
| FSM to Finish | Wait for terminal FSM completion. |
| FSM or State to Finish | Select the intended completion target. |
| Singleton variants | Equivalent wait against the registered Singleton. |
| Available / Lost Events | Observe a target appearing or being replaced/lost. |
| Enabled / Disabled / Started / Finished Events | React to lifecycle changes. |
| Variable Changed Event | React after the baseline value has been observed. |

Assign timeouts and result destinations where exposed. Treat canceled, timed-out, invalid-target, and successful results separately. Full state paths avoid short-name collisions in nested graphs.

## Collections and Vector Components

The variable utilities support read, write, copy, existence/comparison, vector component extraction, and collection operations. Collection operations cover count, get/set, add/insert/remove/clear, contains, index-of, and GC2 list transfers.

Use a compatible PlayMaker collection reference and a writable destination. Fractional/out-of-range indices fail. Fixed-size or read-only collections reject unsupported operations. Whole-list transfers validate types before mutation, so a failed conversion should not be handled as a partial successful copy.

Vector2/Vector3/Vector4 and Quaternion component utilities expose individual numeric components where provided. Select the intended component and typed variable; these utilities do not change the simpler Name Variable action's Float-only Number contract.

## Troubleshooting

If a selector shows a missing Singleton, inspect its saved registration name in Settings. If a query returns nothing, check instantiation, target identity, enabled state, and search scope. If a collection operation fails, inspect the destination element type before changing existing list data.
