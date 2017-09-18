package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

import com.amazonaws.mobile.AWSMobileClient;
import com.amazonaws.mobilehelper.auth.IdentityHandler;

import java.io.IOException;

public class RecordingActivity extends AppCompatActivity {
    private static final String TAG = "RecordingActivity";
    private Button mRecordButton;
    private Button mPlayButton;
    private Button mNextButton;
    private Spinner mLanguageSelectSpinner;

    private MediaRecorder mRecorder;
    private MediaPlayer mPlayer;
    private String mFileName;
    private boolean isRecording = false;
    private boolean isPlaying = false;
    private boolean hasRecordedOnce = false;
    private boolean hasFinishedOnce = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recording);

        mRecordButton = (Button) findViewById(R.id.btn_record);
        mPlayButton = (Button) findViewById(R.id.btn_play);

        // set play button to be disabled until recording is completed
        mPlayButton.setEnabled(false);

        mNextButton = (Button) findViewById(R.id.btn_recording_next);


        mLanguageSelectSpinner = (Spinner) findViewById(R.id.spinner_language_select);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.languages_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        mLanguageSelectSpinner.setAdapter(adapter);

        setFileName();

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
                    if(hasRecordedOnce) {
                        hasFinishedOnce = true;
                        mPlayButton.setEnabled(true);
                    }
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
                if(hasRecordedOnce && hasFinishedOnce) {
                    Intent startUploadActivityIntent = new Intent(RecordingActivity.this, UploadingActivity.class);
                    startUploadActivityIntent.putExtra(Constants.FILENAME_KEY, mFileName);
                    Log.d(TAG, "selected language: " + String.valueOf(mLanguageSelectSpinner.getSelectedItem()));
                    startUploadActivityIntent.putExtra(Constants.SELECTED_LANGUAGE_KEY, String.valueOf(mLanguageSelectSpinner.getSelectedItem()));
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
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_WB);
        mRecorder.setAudioEncodingBitRate(96000);
        mRecorder.setAudioSamplingRate(44100);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4);
        mRecorder.setOutputFile(mFileName);

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

    // set the saved file name as the cognito id
    private void setFileName(){
        AWSMobileClient.defaultMobileClient()
                .getIdentityManager()
                .getUserID(new IdentityHandler() {

                    @Override
                    public void onIdentityId(String identityId) {
                        Log.d(TAG, "identity: " + identityId);
                        mFileName = getExternalCacheDir().getAbsolutePath();
                        mFileName += "/"+ identityId +".mp4";
                    }

                    @Override
                    public void handleError(Exception exception) {

                        // We failed to retrieve the user's identity. Set unknown user identifier
                        // in text view. Perhaps there was no network access available.

                        // ... add error handling logic here ...
                        exception.printStackTrace();
                    }
                });
    }
}
