using UnityEngine;
using UnityEngine.UI;

public class AmmoUI : MonoBehaviour
{
    public Image[] segments;
    public Color fullColor = Color.cyan;
    public Color emptyColor = Color.black;

    int maxAmmo;

    public void Init(int max)
    {
        maxAmmo = max;
        SetAmmo(maxAmmo);
    }

    public void SetAmmo(int current)
    {
        for (int i = 0; i < segments.Length; i++)
        {
            segments[i].color = i < current ? fullColor : emptyColor;
        }
    }
}
