const workspace = document.querySelector('.workspace');
const taskToast = document.querySelector('.task-toast');
let saving = false;
let toastTimeout;

function hideTaskToast() {
    window.clearTimeout(toastTimeout);
    taskToast.hidden = true;
}

function showTaskCreated() {
    window.clearTimeout(toastTimeout);
    taskToast.hidden = false;
    toastTimeout = window.setTimeout(hideTaskToast, 10_000);
}

taskToast?.querySelector('.task-toast-close').addEventListener('click', hideTaskToast);

async function refreshTaskResults() {
    const response = await fetch(window.location.href, { cache: 'no-store' });
    if (!response.ok) throw new Error('Task list request failed');

    const page = new DOMParser().parseFromString(await response.text(), 'text/html');
    const results = page.getElementById('task-results');
    if (!results) throw new Error('Task list is missing');

    document.getElementById('task-results').replaceWith(results);
}

workspace.addEventListener('click', (event) => {
    const control = event.target.closest('[data-edit-title], [data-cancel-title]');
    if (!control) return;

    const card = control.closest('.task-card');
    const editButton = card.querySelector('[data-edit-title]');
    const form = card.querySelector('.task-rename');
    const opening = control === editButton && form.hidden;
    form.hidden = !opening;
    editButton.setAttribute('aria-expanded', String(opening));

    if (opening) {
        form.elements.title.focus();
        form.elements.title.select();
    } else {
        form.reset();
        form.querySelector('.task-error').hidden = true;
        editButton.focus();
    }
});

workspace.addEventListener('submit', async (event) => {
    const form = event.target;
    const method = form.dataset.taskMethod;
    if (!method) return;

    event.preventDefault();
    if (saving) return;
    if (method === 'DELETE' && !window.confirm('Точно удалить задачу? Восстановить её не получится.')) return;

    const error = form.querySelector('.task-error');
    const fields = new FormData(form);
    const csrfToken = fields.get('csrfmiddlewaretoken');
    fields.delete('csrfmiddlewaretoken');

    if (fields.has('title')) {
        const title = fields.get('title').trim();
        if (title.length < 5) {
            error.textContent = 'Название задачи должно быть не короче 5 символов.';
            error.hidden = false;
            return;
        }
        fields.set('title', title);
    }

    if (fields.has('description')) {
        const description = fields.get('description').trim();
        if (description && description.length < 10) {
            error.textContent = 'Описание задачи должно быть не короче 10 символов.';
            error.hidden = false;
            return;
        }
        if (description) {
            fields.set('description', description);
        } else {
            fields.delete('description');
        }
    }

    const buttons = workspace.querySelectorAll('button');
    saving = true;
    error.hidden = true;
    buttons.forEach((button) => { button.disabled = true; });

    try {
        const response = await fetch(form.action, {
            method,
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: method === 'DELETE' ? undefined : JSON.stringify(Object.fromEntries(fields)),
        });
        if (response.ok) {
            if (method === 'POST') {
                form.reset();
                showTaskCreated();
                try {
                    await refreshTaskResults();
                } catch {
                    error.textContent = 'Задача сохранена. Обновите страницу, чтобы увидеть актуальный список.';
                    error.hidden = false;
                } finally {
                    saving = false;
                    buttons.forEach((button) => { button.disabled = false; });
                }
                return;
            }
            window.location.reload();
            return;
        }
        error.textContent = response.status === 403
            ? 'Не удалось подтвердить сеанс. Обнови страницу и попробуй снова.'
            : 'Не удалось сохранить изменение. Обнови страницу и попробуй снова.';
    } catch {
        error.textContent = 'Нет связи с сервером. Повторите попытку позже.';
    }

    error.hidden = false;
    saving = false;
    buttons.forEach((button) => { button.disabled = false; });
});
