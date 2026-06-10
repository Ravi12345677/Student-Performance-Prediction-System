function validateForm(){

let attendance =
document.getElementById(
"attendance").value;

if(attendance<0 ||
attendance>100){

alert(
"Attendance should be between 0 and 100"
);

return false;
}

return true;
}