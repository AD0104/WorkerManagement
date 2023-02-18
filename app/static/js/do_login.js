document
	.getElementById("submit-btn")
	.addEventListener("click", async (event) => {
		event.preventDefault();

		let base_form = document.getElementById("login-form");
		let form_data = new FormData(base_form);
		let json = {};
		form_data.forEach((value, key) => {
			json[key] = value;
		});
		json = JSON.stringify(json);

		let hdrs = new Headers({ "Content-Type": "application/json" });
		let init = {
			method: "POST",
			headers: hdrs,
			mode: "cors",
			cache: "default",
			body: json,
		};

		let url = "/auth/login";

		let response = await do_fetch(url, init);
		Swal.fire({
			title: "Verificando datos de acceso",
			timer: 1000,
			didOpen: () => {
				Swal.showLoading();
			},
		}).then(() => {
			if (response.status != "200") {
				Swal.fire({
					icon: "error",
					title: "Error en los datos!",
					text: response.result_message,
					showCloseButton: true,
				});
			} else {
				Swal.fire({
					icon: "success",
					title: "Acceso correcto",
					confirmButtonText: "Continuar",
					timer: 5000,
				}).then(() => {
					window.location.replace(response.result_message);
				});
			}
		});
	});
async function do_fetch(url, opts) {
	const response = await fetch(url, opts);
	return response.json();
}
