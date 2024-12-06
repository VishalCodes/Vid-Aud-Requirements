import os
#from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Load environment variables from .env file
#load_dotenv()

# Set your OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]


sys_prompt = """
<Inputs>
<TRANSCRIPT>
</Inputs>

<Instructions Structure>
1. Introduce the task of generating detailed user requirements from a project discussion transcript using natural language processing techniques.
2. Provide guidance on analyzing the transcript for extracting essential project details.
3. Specify the format and structure for presenting the requirements, including objectives, deliverables, tools, and timelines.
4. Emphasize the importance of precision and accuracy, correcting any contextually relevant errors.
5. Instruct to exclude irrelevant information and provide the output in a point-wise format.
6. Conclude with instructions to present the final output in plain text format.
</Instructions Structure>

<Instructions>
You are tasked with generating a detailed description of user requirements for a system using natural language processing methodologies by analyzing the transcript of a project discussion. Your goal is to ensure high precision and accuracy while extracting essential project details. Follow these instructions:

1. Begin by reviewing the entire transcript provided within the <TRANSCRIPT> tags. Pay close attention to the context and content of the discussion.

2. Analyze the transcript to identify and extract all essential details related to the project's specifications. This includes:
   - Project objectives: What the project aims to achieve.
   - Deliverables: What will be produced or delivered at the end of the project.
   - Tools required: Any specific tools or technologies mentioned as necessary for the project.
   - Timelines: The number of days or deadlines related to the project timeline.

3. Ensure that the extracted information is contextually accurate and relevant. Correct any contextual errors to ensure clarity and precision.

4. Exclude any irrelevant or extraneous information that does not contribute to the understanding of the project's requirements.

5. Organize the extracted information in a point-wise format, similar to what a Business Requirements Document (BRD) would look like from a Business Analyst or Product Owner perspective. This format should be concise and structured to facilitate easy understanding.

6. Present the final output in plain text format, ensuring it is well-organized and free from any formatting errors.

By following these steps, you will generate a comprehensive and accurate set of user requirements from the project discussion transcript.
</Instructions>
"""
# Function to transcribe audio and generate requirements
def process_audio(audio_file):
    # Audio transcription
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )

    # Generate requirements
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt + transcription}
        ],
        temperature=0,
    )

    response_message = response.choices[0].message.content
    st.write("Generated Requirements:")
    st.write(response_message)

    # Create output directory if it doesn't exist
    output_dir = "Output"
    os.makedirs(output_dir, exist_ok=True)

    # Save the output to a text file with the same name as the input file
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(audio_file.name)[0]}.txt")
    with open(output_file_path, "w") as f:
        f.write(response_message)  # Write the response to the file

# Streamlit app
def main():
    st.title("Audio/Video to Business Requirements Generator")

    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

    if uploaded_file is not None:
        # Generate button
        if st.button("Generate"):
            # Process audio and generate requirements
            process_audio(uploaded_file)

if __name__ == "__main__":
    main()
