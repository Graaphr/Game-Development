using UnityEngine;

public class TriggerArea : MonoBehaviour
{
    public DoorUnlock door;  
    public string monsterTag = "Monster";

    [Header("Indicator Lights (Renderers)")]
    public Renderer[] indicatorRenderers; // Include the ball mesh renderers here
    public Color lockedColor = Color.red;
    public Color unlockedColor = Color.green;

    [Header("Point Lights")]
    public Light[] indicatorLights; // Add point lights if present

    private int monstersInside = 0;

    private void Start()
    {
        SetIndicatorLight(false);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag(monsterTag))
        {
            monstersInside++;
            door.SetDoorUnlocked(true);
            SetIndicatorLight(true);

            Debug.Log("Door can be opened manually");
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag(monsterTag))
        {
            monstersInside = Mathf.Max(0, monstersInside - 1);

            if (monstersInside == 0)
            {
                door.SetDoorUnlocked(false);
                door.ForceCloseIfOpen();
                SetIndicatorLight(false);

                Debug.Log("Door closing");
            }
        }
    }

    private void SetIndicatorLight(bool unlocked)
    {
        Color lightColor = unlocked ? unlockedColor : lockedColor;

        foreach (Light light in indicatorLights)
        {
            if (light != null)
                light.color = lightColor;
        }

        foreach (Renderer rend in indicatorRenderers)
        {
            if (rend != null)
            {
                Material mat = rend.material;
                mat.SetColor("_EmissionColor", lightColor * 2f); 
                DynamicGI.SetEmissive(rend, lightColor * 2f);
            }
        }
    }
}
