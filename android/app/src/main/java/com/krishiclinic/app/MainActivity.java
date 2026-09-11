package com.krishiclinic.app;

import android.annotation.SuppressLint;
import android.app.DownloadManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.view.KeyEvent;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.DownloadListener;
import android.webkit.PermissionRequest;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class MainActivity extends AppCompatActivity {

    // ─── CONFIGURE YOUR DEPLOYMENT URL HERE ───────────────────────────────────
    // For production deployment, replace with your Vercel URL:
    private static final String WEB_APP_URL = "https://frontend-woad-mu-58.vercel.app";
    // For local development on same network:
    // private static final String WEB_APP_URL = "http://192.168.x.x:3000";
    // ──────────────────────────────────────────────────────────────────────────

    private WebView webView;
    private ProgressBar progressBar;
    private SwipeRefreshLayout swipeRefreshLayout;
    private View offlineMessage;
    private TextView offlineMessageText;
    private ValueCallback<Uri[]> fileChooserCallback;

    private final ActivityResultLauncher<Intent> fileChooserLauncher =
        registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                Uri[] results = null;
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Uri dataUri = result.getData().getData();
                    if (dataUri != null) {
                        results = new Uri[]{dataUri};
                    }
                }
                if (fileChooserCallback != null) {
                    fileChooserCallback.onReceiveValue(results);
                    fileChooserCallback = null;
                }
            }
        );

    @SuppressLint({"SetJavaScriptEnabled", "ClickableViewAccessibility"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webView);
        progressBar = findViewById(R.id.progressBar);
        swipeRefreshLayout = findViewById(R.id.swipeRefreshLayout);
        offlineMessage = findViewById(R.id.offlineMessage);
        offlineMessageText = findViewById(R.id.offlineMessageText);

        setupWebView();
        setupSwipeRefresh();

        if (savedInstanceState != null) {
            webView.restoreState(savedInstanceState);
        } else {
            webView.loadUrl(WEB_APP_URL);
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private void setupWebView() {
        WebSettings settings = webView.getSettings();

        // Enable JavaScript
        settings.setJavaScriptEnabled(true);

        // Enable DOM storage (for localStorage / SessionStorage)
        settings.setDomStorageEnabled(true);

        // Enable database storage
        settings.setDatabaseEnabled(true);

        // Allow mixed content for local dev
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        // Enable file access for camera / file picker
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);

        // Modern media
        settings.setMediaPlaybackRequiresUserGesture(false);

        // Cache settings
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        // Zoom
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);

        // Viewport
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        // User agent — include KrishiClinicApp for server-side detection
        settings.setUserAgentString(
            settings.getUserAgentString() + " KrishiClinicAndroid/1.0"
        );

        // Cookie support
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, true);

        // WebViewClient — handles navigation
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                // Allow all KrishiClinic URLs inside the app
                if (url.startsWith("https://krishiclinic") ||
                    url.startsWith("http://192.168") ||
                    url.startsWith("http://10.") ||
                    url.startsWith("http://localhost") ||
                    url.startsWith(WEB_APP_URL)) {
                    return false;
                }
                // Open external URLs in system browser
                startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
                return true;
            }

            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                progressBar.setVisibility(View.VISIBLE);
                offlineMessage.setVisibility(View.GONE);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                progressBar.setVisibility(View.GONE);
                swipeRefreshLayout.setRefreshing(false);

                // Inject mobile CSS overrides for PWA feel
                webView.evaluateJavascript(
                    "document.documentElement.style.setProperty('--app-source', '\"android-webview\"');",
                    null
                );
            }

            @Override
            public void onReceivedError(android.webkit.WebView view,
                                         int errorCode, String description, String failingUrl) {
                progressBar.setVisibility(View.GONE);
                swipeRefreshLayout.setRefreshing(false);
                offlineMessage.setVisibility(View.VISIBLE);
                if (offlineMessageText != null) {
                    offlineMessageText.setText("⚠️ Cannot connect to KrishiClinic.\nPlease check your internet connection.\n\n" + description);
                }
            }
        });

        // WebChromeClient — handles file chooser, permissions, progress
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                progressBar.setProgress(newProgress);
                if (newProgress == 100) {
                    progressBar.setVisibility(View.GONE);
                }
            }

            // Camera / microphone permissions
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                request.grant(request.getResources());
            }

            // File chooser for crop image upload
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> callback,
                                              FileChooserParams params) {
                if (fileChooserCallback != null) {
                    fileChooserCallback.onReceiveValue(null);
                }
                fileChooserCallback = callback;

                Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("image/*");

                fileChooserLauncher.launch(intent);
                return true;
            }
        });

        // Download listener
        webView.setDownloadListener(new DownloadListener() {
            @Override
            public void onDownloadStart(String url, String userAgent, String contentDisposition,
                                         String mimeType, long contentLength) {
                DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
                request.setMimeType(mimeType);
                request.addRequestHeader("User-Agent", userAgent);
                request.setDescription("KrishiClinic AI download");
                request.setTitle(Uri.fromFile(new java.io.File(url)).getLastPathSegment());
                request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, "");
                DownloadManager dm = (DownloadManager) getSystemService(Context.DOWNLOAD_SERVICE);
                dm.enqueue(request);
                Toast.makeText(getApplicationContext(), "Downloading file...", Toast.LENGTH_LONG).show();
            }
        });
    }

    private void setupSwipeRefresh() {
        swipeRefreshLayout.setColorSchemeResources(
            android.R.color.holo_green_dark,
            android.R.color.holo_green_light
        );
        swipeRefreshLayout.setOnRefreshListener(() -> {
            offlineMessage.setVisibility(View.GONE);
            webView.reload();
        });
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            if (webView.canGoBack()) {
                webView.goBack();
                return true;
            }
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        webView.saveState(outState);
    }

    @Override
    protected void onResume() {
        super.onResume();
        webView.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        webView.onPause();
    }

    @Override
    protected void onDestroy() {
        webView.destroy();
        super.onDestroy();
    }
}
