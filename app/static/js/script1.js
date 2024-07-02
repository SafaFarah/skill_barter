function addSkill(selectId) {
    var selectElement = document.getElementById(selectId);
    var selectedSkill = selectElement.options[selectElement.selectedIndex].value;

    if (selectedSkill !== "-- Select a skill --") {
        var containerId = selectId + "_container";
        var containerElement = document.getElementById(containerId);
        var hiddenInput = document.getElementById(selectId + "_hidden");

        // Check if skill already added
        if (!hiddenInput.value.includes(selectedSkill)) {
            // Create a new div for the skill
            var skillDiv = document.createElement('div');
            skillDiv.textContent = selectedSkill;
            skillDiv.className = 'skill-item';

            // Add a remove button
            var removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.className = 'remove-skill-button';
            removeButton.onclick = function() {
                containerElement.removeChild(skillDiv);
                hiddenInput.value = hiddenInput.value.replace(selectedSkill + ',', '');
            };
            skillDiv.appendChild(removeButton);

            // Append the new skill to the list
            containerElement.appendChild(skillDiv);

            // Update the hidden input value
            hiddenInput.value += selectedSkill + ',';
        }
    }
}

function removeSkill(containerId, skill) {
    var containerElement = document.getElementById(containerId + "_container");
    var hiddenInput = document.getElementById(containerId + "_hidden");

    // Remove skill from display
    var skillElements = containerElement.getElementsByClassName('skill-item');
    for (var i = 0; i < skillElements.length; i++) {
        if (skillElements[i].textContent.trim() === skill) {
            containerElement.removeChild(skillElements[i]);
            break;
        }
    }

    // Update hidden input value
    hiddenInput.value = hiddenInput.value.replace(skill + ',', '');
}

window.onload = function() {
    var skillsIHave = "{{ user_skills_i_have|join(',') }}".split(',');
    var skillsIWant = "{{ user_skills_i_want|join(',') }}".split(',');

    initializeSkillList('skills_i_have', skillsIHave);
    initializeSkillList('skills_i_want', skillsIWant);
};

function initializeSkillList(selectId, skills) {
    var containerId = selectId + "_container";
    var containerElement = document.getElementById(containerId);
    var hiddenInput = document.getElementById(selectId + "_hidden");

    skills.forEach(function(skill) {
        if (skill.trim() !== '') {
            // Create a new div for the skill
            var skillDiv = document.createElement('div');
            skillDiv.textContent = skill;
            skillDiv.className = 'skill-item';

            // Add a remove button
            var removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.className = 'remove-skill-button';
            removeButton.onclick = function() {
                containerElement.removeChild(skillDiv);
                hiddenInput.value = hiddenInput.value.replace(skill + ',', '');
            };
            skillDiv.appendChild(removeButton);

            // Append the new skill to the list
            containerElement.appendChild(skillDiv);
        }
    });

    // Set the hidden input value
    hiddenInput.value = skills.join(',');
}

