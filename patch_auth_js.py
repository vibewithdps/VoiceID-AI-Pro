with open('static/js/auth.js', 'r') as f:
    content = f.read()

content = content.replace(
"""            } catch (err) {
                alertBox.textContent = "Connection error.";
                alertBox.classList.remove('d-none');
            }""",
"""            } catch (err) {
                alertBox.textContent = "Error: " + err.message;
                alertBox.classList.remove('d-none');
            }"""
)

with open('static/js/auth.js', 'w') as f:
    f.write(content)
