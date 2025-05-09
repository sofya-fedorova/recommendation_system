function validateForm() {

    const choices0 = document.querySelectorAll('input[name="rating0"]:checked');
    const choices1 = document.querySelectorAll('input[name="rating1"]:checked');
    const choices2 = document.querySelectorAll('input[name="rating2"]:checked');
    const choices3 = document.querySelectorAll('input[name="rating3"]:checked');
    const choices4 = document.querySelectorAll('input[name="rating4"]:checked');

    let flag = 0;

    if ((choices0.length > 0) && (choices1.length > 0) && (choices2.length > 0) && (choices3.length > 0) && (choices4.length > 0)) {
        flag =  0;
    } else {
        flag = 1;
    }

    if (flag === 0) {
        return true;
    } else {
        alert("Оцените, пожалуйста, все рекомендации!");
        return false;
    }
}