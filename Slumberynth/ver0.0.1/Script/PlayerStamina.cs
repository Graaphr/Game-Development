using UnityEngine;

public class PlayerStamina : MonoBehaviour
{
    [Header("Stamina Settings")]
    public float maxStamina = 100f;
    public float currentStamina;
    public float staminaDrainPerSecond = 20f;
    public float staminaRegenPerSecond = 15f;

    [Header("Sprint Threshold")]
    public float staminaSprintThreshold = 20f; 
    // boleh sprint lagi kalau stamina >= angka ini

    [Header("Exhaust Settings")]
    public float exhaustedDuration = 5f;

    [HideInInspector] public bool canSprint = true;

    [Header("UI")]
    public UnityEngine.UI.Image staminaBar;

    private PlayerMovementAdvanced movement;

    private void Start()
    {
        currentStamina = maxStamina;
        movement = GetComponent<PlayerMovementAdvanced>();
    }

    private void Update()
    {
        HandleStamina();
        UpdateStaminaUI();
    }

    public void HandleStamina()
    {
        // Jika sprint
        if (movement.state == PlayerMovementAdvanced.MovementState.sprinting && movement.grounded)
        {
            currentStamina -= staminaDrainPerSecond * Time.deltaTime;

            if (currentStamina <= 0)
            {
                currentStamina = 0;
                canSprint = false;

                movement.TriggerExhaust(exhaustedDuration);
            }
        }
        else
        {
            currentStamina += staminaRegenPerSecond * Time.deltaTime;

            if (currentStamina >= maxStamina)
                currentStamina = maxStamina;
        }

        // 🔥 Aturan baru: setelah exhaust selesai, stamina cukup segini sudah bisa sprint lagi
        if (currentStamina >= staminaSprintThreshold)
            canSprint = true;
    }

    private void UpdateStaminaUI()
    {
        if (staminaBar != null)
        {
            staminaBar.fillAmount = currentStamina / maxStamina;
        }
    }
}
