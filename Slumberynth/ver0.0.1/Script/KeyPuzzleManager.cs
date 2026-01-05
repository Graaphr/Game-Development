using UnityEngine;

public class KeyPuzzleManager : MonoBehaviour
{
    public DoorUnlock door;
    public int requiredKeys = 4;

    private int currentKeys = 0;

    public void AddKey()
    {
        currentKeys++;

        if (currentKeys >= requiredKeys)
        {
            Debug.Log("All keys collected — Door unlocked!");
            door.SetDoorUnlocked(true);  
        }
    }
}
