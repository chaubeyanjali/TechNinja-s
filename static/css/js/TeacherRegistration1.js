function addSubject() {
    const input = document.getElementById('subjectInput');
    const container = document.getElementById('tagContainer');
    const value = input.value.trim();

    if (value !== "") {
        // Prevent duplicates
        const existing = [...document.getElementsByName('subject')]
            .map(i => i.value.toLowerCase());

        if (existing.includes(value.toLowerCase())) {
            alert("Subject already added");
            return;
        }

        const tag = document.createElement('span');
        tag.className = 'tag';
        tag.innerText = value + ' ×';

        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'subject';
        hiddenInput.value = value;

        tag.onclick = () => {
            tag.remove();
            hiddenInput.remove();
        };

        container.appendChild(tag);
        container.appendChild(hiddenInput);

        input.value = "";
    }
}
