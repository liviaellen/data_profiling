import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import logging
import time
from io import StringIO
import sys
import os
st.set_page_config(layout="wide")

# Function to load data
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.json'):
        return pd.read_json(file)
    else:
        st.error('Unsupported file format')
        return None

# Function to capture logging output
class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ydata_profiling')
log_stream = StringIO()
ch = logging.StreamHandler(log_stream)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def main():
    st.title("Data Profiling - Livia Ellen")
    st.text("This app uses the pandas-profiling library to generate a profile report for your data.")
    url="https://github.com/liviaellen/data-profiling"
    git_url="https://github.com/liviaellen/data-profiling"
    st.write("Created with 💙 by [Livia Ellen](%s)" % url)
    st.write("Find the code [here](%s)" % git_url)


    st.write("**Upload your CSV or JSON file for profiling**")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "json"])
    # st.write("This is a sample of result from the profiling report")
    # # Provide link to open in new tab
    # sample_report_file_name="report.html"
    # st.markdown(f'<a href="{sample_report_file_name}" target="_blank">Open HTML report in new tab</a>', unsafe_allow_html=True)

    # # Show the report in Streamlit
    # sample_report_html=open(sample_report_file_name, "r")
    # st_profile_report(sample_report_html)

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        if data is not None:
            st.write("Here's a preview of your data:")
            st.dataframe(data.head())

            st.write("Generating profiling report...")
            log_output = st.empty()

            # Redirect stdout to logging
            sys.stdout = StreamToLogger(logger, logging.INFO)

            # Extract base name from uploaded file name
            base_name = os.path.splitext(uploaded_file.name)[0]
            report_file_name = f"{base_name}_report.html"

            # Generate profiling report
            try:
                profile = ProfileReport(data, title="Pandas Profiling Report", explorative=True)
                report_html = profile.to_html()
                st.success("Profile report generated successfully!")

                # Save report to a temporary file with dynamic name
                with open(report_file_name, "w") as f:
                    f.write(report_html)

                # Provide download link
                st.download_button(
                    label="Download HTML report",
                    data=report_html,
                    file_name=report_file_name,
                    mime="text/html"
                )

                # Provide link to open in new tab
                st.markdown(f'<a href="{report_file_name}" target="_blank">Open HTML report in new tab</a>', unsafe_allow_html=True)

                # Show the report in Streamlit
                st_profile_report(report_html)

            except Exception as e:
                st.error(f"An error occurred during profiling: {e}")

            # Reset stdout
            sys.stdout = sys.__stdout__

            # Display log output
            log_output.text(log_stream.getvalue())

def st_profile_report(report_html):
    st.components.v1.html(report_html, height=800, scrolling=True)

if __name__ == "__main__":
    main()
