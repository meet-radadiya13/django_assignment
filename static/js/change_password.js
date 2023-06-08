document.addEventListener('keyup', function() {
    var conditions = {};
    var password = document.querySelector('#password').value;
    var passwordsMatch = document.querySelector('#confirm-password').value === password;
    var submitButton = document.querySelector('.submit-password');
    var passwordStrength = document.querySelector('#password-strength span');

    if (!/.{8,}/g.test(password)) {
        conditions.tooShort = true;
    }
    if (!/[a-z]/g.test(password)) {
        conditions.noLowerCaseLetter = true;
    }
    if (!/[A-Z]/g.test(password)) {
        conditions.noUpperCaseLetter = true;
    }
    if (!/[0-9]/g.test(password)) {
        conditions.noNumber = true;
    }
    if (!/[^0-9A-Za-z]/g.test(password)) {
        conditions.noSymbol = true;
    }

    if (!passwordsMatch) {
        submitButton.textContent = 'Passwords Mismatch';
        submitButton.disabled = true;
    } else {
        submitButton.textContent = 'Submit';
    }

    if (password == '') {
        passwordStrength.className = '';
    } else if (Object.keys(conditions).length >= 3) {
        passwordStrength.className = 'weak';
    } else if (Object.keys(conditions).length >= 2) {
        passwordStrength.className = 'medium';
    } else if (!conditions.tooShort && Object.keys(conditions).length <= 1) {
        passwordStrength.className = 'strong';

        if (passwordsMatch) {
            submitButton.disabled = false;
        }
    }
});