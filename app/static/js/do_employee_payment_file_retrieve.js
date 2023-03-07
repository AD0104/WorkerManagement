document
    .getElementById("gendoc-btn")
    .addEventListener("click", async (event) => {
        event.preventDefault();
        let array = Array.from(document.querySelectorAll(".form input.input"))
        let form_data = {}
        array.forEach((node) => {
            form_data[node.id] = node.value;
        });
        let form_data_json = JSON.stringify(form_data);
        let hdrs = new Headers({ "Content-Type": "application/json" });
        let init = {
            method: "POST",
            headers: hdrs,
            mode: "cors",
            cache: "default",
            body: form_data_json
        };
        let url = window.location.href

        let response = await do_fetch(url, init);
        console.log(response);
    })
async function do_fetch(url, opts) {
    const response = await fetch(url, opts);
    return response.json();
}
