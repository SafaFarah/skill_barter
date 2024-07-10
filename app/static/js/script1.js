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
        var skill = skillsList[i].querySelector('.skill-text').textContent.trim();
        if (skill === selectedSkill) {
            alert('Skill already added!');
            return;
        }
    }

    // Create a new skill item
    var skillItem = document.createElement('div');
    skillItem.classList.add('skill-item');

    // Create a span for skill text
    var skillText = document.createElement('span');
    skillText.classList.add('skill-text');
    skillText.textContent = selectedSkill;

    // Create a remove button
    var removeButton = document.createElement('button');
    removeButton.textContent = 'Remove';
    removeButton.type = 'button';
    removeButton.classList.add('remove-skill-button');
    removeButton.onclick = function() {
        removeSkill(containerId, selectedSkill);
    };

    // Append the skill text and remove button to the skill item
    skillItem.appendChild(skillText);
    skillItem.appendChild(removeButton);
    skillsContainer.appendChild(skillItem);

    // Update hidden input field with selected skills
    updateHiddenSkills(containerId);
}

// Function to remove a selected skill from the display area
function removeSkill(containerId, skillToRemove) {
    console.log(`Removing skill: ${skillToRemove} from ${containerId}`);
    var skillsContainer = document.getElementById(containerId + '_container');
    var skillsList = skillsContainer.querySelectorAll('.skill-item');

    for (var i = 0; i < skillsList.length; i++) {
        var skillItem = skillsList[i];
        var skill = skillItem.querySelector('.skill-text').textContent.trim();

        if (skill === skillToRemove) {
            skillsContainer.removeChild(skillItem);

            // Update hidden input field with removed skill
            updateHiddenSkills(containerId);
            break;
        }
    }
}

// Function to update hidden input field with selected skills
function updateHiddenSkills(containerId) {
    var skillsContainer = document.getElementById(containerId + '_container');
    var skillsList = skillsContainer.querySelectorAll('.skill-item');
    var hiddenInput = document.getElementById(containerId + '_hidden');

    var currentSkills = [];
    for (var i = 0; i < skillsList.length; i++) {
        var skill = skillsList[i].querySelector('.skill-text').textContent.trim();
        currentSkills.push(skill);
    }

    hiddenInput.value = currentSkills.join(',');
    console.log(`Updated hidden input for ${containerId}: ${hiddenInput.value}`);
}

