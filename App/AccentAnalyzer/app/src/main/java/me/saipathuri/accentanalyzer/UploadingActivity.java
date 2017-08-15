package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ProgressBar;
import android.widget.Toast;

import com.amazonaws.mobile.AWSConfiguration;
import com.amazonaws.mobile.AWSMobileClient;
import com.amazonaws.mobile.content.ContentItem;
import com.amazonaws.mobile.content.ContentProgressListener;
import com.amazonaws.mobile.content.UserFileManager;
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
        AWSMobileClient.defaultMobileClient().createUserFileManager(this,
                AWSConfiguration.AMAZON_S3_USER_FILES_BUCKET,
                "uploads/",
                AWSConfiguration.AMAZON_S3_USER_FILES_BUCKET_REGION,
                new UserFileManager.BuilderResultHandler() {
                    @Override
                    public void onComplete(UserFileManager userFileManager) {
                        final File file = new File(mFileName);
                        userFileManager.uploadContent(file, file.getName(), new ContentProgressListener() {
                            @Override
                            public void onSuccess(ContentItem contentItem) {
                                Log.d(TAG, "filename: " + file.getName());
                                Toast.makeText(UploadingActivity.this, "Upload Completed.", Toast.LENGTH_SHORT).show();
                                postServer(file.getName());
                            }

                            @Override
                            public void onProgressUpdate(String filePath, boolean isWaiting, long bytesCurrent, long bytesTotal) {
                                long divisor = bytesTotal / 100;
                                int progressAmount = (int)(bytesCurrent / divisor);
                                mUploadProgressBar.setMax(100);


                                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
                                    mUploadProgressBar.setProgress(progressAmount, true);
                                } else {
                                    mUploadProgressBar.setProgress(progressAmount);
                                }

                                Log.d(TAG, "completed " + progressAmount + "%");
                            }

                            @Override
                            public void onError(String filePath, Exception ex) {
                                ex.printStackTrace();
                            }
                        });
                    }
                });
    }

    public void postServer(String filename){
        AndroidNetworking.post(Constants.URL)
                .addBodyParameter("s3_filename", filename)
                .setPriority(Priority.IMMEDIATE)
                .build()
                .getAsJSONObject(new JSONObjectRequestListener() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // do anything with response
                        try {
                            String error = response.getString("error");
                            String result = response.getString("result");
                            startResultActivityIntent.putExtra(Constants.ERROR_KEY, error);
                            startResultActivityIntent.putExtra(Constants.RESULTS_KEY, result);

                            Handler handler = new Handler();
                            Runnable startActivityRunnable = new Runnable() {
                                @Override
                                public void run() {
                                    startActivity(startResultActivityIntent);
                                }
                            };
                            handler.postDelayed(startActivityRunnable, 2000);

                            Log.d(TAG, "error: " + error);
                            Log.d(TAG, "result: " + result);
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    @Override
                    public void onError(ANError error) {
                        // handle error
                        error.printStackTrace();
                    }
                });
    }
}
