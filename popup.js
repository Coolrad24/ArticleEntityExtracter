document.querySelector("#highlight").addEventListener('click', function() {
    console.log("Pressed");
    chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, { command: 'use' });
    });
  });

  