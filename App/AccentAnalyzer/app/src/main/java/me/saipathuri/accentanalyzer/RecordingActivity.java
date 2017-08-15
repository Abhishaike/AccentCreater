package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.IOException;

public class RecordingActivity extends AppCompatActivity {
    private static final String TAG = "RecordingActivity";
    private Button mRecordButton;
    private Button mPlayButton;
    private Button mNextButton;

    private MediaRecorder mRecorder;
    private MediaPlayer mPlayer;
    private String mFileName;
    private boolean isRecording = false;
    private boolean isPlaying = false;
    private boolean hasRecordedOnce = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recording);

        mRecordButton = (Button) findViewById(R.id.btn_record);
        mPlayButton = (Button) findViewById(R.id.btn_play);
        mNextButton = (Button) findViewById(R.id.btn_recording_next);

        mFileName = getExternalCacheDir().getAbsolutePath();
        mFileName += "/audiorecordtest.3gp";

        mRecordButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isRecording = !isRecording;
                if(isRecording){
                    mRecordButton.setText("Stop recording");
                    Toast.makeText(RecordingActivity.this, "Recording started.", Toast.LENGTH_SHORT).show();
                    hasRecordedOnce = true;
                    startRecording();
                } else{
                    mRecordButton.setText("Start recording");
                    Toast.makeText(RecordingActivity.this, "Recording stopped", Toast.LENGTH_SHORT).show();
                    stopRecording();
                }
            }
        });

        mPlayButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isPlaying = !isPlaying;
                if(isPlaying){
                    mPlayButton.setText("Stop playing");
                    Toast.makeText(RecordingActivity.this, "Playing started.", Toast.LENGTH_SHORT).show();
                    startPlaying();
                } else{
                    mPlayButton.setText("Start playing");
                    Toast.makeText(RecordingActivity.this, "Playing stopped.", Toast.LENGTH_SHORT).show();
                    stopPlaying();
                }
            }
        });

        mNextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(hasRecordedOnce) {
                    Intent startUploadActivityIntent = new Intent(RecordingActivity.this, UploadingActivity.class);
                    startUploadActivityIntent.putExtra(Constants.FILENAME_KEY, mFileName);
                    startActivity(startUploadActivityIntent);
                } else{
                    Toast.makeText(RecordingActivity.this, "Record something first", Toast.LENGTH_SHORT).show();
                }
            }
        });
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

    private void startPlaying() {
        mPlayer = new MediaPlayer();
        try {
            mPlayer.setDataSource(mFileName);
            mPlayer.prepare();
            mPlayer.start();
        } catch (IOException e) {
            Log.e(TAG, "prepare() failed");
        }
    }

    private void stopPlaying() {
        mPlayer.release();
        mPlayer = null;
    }
}
