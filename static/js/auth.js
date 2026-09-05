document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            const alertBox = document.getElementById('loginAlert');

            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email, password})
                });
                const data = await res.json();
                
                if (res.ok) {
                    window.location.href = '/dashboard';
                } else {
                    alertBox.textContent = data.message;
                    alertBox.classList.remove('d-none');
                }
            } catch (err) {
                alertBox.textContent = "Error: " + err.message;
                alertBox.classList.remove('d-none');
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const full_name = document.getElementById('regName').value;
            const username = document.getElementById('regUsername').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            const confirm_password = document.getElementById('regConfirm').value;
            const alertBox = document.getElementById('signupAlert');

            try {
                const res = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({full_name, username, email, password, confirm_password})
                });
                const data = await res.json();
                
                if (res.ok) {
                    alert('Account created! You can now login.');
                    bootstrap.Modal.getInstance(document.getElementById('signupModal')).hide();
                    new bootstrap.Modal(document.getElementById('loginModal')).show();
                } else {
                    alertBox.textContent = data.message;
                    alertBox.classList.remove('d-none');
                }
            } catch (err) {
                alertBox.textContent = "Error: " + err.message;
                alertBox.classList.remove('d-none');
            }
        });
    }
});
