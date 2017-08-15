package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ProgressBar;
import android.widget.Toast;

import com.androidnetworking.AndroidNetworking;
import com.androidnetworking.common.Priority;
import com.androidnetworking.error.ANError;
import com.androidnetworking.interfaces.JSONObjectRequestListener;
import com.androidnetworking.interfaces.UploadProgressListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;

public class UploadingActivity extends AppCompatActivity {

    private static final String TAG = "UploadingActivity";
    private ProgressBar mUploadProgressBar;
    private String mFileName;
    private Intent startResultActivityIntent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_uploading);

        mUploadProgressBar = (ProgressBar) findViewById(R.id.pb_upload);

        Intent intentThatStartedThisActivity = getIntent();
        mFileName = intentThatStartedThisActivity.getStringExtra(Constants.FILENAME_KEY);

        startResultActivityIntent = new Intent(this, ResultActivity.class);

        AndroidNetworking.initialize(getApplicationContext());
        upload();
    }

    private void upload(){
        File file = new File(mFileName);
        AndroidNetworking.upload(Constants.URL)
                .addMultipartFile("file",file)
                .setTag("uploadTest")
                .setPriority(Priority.IMMEDIATE)
                .build()
                .setUploadProgressListener(new UploadProgressListener() {
                    @Override
                    public void onProgress(long bytesUploaded, long totalBytes) {
                        // do anything with progress
                        long divisor = totalBytes / 100;
                        int progressAmount = (int)(bytesUploaded / divisor);
                        mUploadProgressBar.setMax(100);


                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                            mUploadProgressBar.setProgress(progressAmount, true);
                        } else {
                            mUploadProgressBar.setProgress(progressAmount);
                        }

                        Log.d(TAG, "completed " + progressAmount + "%");

                        if(progressAmount == 100){
                            Toast.makeText(UploadingActivity.this, "Upload Completed.", Toast.LENGTH_SHORT).show();
                            Handler handler = new Handler();
                            Runnable startActivityRunnable = new Runnable() {
                                @Override
                                public void run() {
                                    startActivity(startResultActivityIntent);
                                }
                            };
                            handler.postDelayed(startActivityRunnable, 2000);
                        }
                    }
                })
                .getAsJSONObject(new JSONObjectRequestListener() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // do anything with response
                        try {
                            String error = response.getString("error");
                            String result = response.getString("result");
                            startResultActivityIntent.putExtra(Constants.ERROR_KEY, error);
                            startResultActivityIntent.putExtra(Constants.RESULTS_KEY, result);

                            Log.d(TAG, "error: " + error);
                            Log.d(TAG, "result: " + result);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    @Override
                    public void onError(ANError error) {
                        // handle error
                        Log.e(TAG, error.toString());
                    }
                });
    }
}
