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

		let response = await fetch(url, init);
		console.log(response);
	});
