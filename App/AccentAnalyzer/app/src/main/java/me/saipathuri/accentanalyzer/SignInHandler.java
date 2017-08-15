package me.saipathuri.accentanalyzer;
//
// Copyright 2017 Amazon.com, Inc. or its affiliates (Amazon). All Rights Reserved.
//
// Code generated by AWS Mobile Hub. Amazon gives unlimited permission to 
// copy, distribute and modify it.
//
// Source code generated from template: aws-my-sample-app-android v0.18
//

import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

import com.amazonaws.mobilehelper.auth.DefaultSignInResultHandler;
import com.amazonaws.mobilehelper.auth.IdentityProvider;

/**
 * Handles Re-directing to the main activity upon sign-in.
 */
public class SignInHandler extends DefaultSignInResultHandler {
    private static final String LOG_TAG = SignInHandler.class.getSimpleName();

    @Override
    public void onSuccess(final Activity callingActivity, final IdentityProvider provider) {
        if (provider != null) {
            Log.d(LOG_TAG, String.format("User sign-in with %s provider succeeded",
                provider.getDisplayName()));
            Toast.makeText(callingActivity, String.format(
                callingActivity.getString(R.string.sign_in_succeeded_message_format),
                provider.getDisplayName()), Toast.LENGTH_LONG).show();
        }

        goMain(callingActivity);
    }

    @Override
    public boolean onCancel(final Activity callingActivity) {
        // User abandoned sign in flow.
        final boolean shouldFinishSignInActivity = false;
        return shouldFinishSignInActivity;
    }

    /** Go to the main activity. */
    private void goMain(final Activity callingActivity) {
        callingActivity.startActivity(new Intent(callingActivity, MainActivity.class)
            .setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP));
    }
}
