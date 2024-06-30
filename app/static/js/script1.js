function addSkillToList(skillType) {
    var skillSelect = document.getElementById(skillType);
    var selectedSkill = skillSelect.options[skillSelect.selectedIndex].text;
    var skillsLabel = document.getElementById(skillType + '_label');

    // Check if the skill is already added
    if (!skillsLabel.innerText.includes(selectedSkill)) {
        // Append the selected skill to the label
        if (skillsLabel.innerText.trim() === '') {
            skillsLabel.innerText = selectedSkill;
        } else {
            skillsLabel.innerText += ', ' + selectedSkill;
        }
    }

    // Clear the selection after adding
    skillSelect.selectedIndex = 0;
}