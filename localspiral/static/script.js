// Simple frontend logic for the demo UI
function fetchJson(url) {
    return fetch(url).then((res) => {
        if (!res.ok) throw new Error('Request failed');
        return res.json();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt');
    const sendButton = document.getElementById('sendButton');
    const responseDiv = document.getElementById('response');
    const spiralButton = document.getElementById('spiralButton');
    const mapButton = document.getElementById('mapButton');
    const extraOutput = document.getElementById('extra-output');

    sendButton.addEventListener('click', () => {
        const prompt = promptInput.value.trim();
        if (!prompt) return;
        responseDiv.textContent = 'Loading...';
        fetchJson(`/chat?prompt=${encodeURIComponent(prompt)}`)
            .then((data) => {
                responseDiv.textContent = data.message || data.error || 'No response';
            })
            .catch(() => {
                responseDiv.textContent = 'Request failed.';
            });
    });

    if (spiralButton) {
        spiralButton.addEventListener('click', () => {
            extraOutput.textContent = 'Loading...';
            fetchJson('/spiral')
                .then((data) => {
                    extraOutput.textContent = JSON.stringify(data, null, 2);
                })
                .catch(() => {
                    extraOutput.textContent = 'Request failed.';
                });
        });
    }

    if (mapButton) {
        mapButton.addEventListener('click', () => {
            extraOutput.textContent = 'Loading...';
            fetchJson('/map')
                .then((data) => {
                    extraOutput.textContent = JSON.stringify(data, null, 2);
                })
                .catch(() => {
                    extraOutput.textContent = 'Request failed.';
                });
        });
    }
});
