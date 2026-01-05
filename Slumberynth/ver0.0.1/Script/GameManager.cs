using UnityEngine;
using UnityEngine.SceneManagement;


public class GameManager : MonoBehaviour
{
    [Header("UI")]
    public GameObject mainMenuUI;
    public GameObject hudUI;
    public GameObject pauseMenuUI;
    public GameObject congratsUI;

    [Header("Player References")]
    public GameObject player;                       
    public PlayerMovementAdvanced playerMove;       
    public PlayerCam playerCam;                     

    bool isPaused = false;

    // AWAKe dipanggil sangat awal -> aman untuk mematikan komponen sebelum Start() lainnya berjalan
    public void Awake()
    {
        // UI awal
        mainMenuUI.SetActive(true);
        hudUI.SetActive(false);
        pauseMenuUI.SetActive(false);
        congratsUI.SetActive(false);

        // Pastikan player aktif di scene (agar kamera dapat menampilkan background),
        // tapi matikan script kontrol agar tidak merespon input.
        if (player != null) player.SetActive(true);

        if (playerMove != null) playerMove.enabled = false;
        if (playerCam != null) playerCam.enabled = false;

        // Cursor bebas saat di Main Menu
        Cursor.lockState = CursorLockMode.None;
        Cursor.visible = true;

        // Dunia freeze sebelum Start Game
        Time.timeScale = 0f;
    }

    // START tetap ada jika perlu inisialisasi lain
    private void Start()
    {
        // (kosong) — sebagian besar inisialisasi sudah di Awake()
    }

    // ===========================
    //        START GAME
    // ===========================
    public void StartGame()
    {
        mainMenuUI.SetActive(false);
        hudUI.SetActive(true);
        pauseMenuUI.SetActive(false);

        // Aktifkan movement setelah Start
        if (playerMove != null) playerMove.enabled = true;
        if (playerCam != null) playerCam.enabled = true;

        // Lock cursor untuk FPS control
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;

        // Jalankan world
        Time.timeScale = 1f;
        isPaused = false;
    }


    // ===========================
    //           UPDATE
    // ===========================
    private void Update()
    {
        // Allow toggle pause only saat playerMove ada dan sudah di-enable (artinya sedang di gameplay)
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            // Jika sedang di main menu (playerMove disabled) maka ESC sebaiknya tidak membuka pause.
            if (playerMove != null && playerMove.enabled)
            {
                if (isPaused) ResumeGame();
                else PauseGame();
            }
            // Optional: jika ingin ESC dari main menu menutup game atau kembali ke menu lain, tangani di sini.
        }
    }


    // ===========================
    //         PAUSE GAME
    // ===========================
    public void PauseGame()
    {
        isPaused = true;
        pauseMenuUI.SetActive(true);
        hudUI.SetActive(true); // HUD tetap tampil (sesuai permintaan)

        // Matikan kontrol
        if (playerMove != null) playerMove.enabled = false;
        if (playerCam != null) playerCam.enabled = false;

        // Cursor bebas untuk navigasi menu
        Cursor.lockState = CursorLockMode.None;
        Cursor.visible = true;

        Time.timeScale = 0f;
    }


    // ===========================
    //        RESUME GAME
    // ===========================
    public void ResumeGame()
    {
        isPaused = false;
        pauseMenuUI.SetActive(false);

        // Hidupkan kontrol lagi
        if (playerMove != null) playerMove.enabled = true;
        if (playerCam != null) playerCam.enabled = true;

        // Lock cursor kembali
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;

        Time.timeScale = 1f;
    }


    // ===========================
    //         RESTART GAME
    // ===========================
    public void RestartGame()
    {
        // Balikkan timescale dulu supaya scene bisa load dengan benar
        Time.timeScale = 1f;

        // Ambil scene aktif saat ini
        string currentScene = SceneManager.GetActiveScene().name;

        // Load ulang scene
        SceneManager.LoadScene(currentScene);

        Debug.Log("Game Restarted");
    }


    // ===========================
    //        QUIT / EXIT
    // ===========================
    public void QuitGame()
    {
        Application.Quit();
        Debug.Log("Game Quit");
    }
}
