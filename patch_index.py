with open("templates/index.html", "r") as f:
    html = f.read()

# Add Login Button to Navbar
login_btn = """                <div class="ms-lg-3 mt-3 mt-lg-0 d-flex gap-2">
                    <button class="btn btn-primary btn-sm rounded-pill px-3" data-bs-toggle="modal" data-bs-target="#loginModal">
                        Login / Sign Up
                    </button>
                    <a href="https://github.com/vibewithdps" target="_blank" class="btn btn-outline-light btn-sm rounded-pill px-3">
                        <i class="fa-brands fa-github me-1"></i> GitHub
                    </a>
                </div>"""

html = html.replace("""                <div class="ms-lg-3 mt-3 mt-lg-0">
                    <a href="https://github.com/vibewithdps" target="_blank" class="btn btn-outline-light btn-sm rounded-pill px-3">
                        <i class="fa-brands fa-github me-1"></i> GitHub
                    </a>
                </div>""", login_btn)

# Add Modals and JS at the bottom
modals = """
    <!-- Auth Modals -->
    <div class="modal fade" id="loginModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-0 pb-0">
                    <h5 class="modal-title fw-bold">Welcome Back</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4">
                    <div id="loginAlert" class="alert alert-danger d-none"></div>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" id="loginEmail" required>
                        </div>
                        <div class="mb-4">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" id="loginPassword" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 rounded-pill">Login</button>
                        <div class="text-center mt-3">
                            <small class="text-muted">Don't have an account? <a href="#" data-bs-toggle="modal" data-bs-target="#signupModal">Sign up</a></small>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="signupModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header border-0 pb-0">
                    <h5 class="modal-title fw-bold">Create Account</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-4">
                    <div id="signupAlert" class="alert alert-danger d-none"></div>
                    <form id="signupForm">
                        <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="regName" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" class="form-control" id="regUsername" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" id="regEmail" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" id="regPassword" required>
                        </div>
                        <div class="mb-4">
                            <label class="form-label">Confirm Password</label>
                            <input type="password" class="form-control" id="regConfirm" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100 rounded-pill">Create Account</button>
                        <div class="text-center mt-3">
                            <small class="text-muted">Already have an account? <a href="#" data-bs-toggle="modal" data-bs-target="#loginModal">Login</a></small>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/auth.js"></script>
"""

html = html.replace("</body>", modals + "\n</body>")

with open("templates/index.html", "w") as f:
    f.write(html)
