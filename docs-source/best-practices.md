# Best Practices

Make the boundary between the two frameworks visible in your graph: what starts the work, who owns it, what data crosses, and how completion is observed.

## One Owner per State and Value

Let PlayMaker own durable modes and transitions. Keep authored gameplay sequences in native GC2 Actions. Choose one store to own each gameplay value and use explicit access where possible.

A direct read/write shares access. A Property Binder adds a configured synchronization policy. Neither changes save ownership.

## Name Targets and Completion

Use unique FSM names when an object can have multiple FSM components. Prefer full state paths in nested or parallel graphs. Give events meaningful request/result names such as `Request-Open` and `Door-Opened`.

Document whether completion means a native FSM finish, reaching a state, receiving an event, or a GC2 task terminating. These are different boundaries.

## Make Busy and Failure Paths Visible

| Situation | Recommended handling |
| --- | --- |
| GC2 Actions already running | Reject with Busy Event, or explicitly Join and wait. |
| Missing or ambiguous FSM | Correct target/name; do not retry against an arbitrary first FSM. |
| False condition | Author a normal False branch. |
| Evaluation error | Author Failure handling; do not turn it into normal false completion. |
| Timeout/cancellation | Keep distinct from success where exposed. |
| Getter returns a surprising default | Inspect diagnostics before using the value as valid data. |

A join observes another caller's work. A detached call transfers lifetime to the running system. Do not cancel them as if you owned them.

## Keep Context Close to Gameplay

Check Self/Invoker and Target whenever reusing an Actions component on another object. Use a Context Provider when repeated slot configuration would obscure the graph, but keep its runtime target understandable.

Test dynamic references with the actual spawning and destruction sequence. A static inspector selection cannot prove a future runtime target exists.

## Poll and Bind Intentionally

Prefer one-shot reads or explicit notifications to per-frame polling. Choose Every Frame only for values that need it; give waits an appropriate interval and timeout. Unscaled timing is useful during pause, but gameplay inside the called routine may still use scaled time.

Choose one-way binding when authority is clear. Review two-way writers, structural reconciliation, and deletion policies before using them on authored data.

## Validate after Refactors

Re-index after structural changes, inspect Diagnostics, and test a representative interaction with Execution Trace. In v1.1.3, Singleton registration names survive source asset renames; missing references still need attention.

Exercise imports, serialization, optional modules, and player builds against the versions your team ships. See [Compatibility](compatibility.md) for which checks are qualified and which remain limited.
