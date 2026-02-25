using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public abstract class EnemyBase : MonoBehaviour
{
    [Header("References")]
    protected Transform player;
    protected Rigidbody rb;

    [Header("Movement")]
    public float moveSpeed = 3f;
    public float groundDrag = 6f;
    public float airMultiplier = 0.4f;

    [Header("Combat")]
    public float attackRange = 2f;
    public float damage = 1f;

    [Header("Ground Check")]
    public float enemyHeight = 2f;
    public LayerMask groundLayer;

    [Header("Slope Handling")]
    public float maxSlopeAngle = 45f;

    protected Vector3 moveDirection;
    protected bool grounded;
    protected bool exitingSlope;

    RaycastHit slopeHit;

    protected virtual void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player").transform;
        rb = GetComponent<Rigidbody>();
        rb.freezeRotation = true;
    }

    protected virtual void Update()
    {
        GroundCheck();
        HandleDrag();
    }

    protected virtual void FixedUpdate()
    {
        FacePlayer();
        MoveEnemy();
        SpeedControl();
    }

    // ================= MOVEMENT =================

    protected virtual void MoveEnemy()
    {
        if (player == null) return;

        Vector3 dirToPlayer = (player.position - transform.position).normalized;
        moveDirection = new Vector3(dirToPlayer.x, 0f, dirToPlayer.z);

        // On slope
        if (OnSlope() && !exitingSlope)
        {
            rb.AddForce(GetSlopeMoveDirection(moveDirection) * moveSpeed * 20f, ForceMode.Force);

            if (rb.linearVelocity.y > 0)
                rb.AddForce(Vector3.down * 80f, ForceMode.Force);
        }
        // On ground
        else if (grounded)
        {
            rb.AddForce(moveDirection * moveSpeed * 10f, ForceMode.Force);
        }
        // In air
        else
        {
            rb.AddForce(moveDirection * moveSpeed * 10f * airMultiplier, ForceMode.Force);
        }

        rb.useGravity = !OnSlope();
    }

    protected void FacePlayer()
    {
        if (player == null) return;

        Vector3 lookDir = player.position - transform.position;
        lookDir.y = 0f;

        if (lookDir.sqrMagnitude < 0.01f) return;

        Quaternion targetRot = Quaternion.LookRotation(lookDir);
        transform.rotation = Quaternion.Slerp(
            transform.rotation,
            targetRot,
            Time.deltaTime * 10f
        );
    }

    protected void SpeedControl()
    {
        if (OnSlope() && !exitingSlope)
        {
            if (rb.linearVelocity.magnitude > moveSpeed)
                rb.linearVelocity = rb.linearVelocity.normalized * moveSpeed;
        }
        else
        {
            Vector3 flatVel = new Vector3(rb.linearVelocity.x, 0f, rb.linearVelocity.z);

            if (flatVel.magnitude > moveSpeed)
            {
                Vector3 limitedVel = flatVel.normalized * moveSpeed;
                rb.linearVelocity = new Vector3(
                    limitedVel.x,
                    rb.linearVelocity.y,
                    limitedVel.z
                );
            }
        }
    }

    protected void GroundCheck()
    {
        grounded = Physics.Raycast(
            transform.position,
            Vector3.down,
            enemyHeight * 0.5f + 0.3f,
            groundLayer
        );
    }

    protected void HandleDrag()
    {
        rb.linearDamping = grounded ? groundDrag : 0f;
    }

    protected bool OnSlope()
    {
        if (Physics.Raycast(
            transform.position,
            Vector3.down,
            out slopeHit,
            enemyHeight * 0.5f + 0.3f
        ))
        {
            float angle = Vector3.Angle(Vector3.up, slopeHit.normal);
            return angle < maxSlopeAngle && angle != 0;
        }
        return false;
    }

    protected Vector3 GetSlopeMoveDirection(Vector3 direction)
    {
        return Vector3.ProjectOnPlane(direction, slopeHit.normal).normalized;
    }

    // ================= UTILITY =================

    protected float DistanceToPlayer()
    {
        if (player == null) return Mathf.Infinity;
        return Vector3.Distance(transform.position, player.position);
    }
}
