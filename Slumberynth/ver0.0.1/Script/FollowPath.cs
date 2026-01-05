using System.Collections;
using UnityEngine;

public class FollowPath : MonoBehaviour
{
    [Header("Movement Settings")]
    public Transform[] waypoints;
    public float patrolSpeed = 3f;
    public float chaseSpeed = 5f;
    public float rotationSpeed = 7f;
    public float pauseDuration = 1f;

    [Header("Player Detection")]
    public Transform player;
    public float detectionRange = 10f;
    public float fieldOfView = 100f;
    public LayerMask obstacleLayers;

    [Header("Attack Settings")]
    public float attackRange = 2f;
    public float attackCooldown = 1.5f;
    private bool canAttack = true;
    public Transform playerSpawnPoint;
    public GameManager gameManager;

    private int currentIndex = 0;
    private bool chasingPlayer = false;
    private bool attacking = false;

    void Start()
    {
        StartCoroutine(PatrolRoutine());
    }

    void Update()
    {
        DetectPlayer();
    }

    void DetectPlayer()
    {
        Vector3 dirToPlayer = player.position - transform.position;
        float distance = dirToPlayer.magnitude;
        float angle = Vector3.Angle(transform.forward, dirToPlayer);

        bool playerInSight = distance <= detectionRange &&
                             angle <= fieldOfView / 2f &&
                             !Physics.Raycast(transform.position + Vector3.up,
                                 dirToPlayer.normalized, distance, obstacleLayers);

        if (playerInSight)
        {
            chasingPlayer = true;
            StopAllCoroutines();
            StartCoroutine(ChasePlayer());
        }
        else if (chasingPlayer && !playerInSight)
        {
            chasingPlayer = false;
            attacking = false;
            StopAllCoroutines();
            StartCoroutine(PatrolRoutine());
        }
    }

    IEnumerator PatrolRoutine()
    {
        while (!chasingPlayer)
        {
            Transform target = waypoints[currentIndex];
            MoveToward(target.position, patrolSpeed);

            if (Vector3.Distance(transform.position, target.position) < 0.2f)
            {
                currentIndex = (currentIndex + 1) % waypoints.Length;
                yield return new WaitForSeconds(pauseDuration);
            }

            yield return null;
        }
    }

    IEnumerator ChasePlayer()
    {
        while (chasingPlayer)
        {
            float distance = Vector3.Distance(transform.position, player.position);

            if (distance > attackRange)
            {
                attacking = false;
                MoveToward(player.position, chaseSpeed);
            }
            else
            {
                if (!attacking)
                {
                    StartCoroutine(AttackPlayer());
                }
            }

            yield return null;
        }
    }

    IEnumerator AttackPlayer()
{
    attacking = true;

    while (attacking && canAttack)
    {
        // Rotate toward player but stop moving
        Vector3 direction = (player.position - transform.position).normalized;
        Quaternion rot = Quaternion.LookRotation(direction);
        transform.rotation = Quaternion.Slerp(transform.rotation, rot, rotationSpeed * Time.deltaTime);

        canAttack = false;
        Debug.Log("Monster attacks player!");

        // RESET PLAYER POSITION HERE
        gameManager.QuitGame();
        Debug.Log("It works");

        yield return new WaitForSeconds(attackCooldown);
        canAttack = true;
    }
}


    void MoveToward(Vector3 targetPos, float speed)
    {
        if (!attacking)
        {
            Vector3 direction = (targetPos - transform.position).normalized;
            Quaternion rot = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(transform.rotation, rot, rotationSpeed * Time.deltaTime);

            transform.position += transform.forward * speed * Time.deltaTime;
        }
    }

    private void OnDrawGizmosSelected()
    {
        // Detection area
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, detectionRange);

        // Attack range
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, attackRange);
    }
}
