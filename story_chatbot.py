import streamlit as st
import cohere

# Initialize Cohere client
API_KEY = "NoHiP3iOS1uK5uRYHlAl6QleVUoMZK02B4mq2aTV"  # Replace with your actual key if necessary
co = cohere.Client(API_KEY)

# Streamlit app interface
st.title("Story Generator Bot")
st.markdown("### Create your own story in three simple steps:")

# Step 1: Add Character Names
if "characters" not in st.session_state:
    st.session_state.characters = []

st.header("Step 1: Add Characters")
character_input = st.text_input("Enter a character name:")
if st.button("Add Character"):
    if character_input.strip():
        st.session_state.characters.append(character_input.strip())
        st.success(f"Character '{character_input.strip()}' added!")
    else:
        st.error("Please enter a valid character name.")

if st.session_state.characters:
    st.write("**Characters Added:**")
    st.write(", ".join(st.session_state.characters))

# Step 2: Enter Story Idea
if st.session_state.characters:
    st.header("Step 2: Enter a Story Idea")
    story_idea = st.text_area("What’s your story idea? (Be as creative or specific as you'd like)")

    # Step 3: Generate the Story
    if story_idea and st.button("Generate Story"):
        with st.spinner("Generating your story..."):
            prompt = (
                f"Characters: {', '.join(st.session_state.characters)}\n"
                f"Story Idea: {story_idea}\n\n"
                "Write a detailed and engaging story based on the above characters and idea:"
            )
            try:
                # Maximum token usage
                response = co.generate(
                    model="command-xlarge",
                    prompt=prompt,
                    max_tokens=200000,  # Maximum allowed tokens for the response
                    temperature=0.9,  # Adjust for more/less creativity
                    stop_sequences=["--End--"]
                )
                story = response.generations[0].text.strip()
                st.success("Here’s your generated story:")
                st.text_area("Generated Story", story, height=400)
            except Exception as e:
                st.error(f"An error occurred while generating the story: {e}")
else:
    st.info("Please add at least one character to proceed.")

# Step 4: Reset Characters
if st.button("Reset Characters"):
    st.session_state.characters = []
    st.success("All characters have been removed!")
