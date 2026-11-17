const pattern = document.querySelector('.task-pattern');
const numbers = Array.from({ length: 120 }, (_, index) => index + 1);

for (let index = numbers.length - 1; index > 0; index--) {
    const otherIndex = Math.floor(Math.random() * (index + 1));
    [numbers[index], numbers[otherIndex]] = [numbers[otherIndex], numbers[index]];
}

function fillPattern() {
    const styles = getComputedStyle(pattern);
    const rowHeight = parseFloat(styles.gridAutoRows);
    const columnWidth = rowHeight / parseFloat(styles.getPropertyValue('--hex-row-ratio'));
    const rowCount = Math.ceil(pattern.clientHeight / rowHeight) + 1;
    const columnCount = Math.ceil(pattern.clientWidth / columnWidth) + 1;

    if (pattern.childElementCount === rowCount && pattern.firstElementChild.childElementCount === columnCount) {
        return;
    }

    const rows = document.createDocumentFragment();
    let numberIndex = 0;
    for (let rowIndex = 0; rowIndex < rowCount; rowIndex++) {
        const row = document.createElement('div');
        row.className = 'task-pattern-row';
        for (let columnIndex = 0; columnIndex < columnCount; columnIndex++) {
            const tile = document.createElement('span');
            tile.textContent = `task ${numbers[numberIndex % numbers.length]}`;
            row.append(tile);
            numberIndex++;
        }
        rows.append(row);
    }
    pattern.replaceChildren(rows);
}

const observer = new ResizeObserver(fillPattern);
observer.observe(pattern);
