const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const convertBtn = document.getElementById('convertBtn');
const btnText = document.getElementById('btnText');
const loader = document.getElementById('loader');
const audioContainer = document.getElementById('audioContainer');
const audioPlayer = document.getElementById('audioPlayer');
const downloadLink = document.getElementById('downloadLink');

// Update character count
textInput.addEventListener('input', () => {
    charCount.textContent = textInput.value.length;
});

async function convertText() {
    const text = textInput.value.trim();
    const language = document.getElementById('languageSelect').value;

    if (!text) {
        alert("Please enter some text first.");
        return;
    }

    // UI Loading State
    setLoading(true);
    audioContainer.classList.add('hidden');

    try {
        const response = await fetch('/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, language }),
        });

        const data = await response.json();

        if (data.success) {
            // Update Audio Player
            audioPlayer.src = data.audio_url;
            downloadLink.href = data.audio_url;
            downloadLink.download = `voice_${data.filename}`;
            
            audioContainer.classList.remove('hidden');
            audioPlayer.play();
        } else {
            alert("Error: " + data.error);
        }

    } catch (error) {
        console.error('Error:', error);
        alert("Something went wrong. Please try again.");
    } finally {
        setLoading(false);
    }
}

function setLoading(isLoading) {
    convertBtn.disabled = isLoading;
    if (isLoading) {
        btnText.style.display = 'none';
        loader.style.display = 'block';
    } else {
        btnText.style.display = 'block';
        loader.style.display = 'none';
    }
}