package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import org.w3c.dom.Text;

public class ResultActivity extends AppCompatActivity {
    private String mResult;
    private String mError;

    private TextView mResultTextView;
    private TextView mErrorTextView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        Intent intentThatStartedThisActivty = getIntent();

        mResult = intentThatStartedThisActivty.getStringExtra(Constants.RESULTS_KEY);
        mError = intentThatStartedThisActivty.getStringExtra(Constants.ERROR_KEY);

        mResultTextView = (TextView) findViewById(R.id.tv_result_result);
        mErrorTextView = (TextView) findViewById(R.id.tv_result_error);

        mResultTextView.setText(mResult);
        mErrorTextView.setText(mError);
    }
}
