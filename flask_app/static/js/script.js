function submitPriorityForm(taskId) {
    const formId = 'priority-form-' + taskId;
    document.getElementById(formId).submit();

    // Add jump class to the task card
    const taskCard = document.getElementById('task-' + taskId);
    if (taskCard) {
        taskCard.classList.add('jump');

        // Optionally remove the class after the animation ends to reset the animation
        taskCard.addEventListener('animationend', () => {
            taskCard.classList.remove('jump');
        });
    }
}