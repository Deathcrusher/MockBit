using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

#if UNITY_EDITOR
using UnityEditor;
#endif

public class ScreenshotUploader : MonoBehaviour
{
    [SerializeField]
    private string uploadUrl = "http://localhost:8000/upload"; // Replace with your MCP server URL

    [SerializeField]
    private string llmUrl = "http://localhost:8000/llm"; // Endpoint of the LLM requesting the screenshot

    [SerializeField]
    private bool autoSendOnStart = false; // If true, capture a screenshot automatically on start

    private void Start()
    {
        if (autoSendOnStart)
        {
            StartCoroutine(CaptureAndUploadViaMcpCoroutine());
        }
    }

    [ContextMenu("Capture & Upload Screenshot")]
    public void CaptureAndUpload()
    {
        StartCoroutine(CaptureAndUploadCoroutine(uploadUrl));
    }

    [ContextMenu("Capture & Send To LLM Directly")]
    public void CaptureAndUploadToLLM()
    {
        StartCoroutine(CaptureAndUploadCoroutine(llmUrl));
    }

    [ContextMenu("Capture & Forward via MCP")]
    public void CaptureAndForwardViaMcp()
    {
        StartCoroutine(CaptureAndUploadViaMcpCoroutine());
    }

    /// <summary>
    /// Capture a screenshot and upload it to the MCP server. The llmUrl is sent
    /// as an additional form field so the server can forward the image to the
    /// requesting LLM.
    /// </summary>
    private IEnumerator CaptureAndUploadViaMcpCoroutine()
    {
        yield return CaptureAndUploadCoroutine(uploadUrl, llmUrl);
    }

    /// <summary>
    /// Capture a screenshot and upload it to the given URL (e.g. your MCP server).
    /// </summary>
    private IEnumerator CaptureAndUploadCoroutine(string targetUrl, string forwardUrl = null)
    {
        // Capture screenshot as texture
        int width = Screen.width;
        int height = Screen.height;
        Texture2D screenshot = new Texture2D(width, height, TextureFormat.RGB24, false);

        yield return new WaitForEndOfFrame();
        screenshot.ReadPixels(new Rect(0, 0, width, height), 0, 0);
        screenshot.Apply();

        byte[] bytes = screenshot.EncodeToPNG();
        Destroy(screenshot);

        // Send screenshot to server
        WWWForm form = new WWWForm();
        form.AddBinaryData("file", bytes, "screenshot.png", "image/png");

        if (!string.IsNullOrEmpty(forwardUrl))
        {
            form.AddField("forward_url", forwardUrl);
        }

        UnityWebRequest www = UnityWebRequest.Post(targetUrl, form);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Upload failed: " + www.error);
        }
        else
        {
            Debug.Log("Upload complete: " + www.downloadHandler.text);
        }
    }
}

#if UNITY_EDITOR
[CustomEditor(typeof(ScreenshotUploader))]
public class ScreenshotUploaderEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        ScreenshotUploader uploader = (ScreenshotUploader)target;
        if (GUILayout.Button("Capture && Upload Screenshot"))
        {
            uploader.CaptureAndUpload();
        }
        if (GUILayout.Button("Capture && Send To LLM Directly"))
        {
            uploader.CaptureAndUploadToLLM();
        }
        if (GUILayout.Button("Capture && Forward via MCP"))
        {
            uploader.CaptureAndForwardViaMcp();
        }
    }
}
#endif
