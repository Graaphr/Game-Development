using UnityEngine;
using System.Collections;

public class PlayerHealth : MonoBehaviour, IDamageable
{
    public int maxHealth = 5;
    int currentHealth;

    public float iFrameDuration = 0.6f;
    bool invincible;

    public CameraShake cameraShake;
    public BatteryHealthUI healthUI;

    void Start()
    {
        currentHealth = maxHealth;

        if (healthUI != null)
            healthUI.SetHealth(currentHealth);
        else
            Debug.LogError("HealthUI is NOT assigned!");
    }


    public void TakeDamage(float amount, Vector3 hitPoint)
    {
        if (invincible) return;

        currentHealth -= 1;
        currentHealth = Mathf.Clamp(currentHealth, 0, maxHealth);

        healthUI.SetHealth(currentHealth);

        StartCoroutine(InvincibilityFrames());
        cameraShake.Shake();

        if (currentHealth <= 0)
            Die();
    }


    IEnumerator InvincibilityFrames()
    {
        invincible = true;
        yield return new WaitForSeconds(iFrameDuration);
        invincible = false;
    }

    void Die()
    {
        Debug.Log("Player died");
    }
}
