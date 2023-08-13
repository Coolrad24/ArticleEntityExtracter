function selectArticleContent() {
  // Target the specific HTML elements that usually contain the article content
  const articleElements = document.querySelectorAll('div[class*="article"][class*="content"], span[class*="article"][class*="content"], div[id*="article"][id*="content"], span[id*="article"][id*="content"]');

  let allText = '';

  // Concatenate the text content of each article element
  for (const element of articleElements) {
    allText += element.innerText + '\n';
  }

  // Send the selected article content to the Flask server
  fetch('http://localhost:5000/Siter', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ selectedText: allText }),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Response from server:', data);
    for (const element of articleElements) {
      element.innerHTML = data.highlightedText;
    }
  })
  .catch(error => {
    console.error('Error sending data to server:', error);
  });
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.command === 'use') {
    console.log('Used');
    selectArticleContent();
  }
});
