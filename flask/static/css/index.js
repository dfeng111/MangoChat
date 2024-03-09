document.getElementById('check').addEventListener('change', function () {
    if (this.checked) {
      document.querySelector('.login.form').style.display = 'none';
      document.querySelector('.registration.form').style.display = 'block';
    } else {
      document.querySelector('.login.form').style.display = 'block';
      document.querySelector('.registration.form').style.display = 'none';
    }
});

function validateLoginForm() {
    var name = document.getElementById('logName').value;
    var password = document.getElementById('logPassword').value;

    if (name == "" || password == "") {
      alert("Please fill the required fields");
      return false;
    }
    else {
      alert("Successfully logged in");
      return true;
    }
}

function validateRegisterForm() {
    var mail = document.getElementById('registerEmail').value;
    var password = document.getElementById('registerPassword').value;

    if (mail == "" || password == "") {
      alert("Please fill the required fields");
      return false;
    }

    if (password.length < 8) {
      alert("Your password must include at least 8 characters");
      return false;
    }

    if (password.length >= 8) {
      alert("Successfully signed up");
      document.getElementById('check').checked = false; // Redirect to the login form
      return true;
    }
}