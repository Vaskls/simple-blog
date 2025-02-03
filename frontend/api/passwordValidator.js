const passwordValidator = (password, username) => {
    let passwordLengthValid = password.value.length >= 8;
    let passwordNumberValid = /[0-9]/.test(password.value);
    let passwordSpecialValid = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/.test(password.value)
    let passwordCapitalValid = /[A-Z]/.test(password.value)
    let passwordContainsUsernameError = false;
    if (password.value.includes(username) && username.length > 0) {
        passwordContainsUsernameError = true;
    } else {
        passwordContainsUsernameError = false;
    }
    
    let isPasswordValid = passwordLengthValid && passwordNumberValid && passwordSpecialValid && passwordCapitalValid && !passwordContainsUsernameError
    return {
        passwordLengthValid: passwordLengthValid,
        passwordNumberValid: passwordNumberValid,
        passwordSpecialValid: passwordSpecialValid,
        passwordCapitalValid: passwordCapitalValid,
        passwordContainsUsernameError: passwordContainsUsernameError,
        isPasswordValid: isPasswordValid
    }
};

export default passwordValidator;