using UnityEngine;

public class KeySlot : MonoBehaviour
{
    public bool keyInserted = false;
    public string requiredTag = "Key";
    public KeyPuzzleManager puzzleManager;

    private void OnTriggerEnter(Collider other)
    {
        if (!keyInserted && other.CompareTag(requiredTag))
        {
            keyInserted = true;
            puzzleManager.AddKey();
            
            Rigidbody rb = other.GetComponent<Rigidbody>();
            if (rb != null)
                rb.isKinematic = true;

            other.transform.position = transform.position;
            other.transform.rotation = transform.rotation;

            Debug.Log("Key inserted in slot!");
        }
    }
}
