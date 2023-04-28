function debounce(func, wait, immediate) {
    let timeout;
    return function () {
        const context = this; const
            args = arguments;
        const later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

class FieldRegistry {
    constructor() {
        this.registeredFieldNames = [];
        this.fields = $('.waf--field');
    }

    swapRulesInputsForSelectDropdowns() {
        if (this.registeredFieldNames.length) {
            const rulesContainersInputs = $('.waf--form-rules .waf--rule-condition');
            rulesContainersInputs.each((index, element) => {

                const $ruleContainer = $(element);

                // Create the select list options
                const selectListOptions = [];

                // Find this blocks field name and exclude it from here
                const fieldNameFieldValue = $ruleContainer.parents('.waf--field').find('input[type="text"]').first()
                    .val();

                // Find any HTML field blocks to exclude from dropdown
                const htmlFieldBlocks = $('.waf--html-field');
                const htmlFieldNames = [];
                htmlFieldBlocks.each((i, htmlElement) => {
                    htmlFieldNames.push($(htmlElement).find('input[type="text"]').first().val());
                });

                for (let i = 0; i < this.registeredFieldNames.length; i++) {
                    if (this.registeredFieldNames[i] !== fieldNameFieldValue && htmlFieldNames.indexOf(this.registeredFieldNames[i]) === -1) {
                        const option = document.createElement('option');
                        option.value = this.registeredFieldNames[i];
                        option.text = this.registeredFieldNames[i];
                        selectListOptions.push(option);
                    }
                }

                const inputToReplace = $ruleContainer.find('input[type="text"][name$="field_name"]').first();
                if (inputToReplace.length) {
                    inputToReplace.parent().parent().addClass('choice_field widget-select');
                    const currentValue = inputToReplace.val();
                    const selectList = document.createElement('select');
                    selectList.id = inputToReplace.attr('id');
                    selectList.name = inputToReplace.attr('name');
                    for (let i = 0; i < selectListOptions.length; i++) {
                        selectList.appendChild(selectListOptions[i]);
                    }
                    inputToReplace.replaceWith(selectList);
                    $(selectList).val(currentValue);
                } else {
                    const selectToUpdate = $ruleContainer.find('select').first();
                    const currentValue = selectToUpdate.val();
                    selectToUpdate.empty();
                    for (let i = 0; i < selectListOptions.length; i++) {
                        selectToUpdate[0].appendChild(selectListOptions[i]);
                    }
                    selectToUpdate.val(currentValue);
                }
            });
        }
    }

    toggleRulesContainers() {
        this.formRulesContainers = $('.waf--form-rules');
        if (this.registeredFieldNames.length > 1) {
            this.swapRulesInputsForSelectDropdowns();
        }
    }

    registerFieldNames() {

        this.registeredFieldNames = [];
        this.fields = $('.waf--field');

        this.fields.each((index, element) => {

            const $field = $(element);

            // Determine the parent streamfield container for this field
            let $fieldParentContainer = $field.parents('section').first().parent('div');

            // Determine if this Streamfield has been deleted already
            const isDeleted = $fieldParentContainer.find('input[type="hidden"][id$="-deleted"]').first();
            if (isDeleted.attr('value') !== '1') {
                // Find the field name for this streamfield field from the first input element in the block
                const $nameField = $field.find('input[type="text"]').first();
                const fieldName = $nameField.val();
                if (fieldName !== undefined && fieldName !== '') {
                    this.registeredFieldNames.push(fieldName);
                }

                // Bind listeners to this name field
                $nameField.unbind('keyup change');
                $nameField.on('keyup change', debounce(() => {
                    this.registerFieldNames();
                }, 500));
            }
        });

        this.toggleRulesContainers();

    }
}

class FormBuilder {

    constructor() {
        this.mutationObserverConfig = {
            attributes: true,
            childList: true,
            characterData: true,
            subTree: true,
        };

        // Fetch the streamfield field containers so mutation observers can be attached.
        this.streamfieldList = $('.waf--field').first().parents('[data-streamfield-stream-container]');

        // Handles the case where there aren't any waf--fields on the form page yet.
        if (!this.streamfieldList.length) {
            this.streamfieldList = $('[data-streamfield-stream-container]');
        }

        // Fetch any existing conditions blocks on existing fields so mutation observers can be attached to them.
        this.formRulesLists = $('[data-contentpath="conditions"]').find('[data-streamfield-stream-container]');
    }

    monitorMutations() {

        this.newFieldMutationObserver = new MutationObserver(((mutations) => {
            mutations.forEach((mutation) => {
                const newNodes = mutation.addedNodes; // DOM NodeList
                if (newNodes !== null) { // If there are new nodes added
                    this.fieldRegistry.registerFieldNames();
                    const $nodes = $(newNodes); // jQuery set
                    $nodes.find('[data-contentpath="conditions"]').find('[data-streamfield-stream-container]').each((index, element) => {
                        this.newRuleMutationObserver.observe(element, this.mutationObserverConfig);
                    });
                }
            });
        }));

        this.streamfieldList.each((index, element) => {
            this.newFieldMutationObserver.observe(element, this.mutationObserverConfig);
        });

        this.newRuleMutationObserver = new MutationObserver(((mutations) => {
            mutations.forEach((mutation) => {
                const newNodes = mutation.addedNodes; // DOM NodeList
                if (newNodes !== null) { // If there are new nodes added
                    this.fieldRegistry.registerFieldNames();
                }
            });
        }));

        this.formRulesLists.each((index, element) => {
            this.newRuleMutationObserver.observe(element, this.mutationObserverConfig);
        });

        // Reregister field names when delete buttons are clicked on streamfield
        $(this.streamfieldList).find('.button[title="Delete"]').on('click', (event) => {
            this.fieldRegistry.registerFieldNames();
        });

    }

    init() {
        this.fieldRegistry = new FieldRegistry();
        this.fieldRegistry.registerFieldNames();
        this.monitorMutations();

    }
}

$(document).ready(function() {
    const formBuilder = new FormBuilder();
    formBuilder.init();
});
