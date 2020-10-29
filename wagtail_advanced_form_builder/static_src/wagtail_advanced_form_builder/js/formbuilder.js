import { Datepicker } from 'vanillajs-datepicker';
import toDate from 'date-fns/toDate';
let wafDateFormat = null;


function findFieldsFromName(name, returnOneOnly = false) {
    const fields = document.getElementsByName(name);
    if (fields.length) {
        return returnOneOnly ? fields[0] : fields;
    }
    return null;
}

function findFieldParentContainer(element) {
    if (element) {
        const parent = element.closest('[data-waf-field]');
        if (parent) {
            return parent;
        }
    }
    return null;
}

function isMultipleFields(field) {
    return typeof field.length !== 'undefined' && typeof field.item !== 'undefined' && field.length > 1;
}

function isCheckboxOrRadio(field) {
    const fieldType = field.getAttribute('type');
    return fieldType === 'checkbox' || fieldType === 'radio';
}

function isMultiSelectField(field) {
    return field.hasAttribute('multiple');
}

function getValueFromAllSelectedOptions(field) {
    const options = field && field.options;
    let value = '';
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        if (option.selected) {
            value += option.value + ',';
        }
    }
    value = value.replace(/[,/]\s*$/, '');
    return value;
}

function getFieldValue(field) {
    if (isMultipleFields(field)) {
        let fieldValue = '';
        field.forEach((f) => {
            if (isCheckboxOrRadio(f)) {
                if (f.checked) {
                    fieldValue += `${ f.value.trim() },`;
                }
            }
        });

        // cleanup the field value
        fieldValue = fieldValue.replace(/[,/]\s*$/, '');
        return fieldValue;
    }
    field = field[0];
    if (isCheckboxOrRadio(field)) {
        if (field.checked) {
            return 'on';
        }
        return '';
    }

    if (isMultiSelectField(field)) {
        return getValueFromAllSelectedOptions(field);
    }
    // We're dealing with a standard string field here so trim it up and send it off
    return field.value.trim();
}

function toggleField(field, showHide) {
    if (field) {
        if (showHide === 'show') {
            field.style.display = 'block';
        } else {
            field.style.display = 'none';
        }
    }
}

function parseDateStringToTime(dateString) {
    return Datepicker.parseDate(dateString, wafDateFormat)
}

function conditionsPassed(conditionRule, conditionValue, conditionField) {
    let conditionFieldValue = null;
    let parsedValue = null;

    switch (conditionRule) {
    case 'is':
        if (conditionField.value !== conditionValue) {
            return false;
        }
        break;
    case 'is_not':
        if (conditionField.value === conditionValue) {
            return false;
        }
        break;
    case 'is_blank':
        if (conditionField.value !== '') {
            return false;
        }
        break;
    case 'is_not_blank':
        if (conditionField.value === '') {
            return false;
        }
        break;
    case 'greater_than':
        if (conditionField.type === 'datepicker') {
            conditionFieldValue = parseDateStringToTime(conditionField.value);
            parsedValue = parseDateStringToTime(conditionValue);
            if (conditionFieldValue <= parsedValue) {
                return false;
            }
        } else {
            conditionFieldValue = parseFloat(conditionField.value);
            parsedValue = parseFloat(conditionValue);
            // eslint-disable-next-line no-restricted-globals
            if (isNaN(conditionFieldValue) || conditionFieldValue <= parsedValue) {
                return false;
            }
        }
        break;
    case 'greater_than_equal':
        if (conditionField.type === 'datepicker') {
            conditionFieldValue = parseDateStringToTime(conditionField.value);
            parsedValue = parseDateStringToTime(conditionValue);
            if (conditionFieldValue < parsedValue) {
                return false;
            }
        } else {
            conditionFieldValue = parseFloat(conditionField.value);
            parsedValue = parseFloat(conditionValue);
            // eslint-disable-next-line no-restricted-globals
            if (isNaN(conditionFieldValue) || conditionFieldValue < parsedValue) {
                return false;
            }
        }

        break;
    case 'less_than':
        if (conditionField.type === 'datepicker') {
            conditionFieldValue = parseDateStringToTime(conditionField.value);
            parsedValue = parseDateStringToTime(conditionValue);
            if (conditionFieldValue >= parsedValue) {
                return false;
            }
        } else {
            conditionFieldValue = parseFloat(conditionField.value);
            parsedValue = parseFloat(conditionValue);
            // eslint-disable-next-line no-restricted-globals
            if (isNaN(conditionFieldValue) || conditionFieldValue >= parsedValue) {
                return false;
            }
        }
        break;
    case 'less_than_equal':
        if (conditionField.type === 'datepicker') {
            conditionFieldValue = parseDateStringToTime(conditionField.value);
            parsedValue = parseDateStringToTime(conditionValue);
            if (conditionFieldValue > parsedValue) {
                return false;
            }
        } else {
            conditionFieldValue = parseFloat(conditionField.value);
            parsedValue = parseFloat(conditionValue);
            // eslint-disable-next-line no-restricted-globals
            if (isNaN(conditionFieldValue) || conditionFieldValue > parsedValue) {
                return false;
            }
        }
        break;
    case 'contains':
        if (!conditionField.value.includes(conditionValue)) {
            return false;
        }
        break;
    case 'starts-with':
        if (!conditionField.value.startsWith(conditionValue)) {
            return false;
        }
        break;
    case 'ends-with':
        if (!conditionField.value.endsWith(conditionValue)) {
            return false;
        }
        break;
    default:
        break;
    }
    return true;
}

function checkConditions() {
    window.wafFormConditions.forEach((condition) => {

        // Default pass on conditions
        let allConditionsPassed = true;

        // Grab the action field details
        const actionField = {};
        actionField.action = condition.action;
        actionField.type = condition.field_type;
        actionField.field = findFieldsFromName(condition.field_name, true);
        actionField.parent = findFieldParentContainer(actionField.field);
        actionField.required = actionField.type === 'checkboxes' ? false : condition.required;

        // Cycle through the conditions associated with the action field
        for (let i = 0; i < condition.conditions.length; i++) {
            const cond = condition.conditions[i];
            const conditionRule = cond.rule;
            const conditionValue = cond.value;

            const conditionField = {};
            conditionField.field = findFieldsFromName(cond.field_name);
            conditionField.value = getFieldValue(conditionField.field);
            conditionField.type = cond.field_type;

            // Check whether the conditions have passed for this field.
            allConditionsPassed = conditionsPassed(conditionRule, conditionValue, conditionField);

            // Any conditions not passed then break out of the loop.
            if (!allConditionsPassed) {
                break;
            }
        }

        if (allConditionsPassed) {
            if (actionField.action === 'show') {
                toggleField(actionField.parent, 'show');
                if (actionField.required) {
                    actionField.field.setAttribute('required', true);
                }
            } else {
                toggleField(actionField.parent, 'hide');
                actionField.field.setAttribute('required', false);
            }
        } else if (actionField.action === 'show') {
            toggleField(actionField.parent, 'hide');
            actionField.field.setAttribute('required', false);
        } else {
            toggleField(actionField.parent, 'show');
            if (actionField.required) {
                actionField.field.setAttribute('required', true);
            }
        }
    });
}

function initialiseFormListeners(form) {
    // Assign event listeners to fields of this type
    const tags = ['input', 'select', 'textarea'];
    tags.forEach((tag) => {
        const tagEls = form.getElementsByTagName(tag);
        if (tagEls.length) {
            for (let i = 0; i < tagEls.length; i++) {
                tagEls[i].addEventListener('keyup', () => {
                    checkConditions();
                });
                tagEls[i].addEventListener('change', () => {
                    checkConditions();
                });
            }
        }
    });

    form.addEventListener('submit', (e) => {
        // Grab any date pickers and update their values to same format as Django
        const datePickers = document.querySelectorAll('input[data-waf-datepicker]');
        datePickers.forEach((dp) => {
            if (dp.value.length) {
                let dateTimeStamp = Datepicker.parseDate(dp.value, wafDateFormat);
                dp.value = Datepicker.formatDate(toDate(dateTimeStamp), 'yyyy-mm-dd');
            }
        });
    });
}

function initialiseFormFields() {

    // Initialise date pickers
    const datePickers = document.querySelectorAll('input[data-waf-datepicker]');
    datePickers.forEach((dp) => {
        wafDateFormat = dp.getAttribute('data-waf-date-format');
        new Datepicker(dp, {
            'format': wafDateFormat,
            'container': `[data-waf-datepicker--${dp.getAttribute('name')}]`,
            'autohide': true,
            'maxDate': dp.getAttribute('data-waf-datepicker-max-date'),
            'minDate': dp.getAttribute('data-waf-datepicker-min-date')
            // ...options
        });
        dp.addEventListener('changeDate', () => {
            checkConditions();
        });
    });

}

function scrollToError() {
    const errors = document.getElementsByClassName('waf--field-container--error');
    if (errors.length) {
        errors[0].scrollIntoView();
    }
}

function init() {
    if (window.wafFormConditions) {
        // Grab the form
        const form = document.getElementById('waf--form-page-form');

        // Initialise form field displays
        initialiseFormFields();

        // Initialise the form listeners
        initialiseFormListeners(form);

        // Check the conditions on page load
        checkConditions();

        // All conditions checked, so display the form.
        form.style.display = 'block';

        // Check for errors to scroll to
        scrollToError();
    }
}

init();
