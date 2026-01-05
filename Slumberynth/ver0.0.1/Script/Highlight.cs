using UnityEngine;

public class Highlight : MonoBehaviour
{
    public Renderer targetRenderer; 
    private Material[] originalMats;
    public Material outlineMaterial;

    void Start()
    {
        if (!targetRenderer)
            targetRenderer = GetComponent<Renderer>();

        originalMats = targetRenderer.materials;
    }

    public void ShowOutline()
    {
        Material[] mats = new Material[originalMats.Length + 1];
        originalMats.CopyTo(mats, 0);
        mats[mats.Length - 1] = outlineMaterial;
        targetRenderer.materials = mats;
    }

    public void HideOutline()
    {
        targetRenderer.materials = originalMats;
    }
}
