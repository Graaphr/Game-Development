using System.Collections;
using UnityEngine;
using TMPro;

public class DoorUnlock : MonoBehaviour
{
    [Header("Door Settings")]
    public Transform hingePivot;
    public float rotateSpeed = 2f;
    public float openAngle = 90f;
    public float interactRange = 3.0f;

    [Header("Interaction")]
    public KeyCode interactKey = KeyCode.E;
    public TextMeshProUGUI interactText;
    public Camera playerCam;

    [Header("Door State")]
    public bool doorUnlocked = false;

    private bool isOpen = false;
    private bool isMoving = false;
    private Quaternion closedRot;
    private Quaternion openRot;
    private Transform player;

    void Start()
    {
        player = playerCam.transform;
        closedRot = hingePivot.localRotation;
    }

    void Update()
    {
        ShowPrompt();

        if (Input.GetKeyDown(interactKey) && !isMoving)
        {
            if (!IsPlayerClose()) return;

            if (!doorUnlocked)
            {
                interactText.text = "Locked";
                return;
            }

            if (!isOpen)
                SetOpenDirection();

            StartCoroutine(isOpen ? CloseDoor() : OpenDoor());
        }
    }

    void ShowPrompt()
    {
        if (!IsPlayerClose())
        {
            interactText.text = "";
            return;
        }

        interactText.text = doorUnlocked ? "Press E" : "Locked";
    }

    bool IsPlayerClose()
    {
        return Vector3.Distance(player.position, hingePivot.position) < interactRange;
    }

    void SetOpenDirection()
    {
        Vector3 toPlayer = player.position - hingePivot.position;
        float dot = Vector3.Dot(hingePivot.right, toPlayer);
        float direction = (dot > 0) ? -1 : 1;
        openRot = closedRot * Quaternion.Euler(0f, 0f, openAngle * direction);
    }

    IEnumerator OpenDoor()
    {
        isMoving = true;
        float t = 0f;

        while (t < 1f)
        {
            hingePivot.localRotation = Quaternion.Slerp(hingePivot.localRotation, openRot, t);
            t += Time.deltaTime * rotateSpeed;
            yield return null;
        }

        isOpen = true;
        isMoving = false;
    }

    IEnumerator CloseDoor()
    {
        isMoving = true;
        float t = 0f;

        while (t < 1f)
        {
            hingePivot.localRotation = Quaternion.Slerp(hingePivot.localRotation, closedRot, t);
            t += Time.deltaTime * rotateSpeed;
            yield return null;
        }

        isOpen = false;
        isMoving = false;
    }

    public void SetDoorUnlocked(bool unlocked)
    {
        doorUnlocked = unlocked;

        if (!doorUnlocked)
            ForceCloseIfOpen();
    }

    public void ForceCloseIfOpen()
    {
        if (isOpen && !isMoving)
        Debug.Log("It Should Work");
            StartCoroutine(CloseDoor());
    }
}
