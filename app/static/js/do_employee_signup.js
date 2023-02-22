document
    .getElementById("submit-btn")
    .addEventListener("click", async (event) => {
        event.preventDefault();

        let base_form = document.getElementById("register-form");
        let form_data = new FormData(base_form);
        let hdrs = new Headers();
        let opts = {
            method: "POST",
			headers: hdrs,
			mode: "cors",
			cache: "default",
			body: form_data,
        };
        let url = "/employees/add"

        let response = await do_fetch(url, opts);
        Swal.fire({
            title: "Procesando datos",
            timer: 2000,
            didOpen: () => {
                Swal.showLoading();
            }
        }).then(() => {
            if(response.status != "200"){
                Swal.fire({
                    icon: "error",
                    title: "Algo salió mal",
                    text: response.message,
                    showCloseButton: true,
                });
            } else {
                Swal.fire({
                    icon: "success",
                    title: "Terminado",
                    text: "Todos los datos fueron correctamente ingresados",
                    confirmButtonText: "Continuar",
                    timer: 5000
                }).then((result) => {
                    if(result.isConfirmed)
                        window.location.reload();
                })
            }
        })
    });
async function do_fetch(url, opts){
    return (await fetch(url, opts)).json();
}