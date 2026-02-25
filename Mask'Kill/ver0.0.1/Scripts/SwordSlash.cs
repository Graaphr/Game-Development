using UnityEngine;

public class SwordSlash : MonoBehaviour
{
    public float damage = 25f;
    public float range = 3f;
    public float radius = 1.5f;
    public LayerMask enemyLayer;
    public LayerMask obstacleLayer;

    public void Fire(Transform cam)
    {
        Vector3 origin = cam.position;
        Vector3 dir = cam.forward;

        RaycastHit wallHit;
        float finalRange = range;

        // Stop at wall
        if (Physics.Raycast(origin, dir, out wallHit, range, obstacleLayer))
        {
            finalRange = wallHit.distance;
        }

        // Multi-hit enemies
        Collider[] hits = Physics.OverlapSphere(
            origin + dir * finalRange * 0.5f,
            radius,
            enemyLayer
        );

        foreach (Collider c in hits)
        {
            IDamageable dmg = c.GetComponent<IDamageable>();
            if (dmg != null)
                dmg.TakeDamage(damage, c.ClosestPoint(origin));
        }
    }
}
