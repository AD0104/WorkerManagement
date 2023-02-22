let buttons = Array.from(document.getElementsByClassName("remove-btn"));

console.log(buttons);

buttons.forEach(button => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
		Swal.fire({
			title: 'Confirmación para eliminar usuarios',
			showDenyButton: true,
			confirmButtonText: 'Eliminar',
			denyButtonText: `Cancelar`,
		}).then(async (result) => {
			/* Read more about isConfirmed, isDenied below */
			if (result.isConfirmed) {
				let hdrs = new Headers();
				let init = {
					method: "DELETE",
					headers: hdrs,
					mode: "cors",
					cache: "default",
					body: {}
				}
				let response = await do_fetch(button.value, init)
				Swal.fire({
					title: "Procesando petición",
					timer: 1000,
					didOpen: () => {
						Swal.showLoading();
					},
				}).then(() => {
					if (response.status != "200") {
						Swal.fire({
							icon: "error",
							title: "Error al eliminar!",
							text: response.result_message,
							showCloseButton: true,
						});
					} else {
						Swal.fire({
							icon: "success",
							title: "Empleado eliminado",
							confirmButtonText: "Continuar",
							timer: 5000,
						}).then(() => {
							window.location.reload();
						});
					}
				});
			} else if (result.isDenied) {
			  Swal.fire('Operación canelada', '', 'info')
			}
		  })
		  
        
    })
})

async function do_fetch(url, opts) {
	const response = await fetch(url, opts);
	return response.json();
}
