using UnityEngine;
using TMPro;

public class KeypadSafe : MonoBehaviour
{
    [Header("Code Settings")]
    public string correctCode = "1234";
    private string enteredCode = "";

    [Header("UI")]
    public TextMeshProUGUI displayText;
    public GameObject uiPanel;

    [Header("Player")]
    public Camera playerCam;
    public GameObject playerObj;
    public float interactRange = 2f;
    public KeyCode interactKey = KeyCode.E;

    public DoorUnlock doorUnlock;

    private bool uiActive;
    private bool isUnlocked = false;

    private Transform player;

    void Start()
    {
        player = playerCam.transform;
        uiPanel.SetActive(false);
        UpdateDisplay();
    }

    void Update()
    {
        if (isUnlocked) return; // Prevent accessing again

        if (Input.GetKeyDown(interactKey))
        {
            if (!uiActive)
            {
                if (Vector3.Distance(player.position, transform.position) <= interactRange)
                {
                    OpenUI();
                }
            }
            else
            {
                CloseUI();
            }
        }
    }

    public void EnterNumber(string num)
    {
        if (isUnlocked) return; // Block input if unlocked
        if (enteredCode.Length >= correctCode.Length) return;

        enteredCode += num;
        UpdateDisplay();

        if (enteredCode.Length == correctCode.Length)
            CheckCode();
    }

    public void ClearCode()
    {
        if (isUnlocked) return;
        enteredCode = "";
        UpdateDisplay();
    }

    void CheckCode()
    {
        if (isUnlocked) return;

        if (enteredCode == correctCode)
        {
            displayText.text = "<color=green>Unlocked!</color>";
            isUnlocked = true;
            Invoke(nameof(UnlockSafe), 0.5f);
        }
        else
        {
            displayText.text = "<color=red>Wrong!</color>";
            Invoke(nameof(ClearCode), 1f);
        }
    }

    void UnlockSafe()
    {
        CloseUI();

        if (doorUnlock != null)
        {
            doorUnlock.doorUnlocked = true;
            Debug.Log("Safe Unlocked!");
        }
    }

    void UpdateDisplay()
    {
        displayText.text = enteredCode;
    }

    void OpenUI()
    {
        uiActive = true;
        uiPanel.SetActive(true);

        Cursor.lockState = CursorLockMode.None;
        Cursor.visible = true;

        Rigidbody rb = playerObj.GetComponent<Rigidbody>();
        if (rb != null)
        {
            rb.linearVelocity = Vector3.zero;
            rb.isKinematic = true;
        }

        if (playerCam.GetComponent<PlayerCam>() != null)
            playerCam.GetComponent<PlayerCam>().enabled = false;
    }

    void CloseUI()
    {
        uiActive = false;
        uiPanel.SetActive(false);

        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;

        Rigidbody rb = playerObj.GetComponent<Rigidbody>();
        if (rb != null)
        {
            rb.isKinematic = false;
        }

        if (playerCam.GetComponent<PlayerCam>() != null)
            playerCam.GetComponent<PlayerCam>().enabled = true;
    }
}
