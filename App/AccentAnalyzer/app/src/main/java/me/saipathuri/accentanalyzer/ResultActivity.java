package me.saipathuri.accentanalyzer;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import org.w3c.dom.Text;

public class ResultActivity extends AppCompatActivity {
    private String mResult;
    private String mError;
    private String mSelectedLanguage;

    private TextView mResultTextView;
    private TextView mErrorTextView;
    private TextView mLanguageTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result);

        Intent intentThatStartedThisActivty = getIntent();

        mResult = intentThatStartedThisActivty.getStringExtra(Constants.RESULTS_KEY);
        mError = intentThatStartedThisActivty.getStringExtra(Constants.ERROR_KEY);
        mSelectedLanguage = intentThatStartedThisActivty.getStringExtra(Constants.SELECTED_LANGUAGE_KEY);

        mResultTextView = (TextView) findViewById(R.id.tv_result_result);
        mErrorTextView = (TextView) findViewById(R.id.tv_result_error);
        mLanguageTextView = (TextView) findViewById(R.id.tv_result_language);

        mResultTextView.setText(mResult);
        mErrorTextView.setText(mError);
        mLanguageTextView.setText(mSelectedLanguage);

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
