// Custom number input controls
const numberInput = document.getElementById('verseCount');
const incrementBtn = document.querySelector('.increment-btn');
const decrementBtn = document.querySelector('.decrement-btn');

incrementBtn.addEventListener('click', function () {
    const currentValue = parseInt(numberInput.value) || 0;
    const max = parseInt(numberInput.max);
    if (currentValue < max) {
        numberInput.value = currentValue + 1;
    }
});

decrementBtn.addEventListener('click', function () {
    const currentValue = parseInt(numberInput.value) || 0;
    const min = parseInt(numberInput.min);
    if (currentValue > min) {
        numberInput.value = currentValue - 1;
    }
});

// Main button functionality
document.getElementById('generateBtn').addEventListener('click', function () {
    const verseCount = parseInt(numberInput.value);

    if (!verseCount || verseCount < 1) {
        alert('Please enter a valid number of verses.');
        return;
    }

    // Show loading state
    const resultArea = document.getElementById('resultArea');
    resultArea.classList.remove('active');
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('generateBtn').textContent = 'Finding...';

    fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({ verseCount: verseCount })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);

            // Format the sequence
            let sequence = "";
            if (Array.isArray(data) && data.length > 0) {
                data.forEach((chapter, index) => {
                    sequence += chapter;
                    if (index < data.length - 1) {
                        sequence += ", ";
                    }
                });
            } else {
                sequence = "No chapters found";
            }

            // Display the result
            setTimeout(() => {
                resultArea.classList.add('active');
                document.getElementById('chapterList').innerHTML = `<p>${sequence}</p>`;
                document.getElementById('generateBtn').disabled = false;
                document.getElementById('generateBtn').textContent = 'Find Chapters';
            }, 100);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('chapterList').innerHTML =
                `<p style="color: #ffcccc;">Error: Could not fetch chapter data. Please try again later.</p>`;
            resultArea.classList.add('active');
            document.getElementById('generateBtn').disabled = false;
            document.getElementById('generateBtn').textContent = 'Find Chapters';
        });
});