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
        this.formRulesContainers = $('.waf--form-rules');
        this.uniqueFieldCounter = 0;
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
                const htmlFieldBlocks = $ruleContainer.parents('#form-list').first().find('.waf--html-field');
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
            this.formRulesContainers.show();
            this.formRulesContainers.siblings('label').show();
            this.swapRulesInputsForSelectDropdowns();
        } else {
            this.formRulesContainers.hide();
            this.formRulesContainers.siblings('label').hide();
        }
    }

    registerFieldNames() {

        this.registeredFieldNames = [];
        this.fields = $('.waf--field');

        this.fields.each((index, element) => {

            const $field = $(element);

            // Determine the parent streamfield container for this field
            let $fieldParentContainer = $field.parents('div[id^="form-"][id$="-container"]').first();
            if (!$fieldParentContainer.length) {
                $fieldParentContainer = $field.parents('div[id^="field-list"]').first();
            }

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

    initField($field) {
        const $fieldParentContainer = $field.parents('.c-sf-container__block-container').first();
        const $childFields = $field.find('> .field');
        const $headerBar = $fieldParentContainer.find('.c-sf-block__header');
        if (!$fieldParentContainer.find('[data-expand-trigger]').length) {
            $field.attr('id', `field-list-${ this.uniqueFieldCounter }`);
            let hasHiddenFields = false;
            $childFields.each((index, childField) => {
                if (index > 0) {
                    const $childField = $(childField);
                    const inError = $childField.find('div.error');
                    if (!inError.length) {
                        $childField.hide();
                        hasHiddenFields = true;
                    }
                }
            });
            $(`<a href="#" data-expand-trigger="field-list-${ this.uniqueFieldCounter }">${ hasHiddenFields ? 'Configure field' : 'Collapse field' }</a>`).insertBefore($headerBar.find('h3').first());
            this.uniqueFieldCounter += 1;
        }
    }

    initFieldDisplay() {
        this.fields.each((i, field) => {
            this.initField($(field));
        });
    }

    initExpandTrigger($trigger) {
        const fieldsListId = $trigger.attr('data-expand-trigger');
        const fieldsContainer = $(`#${ fieldsListId }`);
        const fields = fieldsContainer.find('> .field');
        if ($trigger.html() === 'Collapse field') {
            fields.each(function (i) {
                if (i > 0) {
                    $(this).hide();
                }
            });
            $trigger.html('Configure field');
        } else {
            fields.each(function () {
                $(this).show();
            });
            $trigger.html('Collapse field');
        }
    }
    initExpandTriggers() {
        this.expandTriggers = $('[data-expand-trigger]');
        this.expandTriggers.on('click', (event) => {
            event.preventDefault();
            this.initExpandTrigger($(event.currentTarget));
        });
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
        this.streamfieldList = $('#form-list')[0];
        this.formRulesLists = $('[id$=-rules-conditions-list]');
    }

    monitorMutations() {

        this.newFieldMutationObserver = new MutationObserver(((mutations) => {
            mutations.forEach((mutation) => {
                const newNodes = mutation.addedNodes; // DOM NodeList
                if (newNodes !== null) { // If there are new nodes added
                    this.fieldRegistry.registerFieldNames();
                    const $nodes = $(newNodes); // jQuery set
                    $nodes.each((index, node) => {
                        const $node = $(node);
                        this.fieldRegistry.initField($node);
                        const expandNodes = $nodes.find('[data-expand-trigger]');
                        expandNodes.unbind('click');
                        expandNodes.on('click', (event) => {
                            event.preventDefault();
                            this.fieldRegistry.initExpandTrigger($(event.currentTarget));
                        });
                    });

                    $nodes.find('[id$=-rules-conditions-list]').each((index, element) => {
                        this.newRuleMutationObserver.observe(element, this.mutationObserverConfig);
                    });
                }
            });
        }));

        this.newFieldMutationObserver.observe(this.streamfieldList, this.mutationObserverConfig);

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
        $(this.streamfieldList).find('[id^="form-"][id$="-delete"]').on('click', (event) => {
            this.fieldRegistry.registerFieldNames();
        });

    }

    init() {
        this.fieldRegistry = new FieldRegistry();
        this.fieldRegistry.registerFieldNames();
        this.fieldRegistry.initFieldDisplay();
        this.fieldRegistry.initExpandTriggers();
        this.monitorMutations();

    }
}

$(document).ready(function() {
    const formBuilder = new FormBuilder();
    formBuilder.init();
});
