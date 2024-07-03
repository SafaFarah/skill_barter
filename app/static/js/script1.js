// Function to add a selected skill to the display area
function addSelectedSkill(containerId) {
    var selectElement = document.getElementById(containerId);
    var selectedSkill = selectElement.options[selectElement.selectedIndex].value;

    if (selectedSkill === '-- Select a skill --') {
        return;
    }

    // Check if the skill is already added
    var skillsContainer = document.getElementById(containerId + '_container');
    var skillsList = skillsContainer.querySelectorAll('.skill-item');
    for (var i = 0; i < skillsList.length; i++) {
        var skill = skillsList[i].innerText.trim();
        if (skill === selectedSkill) {
            alert('Skill already added!');
            return;
        }
    }

    // Create a new skill item
    var skillItem = document.createElement('div');
    skillItem.classList.add('skill-item');
    skillItem.textContent = selectedSkill;

    // Create a remove button
    var removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.type = 'button';
    removeButton.classList.add('remove-skill-button');
    removeButton.setAttribute('onclick', 'removeSkill("' + containerId + '", "' + selectedSkill + '")');

    // Append the skill item and remove button to the container
    skillItem.appendChild(removeButton);
    skillsContainer.appendChild(skillItem);

    // Update hidden input field with selected skills
    var hiddenInput = document.getElementById(containerId + '_hidden');
    var currentSkills = hiddenInput.value ? hiddenInput.value.split(',') : [];
    currentSkills.push(selectedSkill);
    hiddenInput.value = currentSkills.join(',');
}

// Function to remove a selected skill from the display area
function removeSkill(containerId, skillToRemove) {
    var skillsContainer = document.getElementById(containerId + '_container');
    var skillsList = skillsContainer.querySelectorAll('.skill-item');

    for (var i = 0; i < skillsList.length; i++) {
        var skillItem = skillsList[i];
        var skill = skillItem.childNodes[0].nodeValue.trim();

        if (skill === skillToRemove) {
            skillsContainer.removeChild(skillItem);

            // Update hidden input field with removed skill
            var hiddenInput = document.getElementById(containerId + '_hidden');
            var currentSkills = hiddenInput.value ? hiddenInput.value.split(',') : [];
            var index = currentSkills.indexOf(skillToRemove);
            if (index !== -1) {
                currentSkills.splice(index, 1);
                hiddenInput.value = currentSkills.join(',');
            }
            break;
        }
    }
}

