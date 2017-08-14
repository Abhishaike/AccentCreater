package me.saipathuri.accentanalyzer;

import android.Manifest;
import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private Button mRecordButton;
    private Button mUploadButton;
    private MediaRecorder mRecorder;
    private String mFileName;
    private boolean isRecording = false;

    // Requesting permission to RECORD_AUDIO
    private boolean permissionToRecordAccepted = false;
    private boolean permissionForInternetAccepted = false;
    private String [] audioPermission = {Manifest.permission.RECORD_AUDIO};
    private String [] internetPermission = {Manifest.permission.INTERNET};
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private static final int REQUEST_INTERNET_PERMISSION = 201;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mRecordButton = (Button) findViewById(R.id.btn_record);
        mUploadButton = (Button) findViewById(R.id.btn_upload);

        mFileName = getExternalCacheDir().getAbsolutePath();
        mFileName += "/audiorecordtest.3gp";

        ActivityCompat.requestPermissions(this, audioPermission, REQUEST_RECORD_AUDIO_PERMISSION);
        ActivityCompat.requestPermissions(this, audioPermission, REQUEST_INTERNET_PERMISSION);

        mRecordButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isRecording = !isRecording;
                if(isRecording){
                    mRecordButton.setText("Stop recording");
                    Toast.makeText(MainActivity.this, "Recording started.", Toast.LENGTH_SHORT).show();
                    startRecording();
                } else{
                    mRecordButton.setText("Start recording");
                    Toast.makeText(MainActivity.this, "Recording stopped", Toast.LENGTH_SHORT).show();
                    stopRecording();
                }
            }
        });

        mUploadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(MainActivity.this, "To be implemented", Toast.LENGTH_SHORT).show();
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode){
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted  = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                break;
            case REQUEST_INTERNET_PERMISSION:
                permissionForInternetAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                break;
        }
        if (!permissionToRecordAccepted ) finish();
        if (!permissionForInternetAccepted) finish();
    }

    private void startRecording() {
        mRecorder = new MediaRecorder();
        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        mRecorder.setOutputFile(mFileName);
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            mRecorder.prepare();
        } catch (IOException e) {
            Log.e(TAG, "prepare() failed");
        }

        mRecorder.start();
    }

    private void stopRecording() {
        mRecorder.stop();
        mRecorder.release();
        mRecorder = null;
    }
}
