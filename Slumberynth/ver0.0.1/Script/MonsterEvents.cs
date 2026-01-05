using UnityEngine;
using UnityEngine.Events;

public class MonsterEvents : MonoBehaviour
{
    [Header("Monster Event")]
    public UnityEvent onTriggered;

    public void TriggerEvent()
    {
        onTriggered?.Invoke();
    }
}
