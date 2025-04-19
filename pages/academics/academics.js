

// switching the content  

function changeTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
    
    document.querySelectorAll('.content-section').forEach(c => c.classList.remove('active'));
    document.getElementById(`content-${tab}`).classList.add('active');
    
    const underline = document.getElementById('underline');
    const activeTab = document.getElementById(tab);
    underline.style.width = `${activeTab.offsetWidth}px`;
    underline.style.left = `${activeTab.offsetLeft}px`;
}

window.onload = function() {
    const activeTab = document.querySelector('.tab.active');
    const underline = document.getElementById('underline');
    underline.style.width = `${activeTab.offsetWidth}px`;
    underline.style.left = `${activeTab.offsetLeft}px`;
};




