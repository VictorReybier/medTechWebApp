const BACKEND_URL = 'https://YOUR_BACKEND_DOMAIN.example.com';
const fileInput = document.getElementById('fileInput');
const submitBtn = document.getElementById('submitBtn');
const statusEl = document.getElementById('status');
const originalImg = document.getElementById('originalImg');
const processedImg = document.getElementById('processedImg');
const viewer = document.getElementById('viewer');

let lastFile = null;

fileInput.addEventListener('change', (e) => {
    const f = e.target.files[0];
    lastFile = f || null;
    if (f) {
        originalImg.src = URL.createObjectURL(f);
        processedImg.src = '';
        viewer.style.display = 'flex';
    } else {
        originalImg.src = '';
        processedImg.src = '';
        viewer.style.display = 'none';
    }
});

submitBtn.addEventListener('click', async () => {
    if (!lastFile) {
        statusEl.textContent = 'Please select an image first.';
        return;
    }

    const phase = document.querySelector('input[name="phase"]:checked').value;
    statusEl.textContent = 'Uploading & processing...';
    submitBtn.disabled = true;

    try {
        const form = new FormData();
        form.append('phase', phase);
        form.append('file', lastFile, lastFile.name);

        const resp = await fetch(`${BACKEND_URL}/process`, {
            method: 'POST',
            body: form,
        });

        if (!resp.ok) {
            const txt = await resp.text();
            throw new Error(`Server error: ${resp.status} ${txt}`);
        }

        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        processedImg.src = url;
        statusEl.textContent = 'Done.';
    } catch (err) {
        console.error(err);
        statusEl.textContent = 'Error: ' + err.message;
    } finally {
        submitBtn.disabled = false;
    }
});