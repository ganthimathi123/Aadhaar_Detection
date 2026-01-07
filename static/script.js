const dropArea = document.getElementById("dropArea");
const fileInput = document.getElementById("fileInput");
const resultDiv = document.getElementById("result");

function uploadImage(file) {
    const formData = new FormData();
    formData.append("image", file);

    resultDiv.innerHTML = `<span style="color:#f1c40f;">⏳ Verifying Aadhaar...</span>`;

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = `<span style="color:red;">❌ ${data.error}</span>`;
            return;
        }

        let color = "#e74c3c";
        let icon = "❌";

        if (data.final_verdict.includes("REAL") || data.final_verdict.includes("AUTHENTIC")) {
            color = "#2ecc71";
            icon = "✅";
        }

        resultDiv.innerHTML = `
            <div class="result" style="border-color:${color};color:${color}">
                ${icon} <b>${data.final_verdict}</b><br>
                Confidence: ${data.confidence}%<br>
                <small>${data.reason}</small>
            </div>
        `;
    })
    .catch(() => {
        resultDiv.innerHTML = `<span style="color:red;">❌ Error processing image</span>`;
    });
}

// Drag & Drop
dropArea.addEventListener("drop", e => {
    e.preventDefault();
    uploadImage(e.dataTransfer.files[0]);
});

fileInput.addEventListener("change", () => {
    uploadImage(fileInput.files[0]);
});
