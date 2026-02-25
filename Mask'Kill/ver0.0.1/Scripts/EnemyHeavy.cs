using UnityEngine;

public class EnemyHeavy : EnemyBase
{
    [Header("Heavy Attack")]
    public float stopDistance = 2.5f;
    public float attackRadius = 1.2f;
    public float attackCooldown = 2f;
    public float attackWindUp = 0.7f;
    public Transform attackPoint;

    [Header("Knockback")]
    public float knockbackForce = 14f;
    public float knockbackUpForce = 4f;

    [Header("Stun")]
    public float stunDuration = 0.6f;

    float cooldownTimer;
    float windUpTimer;
    bool windingUp;

    protected override void Update()
    {
        base.Update();

        if (cooldownTimer > 0)
            cooldownTimer -= Time.deltaTime;

        if (windingUp)
            windUpTimer -= Time.deltaTime;
    }

    protected override void MoveEnemy()
    {
        if (player == null) return;

        float dist = DistanceToPlayer();

        // Stop sliding
        rb.linearVelocity = new Vector3(0f, rb.linearVelocity.y, 0f);

        // Move toward player
        if (dist > stopDistance && !windingUp && cooldownTimer <= 0)
        {
            Vector3 dir = player.position - transform.position;
            dir.y = 0f;
            dir.Normalize();

            rb.AddForce(dir * moveSpeed * 10f, ForceMode.Force);
            return;
        }

        // Start wind-up
        if (dist <= stopDistance && !windingUp && cooldownTimer <= 0)
        {
            windingUp = true;
            windUpTimer = attackWindUp;
            return;
        }

        // Cancel if player escapes
        if (windingUp && dist > stopDistance)
        {
            windingUp = false;
            return;
        }

        // Execute slam
        if (windingUp && windUpTimer <= 0f)
        {
            Slam();
            windingUp = false;
            cooldownTimer = attackCooldown;
        }
    }

    void Slam()
    {
        Debug.Log("EnemyHeavy SLAM!");

        Collider[] hits = Physics.OverlapSphere(
            attackPoint.position,
            attackRadius,
            LayerMask.GetMask("whatIsPlayer")
        );

        foreach (Collider hit in hits)
        {
            // DAMAGE
            IDamageable dmg = hit.GetComponentInParent<IDamageable>();
            if (dmg != null)
                dmg.TakeDamage(damage, attackPoint.position);

            // KNOCKBACK
            Rigidbody playerRb = hit.GetComponentInParent<Rigidbody>();
            if (playerRb != null)
            {
                Vector3 dir =
                    (hit.transform.position - transform.position).normalized;
                dir.y = 0f;

                Vector3 force =
                    dir * knockbackForce +
                    Vector3.up * knockbackUpForce;

                playerRb.AddForce(force, ForceMode.Impulse);
            }

            // STUN (correct way)
            PlayerMovement move = hit.GetComponentInParent<PlayerMovement>();
            if (move != null)
            {
                move.Stun(stunDuration);
            }

            break;
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
