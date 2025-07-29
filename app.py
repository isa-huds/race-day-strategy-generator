import streamlit as st
import openai

# Initialize OpenAI client using new SDK format 
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page Title 
st.title("🏁 Race Day Strategy Generator")
st.write("Get your personalized pacing, fueling, and mental strategy plan.")

# User Inputs
race_distance = st.selectbox("Select your race distance:", ["5K", "10K", "Half Marathon", "Marathon"])
goal_time = st.text_input("Enter your goal finish time (hh:mm:ss):")
course_notes = st.text_area("Any notes about the course? (Optional)")
long_run_pace = st.text_input("Recent long run pace (e.g. 9:10 per mile, optional):")
training_status = st.selectbox("How’s your training been?", ["On track", "Missed a few weeks", "Coming back from injury"])

# Generate Button
if st.button("Generate My Strategy"):
    with st.spinner("Generating strategy..."):
        # Format prompt
        prompt = f"""
You're a running coach. Help me prepare for my upcoming {race_distance}.

Goal finish time: {goal_time}
Course details: {course_notes or 'N/A'}
Recent long run pace: {long_run_pace or 'N/A'}
Training status: {training_status}

Give me:
1. A pacing plan (mile-by-mile if long race, or per kilometer if short)
2. Fueling advice (gels, water, electrolytes)
3. Mental strategy for key race moments
4. Optional race week preparation tips
"""

        # Call GPT using new SDK
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an experienced running coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            output = response.choices[0].message.content
            st.success("Done!")
            st.markdown(output)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
