using UnityEngine;

public class DrawerSlide : MonoBehaviour
{
    public Vector3 openOffset;
    public float slideSpeed = 3f;
    public bool isOpen;
    public Rigidbody keyRb;

    private Vector3 closedPos;
    private Vector3 openPos;

    void Start()
    {
        closedPos = transform.localPosition;
        openPos = closedPos + openOffset;
    }

    void Update()
    {
        Vector3 targetPos = isOpen ? openPos : closedPos;
        transform.localPosition = Vector3.Lerp(transform.localPosition, targetPos, Time.deltaTime * slideSpeed);


        if (isOpen && keyRb != null && keyRb.isKinematic)
        {
            keyRb.isKinematic = false; 
        }
    }

    public void ToggleDrawer()
    {
        isOpen = !isOpen;
    }
}
