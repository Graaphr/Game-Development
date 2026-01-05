using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class TimedImageWithIdle : MonoBehaviour
{
    [Header("UI")]
    public Image popupImage;
    public float showDuration = 2f;

    [Header("Player")]
    public Transform player; // drag Player di sini
    public float idleThreshold = 5f; // berapa detik dianggap diam

    private Vector3 lastPosition;
    private float idleTimer;

    void Start()
    {
        popupImage.gameObject.SetActive(false);

        lastPosition = player.position;

        // Tampilkan UI saat game dimulai
        StartCoroutine(ShowImageRoutine());
    }

    void Update()
    {
        // Cek apakah player bergerak
        if (Vector3.Distance(player.position, lastPosition) < 0.01f)
        {
            idleTimer += Time.deltaTime;

            // jika idle melebihi batas → tampilkan UI
            if (idleTimer >= idleThreshold)
            {
                StartCoroutine(ShowImageRoutine());
                idleTimer = 0f; // reset
            }
        }
        else
        {
            idleTimer = 0f;  // reset kalau bergerak
        }

        lastPosition = player.position;
    }

    IEnumerator ShowImageRoutine()
    {
        popupImage.gameObject.SetActive(true);
        yield return new WaitForSeconds(showDuration);
        popupImage.gameObject.SetActive(false);
    }
}
