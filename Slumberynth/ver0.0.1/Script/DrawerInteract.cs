using UnityEngine;

public class DrawerInteract : MonoBehaviour
{
    public float interactRange = 3f;
    public LayerMask interactLayer;

    Camera cam;

    private void Start()
    {
        cam = Camera.main;
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.E))
        {
            if (Physics.Raycast(cam.transform.position, cam.transform.forward, out RaycastHit hit, interactRange, interactLayer))
            {
                DrawerSlide drawer = hit.collider.GetComponentInParent<DrawerSlide>();
                if (drawer != null)
                {
                    drawer.ToggleDrawer();
                }
            }
        }
    }
}
