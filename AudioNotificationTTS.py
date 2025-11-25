import pyttsx3

# Initialize the speech engine
engine = pyttsx3.init()

# Set properties (optional)
# You can change voice, rate, and volume
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # Change to a different voice
engine.setProperty('rate', 172) # Adjust speech rate

# Convert text to speech
engine.say("Kindly re configure the product");

# Play the speech and wait for it to finish
engine.runAndWait()

# Stop the engine (optional)
engine.stop()
