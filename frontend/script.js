// frontend/script.js
async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const status = document.getElementById("status");
  
    if (!fileInput.files.length) {
      alert("Please select a PDF file.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
  
    status.innerText = "Uploading and processing...";
  
    try {
      const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData
      });
  
      if (!response.ok) throw new Error("Server returned error");
  
      const result = await response.json();
      status.innerText = "Graph generated!";
      document.getElementById("graphContainer").style.display = "block";
    } catch (err) {
      console.error(err);
      status.innerText = "Something went wrong: Failed to fetch.";
    }
  }
  