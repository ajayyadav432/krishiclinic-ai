package com.krishiclinic.app;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class SplashActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        ImageView logoView = findViewById(R.id.splash_logo);
        TextView taglineView = findViewById(R.id.splash_tagline);

        // Fade-in animation
        AlphaAnimation fadeIn = new AlphaAnimation(0f, 1f);
        fadeIn.setDuration(700);
        logoView.startAnimation(fadeIn);

        AlphaAnimation fadeInDelay = new AlphaAnimation(0f, 1f);
        fadeInDelay.setDuration(500);
        fadeInDelay.setStartOffset(400);
        taglineView.startAnimation(fadeInDelay);

        // Navigate to MainActivity after 2 seconds
        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            startActivity(new Intent(SplashActivity.this, MainActivity.class));
            finish();
        }, 2000);
    }
}
