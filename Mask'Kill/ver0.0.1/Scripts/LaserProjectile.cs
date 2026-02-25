using UnityEngine;

public class LaserProjectile : MonoBehaviour
{
    public float speed = 60f;

    float damage;
    LayerMask targetLayer;
    Vector3 moveDir;
    int ownerLayer;

    Rigidbody rb;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    public void Init(float dmg, LayerMask target, Vector3 direction, int owner)
    {
        damage = dmg;
        targetLayer = target;
        moveDir = direction.normalized;
        ownerLayer = owner;

        rb.linearVelocity = moveDir * speed;
        transform.forward = moveDir;

        Destroy(gameObject, 3f);
    }

    void OnTriggerEnter(Collider other)
    {
        if (other is BoxCollider)
        {
            Physics.IgnoreCollision(other, GetComponent<Collider>());
            return;
        }

        if (other.GetComponentInParent<IDamageable>() is IDamageable dmg)
        {
            dmg.TakeDamage(damage, transform.position);
            Destroy(gameObject);
        }
    }

}

