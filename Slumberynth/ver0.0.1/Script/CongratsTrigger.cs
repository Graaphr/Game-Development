using UnityEngine;

public class CongratsTrigger : MonoBehaviour
{
    public GameObject congratsUI;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            congratsUI.SetActive(true);

            // Freeze player movement
            PlayerMovementAdvanced movement = other.GetComponent<PlayerMovementAdvanced>();
            if (movement != null)
                movement.enabled = false;

            // Unlock cursor so player can see mouse on UI
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }
    }
}
