let percepciones_field_swal_object,
    percepciones_value_swal_object;
let percepciones_field_name,
    percepciones_field_key,
    percepciones_field_value;
let percepciones_options = {
    "redondeo": "Redondeo",
    "dia_festivo": "Día Festivo"
}
let deducciones_field_swal_object,
    deducciones_value_swal_object;
let deducciones_field_name,
    deducciones_field_key,
    deducciones_field_value;
let deducciones_options = {
    "anticipos": "Anticipos",
    "prestamos": "Prestamos"
}

let fixed_decimals = 2,
    exists_empty_input = false,
    wages = {};

// --* START OF PERCEPCIONES RELATED FUNCTIONS *--
document
    .getElementById("percepciones-btn")
    .addEventListener("click", async (event) => {
        event.preventDefault();
        await open_percepciones_concept();
        await open_percepciones_value();
        add_form_field("percepciones-form", percepciones_field_name, percepciones_field_key, percepciones_field_value);
    });

async function open_percepciones_concept() {
    percepciones_field_swal_object = await Swal.fire({
        title: 'Percepciones adicionales',
        input: 'select',
        inputPlaceholder: 'Selecciona un concepto',
        inputOptions: percepciones_options,
        showCancelButton: true,
        inputValidator: (value) => {
            return new Promise((resolve) => {
                for (let key in percepciones_options) {
                    if (key === value) {
                        percepciones_field_key = key;
                        percepciones_field_name = percepciones_options[key];
                        resolve()
                    }
                }
                resolve('Por favor elige un concepto aceptable')
            })
        }
    });
}

async function open_percepciones_value() {
    percepciones_value_swal_object = await Swal.fire({
        title: 'Percepciones adicionales',
        input: 'text',
        inputLabel: 'Valor del concepto',
        showCancelButton: true,
        inputValidator: (value) => {
            if (!value) {
                return "Es necesario poner un valor.";
            }
            percepciones_field_value = value;
        }
    });
}

// --* END OF PERCEPCIONES RELATED FUNCTIONS *--

// --* START OF DEDUCCIONES RELATED FUNCTIONS *--

document
    .getElementById("deducciones-btn")
    .addEventListener("click", async (event) => {
        event.preventDefault();
        await open_deducciones_concept();
        await open_deducciones_value();
        add_form_field("deducciones-form", deducciones_field_name, deducciones_field_key, deducciones_field_value);
    });

async function open_deducciones_concept() {
    deducciones_field_swal_object = await Swal.fire({
        title: 'Deducciones adicionales',
        input: 'select',
        inputPlaceholder: 'Selecciona un concepto',
        inputOptions: deducciones_options,
        showCancelButton: true,
        inputValidator: (value) => {
            return new Promise((resolve) => {
                for (let key in deducciones_options) {
                    if (key === value) {
                        deducciones_field_key = key;
                        deducciones_field_name = deducciones_options[key];
                        resolve()
                    }
                }
                resolve('Por favor elige un concepto aceptable')
            })
        }
    });
}

async function open_deducciones_value() {
    deducciones_value_swal_object = await Swal.fire({
        title: 'Percepciones adicionales',
        input: 'text',
        inputLabel: 'Valor del concepto',
        showCancelButton: true,
        inputValidator: (value) => {
            if (!value) {
                return "Es necesario poner un valor.";
            }
            deducciones_field_value = value;
        }
    });
}

// --* END OF DEDUCCIONES RELATED FUNCTIONS *--

// --* START OF DOM MANIPULATION *--

async function add_form_field(form_id, field_label, field_key, field_value) {
    let form = document.getElementById(form_id);

    let div_field = document.createElement("div");
    div_field.classList.add("field");

    let div_field_label = document.createElement("label");
    div_field_label.classList.add("label");
    div_field_label.innerText = field_label;

    let div_field_control = document.createElement("div");
    div_field_control.classList.add("control");

    let input = document.createElement("input");
    input.type = "text";
    input.classList.add("input", "is-small");
    input.name = field_key;
    input.id = field_key;
    input.value = field_value;

    div_field_control.appendChild(input)

    div_field.appendChild(div_field_label);
    div_field.appendChild(div_field_control);
    form.appendChild(div_field);
}

document
    .getElementById("totales-btn")
    .addEventListener("click", (event) => {
        event.preventDefault();
        do_get_wages();
        let percepciones_total = parseFloat(get_percepciones_sum());
        let deducciones_total = parseFloat(get_deducciones_sum());
        let general_total = do_sum(percepciones_total, -deducciones_total);

        if (exists_empty_input) {
            exists_empty_input = false;
            return;
        }

        do_refresh_totals(percepciones_total, deducciones_total, general_total);
        document.getElementById("gendoc-btn").disabled = false;

    });

function do_refresh_totals(percepciones, deducciones, general) {
    document.getElementById("percepciones_total").value = percepciones;
    document.getElementById("deducciones_total").value = deducciones;
    document.getElementById("general_total").value = general;
}

document
    .getElementById("periodo-form")
    .addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });

document
    .getElementById("percepciones-form")
    .addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });

document
    .getElementById("deducciones-form")
    .addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });

document
    .getElementById("totales-form")
    .addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });

// --* END OF DOM MANIPULATION *--

// --* START OF CALCULATIONS *--

function get_percepciones_sum() {
    let wages_inputs = document.querySelectorAll("#percepciones-form input");

    if (do_check_empty_field(Array.from(wages_inputs), "Percepciones"))
        return;

    let wages_array = [], wages_total = 0;
    for (let wage_current of wages_inputs) {
        let wage_value, wage_dict_value;

        if (wage_current.value === "")
            wage_value = 0
        else
            wage_value = parseFloat(wage_current.value);
        switch (wage_current.name) {
            case "worked_days":
                wage_dict_value = wages["daily_salary"];
                wages_array.push(do_mult(wage_value, wage_dict_value))
                break;
            case "extra_minutes":
                wage_dict_value = do_mult(wage_value, wages['minutely_salary'])
                wages_array.push(wage_dict_value)
                break;
            case "dia_festivo":
                const wage_day = do_mult(wage_value, wages['daily_salary'])
                const wage_hour = do_mult(wage_value, wages['hourly_salary'])

                wages_array.push(do_sum(wage_day, wage_hour))

                break;

            case "redondeo":
                wages_array.push(do_sum(wages_array.pop(), wage_value));
                break;

            default:
                break;
        }
    }
    wages_array.forEach((element) => {
        wages_total = do_sum(parseFloat(wages_total), parseFloat(element));
    })
    return wages_total;
}

function get_deducciones_sum() {
    let deductions_inputs = document.querySelectorAll("#deducciones-form input");

    if (do_check_empty_field(Array.from(deductions_inputs), "Deducciones"))
        return;

    let deductions_values = []
    for (let deductions_current of deductions_inputs) {
        let current_deduction_value, deduction_dict_value, current_operation;

        if (deductions_current.value === "")
            current_deduction_value = 0
        else
            current_deduction_value = parseFloat(deductions_current.value);

        switch (deductions_current.name) {
            case "minutes_late":
                deduction_dict_value = wages["minutely_salary"];
                current_operation = do_mult(parseFloat(current_deduction_value), parseFloat(deduction_dict_value));
                deductions_values.push(current_operation);
                break;
            case "anticipos":
                deductions_values.push(do_sum(deductions_values.pop(), current_deduction_value))
                break;
            case "prestamos":
                deductions_values.push(do_sum(deductions_values.pop(), current_deduction_value));
                break;
            default:
                break;
        }
    }
    return deductions_values[0]
}
// --* END OF CALCULATIONS *--

// --* START OF ARITHMETIC OPERATIONS *--
function do_mult(a, b) {
    return parseFloat(a * b).toFixed(fixed_decimals);
}

function do_sum(a, b) {
    return parseFloat(a + b).toFixed(fixed_decimals);
}
// --* END OF ARITHMETIC OPERATIONS *--

// --* START OF HELPER FUNCTIONS *--

function do_get_wages() {
    wages_nodes = document.querySelectorAll(".content span");
    for (let node of wages_nodes) {
        wages[node.id] = parseFloat(node.innerText);
    }
}

function do_check_empty_field(fields, section_name) {
    let is_empty = false;
    fields.forEach(element => {
        if (element.value === "") {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: `Detectamos un campo vacio en ${section_name}!`,
            })
            is_empty = true;
            exists_empty_input = true;
        }
    });
    return is_empty;
}

async function do_fetch(url, opts) {
    const response = await fetch(url, opts);
    return response.json()
}
// --* END OF HELPER FUNCTIONS *--
