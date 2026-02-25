using UnityEngine;

public class EnemyNormal : EnemyBase
{
    [Header("Melee")]
    public Transform attackPoint;
    public float attackRadius = 0.8f;

    [Header("Timing")]
    public float attackWindUp = 0.4f;
    public float attackCooldown = 1f;

    [Header("Knockback")]
    public float knockbackForce = 8f;
    public float knockbackUpForce = 2f;

    float windUpTimer;
    float cooldownTimer;
    bool windingUp;

    protected override void Update()
    {
        base.Update();

        if (windingUp)
            windUpTimer -= Time.deltaTime;

        if (cooldownTimer > 0)
            cooldownTimer -= Time.deltaTime;
    }

    protected override void MoveEnemy()
    {
        if (player == null) return;

        float dist = DistanceToPlayer();

        // Stop sliding when close
        rb.linearVelocity = new Vector3(0f, rb.linearVelocity.y, 0f);

        // Move toward player
        if (dist > attackRange && !windingUp && cooldownTimer <= 0)
        {
            Vector3 dir = (player.position - transform.position);
            dir.y = 0f;
            dir.Normalize();

            rb.AddForce(dir * moveSpeed * 10f, ForceMode.Force);
            return;
        }

        // Start wind-up
        if (dist <= attackRange && !windingUp && cooldownTimer <= 0)
        {
            windingUp = true;
            windUpTimer = attackWindUp;
        }

        // Cancel attack if player escapes
        if (windingUp && dist > attackRange)
        {
            windingUp = false;
        }

        // Execute attack
        if (windingUp && windUpTimer <= 0f)
        {
            Attack();
            windingUp = false;
            cooldownTimer = attackCooldown;
        }
    }

    void Attack()
{
    Collider[] hits = Physics.OverlapSphere(
        attackPoint.position,
        attackRadius,
        LayerMask.GetMask("whatIsPlayer")
    );

    foreach (Collider hit in hits)
    {
        // Damage
        if (hit.GetComponentInParent<IDamageable>() is IDamageable dmg)
        {
            Debug.Log("EnemyNormal HIT player");
            dmg.TakeDamage(damage, attackPoint.position);
        }

        // Knockback
        Rigidbody playerRb = hit.GetComponentInParent<Rigidbody>();
        if (playerRb != null)
        {
            Vector3 knockDir = (hit.transform.position - transform.position).normalized;
            knockDir.y = 0f;

            Vector3 force =
                knockDir * knockbackForce +
                Vector3.up * knockbackUpForce;

            playerRb.AddForce(force, ForceMode.Impulse);
        }

        break; // hit only once
    }
}


#if UNITY_EDITOR
    void OnDrawGizmosSelected()
    {
        if (attackPoint == null) return;
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(attackPoint.position, attackRadius);
    }
#endif
}
