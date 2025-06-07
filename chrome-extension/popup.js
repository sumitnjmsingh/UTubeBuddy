document.getElementById('ask').addEventListener('click', async () => {
  const question = document.getElementById('question').value;

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = new URL(tab.url);
  const videoId = url.searchParams.get("v"); 

  if (!videoId) {
    document.getElementById('answer').textContent = "Not a YouTube video!";
    return;
  }

  const apiUrl = `http://127.0.0.1:8000/ask?video_id=${videoId}&question=${encodeURIComponent(question)}`;

  const response = await fetch(apiUrl);
  const data = await response.json();
  document.getElementById('answer').textContent = data.answer;
});

document.getElementById("toggle-theme").addEventListener("click", () => {
  document.body.classList.toggle("dark-theme");
});
