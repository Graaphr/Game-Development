using UnityEngine;

public class EnemyRanged : EnemyBase
{
    [Header("Ranged Combat")]
    public GameObject projectilePrefab;
    public Transform firePoint;

    public float minDistance = 5f;
    public float maxDistance = 8f;
    public float fireCooldown = 1.5f;

    float fireTimer;

    protected override void Start()
    {
        base.Start();
        moveSpeed = 3f;
        damage = 1f;
    }

    protected override void Update()
    {
        base.Update();

        fireTimer -= Time.deltaTime;

        if (fireTimer <= 0f && HasLineOfSight())
        {
            Fire();
            fireTimer = fireCooldown;
        }
    }

    protected override void MoveEnemy()
    {
        if (player == null) return;

        float dist = DistanceToPlayer();

        rb.linearVelocity = new Vector3(0f, rb.linearVelocity.y, 0f);

        Vector3 dir = (player.position - transform.position).normalized;
        dir.y = 0f;

        if (dist < minDistance)
        {
            rb.AddForce(-dir * moveSpeed * 10f, ForceMode.Force);
        }
        else if (dist > maxDistance)
        {
            rb.AddForce(dir * moveSpeed * 10f, ForceMode.Force);
        }
    }


    bool HasLineOfSight()
    {
        RaycastHit hit;
        if (Physics.Raycast(
            firePoint.position,
            (player.position - firePoint.position),
            out hit
        ))
        {
            return hit.transform.CompareTag("Player");
        }
        return false;
    }

    void Fire()
    {
        Vector3 dir = (player.position - firePoint.position).normalized;

        GameObject laser = Instantiate(
            projectilePrefab,
            firePoint.position,
            Quaternion.identity
        );

        laser.GetComponent<LaserProjectile>().Init(
            damage,
            LayerMask.GetMask("Player"),
            dir,
            gameObject.layer
        );
    }
}
