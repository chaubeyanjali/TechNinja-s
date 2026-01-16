function addSubject() {
    const input = document.getElementById('subjectInput');
    const container = document.getElementById('tagContainer');
    const value = input.value.trim();

    if (value !== "") {
        const newTag = document.createElement('span');
        newTag.className = 'tag';
        newTag.innerText = '+ ' + value;
        
        // Tag click to remove functionality
        newTag.onclick = function() {
            this.remove();
        };

        container.appendChild(newTag);
        input.value = ""; // Clear input
    }
}

// Allow Enter key to add subject
document.getElementById('subjectInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        addSubject();
    }
});