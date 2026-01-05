using UnityEngine;

public class SlothBar : MonoBehaviour
{
    [Header("Sloth Settings")]
    public float maxSloth = 100f;
    public float currentSloth = 0f;

    public float increaseRate = 10f;   // idle
    public float decreaseRate = 20f;   // sprint

    private PlayerMovementAdvanced pm;

    private void Start()
    {
        pm = GetComponent<PlayerMovementAdvanced>();
        currentSloth = 0;
    }

    private void Update()
    {
        HandleSloth();
        currentSloth = Mathf.Clamp(currentSloth, 0, maxSloth);
    }

    private void HandleSloth()
    {
        float horizontal = Input.GetAxisRaw("Horizontal");
        float vertical = Input.GetAxisRaw("Vertical");

        bool isIdle = pm.grounded && horizontal == 0 && vertical == 0;

        // ● Idle → tambah
        if (isIdle)
        {
            currentSloth += increaseRate * Time.deltaTime;
            return;
        }

        // ● Sprint → berkurang
        if (pm.state == PlayerMovementAdvanced.MovementState.sprinting)
        {
            currentSloth -= decreaseRate * Time.deltaTime;
            return;
        }

        // ● Walking → tetap
        // tidak ada perubahan nilai
    }
}
