"use strict";

const toastContainer = document.querySelector(".toast-container");

function showToast(message, variant = "primary") {
	if (!toastContainer) {
		return;
	}

	const toast = document.createElement("div");
	toast.className = `toast align-items-center text-bg-${variant} border-0`;
	toast.setAttribute("role", "alert");
	toast.setAttribute("aria-live", "assertive");
	toast.setAttribute("aria-atomic", "true");

	toast.innerHTML = `
		<div class="d-flex">
			<div class="toast-body">${message}</div>
			<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
		</div>
	`;

	toastContainer.appendChild(toast);
	const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
	bsToast.show();

	toast.addEventListener("hidden.bs.toast", () => {
		toast.remove();
	});
}

// Socket.IO realtime listener
if (typeof io !== "undefined") {
	const socket = io();

	socket.on("connect", () => {
		console.log("Socket.IO connected");
	});

	socket.on("task_updated", (data) => {
		console.log("Realtime update:", data);

		showToast("Dashboard updated in realtime", "success");

		window.setTimeout(() => {
			window.location.reload();
		}, 800);
	});

	socket.on("task_deleted", (data) => {
		console.log("Task deleted:", data);

		showToast("Task deleted successfully", "warning");

		window.setTimeout(() => {
			window.location.reload();
		}, 800);
	});
}

const registerForm = document.querySelector("form[action*='register']");

if (registerForm) {
	const usernameInput = registerForm.querySelector("input[name='username']");
	const passwordInput = registerForm.querySelector("input[name='password']");
	const confirmPasswordInput = registerForm.querySelector(
		"input[name='confirm_password']"
	);

	function createValidationMessage(input) {
		const message = document.createElement("div");
		message.className = "form-text mt-1 validation-message";
		input.parentElement.appendChild(message);
		return message;
	}

	const usernameMessage = createValidationMessage(usernameInput);
	const passwordMessage = createValidationMessage(passwordInput);
	const confirmMessage = createValidationMessage(confirmPasswordInput);

	function setError(element, messageBox, message) {
		element.classList.add("is-invalid");
		element.classList.remove("is-valid");
		messageBox.textContent = message;
		messageBox.classList.add("text-danger");
		messageBox.classList.remove("text-success");
	}

	function setSuccess(element, messageBox, message) {
		element.classList.remove("is-invalid");
		element.classList.add("is-valid");
		messageBox.textContent = message;
		messageBox.classList.remove("text-danger");
		messageBox.classList.add("text-success");
	}

	usernameInput.addEventListener("input", () => {
		const username = usernameInput.value.trim();

		if (username.length < 3) {
			setError(
				usernameInput,
				usernameMessage,
				"Username must be at least 3 characters"
			);
		} else {
			setSuccess(
				usernameInput,
				usernameMessage,
				"Username looks good"
			);
		}
	});

	passwordInput.addEventListener("input", () => {
		const password = passwordInput.value;

		const hasUppercase = /[A-Z]/.test(password);
		const hasNumber = /[0-9]/.test(password);
		const hasSpecial = /[^A-Za-z0-9]/.test(password);

		if (password.length < 8) {
			setError(
				passwordInput,
				passwordMessage,
				"Password must be at least 8 characters"
			);
		} else if (!hasUppercase) {
			setError(
				passwordInput,
				passwordMessage,
				"Password must contain 1 uppercase letter"
			);
		} else if (!hasNumber) {
			setError(
				passwordInput,
				passwordMessage,
				"Password must contain 1 number"
			);
		} else if (!hasSpecial) {
			setError(
				passwordInput,
				passwordMessage,
				"Password must contain 1 special character"
			);
		} else {
			setSuccess(
				passwordInput,
				passwordMessage,
				"Strong password"
			);
		}
	});

	confirmPasswordInput.addEventListener("input", () => {
		if (confirmPasswordInput.value !== passwordInput.value) {
			setError(
				confirmPasswordInput,
				confirmMessage,
				"Passwords do not match"
			);
		} else {
			setSuccess(
				confirmPasswordInput,
				confirmMessage,
				"Passwords match"
			);
		}
	});
}
