# Changelog

Documentation website updates and release history for PlayMaker 2 Integration for Game Creator 2. Plugin release history is copied from the plugin changelog through v1.1.3. Historical entries preserve their original labels; current selector paths and limitations are documented in the workflow pages.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Documentation Website — 2026-10-20

### Added
- Published online documentation for the package, complementing its included offline PDF and self-contained HTML manuals.
- Added a Documentation & Artwork Disclosure confirming that all artwork featuring the Game Creator 2 (GC2) symbol was duly authorized by Marti and follows Game Creator's publication and branding guidelines.

## [1.1.3] - 2026-10-20

### Added
- Comprehensive offline documentation in PDF and self-contained HTML, bundled in the plugin's `Documentation/` folder for local access after import.
- Direct link to the offline PDF manual from the User Guide index.

### Fixed
- Saved Singleton registration names independently of prefab and FSM template names, so renaming source assets preserves references in instructions, properties, conditions, and events. Existing settings migrate automatically in the editor.
- Singleton selectors preserve missing selections and display a warning instead of silently assigning the first registered Singleton.

### Validation
- Unity 6000.6.0f1: 48 focused EditMode tests and 9 focused PlayMode tests passed, including Singleton rename coverage.
- UPM archive verified against the plugin source files; offline documentation is included and automated tests are excluded.

## [1.1.2] - 2026-10-03

### Added
- Dedicated instructions for waiting for a PlayMaker FSM or a selected state to finish, including equivalent Singleton shortcuts, timeout, cancellation, and result outputs.
- State and FSM pickers for additional properties, conditions, and instructions.
- Regression coverage for renamed FSM ambiguity, incompatible GC2 list destinations, additive scene ordering, unscaled waits, and persistent Singletons with multiple FSM components.

### Changed
- Clear, distinct selector names for ordinary PlayMaker FSM waits and PlayMaker Singleton FSM waits. Selector entries, descriptions, capability names, and added-instruction labels now agree.
- Standardized Singleton variable property names and the Send Event instruction label; retained existing class names, serialized fields, GUIDs, and capability IDs.
- Improved global event discovery across event assets, templates, prefabs, configured Singletons, and loaded scene FSMs.

### Fixed
- Invalidated cached FSM resolution when another component is renamed to the same name.
- Validated Find All destination list types and hierarchy roots before clearing existing contents.
- Normalized Singleton registration names on lookup and accepted valid FSM components after an unconfigured template component.
- Hid remaining private and public GC2 test helpers from instruction and condition selectors.
- Restored project-only test result callbacks after domain reload.

### Validation and known limitations
- Focused utilities suites: 42 EditMode tests and 8 PlayMode tests passed on Unity 6000.6.0f1.
- Player script compilation succeeded, including the PlayMaker and PlayMakerGC2 runtime assemblies.
- Distribution packages contain only the plugin under `Assets/Plugins/SkywardGames/PlayMakerGC2/`; automated tests are excluded by default.
- The broader Core sweeps are not fully green: five EditMode failures involve binding synchronization, an outdated Unity version expectation, state hierarchy expectations, and the configured Console Singleton during domain reload. Two PlayMode failures involve the existing Character fixture and native GC2 Signal delivery. See `Documentation/GC2_PLAYMAKER_UTILITIES.md` for details.

## [1.1.1] - 2026-09-27

### Added
- Strict PlayMaker Singleton selector dropdown (`[PlayMakerSingletonPicker]`):
  - Replaced manual error-prone string input with a popup dropdown listing all registered singletons in the project.
  - Included a direct "Settings" button navigating immediately to the PlayMaker GC2 Workspace Settings tab.
  - Added warning indicators when no singletons are registered or when the selected singleton is invalid.
- PlayMaker Global Event Indexer and Drawer (`PlayMakerGlobalEventIndexer` & `InstructionPlayMakerSendGlobalEventDrawer`):
  - "Choose Global Event..." dropdown populated with all project global events.
  - Background and manual project-wide rescan button to index global events across scene FSMs, prefabs, and templates.
  - Architectural callout warning discouraging spaghetti patterns and recommending singletons or local events where appropriate.
- Rate-limited runtime exception diagnostics:
  - Wrapped `InstructionPlayMakerSendEvent` and `InstructionPlayMakerSendGlobalEvent` execution with defensive try/catch handling.
  - Detailed errors forwarded to `BridgeDiagnostic.FromExecutionFailure` to prevent silent failures and game-breaking unhandled exceptions.
- EditMode integration test suite `PlayMakerSingletonAndGlobalEventIntegrationTests` validating singleton selector and global event indexer behavior.

### Fixed
- Fixed static singleton target resolution in Game Creator 2 action/instruction drawers (`PlayMakerGc2AdapterDrawers.GetStaticTarget`), eliminating false "no PlayMaker FSM found on 'Actions'" warnings and enabling FSM and Local Event pickers when targeting singleton instances.

## [1.1.0] - 2026-09-14

### Added
- Expanded GC2 <-> PlayMaker core utilities:
  - FSM search properties and instructions: Get FSM By Name (unique requirement), Get First FSM By Name, Get First FSM, Find FSM, Find All FSMs.
  - FSM and State execution conditions: Has FSM, FSM Running, FSM Finished, State Active.
  - FSM execution and timing instructions: Wait For FSM Available, Wait For FSM Finished, Wait For State (with timeout and cancel conditions).
  - Variable and Collections suite: Set, Copy, and component extraction for Vector2/Vector3/Vector4/Quaternion; full CRUD for FSM Array and ArrayList collections.
  - FSM Singleton utilities: zero-creation guarantee singleton selector dropdown, singleton property getters, variable accessors, and lifecycle state observation.
- Comprehensive documentation in `Documentation/GC2_PLAYMAKER_UTILITIES.md`.
- EditMode and PlayMode integration tests for all new utilities and singleton bindings.

### Fixed
- Resolved standalone player compilation issue in `InstructionRunGameplayRoutine` with `PlayMakerTemplateCompatibility.TryAssign`.
- Repaired hierarchy search fallback semantics in `InstructionPlayMakerFindFsm`.
- Excluded internal test types from Game Creator 2 inspector pickers.
- Preserved Property Binder assets created with the legacy `m_AutoMirrorVariables` field and repaired custom inspector binding.
- Made Property Binder authoring preview-only in Edit Mode, with an explicit Undoable synchronization action and accurate match diagnostics.
- Rejected ambiguous blank FSM targets when more than one PlayMaker FSM is present.
- Corrected Gameplay Routine start, ownership, reject, join, restart, cancellation, and fire-and-forget output behavior.
- Reset runtime event, routine, receiver, and trace state for domain-reload-disabled Play Mode sessions.
- Ensured global Gameplay Events reach every active FSM even when the receiver registry is only partially populated.
- Made built-in singleton query actions side-effect free, rejected unrelated name collisions, and isolated PlayMaker beta.80's editor/player template-assignment difference.
- Honored exact trace-buffer capacities and restored the neutral `General` category for new Gameplay Event assets.
- Preserved Workspace filters, added live trace refresh, scan progress, duplicate-component prevention, and consistent collapsed information panels.
- Corrected named bridge-event terminology, verified-version documentation, and test asset cleanup.

### Validation
- Unity `6000.4.6f1`: EditMode and PlayMode tests passed, standalone player builds compile cleanly with 0 errors.

## [1.0.0] - 2026-08-21

### Added
- Complete bidirectional integration connecting PlayMaker 2 and Game Creator 2.
- Generic execution bridge: `Run GC2 Actions`, `Run GC2 Instructions`, `Check GC2 Conditions`, `Wait Until GC2 Conditions`, `Wait While GC2 Conditions`.
- GC2 Signal bridge: `Emit GC2 Signal` and `Wait For GC2 Signal` with `Scaled`/`Unscaled` time modes and timeout handling.
- GC2 Variable bridges for Local and Global Name Variables and full CRUD List Variables.
- PlayMaker FSM control: `InstructionPlayMakerSendEvent`, `InstructionPlayMakerSendGlobalEvent`, `InstructionPlayMakerRunFsm` (v2 Callable FSM Routine with parameter mappings), `InstructionPlayMakerSetFsmState`.
- PlayMaker State Lifecycle GC2 Events: `On PlayMaker State Enter`, `On PlayMaker State Exit`, `On PlayMaker FSM Finished`, `On Global Event`.
- PlayMaker DataTable and DataRecord operations, conditions, properties, and synchronization actions.
- PlayMaker EnumDefinition & State Enum integration.
- PlayMaker UI Widget support (DataTableWidget, Meters, Target Managers, Minimap, Data Paging, Animated Lists).
- Deep Subsystems: Stats / Numeric variables, Save/Load Profile coordination, Object Pool, Interactables, Camera Transitions & Shakes, GC2 Audio, and Character Locomotion.
- Unified outcome model (`BridgeOutcome` & `BridgeExecutionResult` with atomic correlation IDs).
- Project-wide Bridge Validator Editor Window (`Tools > PlayMaker GC2 > Bridge Validator`) and cross-navigation inspector drawers.
- Comprehensive EditMode and PlayMode integration test suites.
- Six verified reference scenes: State-Driven Door, Guard State Flow, Shared Boundary Data, Core Game Mode, Callable FSM Routines, Enemy AI Orchestration.

### Fixed
- Eliminated all runtime reflection in widget properties and events.
- Added support for camera shake delay and configurable ShakeEffect.
- Fixed asynchronous Save/Load completion coordination.
- Corrected Callable FSM ownership semantics on joined and detached executions.
- Fixed `WaitForGc2Signal` timeout handling when signal name is empty or not yet emitted.
- Added null safety checks for `TUnitAnimim` mannequin positioning, rotation, scale, and animator proxy creation.
- Replaced direct receiver enumeration in `Signals.cs` with an array snapshot to prevent collection modification exceptions during signal broadcast.
- Optimized async test timing, global run counter resets, and frame yields across PlayMode test suites.
- Corrected active FSM discovery in `InstructionPlayMakerSendGlobalEvent` using `FindObjectsInactive.Exclude`.
