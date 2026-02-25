using UnityEngine;

public class EnemyHealth : MonoBehaviour, IDamageable
{
    public float health = 100f;
    public GameObject damagePopupPrefab;

    public void TakeDamage(float amount, Vector3 hitPoint)
    {
        health -= amount;
        Debug.Log("Enemy took damage: " + amount);

        if (damagePopupPrefab != null)
        {
            GameObject popup = Instantiate(
                damagePopupPrefab,
                hitPoint,
                Quaternion.identity
            );

            popup.GetComponent<DamagePopup>().Setup(amount);
        }

        if (health <= 0f)
        {
            Die();
        }
    }

    void Die()
    {
        Debug.Log("Enemy died");


        Destroy(gameObject);
    }
}
