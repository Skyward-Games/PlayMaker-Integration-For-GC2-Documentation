# Scripting API

The integration exposes public runtime types through the **PlayMakerGC2.Core.Runtime** assembly. Most core types are in `PlayMakerGC2.Runtime`; routines, binding, and gameplay events use the more specific namespaces listed below.

## Runtime Types

| Type | Namespace | Use |
| --- | --- | --- |
| `PlayMakerFsmTarget` | `PlayMakerGC2.Runtime` | Resolve exactly one FSM on a target object. |
| `FsmResolutionResult` | `PlayMakerGC2.Runtime` | Inspect success, status, component, and error. |
| `PlayMakerVariableReference` | `PlayMakerGC2.Runtime` | Resolve typed LocalFsm, GlobalAsset, or Singleton variables. |
| `VariableNumberConversion` | `PlayMakerGC2.Runtime` | Checked Float/double/integer conversions. |
| `Gc2Context` | `PlayMakerGC2.Runtime` | Resolve GC2 Args Self and Target from an FSM context. |
| `InstructionPlayMakerSendEvent` | `PlayMakerGC2.Runtime` | Native GC2 local event Instruction. |
| `GameplayRoutine`, `GameplayRoutineRunner` | `PlayMakerGC2.Core.Runtime.Routines` | Typed reusable routine definition and runner. |
| `PlayMakerGc2BindingComponent` | `PlayMakerGC2.Core.Runtime.Binding` | Configured Property Binder. |
| `GameplayEvent`, `GameplayEventPayload` | `PlayMakerGC2.Core.Runtime.Events` | Reusable typed event definitions/data. |

Custom code in an assembly definition needs references to the integration, Unity, PlayMaker, and GC2 assemblies used by that code. Keep editor code in an editor-only assembly. Optional module types require the separate module assembly and installed dependencies.

## Resolve and Send an Event

This complete component uses the same strict resolver as the integration's native Instruction. Save it as `DoorEventSender.cs` and assign a door in the Inspector.

```csharp
using PlayMakerGC2.Runtime;
using UnityEngine;

public sealed class DoorEventSender : MonoBehaviour
{
    [SerializeField] private GameObject door;
    [SerializeField] private string fsmName = "Door State FSM";

    public void OpenDoor()
    {
        var target = new PlayMakerFsmTarget(door, fsmName);
        FsmResolutionResult result = target.Resolve();
        if (!result.IsSuccess)
        {
            Debug.LogWarning(result.ErrorMessage, this);
            return;
        }

        result.Component.SendEvent("Interact");
    }
}
```

A successful lookup proves identity, not delivery or transition. PlayMaker's active graph still decides how to handle `Interact`.

## Public Resolution Signatures

```csharp
// PlayMakerFsmTarget
public PlayMakerFsmTarget(GameObject gameObject, string fsmName = null);
public FsmResolutionResult Resolve();
public FsmResolutionResult Resolve(GameObject runtimeTarget);
public static BaseFsmComponent ResolveFsm(
    GameObject target, string fsmName, out string error);
public void Invalidate();
```

This block is a signature reference, not a standalone class. `BaseFsmComponent` is in `HutongGames.PlayMaker`. Results distinguish Success, MissingTarget, NotFound, and Ambiguous. Failed lookups can be retried after correcting the configuration.

## Create a GC2 Instruction

Save this complete example as `InstructionOpenNamedDoor.cs`. Its selector evaluates the door from incoming GC2 Args and sends the event only after strict resolution.

```csharp
using System;
using System.Threading.Tasks;
using GameCreator.Runtime.Common;
using GameCreator.Runtime.VisualScripting;
using PlayMakerGC2.Runtime;
using UnityEngine;

[Serializable]
[Title("Open Named Door")]
[Category("Examples/Open Named Door")]
public sealed class InstructionOpenNamedDoor : Instruction
{
    [SerializeField] private PropertyGetGameObject door =
        GetGameObjectSelf.Create();
    [SerializeField] private string fsmName = "Door State FSM";

    protected override Task Run(Args args)
    {
        var target = new PlayMakerFsmTarget(door.Get(args), fsmName);
        FsmResolutionResult result = target.Resolve();
        if (result.IsSuccess)
            result.Component.SendEvent("Interact");
        else
            Debug.LogWarning(result.ErrorMessage);

        return DefaultResult;
    }
}
```

## Checked Numeric Conversion

Use the public `VariableNumberConversion.TryDoubleToFloat(double, out float)` and `TryFloatToDouble(float, out double)` methods when crossing the Float/Number boundary. Both reject non-finite values; narrowing also checks range.

The `BridgeVariableType` enum supports more types than any individual action. Choose the actual action/property contract rather than assuming every enum type is accepted by every transfer.

## Gameplay Routine Entry Point

`GameplayRoutineRunner.ExecuteAsync` takes a `GameplayRoutine`, `BaseFsmComponent`, optional input dictionary, output dictionary, policy override, and CancellationToken. It returns `Task<GameplayRoutineResult>`. `ExecuteRoutineAsync` exposes the same parameter signature.

Call on Unity's gameplay thread with valid authored objects. Inspect the result before consuming output values. Join, restart, ownership, and cancellation rules still apply; see [Callable Routines](callable-routines.md).

## Extension Boundaries

Use native GC2 Instructions/Conditions/Properties and PlayMaker actions as your extension points. Do not rely on internal editor adapters or serialized private fields. There is no generic type-adapter registration API documented here; conversion support follows the current typed implementations.

For the complete behavior contracts, use the workflow pages and test against the specific dependency versions in [Compatibility](compatibility.md).
