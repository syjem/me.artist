const header = document.getElementById('header');

window.addEventListener('scroll', function() {
  if (window.pageYOffset > 0) {
    header.style.background = "linear-gradient(to right, #0f0c29, #302b63, #24243e)"; // Change background color as you desire
  } else {
    header.style.background = 'transparent';
  }
});