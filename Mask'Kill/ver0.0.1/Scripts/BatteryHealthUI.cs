using UnityEngine;
using UnityEngine.UI;

public class BatteryHealthUI : MonoBehaviour
{
    [Header("Segments (left → right)")]
    public Image[] segments;

    public Color fullColor = Color.red;
    public Color emptyColor = new Color(0.3f, 0.3f, 0.3f, 1f);

    public void SetHealth(int currentHealth)
    {
        // Safety
        if (segments == null || segments.Length == 0)
        {
            Debug.LogError("BatteryHealthUI: No segments assigned!");
            return;
        }

        for (int i = 0; i < segments.Length; i++)
        {
            segments[i].color = (i < currentHealth)
                ? fullColor
                : emptyColor;
        }
    }
}
