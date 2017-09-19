package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.w3c.dom.Text;

public class ResultActivity extends AppCompatActivity {
    private String mResult;
    private String mError;

    private TextView mResultTextView;
    private TextView mErrorTextView;
    private Button mStartOverButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        final Intent intentThatStartedThisActivty = getIntent();

        mResult = intentThatStartedThisActivty.getStringExtra(Constants.RESULTS_KEY);
        mError = intentThatStartedThisActivty.getStringExtra(Constants.ERROR_KEY);

        mResultTextView = (TextView) findViewById(R.id.tv_result_result);
        mErrorTextView = (TextView) findViewById(R.id.tv_result_error);
        mStartOverButton = (Button) findViewById(R.id.btn_start_over);
        mStartOverButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentToStartMainActivity = new Intent(ResultActivity.this, MainActivity.class);
                startActivity(intentThatStartedThisActivty);
            }
        });

        mResultTextView.setText(mResult);
        mErrorTextView.setText(mError);

        if(!mError.equals("none")){
            showError();
        }
    }

    private void showError() {
        TextView ErrorTitle = (TextView) findViewById(R.id.tv_result_error_title);
        ErrorTitle.setVisibility(View.VISIBLE);
        mErrorTextView.setVisibility(View.VISIBLE);
    }
}
