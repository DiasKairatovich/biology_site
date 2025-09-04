document.addEventListener('DOMContentLoaded', function() {
    const questionsContainer = document.getElementById('questions-container');
    const totalForms = document.getElementById('id_questions-TOTAL_FORMS');
    const addButton = document.getElementById('add-question');
    const emptyTemplate = document.getElementById('empty-form-template').innerHTML;

    // Функция для переключения видимости полей
    function toggleQuestionFields(questionForm, questionType) {
        // Скрываем все блоки полей
        questionForm.querySelectorAll('.question-fields').forEach(field => {
            field.style.display = 'none';
        });

        // Показываем нужный блок
        const targetField = questionForm.querySelector(`[data-field-type="${questionType}"]`);
        if (targetField) {
            targetField.style.display = 'block';
        }
    }

    // Инициализация существующих вопросов
    function initExistingQuestions() {
        document.querySelectorAll('.question-form').forEach(questionForm => {
            const typeSelect = questionForm.querySelector('.question-type');
            if (typeSelect) {
                // Устанавливаем начальное состояние
                toggleQuestionFields(questionForm, typeSelect.value);

                // Добавляем обработчик изменения
                typeSelect.addEventListener('change', function() {
                    toggleQuestionFields(questionForm, this.value);
                });
            }
        });
    }

    // Добавление нового вопроса
    addButton.addEventListener('click', function() {
        const formIndex = parseInt(totalForms.value);
        const newFormHtml = emptyTemplate.replace(/__prefix__/g, formIndex);

        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newFormHtml;
        const newForm = tempDiv.firstElementChild;

        questionsContainer.appendChild(newForm);
        totalForms.value = formIndex + 1;

        // Инициализируем новый вопрос
        const typeSelect = newForm.querySelector('.question-type');
        toggleQuestionFields(newForm, typeSelect.value);
        typeSelect.addEventListener('change', function() {
            toggleQuestionFields(newForm, this.value);
        });

        // Обновляем нумерацию
        updateQuestionNumbers();
    });

    // Удаление вопроса
    questionsContainer.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-question')) {
            const questionIndex = e.target.dataset.index;
            const questionForm = e.target.closest('.question-form');
            const deleteField = questionForm.querySelector('input[name$="-DELETE"]');

            if (deleteField) {
                deleteField.value = 'on';
                questionForm.style.display = 'none';
            } else {
                questionForm.remove();
            }

            updateQuestionNumbers();
        }
    });

    // Обновление нумерации вопросов
    function updateQuestionNumbers() {
        const visibleQuestions = questionsContainer.querySelectorAll('.question-form:not([style*="display: none"])');
        document.getElementById('question-counter').textContent = `Вопросов: ${visibleQuestions.length}`;

        visibleQuestions.forEach((question, index) => {
            const numberSpan = question.querySelector('.question-number');
            if (numberSpan) {
                numberSpan.textContent = index + 1;
            }
        });
    }

    // Инициализация
    initExistingQuestions();
    updateQuestionNumbers();
});