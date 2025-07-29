import streamlit as st
import openai
import numpy as np
import matplotlib.pyplot as plt

def simulate_elevation_profile(miles, total_gain):
    x = np.linspace(0, miles, 100)
    elevation = 50 * np.sin(2 * np.pi * x / miles) + np.random.normal(0, 10, 100)
    elevation = elevation - min(elevation)
    elevation = elevation / sum(np.diff(np.clip(elevation, a_min=0, a_max=None))) * total_gain
    elevation = np.cumsum(elevation)
    return x, elevation

# Initialize OpenAI client using new SDK format 
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page Title 
st.title("🏁 Race Day Strategy Generator")
st.write("Get your personalized pacing, fueling, and mental strategy plan.")

# User Inputs
race_distance = st.selectbox("Select your race distance:", ["5K", "10K", "Half Marathon", "Marathon"])
goal_time = st.text_input("Enter your goal finish time (hh:mm:ss):")
elevation_gain = st.number_input("Optional: Enter total elevation gain (in feet)", min_value=0, step=10)
course_notes = st.text_area("Optional: Any notes about the course?")
long_run_pace = st.text_input("Recent long run pace (e.g. 9:10 per mile, optional):")
training_status = st.selectbox("How’s your training been?", ["On track", "Missed a few weeks", "Coming back from injury"])

# Generate Button
if st.button("Generate My Strategy"):
    with st.spinner("Generating strategy..."):
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

        # Try GPT separately
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
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
            # Show simulated elevation profile if total gain provided
            if elevation_gain > 0:
                try:
                    # Estimate race distance in miles
                    distance_map = {
                        "5K": 3.1,
                        "10K": 6.2,
                        "Half Marathon": 13.1,
                        "Marathon": 26.2
                    }
                    miles = distance_map[race_distance]
                    x, y = simulate_elevation_profile(miles, elevation_gain)
                    fig, ax = plt.subplots()
                    ax.plot(x, y, color='red')
                    ax.set_title("Simulated Elevation Profile")
                    ax.set_xlabel("Miles")
                    ax.set_ylabel("Elevation (ft)")
                    st.pyplot(fig)
                except Exception as e:
                    st.warning(f"Could not render elevation profile: {e}")
        except Exception as e:
            st.error(f"Something went wrong with the AI response: {e}")
