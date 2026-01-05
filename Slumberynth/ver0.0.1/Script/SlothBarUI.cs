using UnityEngine;
using UnityEngine.UI;

public class SlothBarUI : MonoBehaviour
{
    public SlothBar sloth;
    public Image slothFill; // UI Image tipe Filled

    private void Update()
    {
        slothFill.fillAmount = sloth.currentSloth / sloth.maxSloth;
    }
}
