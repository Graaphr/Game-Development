using TMPro;
using UnityEngine;

public class DamagePopup : MonoBehaviour
{
    [SerializeField] private TextMeshPro text;
    public float floatSpeed = 1.5f;
    public float lifeTime = 1f;

    Transform cam;

    void Awake()
    {
        if (text == null)
            text = GetComponentInChildren<TextMeshPro>();

        Camera camObj = Camera.main;

        if (camObj == null)
            camObj = FindObjectOfType<Camera>();

        if (camObj != null)
            cam = camObj.transform;
    }


    public void Setup(float damage)
    {
        text.text = damage.ToString("0");
        Destroy(gameObject, lifeTime);
    }

    void Update()
    {
        transform.position += Vector3.up * floatSpeed * Time.deltaTime;

        if (cam != null)
        {
            transform.forward = cam.forward; // 👈 PERFECT billboard
        }
    }
}
