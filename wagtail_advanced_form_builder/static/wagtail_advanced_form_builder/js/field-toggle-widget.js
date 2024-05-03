
(function () {
    class FieldToggle {
        constructor (container) {
            this.container = container;
            this.input = container.querySelector('input');
            this.label = container.querySelector('label');
            this.labelText = this.input.dataset.label;
            this.toggledLabelText = this.input.dataset.toggledLabel;
            console.log({ input: this.input, label: this.label });

            this.input.addEventListener('change', this.toggle.bind(this));
        }

        toggle () {
            if (this.input.checked) {
                this.label.innerText = this.toggledLabelText;
            } else {
                this.label.innerText = this.labelText;
            }
        }
    }

    document.querySelectorAll('.waf--field-toggle').forEach(function (fieldToggleContainer) {
        new FieldToggle(fieldToggleContainer);
    });
})();