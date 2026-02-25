using UnityEngine;
using System.Collections;

public enum AttackMode
{
    Ranged,
    Sword
}


public class PlayerAttack : MonoBehaviour
{
    [Header("Mode")]
    public AttackMode currentMode;

    [Header("References")]
    public Camera playerCam;
    public Transform attackPoint;
    public LayerMask enemyLayer;

    [Header("Ranged")]
    public GameObject laserPrefab;
    public float laserDamage = 15f;
    public float laserRange = 100f;
    public int shotsBeforeCooldown = 5;
    public float laserCooldown = 2f;
    float nextFireTime;
    public float fireRate = 0.15f;



    int shotsFired;
    bool canShoot = true;

    float fireVisualTimer;


    [Header("Sword")]
    public float swordDamage = 25f;
    public float swordRange = 2.2f;
    public int swordComboMax = 4;
    public float swordComboResetTime = 1f;

    int swordComboIndex;
    float lastSwordTime;

    [Header("Weapon Models")]
    public GameObject gun;
    public GameObject sword;

    [Header("Gun States")]
    public GameObject gunIdle;
    public GameObject gunFire;

    public float idleDelay = 0.15f;

    bool isFiring;


    float lastFireTime;

    [Header("Gun Recoil")]
    public Transform gunTransform;

    public float recoilKickBack = 0.08f;
    public float recoilUpRotation = 6f;

    public float recoilReturnSpeed = 18f;
    public float recoilSnappiness = 25f;

    Vector3 gunOriginalPos;
    Quaternion gunOriginalRot;

    Vector3 currentRecoilPos;
    Vector3 targetRecoilPos;

    Vector3 currentRecoilRot;
    Vector3 targetRecoilRot;

    [Header("Muzzle Flash")]
    public ParticleSystem muzzleFlash;





    [Header("UI")]
    public AmmoUI ammoUI;
    

    void Start()
    {
        gunOriginalPos = gunTransform.localPosition;
        gunOriginalRot = gunTransform.localRotation;

        if (ammoUI != null)
            ammoUI.Init(shotsBeforeCooldown);

        EquipWeapon(currentMode);
    }




    void Update()
    {
        HandleModeSwitch();
        UpdateRecoil();

        if (currentMode == AttackMode.Ranged && Input.GetMouseButton(0))
        {
            RangedAttack();
        }
        else if (Input.GetMouseButtonDown(0))
        {
            if (currentMode == AttackMode.Sword)
                SwordAttack();
        }

        UpdateGunVisual();
    }



    void EquipWeapon(AttackMode mode)
    {
        gun.SetActive(false);
        sword.SetActive(false);

        switch (mode)
        {
            case AttackMode.Ranged:
                gun.SetActive(true);
                break;

            case AttackMode.Sword:
                sword.SetActive(true);
                break;
        }
    }

    void HandleModeSwitch()
    {
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            currentMode = AttackMode.Ranged;
            EquipWeapon(currentMode);
        }

        if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            currentMode = AttackMode.Sword;
            EquipWeapon(currentMode);
        }
    }


    // ================= RANGED =================
    void RangedAttack()
    {
        if (!canShoot) return;
        if (Time.time < nextFireTime) return;

        nextFireTime = Time.time + fireRate;
        shotsFired++;

        isFiring = true;
        lastFireTime = Time.time;

        ApplyRecoil();

        if (muzzleFlash != null)
        {
            muzzleFlash.Emit(1);
        }



        if (ammoUI != null)
            ammoUI.SetAmmo(shotsBeforeCooldown - shotsFired);

        GameObject laser = Instantiate(
            laserPrefab,
            attackPoint.position,
            Quaternion.identity
        );

        laser.GetComponent<LaserProjectile>().Init(
            laserDamage,
            enemyLayer,
            playerCam.transform.forward,
            gameObject.layer
        );

        if (shotsFired >= shotsBeforeCooldown)
            StartCoroutine(RangedCooldown());
    }

    IEnumerator RangedCooldown()
    {
        canShoot = false;
        yield return new WaitForSeconds(laserCooldown);

        shotsFired = 0;
        canShoot = true;

        if (ammoUI != null)
            ammoUI.SetAmmo(shotsBeforeCooldown);
    }

    void UpdateGunVisual()
    {
        if (currentMode != AttackMode.Ranged) return;

        if (Input.GetMouseButton(0))
        {
            isFiring = true;
        }
        else
        {
            if (Time.time - lastFireTime > idleDelay)
                isFiring = false;
        }

        gunFire.SetActive(isFiring);
        gunIdle.SetActive(!isFiring);
    }

    void UpdateRecoil()
    {
        // Smooth recoil application
        currentRecoilPos = Vector3.Lerp(
            currentRecoilPos,
            targetRecoilPos,
            recoilSnappiness * Time.deltaTime
        );

        currentRecoilRot = Vector3.Lerp(
            currentRecoilRot,
            targetRecoilRot,
            recoilSnappiness * Time.deltaTime
        );

        // Smooth return to zero
        targetRecoilPos = Vector3.Lerp(
            targetRecoilPos,
            Vector3.zero,
            recoilReturnSpeed * Time.deltaTime
        );

        targetRecoilRot = Vector3.Lerp(
            targetRecoilRot,
            Vector3.zero,
            recoilReturnSpeed * Time.deltaTime
        );

        gunTransform.localPosition = gunOriginalPos + currentRecoilPos;
        gunTransform.localRotation = gunOriginalRot * Quaternion.Euler(currentRecoilRot);
    }


    void ApplyRecoil()
    {
        targetRecoilPos += new Vector3(0f, 0f, -recoilKickBack);
        targetRecoilRot += new Vector3(
            -recoilUpRotation,
            Random.Range(-1f, 1f),
            0f
        );
    }








    // ================= SWORD =================
    [SerializeField] GameObject slashVfxPrefab;
    [SerializeField] Transform slashSpawnPoint;

    void SwordAttack()
    {
        if (slashVfxPrefab == null || playerCam == null)
        {
            Debug.LogError("Slash VFX missing reference");
            return;
        }

        Vector3 spawnPos =
            playerCam.transform.position +
            playerCam.transform.forward * 0.6f;

        Quaternion rot =
            Quaternion.LookRotation(playerCam.transform.forward);

        GameObject slash = Instantiate(
            slashVfxPrefab,
            spawnPos,
            rot
        );

        slash.transform.localScale = Vector3.one * 2f;

        DealSlashDamage(swordRange, swordDamage);

        Destroy(slash, 0.25f);
    }





    // ================= DAMAGE =================
    void DealSlashDamage(float range, float damage)
    {
        Vector3 origin = playerCam.transform.position;
        Vector3 direction = playerCam.transform.forward;

        // Check wall first
        float maxDistance = range;
        if (Physics.Raycast(origin, direction, out RaycastHit wallHit, range, ~enemyLayer))
        {
            maxDistance = wallHit.distance;
        }

        // Slash volume
        Vector3 center = origin + direction * (maxDistance * 0.5f);
        Vector3 halfExtents = new Vector3(1.2f, 1.2f, maxDistance * 0.5f);

        Collider[] hits = Physics.OverlapBox(
            center,
            halfExtents,
            Quaternion.LookRotation(direction),
            enemyLayer
        );

        foreach (Collider hit in hits)
        {
            IDamageable dmg = hit.GetComponent<IDamageable>();
            if (dmg != null)
            {
                dmg.TakeDamage(damage, hit.ClosestPoint(origin));
            }
        }
    }

}
