document.getElementById('chatbot-button').addEventListener('click', function () {
  const chatbotContainer = document.getElementById('chatbot-container');
  const openIcon = document.getElementById('chatbot-open-icon');
  const closeIcon = document.getElementById('chatbot-close-icon');
  const tempDiv = document.getElementById('temp');

  // Toggle chatbot visibility
  if (chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '') {
      chatbotContainer.style.display = 'block';  
      openIcon.style.display = 'none';  
      closeIcon.style.display = 'block';  
      tempDiv.style.display = 'flex'; 
  } else {
      chatbotContainer.style.display = 'none'; 
      openIcon.style.display = 'block';  
      closeIcon.style.display = 'none';  
      tempDiv.style.display = 'none'; 
  }
});