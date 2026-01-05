using UnityEngine;
using TMPro;

public class PickUp : MonoBehaviour


{

    public GameObject GetHeldObject()
    {
        return heldObject ? heldObject.gameObject : null;
    }

    public void ForceDrop()
    {
        if (!heldObject) return;

        heldObject.useGravity = true;
        heldObject.linearDamping = 1f;
        heldObject.transform.parent = null;
        heldObject = null;
    }

    public float pickUpRange = 3f;
    public float throwForce = 500f;
    public Transform holdPoint;
    public float holdSmoothness = 10f;
    public Vector3 holdRotation;

    public TextMeshProUGUI interactText;

    private Highlight currentHover;
    private Rigidbody heldObject;

    void Start()
    {
        interactText.gameObject.SetActive(false);
    }

    void Update()
    {
        CheckHover();

        if (Input.GetKeyDown(KeyCode.E))
        {
            if (heldObject == null)
                TryPickUp();
        }

        if (heldObject != null)
        {
            MoveObject();

            if (Input.GetMouseButtonDown(0))
                Throw();
        }
    }

    void MoveObject()
    {
        Vector3 moveDir = (holdPoint.position - heldObject.position);
        heldObject.linearVelocity = moveDir * holdSmoothness;

        Quaternion targetRot = holdPoint.rotation * Quaternion.Euler(holdRotation);
        heldObject.MoveRotation(Quaternion.Slerp(
            heldObject.rotation,
            targetRot,
            Time.deltaTime * holdSmoothness
        ));
    }

    void TryPickUp()
    {
        if (currentHover == null) return;

        Rigidbody rb = currentHover.GetComponent<Rigidbody>();

        heldObject = rb;
        rb.useGravity = false;
        rb.linearDamping = 10f;
        rb.angularDamping = 10f;

        currentHover.HideOutline();
        interactText.gameObject.SetActive(false);
    }

    void Drop()
    {
        if (heldObject == null) return;

        heldObject.useGravity = true;
        heldObject.linearDamping = 1f;
        heldObject.angularDamping = 0.05f;
        heldObject = null;
    }

    void Throw()
    {
        if (heldObject == null) return;

        heldObject.useGravity = true;
        heldObject.linearDamping = 1f;
        heldObject.angularDamping = 0.05f;
        heldObject.AddForce(transform.forward * throwForce);
        heldObject = null;
    }

    void CheckHover()
    {
        if (currentHover != null)
        {
            currentHover.HideOutline();
            currentHover = null;
            interactText.gameObject.SetActive(false);
        }

        if (heldObject != null) return;

        if (Physics.Raycast(transform.position, transform.forward, out RaycastHit hit, pickUpRange))
        {
            if (hit.collider.CompareTag("Pickable") || hit.collider.CompareTag("Key")) 
            {
                Highlight hover = hit.collider.GetComponent<Highlight>();
                if (hover != null)
                {
                    currentHover = hover;
                    currentHover.ShowOutline();
                    interactText.gameObject.SetActive(true);
                }
            }
        }
    }
}
